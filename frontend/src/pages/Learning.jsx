import { useState } from 'react';
import { t } from '../i18n.js';
import { useLocalData } from '../hooks/useLocalData.js';

export default function Learning({ language }) {
  const { updateQuizScore } = useLocalData();
  const [activeQuiz, setActiveQuiz] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showResult, setShowResult] = useState(false);
  const [answered, setAnswered] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const [activeQuestions, setActiveQuestions] = useState([]);

  const QUIZ_POOL = [
    {
      q: t(language, 'quiz_q1'),
      options: [
        t(language, 'quiz_q1_o1'),
        t(language, 'quiz_q1_o2'),
        t(language, 'quiz_q1_o3')
      ],
      a: t(language, 'quiz_q1_o2'),
      explanation: t(language, 'quiz_q1_exp'),
      source: "BIS Standards Overview (kb-007)",
    },
    {
      q: t(language, 'quiz_q2'),
      options: [
        t(language, 'quiz_q2_o1'),
        t(language, 'quiz_q2_o2'),
        t(language, 'quiz_q2_o3')
      ],
      a: t(language, 'quiz_q2_o3'),
      explanation: t(language, 'quiz_q2_exp'),
      source: "BIS Product Certification Scheme (kb-002)",
    },
    {
      q: t(language, 'quiz_q3'),
      options: [
        t(language, 'quiz_q3_o1'),
        t(language, 'quiz_q3_o2'),
        t(language, 'quiz_q3_o3')
      ],
      a: t(language, 'quiz_q3_o2'),
      explanation: t(language, 'quiz_q3_exp'),
      source: "BIS Schemes Overview (kb-008)",
    },
    {
      q: t(language, 'quiz_q4'),
      options: [
        t(language, 'quiz_q4_o1'),
        t(language, 'quiz_q4_o2'),
        t(language, 'quiz_q4_o3')
      ],
      a: t(language, 'quiz_q4_o2'),
      explanation: t(language, 'quiz_q4_exp'),
      source: "Hallmarking Scheme (kb-003)",
    },
    {
      q: t(language, 'quiz_q6'),
      options: [
        t(language, 'quiz_q6_o1'),
        t(language, 'quiz_q6_o2'),
        t(language, 'quiz_q6_o3')
      ],
      a: t(language, 'quiz_q6_o1'),
      explanation: t(language, 'quiz_q6_exp'),
      source: "Consumer Complaints & Grievance Redressal (kb-006)",
    },
    {
      q: t(language, 'quiz_q7'),
      options: [
        t(language, 'quiz_q7_o1'),
        t(language, 'quiz_q7_o2'),
        t(language, 'quiz_q7_o3')
      ],
      a: t(language, 'quiz_q7_o2'),
      explanation: t(language, 'quiz_q7_exp'),
      source: "Packaged Drinking Water (kb-001)"
    },
    {
      q: t(language, 'quiz_q8'),
      options: [
        t(language, 'quiz_q8_o1'),
        t(language, 'quiz_q8_o2'),
        t(language, 'quiz_q8_o3')
      ],
      a: t(language, 'quiz_q8_o3'),
      explanation: t(language, 'quiz_q8_exp'),
      source: "BIS-Recognised Testing Laboratories (kb-004)"
    },
    {
      q: t(language, 'quiz_q9'),
      options: [
        t(language, 'quiz_q9_o1'),
        t(language, 'quiz_q9_o2'),
        t(language, 'quiz_q9_o3')
      ],
      a: t(language, 'quiz_q9_o2'),
      explanation: t(language, 'quiz_q9_exp'),
      source: "BIS Licensing for Manufacturers (kb-005)"
    }
  ];

  const shuffleArray = (array) => {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  };

  const generateQuiz = () => {
    const shuffledPool = shuffleArray(QUIZ_POOL).slice(0, 5);
    return shuffledPool.map(q => {
      const shuffledOptions = shuffleArray(q.options);
      return {
        ...q,
        options: shuffledOptions,
        a: shuffledOptions.indexOf(q.a)
      };
    });
  };

  const handleAnswer = (index) => {
    if (answered) return;
    setSelectedOption(index);
    setAnswered(true);
    if (index === activeQuestions[currentQuestion].a) {
      setScore(s => s + 1);
    }
  };

  const handleNext = () => {
    if (currentQuestion + 1 < activeQuestions.length) {
      setCurrentQuestion(c => c + 1);
      setAnswered(false);
      setSelectedOption(null);
    } else {
      setShowResult(true);
      updateQuizScore(score); // Save the final score
    }
  };

  const startQuiz = () => {
    setActiveQuestions(generateQuiz());
    setActiveQuiz(true);
    resetQuizState();
  };

  const retakeQuiz = () => {
    setActiveQuestions(generateQuiz());
    resetQuizState();
  };

  const resetQuizState = () => {
    setScore(0);
    setCurrentQuestion(0);
    setShowResult(false);
    setAnswered(false);
    setSelectedOption(null);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 min-h-[calc(100vh-64px)]">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">{t(language, 'lbl_learning_centre')}</h1>
        <p className="text-slate-500 mt-2">{t(language, 'lbl_learning_desc')}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
        <div className="bg-white border border-slate-200 rounded-lg p-6 shadow-sm">
          <h2 className="text-xl font-bold text-slate-800 mb-3">{t(language, 'lrn_what_bis')}</h2>
          <p className="text-slate-600 text-sm leading-relaxed mb-4">
            {t(language, 'lrn_bis_desc')}
          </p>
        </div>
        <div className="bg-white border border-slate-200 rounded-lg p-6 shadow-sm">
          <h2 className="text-xl font-bold text-slate-800 mb-3">{t(language, 'lrn_key_marks')}</h2>
          <ul className="space-y-3 text-sm text-slate-600">
            <li className="flex items-start gap-2">
              <div className="w-8 h-8 rounded bg-blue-100 flex items-center justify-center font-bold text-blue-700 shrink-0">ISI</div>
              <span><strong>{t(language, 'lrn_isi_mark')}</strong> {t(language, 'lrn_isi_desc')}</span>
            </li>
            <li className="flex items-start gap-2">
              <div className="w-8 h-8 rounded bg-yellow-100 flex items-center justify-center font-bold text-yellow-700 shrink-0">HM</div>
              <span><strong>{t(language, 'lrn_hm')}</strong> {t(language, 'lrn_hm_desc')}</span>
            </li>
            <li className="flex items-start gap-2">
              <div className="w-8 h-8 rounded bg-green-100 flex items-center justify-center font-bold text-green-700 shrink-0">CRS</div>
              <span><strong>{t(language, 'lrn_crs_mark')}</strong> {t(language, 'lrn_crs_desc')}</span>
            </li>
          </ul>
        </div>
      </div>

      <div className="bg-slate-50 border border-slate-200 rounded-xl p-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-slate-800">{t(language, 'lbl_learning_centre')}</h2>
          {!activeQuiz && (
            <button
              onClick={startQuiz}
              className="bg-navy-600 hover:bg-navy-700 text-white px-4 py-2 rounded-md font-semibold text-sm transition-colors"
            >
              {t(language, 'lbl_start_quiz')}
            </button>
          )}
        </div>

        {activeQuiz && !showResult && activeQuestions.length > 0 && (
          <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
            <div className="flex justify-between text-xs text-slate-500 font-bold uppercase tracking-wider mb-4">
              <span>{t(language, 'lbl_question_of').replace('{current}', currentQuestion + 1).replace('{total}', activeQuestions.length)}</span>
              <span>Score: {score}</span>
            </div>
            <h3 className="text-lg font-medium text-slate-900 mb-6">{activeQuestions[currentQuestion].q}</h3>
            <div className="space-y-3">
              {activeQuestions[currentQuestion].options.map((opt, i) => {
                let btnClass = "w-full text-left px-5 py-3 rounded-lg border font-medium transition-colors ";
                if (!answered) {
                  btnClass += "border-slate-200 hover:border-navy-400 hover:bg-navy-50 text-slate-700";
                } else {
                  if (i === activeQuestions[currentQuestion].a) {
                    btnClass += "border-green-500 bg-green-50 text-green-800";
                  } else if (i === selectedOption) {
                    btnClass += "border-red-500 bg-red-50 text-red-800";
                  } else {
                    btnClass += "border-slate-200 text-slate-400 opacity-50";
                  }
                }

                return (
                  <button
                    key={i}
                    disabled={answered}
                    onClick={() => handleAnswer(i)}
                    className={btnClass}
                  >
                    {opt}
                  </button>
                );
              })}
            </div>

            {answered && (
              <div className="mt-6 pt-6 border-t border-slate-200">
                <div className={`text-sm font-bold mb-2 ${selectedOption === activeQuestions[currentQuestion].a ? 'text-green-700' : 'text-red-700'}`}>
                  {selectedOption === activeQuestions[currentQuestion].a ? '✓ ' + t(language, 'lbl_correct') : '✗ ' + t(language, 'lbl_incorrect')}
                </div>
                <p className="text-sm text-slate-700 mb-3">{activeQuestions[currentQuestion].explanation}</p>
                <div className="text-xs text-slate-500 bg-slate-50 inline-block px-3 py-1.5 rounded border border-slate-200 mb-5">
                  <span className="font-semibold text-slate-600 mr-1">{t(language, 'lbl_source')}:</span> {activeQuestions[currentQuestion].source}
                </div>

                <button
                  onClick={handleNext}
                  className="block w-full bg-navy-600 hover:bg-navy-700 text-white py-3 rounded-lg font-semibold text-sm transition-colors"
                >
                  {currentQuestion + 1 < activeQuestions.length ? t(language, 'lbl_next_question') : t(language, 'lbl_view_results')}
                </button>
              </div>
            )}
          </div>
        )}

        {showResult && (
          <div className="bg-white p-8 rounded-lg border border-slate-200 shadow-sm text-center">
            <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold text-slate-900 mb-2">{t(language, 'lbl_quiz_complete')}</h3>
            <p className="text-slate-600 mb-6">{t(language, 'lbl_you_scored').replace('{score}', score).replace('{total}', activeQuestions.length)}</p>
            <button
              onClick={retakeQuiz}
              className="bg-navy-600 hover:bg-navy-700 text-white px-6 py-2 rounded-md font-semibold text-sm transition-colors"
            >
              {t(language, 'lbl_retake_quiz_btn')}
            </button>
          </div>
        )}

        {!activeQuiz && !showResult && (
          <div className="text-center py-10 text-slate-500">
            Click '{t(language, 'lbl_start_quiz')}' to test your knowledge of BIS standards and marks.
          </div>
        )}
      </div>
    </div>
  );
}
