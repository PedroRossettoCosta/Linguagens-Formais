import React from 'react';
import ReactDOM from 'react-dom';

export default function ModalFullscreen({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
      <div className="relative w-11/12 h-5/6 max-w-6xl bg-[#0f0f0f] border border-abyss-accent rounded-lg shadow-[0_0_30px_#ff3c00] overflow-hidden flex flex-col">
        <div className="flex justify-between items-center p-4 border-b border-abyss-accent/30 bg-[#0a0a0a]">
          <h2 className="text-abyss-accent uppercase tracking-widest font-bold text-lg">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="text-abyss-accent hover:text-white transition-colors text-2xl font-bold leading-none hover:shadow-[0_0_15px_#ff3c00]"
          >
            ✕
          </button>
        </div>

        <div className="flex-1 overflow-auto p-4">
          {children}
        </div>
      </div>
    </div>,
    document.body
  );
}
