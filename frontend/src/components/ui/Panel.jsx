import React from 'react';

export default function Panel({ title, children, textColor = "text-abyss-text", onMaximize, isMaximized = false }) {
  return (
    <div className="bg-abyss-panel border border-gray-800 flex flex-col p-3 rounded h-full">
      <div className="flex justify-between items-center text-xs uppercase text-gray-500 mb-2 border-b border-gray-800 pb-1 flex-shrink-0">
        <span>{title}</span>
        {onMaximize && (
          <button
            onClick={(e) => {
              e.currentTarget.blur();
              onMaximize();
            }}
            className="text-gray-500 hover:text-abyss-accent transition-colors text-base hover:shadow-[0_0_8px_#ff3c00] font-bold px-1"
            title={isMaximized ? "Recolher Tela" : "Expandir para Tela Cheia"}
          >
            {isMaximized ? "✕" : "⛶"}
          </button>
        )}
      </div>
      <div className={`flex-1 overflow-visible text-sm ${textColor} relative min-h-0`}>
        {children}
      </div>
    </div>
  );
}
