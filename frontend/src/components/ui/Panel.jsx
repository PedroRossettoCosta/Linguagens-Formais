import React from 'react';

export default function Panel({ title, children, textColor = "text-abyss-text", onMaximize }) {
  return (
    <div className="bg-abyss-panel border border-gray-800 flex flex-col p-3 rounded h-full">
      <div className="flex justify-between items-center text-xs uppercase text-gray-500 mb-2 border-b border-gray-800 pb-1 flex-shrink-0">
        <span>{title}</span>
        {onMaximize && (
          <button
            onClick={onMaximize}
            className="text-gray-500 hover:text-abyss-accent transition-colors text-lg hover:shadow-[0_0_8px_#ff3c00]"
            title="Expandir para Tela Cheia"
          >
            ⛶
          </button>
        )}
      </div>
      <div className={`flex-1 overflow-auto text-sm ${textColor} relative min-h-0`}>
        {children}
      </div>
    </div>
  );
}
