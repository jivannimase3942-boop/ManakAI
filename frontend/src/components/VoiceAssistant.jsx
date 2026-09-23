import React, { useState, useEffect, useRef } from 'react';
import { t } from '../i18n.js';
import {
  startListening,
  isSpeechRecognitionSupported,
  speakText
} from '../utils/voiceUtils';

// SVG Icons
const MicIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
    <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
    <line x1="12" x2="12" y1="19" y2="22" />
  </svg>
);

const StopIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
  </svg>
);

const SpeakerIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
    <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
  </svg>
);

const LoaderIcon = () => (
  <svg className="animate-spin" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 12a9 9 0 1 1-6.219-8.56" />
  </svg>
);

const VoiceAssistant = ({
  onTextRecognized,
  onTranscriptChange,
  isProcessingRetrieval,
  ttsResponse,
  language = 'en',
  className = ""
}) => {
  const [state, setState] = useState('idle'); // idle, listening, processing, speaking, error
  const [errorMsg, setErrorMsg] = useState('');

  // UI transcript (just for visual updates)
  const [uiTranscript, setUiTranscript] = useState('');

  // Hard session safety and robust transcript preservation
  const sessionTokenRef = useRef(0);
  const recognitionRef = useRef(null);
  const submittedRef = useRef(false);
  const transcriptRef = useRef({ finalText: '', interimText: '' });

  // Sync state with parent processing status
  useEffect(() => {
    if (isProcessingRetrieval && state !== 'speaking') {
      setState('processing');
    }
  }, [isProcessingRetrieval, state]);

  // When TTS response arrives, speak it
  useEffect(() => {
    if (ttsResponse && state === 'processing') {
      setState('speaking');

      const currentSession = sessionTokenRef.current;
      speakText(
        ttsResponse,
        language,
        currentSession,
        () => {
          // onStart - no action needed as state is already 'speaking'
        },
        () => {
          // onEnd
          if (sessionTokenRef.current === currentSession) {
            setState('idle');
          }
        }
      );

      // Fallback in case onEnd never fires
      const estimatedTimeMs = (ttsResponse.length / 15) * 1000 + 3000;
      setTimeout(() => {
        if (sessionTokenRef.current === currentSession) {
          setState(prev => prev === 'speaking' ? 'idle' : prev);
        }
      }, Math.min(estimatedTimeMs, 30000));
    }
  }, [ttsResponse]);

  // Cleanup on unmount or language change
  useEffect(() => {
    sessionTokenRef.current += 1;
    if (recognitionRef.current) {
      recognitionRef.current.onresult = null;
      recognitionRef.current.onerror = null;
      recognitionRef.current.onend = null;
      recognitionRef.current.abort();
    }
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    setState('idle');
  }, [language]);

  const stopListeningAndSubmit = () => {
    const currentSession = sessionTokenRef.current;

    // Invalidate session immediately to block further events
    sessionTokenRef.current += 1;

    // 1. Log explicitly
    console.log(`[VOICE] user-stop session=${currentSession}`);

    // 2. Kill microphone handlers and stop/abort it
    if (recognitionRef.current) {
      recognitionRef.current.onresult = null;
      recognitionRef.current.onerror = null;
      recognitionRef.current.onend = null;
      recognitionRef.current.abort();
    }

    // 3. Extract best transcript directly from the synchronized ref
    const { finalText, interimText } = transcriptRef.current;
    const combined = `${finalText} ${interimText}`.trim().replace(/\s{2,}/g, ' ');

    if (!combined) {
      // Empty string, nothing to submit
      setState('idle');
      return;
    }

    // 4. Submit exactly once
    if (!submittedRef.current) {
      submittedRef.current = true;
      console.log(`[VOICE] submit session=${currentSession} text="${combined}"`);
      setState('processing');
      onTextRecognized(combined);
    }
  };

  const handleMicClick = () => {
    if (state === 'listening') {
      stopListeningAndSubmit();
      return;
    }

    if (state !== 'idle') {
      // Barge-in or interrupt processing/speaking
      sessionTokenRef.current += 1; // Invalidate any active session
      if (recognitionRef.current) recognitionRef.current.abort();
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      setState('idle');
      return;
    }

    if (!isSpeechRecognitionSupported()) {
      setState('error');
      setErrorMsg('Not supported');
      setTimeout(() => setState('idle'), 3000);
      return;
    }

    // Start a fresh listening session
    const currentSession = Date.now();
    sessionTokenRef.current = currentSession;
    submittedRef.current = false;
    transcriptRef.current = { finalText: '', interimText: '' };

    setState('listening');
    setErrorMsg('');
    setUiTranscript('');
    if (onTranscriptChange) {
      onTranscriptChange('');
    }

    recognitionRef.current = startListening(
      language,
      currentSession,
      ({ finalText, interimText }) => {
        // Guard against late events
        if (sessionTokenRef.current !== currentSession) return;

        // 1. Immediately update ref (synchronous preservation)
        transcriptRef.current = { finalText, interimText };

        // 2. Update React UI state safely
        const combined = `${finalText} ${interimText}`.trim().replace(/\s{2,}/g, ' ');
        setUiTranscript(combined);
        if (onTranscriptChange) {
          onTranscriptChange(combined);
        }
      },
      (err) => {
        // onError
        if (sessionTokenRef.current !== currentSession) return;
        setState('error');
        setErrorMsg(err);
        setTimeout(() => setState(prev => prev === 'error' ? 'idle' : prev), 4000);
      },
      () => {
        // onEnd of recognition (silence/timeout occurred without explicit user stop)
        if (sessionTokenRef.current !== currentSession) return;
        if (state === 'listening') {
          // If we reached here without submitting, the browser timed out or mic died.
          // Do NOT restart. Preserve state and return safely.
          const { finalText, interimText } = transcriptRef.current;
          const combined = `${finalText} ${interimText}`.trim().replace(/\s{2,}/g, ' ');
          if (combined && !submittedRef.current) {
            submittedRef.current = true;
            console.log(`[VOICE] submit session=${currentSession} text="${combined}"`);
            setState('processing');
            onTextRecognized(combined);
          } else {
            setState('idle');
          }
        }
      }
    );
  };

  const handleReplay = () => {
    if (!ttsResponse) return;

    // Invalidate any existing TTS session
    const currentSession = Date.now();
    sessionTokenRef.current = currentSession;

    setState('speaking');

    speakText(
      ttsResponse,
      language,
      currentSession,
      () => {},
      () => {
        if (sessionTokenRef.current === currentSession) {
          setState('idle');
        }
      }
    );

    const estimatedTimeMs = (ttsResponse.length / 15) * 1000 + 3000;
    setTimeout(() => {
      if (sessionTokenRef.current === currentSession) {
        setState(prev => prev === 'speaking' ? 'idle' : prev);
      }
    }, Math.min(estimatedTimeMs, 30000));
  };

  const getUI = () => {
    switch (state) {
      case 'listening':
        return {
          icon: <StopIcon />,
          text: language === 'hi' ? 'रोकें' : language === 'mr' ? 'थांबवा' : 'Stop',
          color: 'text-red-600',
          bg: 'bg-red-50 border-red-200 hover:bg-red-100',
          subtext: uiTranscript ? `"${uiTranscript}"` : (language === 'hi' ? 'सुन रहा हूँ...' : language === 'mr' ? 'ऐकत आहे...' : 'Listening...')
        };
      case 'processing':
        return { icon: <LoaderIcon />, text: language === 'hi' ? 'प्रोसेसिंग' : language === 'mr' ? 'प्रक्रिया करत आहे' : 'Processing', color: 'text-navy-700', bg: 'bg-navy-50 border-navy-200', subtext: '' };
      case 'speaking':
        return { icon: <SpeakerIcon />, text: language === 'hi' ? 'बोल रहा हूँ' : language === 'mr' ? 'बोलत आहे' : 'Speaking', color: 'text-green-700', bg: 'bg-green-50 border-green-200 hover:bg-green-100', subtext: '' };
      case 'error':
        return { icon: <MicIcon />, text: errorMsg, color: 'text-orange-600', bg: 'bg-orange-50 border-orange-200', subtext: '' };
      default:
        return { icon: <MicIcon />, text: language === 'hi' ? 'बोलें' : language === 'mr' ? 'बोला' : 'Speak', color: 'text-navy-600', bg: 'bg-white border-slate-200 hover:bg-slate-50 shadow-sm', subtext: '' };
    }
  };

  const ui = getUI();
  const langLabel = language === 'hi' ? 'हिंदी' : language === 'mr' ? 'मराठी' : 'English';
  const replayLabel = language === 'hi' ? 'फिर से सुनें' : language === 'mr' ? 'पुन्हा ऐका' : 'Replay';

  return (
    <div className="flex flex-col items-center justify-center gap-2">
      <div className="flex items-center justify-center gap-3">

        <button
          type="button"
          onClick={handleMicClick}
          aria-label="Voice Search"
          className={`flex items-center justify-center gap-2 px-4 py-2 border rounded-md transition-colors focus-visible outline-none ${ui.bg} ${ui.color} ${className}`}
          title={isSpeechRecognitionSupported() ? "Search with voice" : "Voice not supported"}
        >
          {ui.icon}
          {ui.text && <span className="font-medium tracking-wide whitespace-nowrap">{ui.text}</span>}
        </button>
        {state === 'idle' && ttsResponse && (
          <button
            type="button"
            onClick={handleReplay}
            className={`flex items-center justify-center gap-2 px-4 py-2 border rounded-md transition-colors focus-visible outline-none bg-white border-slate-200 hover:bg-slate-50 shadow-sm text-navy-600 ${className}`}
            title="Replay Voice Answer"
          >
            <SpeakerIcon />
            <span className="font-medium tracking-wide whitespace-nowrap">{replayLabel}</span>
          </button>
        )}
      </div>
    </div>
  );
};

export default VoiceAssistant;
