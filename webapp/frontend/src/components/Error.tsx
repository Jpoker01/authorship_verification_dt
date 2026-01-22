import {CircleX} from 'lucide-react';

interface ErrorSectionProperties {
  error: string;
}

export function Error({ error }: ErrorSectionProperties) {
  return (
    <div className="rounded-2xl shadow-lg p-4 mb-8 pb-2 animate-fadeIn bg-red-50 ">
      <div className="flex items-center justify-center mt-1 mb-3 ml-2 gap-4 ">
        <div>
          <CircleX className="w-11 h-11 text-red-500" />
        </div>
        <div className="flex-1 mb-1">
          <h3 className="text-lg font-semibold pb-1.5 text-slate-700">Error</h3>
          <p className="text-md text-slate-800">{error}</p>
        </div>
      </div>
    </div>
  )
}
