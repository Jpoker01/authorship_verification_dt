import {useEffect, useState} from 'react';
import { AppHeader } from './components/AppHeader';
import { Instructions } from './components/Instructions';
import { TextVerification } from './components/TextVerification.tsx';
import { Results } from './components/Results';

import instructions from './assets/data/instructions.json';

function App() {
  const [text1, setText1] = useState('');
  const [text2, setText2] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<number | null>(null);
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

  const handleAnalyze = () => {
    if (!text1.trim() || !text2.trim()) {
      return;
    }

    setIsAnalyzing(true);
    setResult(null);

    setTimeout(() => {
      const randomResult = Math.floor(Math.random() * 40) + 50;
      setResult(randomResult);
      setIsAnalyzing(false);
    }, 2000);
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