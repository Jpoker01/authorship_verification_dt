import { useState } from 'react';

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

function App() {
  return (
      //Fill screen horizontally, set the background color and gradients
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/*set the max width to 1280px, center horizontally, set horizontal and vertical padding*/}
      <div className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">

      </div>
    </div>
  );
}

export default App;