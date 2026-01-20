import { useState } from 'react';
import { AppHeader } from './components/AppHeader';
import { Instructions } from './components/Instructions';

import instructions from './assets/data/instructions.json';

function App() {
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