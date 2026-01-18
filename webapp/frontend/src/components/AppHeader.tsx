import {  BookCheck } from 'lucide-react';

export function AppHeader() {
  return (
    <div className="text-center mb-12">
      <div className="flex items-center justify-center mb-4">
        <BookCheck className="w-11 h-11 text-blue-900 mr-3"/>
        <h1 className="text-5xl font-bold text-slate-900">
          Authorship Verification
        </h1>
      </div>
      <p className="text-xl text-slate-600 max-w-2xl mx-auto my-10">
          Diploma thesis project focused on determining the likelihood of two texts being authored by the same individual.
      </p>
    </div>
  );
}