import { useState, useRef } from 'react';
import Header from './components/Header';
import Panel from './components/Panel';
import Editor from '@monaco-editor/react'; // NOVO: Importando o VS Code Engine

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

  const [resultado, setResultado] = useState({ cpp: '', ast: '', tokens: '' });
  const [status, setStatus] = useState('Aguardando Ritual');
  const [statusColor, setStatusColor] = useState('gray');

  // NOVO: Referências para o editor poder desenhar as linhas vermelhas
  const editorRef = useRef(null);
  const monacoRef = useRef(null);

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
    monacoRef.current = monaco;
  }

  const compilarRitual = async () => {
    setStatus('Compilando...');
    setStatusColor('yellow');
    
    // Limpa os erros antigos antes de compilar
    if (monacoRef.current && editorRef.current) {
      monacoRef.current.editor.setModelMarkers(editorRef.current.getModel(), 'abyssus', []);
    }

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
        // NOVO: Processamento de Erros Inteligente
        setStatus('Erro no Ritual');
        setStatusColor('#ff3c00');
        setResultado({ cpp: '', ast: '', tokens: '' });

        if (data.erros && monacoRef.current) {
          // Transforma o erro do Python em uma linha vermelha no Editor
          const markers = data.erros.map((err) => ({
            startLineNumber: err.linha,
            startColumn: 1,
            endLineNumber: err.linha,
            endColumn: 100, // Marca a linha toda
            message: err.mensagem,
            severity: monacoRef.current.MarkerSeverity.Error
          }));
          
          monacoRef.current.editor.setModelMarkers(editorRef.current.getModel(), 'abyssus', markers);
        }
      }
    } catch (error) {
      setStatus('Servidor Caído');
      setStatusColor('#ff3c00');
    }
  };

  const baixarArquivoIoT = () => { /* Sua função de baixar continua igual */ };

  return (
    <div className="min-h-screen p-5 font-mono flex flex-col">
      <Header status={status} statusColor={statusColor} />

      <div className="flex gap-4 mb-5">
        <button onClick={compilarRitual} className="bg-abyss-accent hover:bg-abyss-accent-hover text-white font-bold py-3 px-6 uppercase tracking-widest transition-all duration-300 shadow-[0_0_10px_#ff3c00]">
          Executar Transpilação
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 flex-grow">
        <Panel title="Código Fonte Demoníaco (.ld)" textColor="text-abyss-green">
          {/* NOVO: Substituímos o <textarea> pelo Monaco Editor */}
          <Editor
            height="100%"
            theme="vs-dark"
            defaultLanguage="c" // Ajuda a colorir as chaves e parênteses nativamente
            value={codigo}
            onChange={(value) => setCodigo(value)}
            onMount={handleEditorDidMount}
            options={{
              minimap: { enabled: false },
              fontSize: 16,
              fontFamily: "'Fira Code', monospace",
              scrollBeyondLastLine: false,
            }}
          />
        </Panel>

        <Panel title="Código C++ Gerado (Arduino)" textColor="text-abyss-blue">
          <pre>{resultado.cpp}</pre>
        </Panel>

        {/* ... (os outros dois painéis de AST e Tokens continuam aqui embaixo igual) ... */}
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