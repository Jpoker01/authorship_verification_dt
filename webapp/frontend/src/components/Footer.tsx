export function Footer() {
    return (
        <footer className="bg-slate-100 border-t border-slate-300 mt-12">
            <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
                <div className="flex items-center justify-center gap-2">
                    <p className="text-md text-slate-600">For more information about this project: </p>
                    <a
                        href="https://github.com/Jpoker01"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-slate-600 hover:text-slate-900 font-medium transition-colors"
                    >
                        GitHub
                    </a>
                </div>
            </div>
        </footer>
    )
}