// Map internal languages to Web Speech locales
export const LOCALE_MAP = {
  en: 'en-IN',
  hi: 'hi-IN',
  mr: 'mr-IN',
};

// Check if speech recognition is supported
export const isSpeechRecognitionSupported = () => {
  return 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window;
};

// Start speech recognition
export const startListening = (lang, sessionId, onResultUpdate, onError, onEnd) => {
  if (!isSpeechRecognitionSupported()) {
    onError("Speech Recognition is not supported in this browser.");
    return null;
  }

  const targetLang = LOCALE_MAP[lang] || 'en-IN';
  console.log(`[VOICE] start session=${sessionId} lang=${targetLang}`);
  console.log(`[VOICE] recognition.lang=${targetLang}`);

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.lang = targetLang;
  recognition.interimResults = true;
  recognition.maxAlternatives = 1;
  // CRITICAL for V5: Allow pausing without automatically stopping
  recognition.continuous = true;

  recognition.onstart = () => {
    console.log(`[VOICE] onstart session=${sessionId}`);
  };

  recognition.onresult = (event) => {
    let finalTranscript = '';
    let interimTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        finalTranscript += event.results[i][0].transcript;
      } else {
        interimTranscript += event.results[i][0].transcript;
      }
    }

    if (interimTranscript) {
      console.log(`[VOICE] interim session=${sessionId}`);
    }

    if (finalTranscript) {
      console.log(`[VOICE] final session=${sessionId}`);
    }

    if (onResultUpdate) {
      onResultUpdate({
        finalText: finalTranscript,
        interimText: interimTranscript
      });
    }
  };

  recognition.onerror = (event) => {
    console.log(`[VOICE] error session=${sessionId} type=${event.error}`);
    if (event.error === 'not-allowed' || event.error === 'permission-denied') {
      onError("Microphone access is blocked. Allow microphone access for localhost and try again.");
    } else if (event.error !== 'no-speech') {
      onError(`Microphone error: ${event.error}`);
    } else {
      if (onEnd) onEnd();
    }
  };

  recognition.onend = () => {
    console.log(`[VOICE] onend session=${sessionId}`);
    if (onEnd) onEnd();
  };

  recognition.start();
  return recognition;
};

// Strip markdown, URLs, JSON for TTS
export const stripForSpeech = (text) => {
  if (!text) return "";

  let cleanText = text;
  // Remove markdown bold/italic
  cleanText = cleanText.replace(/[*_~`]/g, '');
  // Remove markdown headers
  cleanText = cleanText.replace(/#+\s/g, '');
  // Remove markdown links [text](url) -> text
  cleanText = cleanText.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  // Remove raw URLs
  cleanText = cleanText.replace(/https?:\/\/[^\s]+/g, '');
  // Remove trailing internal IDs or specific debug artifacts
  cleanText = cleanText.replace(/kb-\d{3}/gi, '');
  // Remove JSON blocks if any leaked
  cleanText = cleanText.replace(/```json[\s\S]*?```/g, '');
  // Remove other code blocks
  cleanText = cleanText.replace(/```[\s\S]*?```/g, '');
  // Clean up extra spaces
  cleanText = cleanText.replace(/\s{2,}/g, ' ');

  return cleanText.trim();
};

let voicesLoaded = false;
let availableVoices = [];

const loadVoices = () => {
  if (!('speechSynthesis' in window)) return;
  availableVoices = window.speechSynthesis.getVoices();
  if (availableVoices.length > 0) {
    voicesLoaded = true;
  }
};

if ('speechSynthesis' in window) {
  loadVoices();
  if (window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = loadVoices;
  }
}

// Speak text using SpeechSynthesis
export const speakText = (text, lang, sessionId, onStartCallback = null, onEndCallback = null) => {
  if (!('speechSynthesis' in window)) {
    if (onStartCallback) onStartCallback();
    if (onEndCallback) onEndCallback();
    return;
  }

  window.speechSynthesis.cancel();

  if (!text) {
    if (onStartCallback) onStartCallback();
    if (onEndCallback) onEndCallback();
    return;
  }

  const attemptSpeech = () => {
    const utterance = new SpeechSynthesisUtterance(stripForSpeech(text));
    const targetLang = LOCALE_MAP[lang] || 'en-IN';
    utterance.lang = targetLang;

    // Select best matching voice
    if (availableVoices.length > 0) {
      let voice = availableVoices.find(v => v.lang === targetLang) ||
                  availableVoices.find(v => v.lang.startsWith(lang));

      if (voice) {
        utterance.voice = voice;
        console.log(`[VOICE] tts voice=${voice.name}`);
      } else if (targetLang === 'mr-IN') {
        console.warn(`[VOICE] mr-IN TTS voice unavailable in this Chrome/OS environment`);
      } else {
        console.warn(`[VOICE] ${targetLang} TTS voice unavailable.`);
      }
    }

    console.log(`[VOICE] tts lang=${targetLang}`);

    utterance.onstart = () => {
      console.log(`[VOICE] tts-start session=${sessionId} lang=${targetLang}`);
      if (onStartCallback) onStartCallback();
    };

    utterance.onend = () => {
      console.log(`[VOICE] tts-end session=${sessionId} lang=${targetLang}`);
      if (onEndCallback) onEndCallback();
    };

    utterance.onerror = (e) => {
      console.warn(`[VOICE] tts-error session=${sessionId}`, e);
      if (onEndCallback) onEndCallback();
    };

    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    window.speechSynthesis.speak(utterance);
  };

  if (!voicesLoaded && availableVoices.length === 0) {
    // Retry once after a brief delay if voices aren't loaded yet
    setTimeout(attemptSpeech, 500);
  } else {
    attemptSpeech();
  }
};
