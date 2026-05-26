import React, { useEffect, useState } from 'react';

export default function ErrorToast({ erro, sugestao, onClose }) {
  const [glitch, setGlitch] = useState(false);

  useEffect(() => {
    if (!erro) return;

    const interval = setInterval(() => {
      setGlitch(prev => !prev);
    }, 150);

    return () => clearInterval(interval);
  }, [erro]);

  if (!erro) return null;

  return (
    <div
      className={`fixed bottom-4 right-4 z-40 max-w-sm p-4 rounded border-2 border-abyss-accent bg-[#1a0a0a] transition-all glitch-effect ${
        glitch ? 'translate-x-1 translate-y-1' : ''
      }`}
      style={{
        boxShadow: `0 0 15px ${glitch ? '#ff3c00' : '#ff3c00/50'}`,
      }}
    >
      <div className="text-abyss-accent font-bold uppercase tracking-widest mb-2 text-sm">
        ⚠️ Heresia Detectada
      </div>

      <p className="text-sm text-gray-300 mb-3 font-mono">{erro}</p>

      {sugestao && (
        <div className="text-xs text-yellow-400 italic border-l-2 border-yellow-400 pl-2 mb-3 bg-yellow-400/5 py-2">
          💡 Sugestão: {sugestao}
        </div>
      )}

      <button
        onClick={onClose}
        className="mt-2 text-xs uppercase text-abyss-accent hover:text-white hover:shadow-[0_0_10px_#ff3c00] transition-all px-2 py-1 border border-abyss-accent hover:bg-abyss-accent/20 rounded"
      >
        Aceitar
      </button>
    </div>
  );
}
