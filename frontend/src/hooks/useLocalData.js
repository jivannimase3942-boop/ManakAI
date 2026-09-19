import { useState, useEffect } from 'react';

export function useLocalData() {
  const [history, setHistory] = useState(() => {
    try {
      const saved = localStorage.getItem('manakai_history');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [savedStandards, setSavedStandards] = useState(() => {
    try {
      const saved = localStorage.getItem('manakai_saved_standards');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [quizScore, setQuizScore] = useState(() => {
    try {
      const saved = localStorage.getItem('manakai_quiz_score');
      return saved ? parseInt(saved, 10) : null;
    } catch {
      return null;
    }
  });

  useEffect(() => {
    localStorage.setItem('manakai_history', JSON.stringify(history));
  }, [history]);

  useEffect(() => {
    localStorage.setItem('manakai_saved_standards', JSON.stringify(savedStandards));
  }, [savedStandards]);

  useEffect(() => {
    if (quizScore !== null) {
      localStorage.setItem('manakai_quiz_score', quizScore.toString());
    }
  }, [quizScore]);

  const addHistory = (query) => {
    if (!query) return;
    setHistory(prev => {
      const filtered = prev.filter(q => q.query !== query);
      return [{ query, timestamp: new Date().toISOString() }, ...filtered].slice(0, 20); // Keep last 20
    });
  };

  const clearHistory = () => {
    setHistory([]);
  };

  const saveStandard = (standard) => {
    if (!standard || !standard.standard_number) return;
    setSavedStandards(prev => {
      if (prev.some(s => s.standard_number === standard.standard_number)) return prev;
      return [{ ...standard, savedAt: new Date().toISOString() }, ...prev];
    });
  };

  const removeStandard = (standard_number) => {
    setSavedStandards(prev => prev.filter(s => s.standard_number !== standard_number));
  };

  const isSaved = (standard_number) => {
    return savedStandards.some(s => s.standard_number === standard_number);
  };

  const updateQuizScore = (score) => {
    setQuizScore(score);
  };

  return {
    history,
    addHistory,
    clearHistory,
    savedStandards,
    saveStandard,
    removeStandard,
    isSaved,
    quizScore,
    updateQuizScore
  };
}
