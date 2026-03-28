import { useState } from 'react';
import Header from './components/Header';
import Panel from './components/Panel';

function App() {
  const [codigo, setCodigo] = useState(`Sanguis led = 13;
Sanguis_Fluens freq = 1.5;

Vazium Exordium() {
    Habitus(led, Ignis);
}

Vazium Inferna() {
    Si (freq > 1.0) {
        Incantare(led, Ignis);
        Mora(500);
        Incantare(led, Tenebrae);
        Mora(500);
    }
}`);

  const [resultado, setResultado] = useState({
    cpp: '',
    ast: '',
    tokens: ''
  });

  const [status, setStatus] = useState('Aguardando Ritual');
  const [statusColor, setStatusColor] = useState('gray');

  const compilarRitual = async () => {
    setStatus('Compilando...');
    setStatusColor('yellow');

    try {
      const response = await fetch('http://localhost:5000/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: codigo })
      });

      const data = await response.json();

      if (data.status === 'success') {
        setStatus('Sucesso!');
        setStatusColor('#32ff7e');
        
        setResultado({
          cpp: data.cpp,
          ast: JSON.stringify(data.ast, null, 2),
          tokens: data.tokens.join('\n')
        });
      } else {
        throw new Error(data.error);
      }
    } catch (error) {
      setStatus('Erro no Ritual');
      setStatusColor('#ff3c00');
      
      setResultado({
        cpp: `Erro: ${error.message}`,
        ast: '',
        tokens: ''
      });
    }
  };

  return (
    <div className="min-h-screen p-5 font-mono flex flex-col">
      <Header status={status} statusColor={statusColor} />

      <button 
        onClick={compilarRitual}
        className="bg-abyss-accent hover:bg-abyss-accent-hover text-white font-bold py-3 px-6 uppercase tracking-widest transition-all duration-300 shadow-[0_0_10px_#ff3c00] hover:shadow-[0_0_20px_#ff3c00] mb-5 w-fit"
      >
        Executar Transpilação
      </button>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 flex-grow">
        <Panel title="Código Fonte Demoníaco (.ld)" textColor="text-abyss-green">
          <textarea 
            className="w-full h-full bg-transparent border-none resize-none outline-none font-inherit"
            spellCheck="false"
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
          />
        </Panel>

        <Panel title="Código C++ Gerado (Arduino)" textColor="text-abyss-blue">
          <pre>{resultado.cpp}</pre>
        </Panel>

        <Panel title="Árvore Sintática Abstrata (AST)" textColor="text-gray-300">
          <pre>{resultado.ast}</pre>
        </Panel>

        <Panel title="Tabela de Tokens (Léxico)" textColor="text-orange-400 text-xs">
          <pre>{resultado.tokens}</pre>
        </Panel>
      </div>
    </div>
  );
}

export default App;