interface TextVerificationProperties{
  text1: string;
  text2: string;
  onText1Change: (text: string) => void;
  onText2Change: (text: string) => void;
  isAnalyzing: boolean;
  onAnalyze: () => void;
}

export function TextVerification({
  text1,
  text2,
  onText1Change,
  onText2Change,
  isAnalyzing,
  onAnalyze
}: TextVerificationProperties) {
  return (
    <div className="bg-white rounded-2xl shadow-lg p-8 mb-10">
      <h2 className="text-2xl font-semibold text-slate-700 mb-6">Text Input</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div>
          <label className="block text-md font-medium text-slate-700 mb-3">
            Text 1
          </label>
          <textarea
            value={text1}
            onChange={(e) => onText1Change(e.target.value)}
            placeholder="Paste the first text here..."
            className="w-full h-80 px-4 py-4 border border-slate-300 rounded-lg hover:border-blue-400 focus:ring-inset focus:ring-2 focus:ring-blue-400 resize-none transition-shadow"
          />
          <div className="mt-2 text-sm text-slate-500">
            {/*trim whitespace, then count number of characters*/}
            {text1.trim().length} characters
          </div>
        </div>

        <div>
          <label className="block text-md font-medium text-slate-700 mb-3">
            Text 2
          </label>
          <textarea
            value={text2}
            onChange={(e) => onText2Change(e.target.value)}
            placeholder="Paste the second text here..."
            className="w-full h-80 px-4 py-3 border border-slate-300 rounded-lg hover:border-blue-400 focus:ring-inset focus:ring-2 focus:ring-blue-400 resize-none transition-shadow"
          />
          <div className="mt-2 text-sm text-slate-500">
            {text2.trim().length} characters
          </div>
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={() => {
            onAnalyze();
          }}
          disabled={!text1.trim() || !text2.trim() || isAnalyzing}
          className="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold rounded-lg shadow-xl hover:from-blue-700 hover:to-cyan-600 disabled:from-slate-400 disabled:to-slate-500 disabled:cursor-not-allowed disabled:hover:scale-100 disabled:shadow-none transition-all transform hover:scale-105 active:scale-90"
        >
          {isAnalyzing ? (
            <span className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing...
            </span>
          ) : (
            'Verify Authorship'
          )}
        </button>
      </div>
    </div>
  );
}