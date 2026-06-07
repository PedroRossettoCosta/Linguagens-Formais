import React from 'react';

export default function Header({ status, statusColor, activeTab, setActiveTab }) {
  return (
    <header className="border-b-2 border-abyss-accent mb-5 pb-3 flex flex-col sm:flex-row justify-between items-center gap-4">
      <div className="flex flex-col sm:flex-row items-center gap-6 w-full sm:w-auto">
        <h1 className="text-abyss-accent text-2xl font-bold tracking-wider text-center sm:text-left">
          ABYSSUS COMPILER
        </h1>
        <nav className="flex gap-2 font-mono text-xs w-full sm:w-auto justify-center">
          <button
            onClick={() => setActiveTab('ritual')}
            className={`px-4 py-2 border transition-all duration-300 font-bold uppercase tracking-widest ${
              activeTab === 'ritual'
                ? 'bg-abyss-accent border-abyss-accent text-white shadow-[0_0_10px_#ff3c00]'
                : 'bg-transparent border-gray-800 text-gray-400 hover:border-gray-600 hover:text-gray-200'
            }`}
          >
            📜 Ritual
          </button>
          <button
            onClick={() => setActiveTab('grimorio')}
            className={`px-4 py-2 border transition-all duration-300 font-bold uppercase tracking-widest ${
              activeTab === 'grimorio'
                ? 'bg-abyss-accent border-abyss-accent text-white shadow-[0_0_10px_#ff3c00]'
                : 'bg-transparent border-gray-800 text-gray-400 hover:border-gray-600 hover:text-gray-200'
            }`}
          >
            📖 Grimório
          </button>
        </nav>
      </div>
      <span className="text-sm">
        Status: <strong style={{ color: statusColor }}>{status}</strong>
      </span>
    </header>
  );
}
