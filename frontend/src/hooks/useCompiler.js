import { useState, useRef, useCallback, useEffect } from 'react';
import { DEFAULT_RITUAL_CODE } from '@/constants/ritualTemplates';
import { compileRitual } from '@/services/compilerService';

export function useCompiler() {
  const [codigo, setCodigo] = useState(DEFAULT_RITUAL_CODE);
  const [resultado, setResultado] = useState({ cpp: '', ast: null, graphAst: null, tokens: [], logs: [] });
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

  const handleEditorMount = useCallback((editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
  }, []);

  const handleCodigo = useCallback((value) => {
    setCodigo(value || '');
  }, []);

  const setModalOpen = useCallback((key, isOpen) => {
    setModalState(prev => ({ ...prev, [key]: isOpen }));
  }, []);

  const cleanMarkers = () => {
    if (monacoRef.current && editorRef.current) {
      monacoRef.current.editor.setModelMarkers(editorRef.current.getModel(), 'abyssus', []);
    }
  };

  const applyErrorMarkers = (erros) => {
    if (monacoRef.current && editorRef.current && erros.length > 0) {
      const markers = erros.map((err) => ({
        startLineNumber: err.linha || 1,
        startColumn: 1,
        endLineNumber: err.linha || 1,
        endColumn: 100,
        message: err.mensagem,
        severity: monacoRef.current.MarkerSeverity.Error
      }));
      monacoRef.current.editor.setModelMarkers(editorRef.current.getModel(), 'abyssus', markers);
    }
  };

  // Validação em tempo real (Debounce de 1000ms)
  useEffect(() => {
    if (!editorRef.current || !monacoRef.current) return;

    const timer = setTimeout(async () => {
      try {
        await compileRitual(codigo);
        // Se compilou com sucesso na validação silenciosa: limpa qualquer marcador vermelho!
        cleanMarkers();
      } catch (err) {
        if (err.status === 'error') {
          // Se deu erro, aplica marcadores vermelhos em tempo real!
          cleanMarkers();
          applyErrorMarkers(err.erros);
        }
      }
    }, 1000);

    return () => clearTimeout(timer);
  }, [codigo]);

  const compilar = async () => {
    setStatus('Canalizando Ritual...');
    setStatusColor('#a78bfa');
    setErroAtual(null);
    setSugestaoErro(null);
    cleanMarkers();

    try {
      const tempoMinimoInvocacao = new Promise(resolve => setTimeout(resolve, 1800));
      const chamadaCompilacao = compileRitual(codigo);

      const [data] = await Promise.all([chamadaCompilacao, tempoMinimoInvocacao]);

      setStatus('Ritual Concluído!');
      setStatusColor('#32ff7e');
      setResultado({
        cpp: data.cpp,
        ast: data.ast,
        graphAst: data.graph_ast,
        tokens: data.tokens || [],
        logs: data.logs || []
      });
    } catch (err) {
      if (err.status === 'error') {
        setStatus('Erro no Ritual');
        setStatusColor('#ff3c00');
        setResultado({ cpp: '', ast: null, graphAst: null, tokens: [], logs: [] });

        const primeiroErro = err.erros[0];
        setErroAtual(primeiroErro.mensagem);
        setSugestaoErro(primeiroErro.sugestao || null);
        applyErrorMarkers(err.erros);
      } else {
        setStatus('Conexão Perdida');
        setStatusColor('#ff3c00');
        setErroAtual('Falha na Conexão com o Backend');
        setSugestaoErro('Verifique se o servidor Python está rodando em localhost:5000');
      }
    }
  };

  const baixarArquivoIno = () => {
    if (!resultado.cpp || resultado.cpp.startsWith('Erro')) {
      return;
    }
    
    const agora = new Date();
    const ano = agora.getFullYear();
    const mes = String(agora.getMonth() + 1).padStart(2, '0');
    const dia = String(agora.getDate()).padStart(2, '0');
    const hora = String(agora.getHours()).padStart(2, '0');
    const min = String(agora.getMinutes()).padStart(2, '0');
    const seg = String(agora.getSeconds()).padStart(2, '0');
    const timestamp = `${ano}${mes}${dia}_${hora}${min}${seg}`;

    const blob = new Blob([resultado.cpp], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `ritual_sagrado_${timestamp}.ino`;
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return {
    codigo,
    setCodigo: handleCodigo,
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
  };
}
