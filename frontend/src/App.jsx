import { useIntro } from '@/hooks/useIntro';
import { useCompiler } from '@/hooks/useCompiler';
import Header from '@/components/layout/Header';
import Panel from '@/components/ui/Panel';
import ModalFullscreen from '@/components/ui/ModalFullscreen';
import ErrorToast from '@/components/ui/ErrorToast';
import ASTGraph from '@/features/compiler/components/ASTGraph';
import CodeEditor from '@/features/compiler/components/CodeEditor';

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
    baixarArquivoIoT
  } = useCompiler();

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
          onClick={compilar}
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
            onMaximize={() => setModalOpen('editorFullscreen', true)}
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

        {/* Grid 2x2 - Previews */}
        <div className="grid grid-cols-2 gap-4 flex-1 min-h-0 overflow-hidden">
          {/* C++ Preview */}
          <div className="min-h-0">
            <Panel
              title="Código C++ (Arduino) - Preview"
              textColor="text-abyss-blue"
              onMaximize={() => setModalOpen('cppFullscreen', true)}
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
              onMaximize={() => setModalOpen('astFullscreen', true)}
            >
              <ASTGraph key={resultado.ast ? JSON.stringify(resultado.ast).length : 'empty'} ast={resultado.ast} />
            </Panel>
          </div>

          {/* Tokens Preview */}
          <div className="min-h-0">
            <Panel
              title="Tokens (Léxico) - Preview"
              textColor="text-orange-400"
              onMaximize={() => setModalOpen('tokensFullscreen', true)}
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

      {/* Modais Fullscreen */}
      <ModalFullscreen
        isOpen={modalState.editorFullscreen}
        onClose={() => setModalOpen('editorFullscreen', false)}
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

      <ModalFullscreen
        isOpen={modalState.cppFullscreen}
        onClose={() => setModalOpen('cppFullscreen', false)}
        title="Código C++ Gerado (Arduino) - Fullscreen"
      >
        <div className="w-full h-full overflow-auto bg-[#0a0a0a] rounded">
          <pre className="text-sm font-mono whitespace-pre-wrap break-words p-4 text-gray-300">
            {resultado.cpp || 'Nenhum código gerado ainda...'}
          </pre>
        </div>
      </ModalFullscreen>

      <ModalFullscreen
        isOpen={modalState.astFullscreen}
        onClose={() => setModalOpen('astFullscreen', false)}
        title="Árvore Sintática Abstrata (AST) - Fullscreen"
      >
        <div style={{ width: '100%', height: '100%' }}>
          <ASTGraph key={resultado.ast ? JSON.stringify(resultado.ast).length : 'empty'} ast={resultado.ast} />
        </div>
      </ModalFullscreen>

      <ModalFullscreen
        isOpen={modalState.tokensFullscreen}
        onClose={() => setModalOpen('tokensFullscreen', false)}
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