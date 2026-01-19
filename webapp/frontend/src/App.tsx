import { useState } from 'react';
import { AppHeader } from './components/AppHeader';
import { Instructions } from './components/Instructions';


const instructions = [
  {
    title: 'What is Authorship Verification?',
    content: 'Authorship verification is the process of determining whether two texts were written by the same author. This technique uses stylometric analysis to compare writing patterns, vocabulary, syntax, and other linguistic features.'
  },
  {
    title: 'How to Use This Tool',
    content: 'Enter two text samples in the input fields below. The tool will analyze both texts and provide a similarity score indicating the likelihood that they were written by the same author. A higher percentage indicates greater similarity.'
  },
  {
    title: 'Best Practices',
    content: 'For optimal results, use text samples of at least 100 words each. Ensure the texts are in the same language and preferably from similar contexts (e.g., both formal or both informal). Remove any obvious formatting or citations that might skew the analysis.'
  },
  {
    title: 'Understanding the Results',
    content: 'The percentage score represents the confidence level of authorship similarity. Scores above 70% suggest strong similarity, 50-70% indicates moderate similarity, and below 50% suggests different authors. Consider the context and sample size when interpreting results.'
  }
];

//vice citaci do uvodu
//metodika v budoucim case
//uvest url
//doplnit desetinna mista
//doplnit mezeru mezi procenta a cisla ve vysledcich
//tabulka - zarovnat s textem
//uvest citaci na jednotlive modely
//architektura webovky

function App() {
  //returns an empty field expandedInstructions, and function setExpandedInstructions to replace expandedInstructions
  const [expandedInstructions, setExpandedInstructions] = useState<number[]>([]);
  //function to open or close instruction based on its current state
  function toggleInstruction(index: number) {
      setExpandedInstructions(function (prev) {

      if (prev.includes(index)) {
        return prev.filter(function (item) {
          return item !== index;
        });
      }

      var copy = prev.slice();
      copy.push(index);
      return copy;
    });
  }
  return (
      //Fill screen horizontally, set the background color and gradients
    <div className="min-h-screen bg-gradient-to-br  from-slate-50 via-slate-50 to-slate-200">
      {/*set the max width to 1280px, center horizontally, set horizontal and vertical padding*/}
      <div className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        <AppHeader />
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