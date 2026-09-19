import React from 'react';
import DecisionCard from './DecisionCard.jsx';
import NoVerifiedMatch from './NoVerifiedMatch.jsx';

export default function ChatMessage({ message, language = 'en' }) {
  const isUser = message.role === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end animate-fade-in mb-6 font-sans w-full">
        <div className="max-w-[85%] sm:max-w-[70%] bg-slate-800 text-white rounded-lg px-5 py-3 text-[15px] leading-relaxed shadow-sm">
          {message.content}
        </div>
      </div>
    );
  }

  // If there's an error or generic message lacking structural properties
  if (!message.intent) {
    return (
      <div className="flex justify-start animate-fade-in mb-6 font-sans w-full">
        <div className="w-full bg-white border border-red-200 rounded-sm px-5 py-4 shadow-sm text-red-700">
          <p>{message.content || 'An error occurred.'}</p>
        </div>
      </div>
    );
  }

  const isUnknown = !message.match_found;

  if (isUnknown) {
    return <NoVerifiedMatch message={message} language={language} />;
  }

  return <DecisionCard message={message} language={language} />;
}
