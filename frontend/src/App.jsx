import { useState, useRef, useEffect, useCallback } from 'react';
import Header from './components/Header';
import Panel from './components/Panel';
import ASTGraph from './components/ASTGraph';
import CodeEditor from './components/CodeEditor';
import ModalFullscreen from './components/ModalFullscreen';
import ErrorToast from './components/ErrorToast';

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

  const [resultado, setResultado] = useState({ cpp: '', ast: null, tokens: [], logs: [] });
  const [status, setStatus] = useState('Aguardando Ritual');
  const [statusColor, setStatusColor] = useState('gray');
  const [erroAtual, setErroAtual] = useState(null);
  const [sugestaoErro, setSugestaoErro] = useState(null);

  const [modalState, setModalState] = useState({
    editorFullscreen: false,
    cppFullscreen: false,
    astFullscreen: false,
    tokensFullscreen: false,
  });

  const editorRef = useRef(null);
  const monacoRef = useRef(null);

  useEffect(() => {
    const timerIntro = setTimeout(() => {
      setDespertando(false);
      setTimeout(() => setEsconderIntro(true), 1500);
    }, 2500);
    return () => clearTimeout(timerIntro);
  }, []);

  const handleEditorMount = useCallback((editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
  }, []);

  const handleCodigo = useCallback((value) => {
    setCodigo(value || '');
  }, []);

const compilarRitual = async () => {
    setStatus('Canalizando Ritual...');
    setStatusColor('#a78bfa');
    setErroAtual(null);
    setSugestaoErro(null);

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
          tokens: data.tokens || [],
          logs: data.logs || []
        });
      } else {
        setStatus('Erro no Ritual');
        setStatusColor('#ff3c00');
        setResultado({ cpp: '', ast: null, tokens: [], logs: [] });

        if (data.erros && data.erros.length > 0) {
          const primeiroErro = data.erros[0];
          setErroAtual(primeiroErro.mensagem);
          setSugestaoErro(primeiroErro.sugestao || null);

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
      setErroAtual('Falha na Conexão com o Backend');
      setSugestaoErro('Verifique se o servidor Python está rodando em localhost:5000');
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

      <div className="flex gap-4 mb-5">
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

      <div className="flex-1 flex flex-col gap-4 overflow-hidden">
        {/* Editor - Seção Expansível */}
        <div className="flex-none h-96">
          <Panel
            title="Código Fonte Sobrenatural (.ld)"
            textColor="text-abyss-green"
            onMaximize={() => setModalState(prev => ({ ...prev, editorFullscreen: true }))}
          >
            <div className="w-full h-full">
              <CodeEditor
                codigo={codigo}
                setCodigo={handleCodigo}
                onEditorMount={handleEditorMount}
              />
            </div>
          </Panel>
        </div>

        {/* Grid 2x2 - Previews */}
        <div className="grid grid-cols-2 gap-4 flex-1 min-h-0 overflow-hidden">
          {/* C++ Preview */}
          <div className="min-h-0">
            <Panel
              title="Código C++ (Arduino) - Preview"
              textColor="text-abyss-blue"
              onMaximize={() => setModalState(prev => ({ ...prev, cppFullscreen: true }))}
            >
              <pre className="text-xs overflow-auto h-full whitespace-pre-wrap break-words p-2">
                {resultado.cpp || 'Aguardando compilação...'}
              </pre>
            </Panel>
          </div>

          {/* Terminal Preview */}
          <div className="min-h-0">
            <Panel
              title="Terminal de Revelação (Simulador) - Preview"
              textColor="text-gray-300"
            >
              <div className="bg-[#0a0a0a] h-full w-full p-3 font-mono text-xs overflow-auto border border-gray-900 rounded shadow-inner">
                {resultado.logs && resultado.logs.length > 0 ? (
                  resultado.logs.slice(-12).map((log, index) => {
                    let cor = "text-gray-400";
                    if (log.includes("[SISTEMA]")) cor = "text-blue-400 font-bold";
                    if (log.includes("[HARDWARE]")) cor = "text-yellow-500";
                    if (log.includes("[REVELAÇÃO]")) cor = "text-green-400";
                    if (log.includes("[TEMPO]")) cor = "text-purple-400 italic";

                    return (
                      <div key={index} className={`${cor} tracking-wide mb-0.5`}>
                        <span className="opacity-50">{">"}</span> {log}
                      </div>
                    );
                  })
                ) : (
                  <div className="text-gray-600 italic text-xs">Terminal aguarda compilação...</div>
                )}
              </div>
            </Panel>
          </div>

          {/* AST Preview */}
          <div className="min-h-0">
            <Panel
              title="Árvore Sintática (AST) - Preview"
              textColor="text-gray-300"
              onMaximize={() => setModalState(prev => ({ ...prev, astFullscreen: true }))}
            >
              <ASTGraph key={resultado.ast ? JSON.stringify(resultado.ast).length : 'empty'} ast={resultado.ast} />
            </Panel>
          </div>

          {/* Tokens Preview */}
          <div className="min-h-0">
            <Panel
              title="Tokens (Léxico) - Preview"
              textColor="text-orange-400"
              onMaximize={() => setModalState(prev => ({ ...prev, tokensFullscreen: true }))}
            >
              {resultado.tokens && resultado.tokens.length > 0 ? (
                <div className="overflow-auto h-full">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead className="sticky top-0 bg-[#0a0a0a] z-10">
                      <tr className="border-b border-gray-800 text-gray-500 uppercase">
                        <th className="py-1 px-1 font-medium">L</th>
                        <th className="py-1 px-1 font-medium">Tipo</th>
                        <th className="py-1 px-1 font-medium">Valor</th>
                      </tr>
                    </thead>
                    <tbody>
                      {resultado.tokens.slice(0, 10).map((token, idx) => (
                        <tr key={idx} className="border-b border-gray-800/40 hover:bg-gray-800/40">
                          <td className="py-1 px-1 text-gray-600 font-mono">{token.linha}</td>
                          <td className="py-1 px-1 text-orange-400 font-semibold">{token.tipo}</td>
                          <td className="py-1 px-1 text-gray-300 font-mono truncate">{token.valor}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {resultado.tokens.length > 10 && (
                    <div className="text-xs text-gray-500 p-1 italic bg-[#0a0a0a]">
                      +{resultado.tokens.length - 10} tokens (fullscreen)
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-gray-600 italic text-xs">
                  Aguardando tokens...
                </div>
              )}
            </Panel>
          </div>
        </div>
      </div>

      {/* Modal: Editor Fullscreen */}
      <ModalFullscreen
        isOpen={modalState.editorFullscreen}
        onClose={() => setModalState(prev => ({ ...prev, editorFullscreen: false }))}
        title="Código Fonte Sobrenatural (.ld) - Fullscreen"
      >
        <div className="w-full h-full">
          <CodeEditor
            codigo={codigo}
            setCodigo={setCodigo}
            onEditorMount={handleEditorMount}
          />
        </div>
      </ModalFullscreen>

      {/* Modal: C++ Fullscreen */}
      <ModalFullscreen
        isOpen={modalState.cppFullscreen}
        onClose={() => setModalState(prev => ({ ...prev, cppFullscreen: false }))}
        title="Código C++ Gerado (Arduino) - Fullscreen"
      >
        <div className="w-full h-full overflow-auto bg-[#0a0a0a] rounded">
          <pre className="text-sm font-mono whitespace-pre-wrap break-words p-4 text-gray-300">
            {resultado.cpp || 'Nenhum código gerado ainda...'}
          </pre>
        </div>
      </ModalFullscreen>

      {/* Modal: AST Fullscreen */}
      <ModalFullscreen
        isOpen={modalState.astFullscreen}
        onClose={() => setModalState(prev => ({ ...prev, astFullscreen: false }))}
        title="Árvore Sintática Abstrata (AST) - Fullscreen"
      >
        <div style={{ width: '100%', height: '100%' }}>
          <ASTGraph key={resultado.ast ? JSON.stringify(resultado.ast).length : 'empty'} ast={resultado.ast} />
        </div>
      </ModalFullscreen>

      {/* Modal: Tokens Fullscreen */}
      <ModalFullscreen
        isOpen={modalState.tokensFullscreen}
        onClose={() => setModalState(prev => ({ ...prev, tokensFullscreen: false }))}
        title="Inspetor de Tokens (Léxico) - Fullscreen"
      >
        {resultado.tokens && resultado.tokens.length > 0 ? (
          <div className="overflow-auto w-full h-full">
            <table className="w-full text-left text-sm border-collapse">
              <thead className="sticky top-0 bg-[#0a0a0a] z-10">
                <tr className="border-b border-gray-800 text-gray-500 uppercase tracking-wider">
                  <th className="py-2 px-3 font-medium">Linha</th>
                  <th className="py-2 px-3 font-medium">Tipo (Token)</th>
                  <th className="py-2 px-3 font-medium">Valor Lido</th>
                </tr>
              </thead>
              <tbody>
                {resultado.tokens.map((token, idx) => (
                  <tr
                    key={idx}
                    className="border-b border-gray-800/40 hover:bg-gray-800/40 transition-colors duration-150"
                  >
                    <td className="py-2 px-3 text-gray-600 font-mono">{token.linha}</td>
                    <td className="py-2 px-3 text-orange-400 font-semibold tracking-wide">{token.tipo}</td>
                    <td className="py-2 px-3 text-gray-300 font-mono">{token.valor}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="flex items-center justify-center w-full h-full text-gray-600 italic">
            Aguardando tokens...
          </div>
        )}
      </ModalFullscreen>

      <ErrorToast
        erro={erroAtual}
        sugestao={sugestaoErro}
        onClose={() => {
          setErroAtual(null);
          setSugestaoErro(null);
        }}
      />
    </div>
  );
}

export default App;