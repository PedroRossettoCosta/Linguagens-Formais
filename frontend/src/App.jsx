import { useState, useRef, useEffect } from 'react';
import Header from './components/Header';
import Panel from './components/Panel';
import ASTGraph from './components/ASTGraph';
import Editor from '@monaco-editor/react';

function App() {
  const [despertando, setDespertando] = useState(true);
  const [esconderIntro, setEsconderIntro] = useState(false);

  const [codigo, setCodigo] = useState(`Sanguis led = 13;
Sanguis_Fluens pressao = 1.0;

Vazium Exordium() {
    Revelare("Iniciando a estufa inteligente...");
    Habitus(led, Ignis);
}

Vazium Inferna() {
    pressao = pressao + 0.5;
    
    Si (pressao > 1.2) {
        Revelare("Cuidado! Pressao subiu muito!");
        Incantare(led, Ignis);
        Mora(1000);
        Incantare(led, Tenebrae);
    }
}`);

  const [resultado, setResultado] = useState({ cpp: '', ast: null, tokens: '', logs: [] });
  const [status, setStatus] = useState('Aguardando Ritual');
  const [statusColor, setStatusColor] = useState('gray');

  const editorRef = useRef(null);
  const monacoRef = useRef(null);

  useEffect(() => {
    const timerIntro = setTimeout(() => {
      setDespertando(false);
      setTimeout(() => setEsconderIntro(true), 1500); 
    }, 2500);
    return () => clearTimeout(timerIntro);
  }, []);

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
    monacoRef.current = monaco;
  }

const compilarRitual = async () => {
    setStatus('Canalizando Ritual...');
    setStatusColor('#a78bfa');
    
    if (monacoRef.current && editorRef.current) {
      monacoRef.current.editor.setModelMarkers(editorRef.current.getModel(), 'abyssus', []);
    }

    try {
      const tempoDeInvocacao = new Promise(resolve => setTimeout(resolve, 1800));
      const requisicaoPython = fetch('http://localhost:5000/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: codigo })
      });

      const [response] = await Promise.all([requisicaoPython, tempoDeInvocacao]);
      const data = await response.json();

      if (data.status === 'success') {
        setStatus('Ritual Concluído!');
        setStatusColor('#32ff7e');
        setResultado({
          cpp: data.cpp,
          ast: data.ast,
          tokens: data.tokens.join('\n'),
          logs: data.logs || [] 
        });
      } else {
        setStatus('Erro no Ritual');
        setStatusColor('#ff3c00');
        setResultado({ cpp: '', ast: null, tokens: '', logs: [] });

        if (data.erros && monacoRef.current) {
          const markers = data.erros.map((err) => ({
            startLineNumber: err.linha,
            startColumn: 1,
            endLineNumber: err.linha,
            endColumn: 100,
            message: err.mensagem,
            severity: monacoRef.current.MarkerSeverity.Error
          }));
          monacoRef.current.editor.setModelMarkers(editorRef.current.getModel(), 'abyssus', markers);
        }
      }
    } catch (error) {
      setStatus('Conexão Perdida');
      setStatusColor('#ff3c00');
    }
  };

  const baixarArquivoIoT = () => {
      if (!resultado.cpp || resultado.cpp.startsWith('Erro')) {
        alert("⚠️ Você precisa compilar um ritual com sucesso antes de extrair sua essência!");
        return;
      }
      
      const blob = new Blob([resultado.cpp], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = 'ritual_sagrado.iot';
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    };

  return (
    <div className={`min-h-screen p-5 font-mono flex flex-col bg-[#0f0f0f] text-gray-200 ${status === 'Canalizando Ritual...' ? 'ritual-ativo' : 'transition-all duration-700'}`}>
      {!esconderIntro && (
        <div className={`fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#050505] ${!despertando ? 'intro-desaparecendo' : ''}`}>
          <h1 className="text-abyss-accent text-5xl md:text-7xl font-bold tracking-widest texto-sinistro uppercase text-center">
            Abyssus
          </h1>
          <p className="mt-6 text-gray-500 tracking-[0.3em] uppercase text-sm animate-pulse">
            Despertando o Motor do Compilador...
          </p>
        </div>
      )}

      <Header status={status} statusColor={statusColor} />

      <div className="flex gap-4 mb-5 z-10">
        <button 
          onClick={compilarRitual} 
          className="bg-abyss-accent hover:bg-abyss-accent-hover text-white font-bold py-3 px-6 uppercase tracking-widest transition-all duration-300 shadow-[0_0_10px_#ff3c00] hover:shadow-[0_0_25px_#ff3c00]"
        >
          Executar
        </button>

        <button 
          onClick={baixarArquivoIoT}
          disabled={!resultado.cpp || resultado.cpp.startsWith('Erro')}
          className="bg-abyss-panel border border-abyss-accent text-abyss-accent hover:bg-gray-900 hover:text-white font-bold py-3 px-6 uppercase tracking-widest transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Baixar (.iot)
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 flex-grow z-10">
        <Panel title="Código Fonte Sobrenatural (.ld)" textColor="text-abyss-green">
          <Editor
            height="100%"
            theme="vs-dark"
            defaultLanguage="c"
            value={codigo}
            onChange={(value) => setCodigo(value)}
            onMount={handleEditorDidMount}
            options={{
              minimap: { enabled: false },
              fontSize: 16,
              fontFamily: "'Fira Code', monospace",
              scrollBeyondLastLine: false,
              fixedOverflowWidgets: true, 
              padding: { top: 15 } 
            }}
          />
        </Panel>

        <Panel title="Código C++ Gerado (Arduino)" textColor="text-abyss-blue">
          <pre>{resultado.cpp}</pre>
        </Panel>

        <div className="lg:col-span-2 h-64">
          <Panel title="Terminal de Revelação (Simulador Mágico)" textColor="text-gray-300">
            <div className="bg-[#0a0a0a] h-full w-full p-4 font-mono text-sm overflow-auto border border-gray-900 rounded shadow-inner">
              {resultado.logs && resultado.logs.length > 0 ? (
                resultado.logs.map((log, index) => {
                  let cor = "text-gray-400";
                  if (log.includes("[SISTEMA]")) cor = "text-blue-400 font-bold";
                  if (log.includes("[HARDWARE]")) cor = "text-yellow-500";
                  if (log.includes("[REVELAÇÃO]")) cor = "text-green-400 text-base";
                  if (log.includes("[TEMPO]")) cor = "text-purple-400 italic";

                  return (
                    <div key={index} className={`mb-1 ${cor} tracking-wide`}>
                      <span className="opacity-50 mr-2">{">"}</span>
                      {log}
                    </div>
                  );
                })
              ) : (
                <div className="text-gray-600 italic animate-pulse">
                  O terminal aguarda a invocação do ritual...
                </div>
              )}
            </div>
          </Panel>
        </div>

        <Panel title="Árvore Sintática Abstrata (AST)" textColor="text-gray-300">
          <ASTGraph ast={resultado.ast} />
        </Panel>

        <Panel title="Tabela de Tokens (Léxico)" textColor="text-orange-400 text-xs">
          <pre>{resultado.tokens}</pre>
        </Panel>
      </div>
    </div>
  );
}

export default App;