import {useEffect, useState} from 'react';
import { AppHeader } from './components/AppHeader';
import { Instructions } from './components/Instructions';
import { TextVerification } from './components/TextVerification.tsx';
import { Results } from './components/Results';
import { predictAuthorship, ApiError } from './services/api';

import instructions from './assets/data/instructions.json';

function App() {
  const [text1, setText1] = useState('');
  const [text2, setText2] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  //returns an empty field expandedInstructions, and function setExpandedInstructions to replace expandedInstructions
  const [expandedInstructions, setExpandedInstructions] = useState<number[]>([]);

  //function to open or close instruction based on its current state
  function toggleInstruction(index: number) {
      setExpandedInstructions(function (prev) {

      if (prev.includes(index)) {
        //returns a new list without the item
        return prev.filter(function (item) {
          return item !== index;
        });
      }
      //if instruction not in instructions, add it
      var copy = prev.slice();
      copy.push(index);
      return copy;
    });
  }

    useEffect(() => {
      if (result !== null) {
        const el = document.getElementById("results-section");
        if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, [result]);

  const handleAnalyze = async () => {
    if (!text1.trim() || !text2.trim()) {
      return;
    }

    setIsAnalyzing(true);
    setResult(null);

    setError(null);
    try {
      const response = await predictAuthorship(text1, text2);
      // Convert probability (0-1) to percentage (0-100)
      const percentage = Math.round(response.same_author_probability * 100);
      setResult(percentage);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
      console.error('Prediction error:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };
  return (
      //Fill screen horizontally, set the background color and gradients
    <div className="min-h-screen bg-gradient-to-br  from-slate-50 via-slate-50 to-slate-200">
      {/*set the max width to 1280px, center horizontally, set horizontal and vertical padding*/}
      <div className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        <AppHeader />
        <TextVerification
          text1={text1}
          text2={text2}
          onText1Change={setText1}
          onText2Change={setText2}
          isAnalyzing={isAnalyzing}
          onAnalyze={handleAnalyze}
        />
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded-lg">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            </div>
          )}
          {result !== null && <Results result={result} />}
        <Instructions
          instructions={instructions}
          expandedInstructions={expandedInstructions}
          onToggle={toggleInstruction}
        />
      </div>
    </div>
  );
}

export default App;