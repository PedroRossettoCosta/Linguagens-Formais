import { useState, useMemo } from 'react';
import { useIntro } from '@/hooks/useIntro';
import { useCompiler } from '@/hooks/useCompiler';
import Header from '@/components/layout/Header';
import Panel from '@/components/ui/Panel';
import ErrorToast from '@/components/ui/ErrorToast';
import ASTGraph from '@/features/compiler/components/ASTGraph';
import CodeEditor from '@/features/compiler/components/CodeEditor';
import GrimorioDocs from '@/features/compiler/components/GrimorioDocs';

function App() {
  const { despertando, esconderIntro } = useIntro();
  const {
    codigo,
    setCodigo,
    resultado,
    status,
    statusColor,
    erroAtual,
    setErroAtual,
    sugestaoErro,
    setSugestaoErro,
    modalState,
    setModalOpen,
    handleEditorMount,
    compilar,
    baixarArquivoIno
  } = useCompiler();

  const [activeTab, setActiveTab] = useState('ritual');

  const cppPanelContent = useMemo(() => (
    <pre className="text-xs overflow-auto h-full whitespace-pre-wrap break-words p-2 font-mono">
      {resultado.cpp || 'Aguardando compilação...'}
    </pre>
  ), [resultado.cpp]);

  const terminalPanelContent = useMemo(() => {
    if (!resultado.logs || resultado.logs.length === 0) {
      return <div className="text-gray-600 italic text-xs">Terminal aguarda compilação...</div>;
    }
    return (
      <div className="bg-[#0a0a0a] h-full w-full p-3 font-mono text-xs overflow-auto border border-gray-900 rounded shadow-inner">
        {resultado.logs.slice(-12).map((log, index) => {
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
        })}
      </div>
    );
  }, [resultado.logs]);

  const astPanelContent = useMemo(() => (
    <ASTGraph key={resultado.graphAst ? JSON.stringify(resultado.graphAst).length : 'empty'} ast={resultado.graphAst} />
  ), [resultado.graphAst]);

  const tokensPanelContent = useMemo(() => {
    if (!resultado.tokens || resultado.tokens.length === 0) {
      return (
        <div className="flex items-center justify-center h-full text-gray-600 italic text-xs">
          Aguardando tokens...
        </div>
      );
    }
    return (
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
            {(modalState.tokensFullscreen ? resultado.tokens : resultado.tokens.slice(0, 10)).map((token, idx) => (
              <tr key={idx} className="border-b border-gray-800/40 hover:bg-gray-800/40">
                <td className="py-1 px-1 text-gray-600 font-mono">{token.linha}</td>
                <td className="py-1 px-1 text-orange-400 font-semibold">{token.tipo}</td>
                <td className="py-1 px-1 text-gray-300 font-mono truncate">{token.valor}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {!modalState.tokensFullscreen && resultado.tokens.length > 10 && (
          <div className="text-xs text-gray-500 p-1 italic bg-[#0a0a0a]">
            +{resultado.tokens.length - 10} tokens (fullscreen)
          </div>
        )}
      </div>
    );
  }, [resultado.tokens, modalState.tokensFullscreen]);

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

      <Header status={status} statusColor={statusColor} activeTab={activeTab} setActiveTab={setActiveTab} />

      {activeTab === 'ritual' ? (
        <>
          <div className="flex gap-4 mb-5">
            <button
              onClick={(e) => {
                e.currentTarget.blur();
                compilar();
              }}
              className="bg-abyss-accent hover:bg-abyss-accent-hover text-white font-bold py-3 px-6 uppercase tracking-widest transition-all duration-300 shadow-[0_0_10px_#ff3c00] hover:shadow-[0_0_25px_#ff3c00]"
            >
              Executar
            </button>

            <button
              onClick={(e) => {
                e.currentTarget.blur();
                baixarArquivoIno();
              }}
              disabled={!resultado.cpp || resultado.cpp.startsWith('Erro')}
              className="bg-abyss-panel border border-abyss-accent text-abyss-accent hover:bg-gray-900 hover:text-white font-bold py-3 px-6 uppercase tracking-widest transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Baixar (.ino)
            </button>
          </div>

          <div className="flex-1 flex flex-col gap-4 overflow-hidden relative">
        {/* Editor - Seção Expansível In-Place */}
        <div className={`transition-all duration-300 ${
          modalState.editorFullscreen 
            ? 'fixed inset-6 z-50 m-0 shadow-[0_0_60px_rgba(255,60,0,0.6)] border border-abyss-accent bg-abyss-panel rounded-lg' 
            : 'flex-none h-96'
        }`}>
          <Panel
            title={modalState.editorFullscreen ? "Código Fonte Sobrenatural (.ld) - Tela Cheia" : "Código Fonte Sobrenatural (.ld)"}
            textColor="text-abyss-green"
            onMaximize={() => setModalOpen('editorFullscreen', !modalState.editorFullscreen)}
            isMaximized={modalState.editorFullscreen}
          >
            <div className="w-full h-full">
              <CodeEditor
                codigo={codigo}
                setCodigo={setCodigo}
                onEditorMount={handleEditorMount}
              />
            </div>
          </Panel>
        </div>

        {/* Grid 2x2 - Previews com Expansões In-Place */}
        <div className="grid grid-cols-2 gap-4 flex-1 min-h-0 overflow-hidden">
          
          {/* C++ Preview */}
          <div className={`min-h-0 transition-all duration-300 ${
            modalState.cppFullscreen 
              ? 'fixed inset-6 z-50 m-0 shadow-[0_0_60px_rgba(255,60,0,0.6)] border border-abyss-accent bg-abyss-panel rounded-lg' 
              : ''
          }`}>
            <Panel
              title={modalState.cppFullscreen ? "Código C++ Gerado (Arduino) - Tela Cheia" : "Código C++ (Arduino) - Preview"}
              textColor="text-abyss-blue"
              onMaximize={() => setModalOpen('cppFullscreen', !modalState.cppFullscreen)}
              isMaximized={modalState.cppFullscreen}
            >
              {cppPanelContent}
            </Panel>
          </div>

          {/* Terminal Preview (Apenas Apresentação Fictícia no Simulador) */}
          <div className="min-h-0">
            <Panel
              title="Terminal de Revelação (Simulador) - Preview"
              textColor="text-gray-300"
            >
              {terminalPanelContent}
            </Panel>
          </div>

          {/* AST Preview */}
          <div className={`min-h-0 transition-all duration-300 ${
            modalState.astFullscreen 
              ? 'fixed inset-6 z-50 m-0 shadow-[0_0_60px_rgba(255,60,0,0.6)] border border-abyss-accent bg-abyss-panel rounded-lg' 
              : ''
          }`}>
            <Panel
              title={modalState.astFullscreen ? "Árvore Sintática Abstrata (AST) - Tela Cheia" : "Árvore Sintática (AST) - Preview"}
              textColor="text-gray-300"
              onMaximize={() => setModalOpen('astFullscreen', !modalState.astFullscreen)}
              isMaximized={modalState.astFullscreen}
            >
              {astPanelContent}
            </Panel>
          </div>

          {/* Tokens Preview */}
          <div className={`min-h-0 transition-all duration-300 ${
            modalState.tokensFullscreen 
              ? 'fixed inset-6 z-50 m-0 shadow-[0_0_60px_rgba(255,60,0,0.6)] border border-abyss-accent bg-abyss-panel rounded-lg' 
              : ''
          }`}>
            <Panel
              title={modalState.tokensFullscreen ? "Inspetor de Tokens (Léxico) - Tela Cheia" : "Tokens (Léxico) - Preview"}
              textColor="text-orange-400"
              onMaximize={() => setModalOpen('tokensFullscreen', !modalState.tokensFullscreen)}
              isMaximized={modalState.tokensFullscreen}
            >
              {tokensPanelContent}
            </Panel>
          </div>

        </div>
      </div>
        </>
      ) : (
        <GrimorioDocs />
      )}

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