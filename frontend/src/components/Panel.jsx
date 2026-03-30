import React from 'react';

export default function Panel({ title, children, textColor = "text-abyss-text" }) {
  return (
    <div className="bg-abyss-panel border border-gray-800 flex flex-col p-3 rounded h-full min-h-[250px]">
      <div className="text-xs uppercase text-gray-500 mb-2 border-b border-gray-800 pb-1">
        {title}
      </div>
      <div className={`flex-grow overflow-auto text-sm ${textColor} relative`}>
        {children}
      </div>
    </div>
  );
}