import { useRef, useCallback, useEffect } from 'react';
import Editor from '@monaco-editor/react';

export default function CodeEditor({ codigo, setCodigo, onEditorMount }) {
  const editorRef = useRef(null);
  const monacoRef = useRef(null);
  const lastValueRef = useRef(codigo);
  const providerRef = useRef(null);

  const handleEditorMount = useCallback((editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;

    // Inicializar o valor na primeira montagem
    editor.setValue(codigo);
    lastValueRef.current = codigo;

    // Limpar provedor anterior se existir nesta ref para evitar duplicidade
    if (providerRef.current) {
      providerRef.current.dispose();
    }

    // Registrar provedor de autocompletar para a linguagem do compilador
    providerRef.current = monaco.languages.registerCompletionItemProvider('c', {
        provideCompletionItems: (model, position) => {
          const word = model.getWordUntilPosition(position);
          const range = {
            startLineNumber: position.lineNumber,
            endLineNumber: position.lineNumber,
            startColumn: word.startColumn,
            endColumn: word.endColumn,
          };

          const suggestions = [
            // Tipos primitivos
            { label: 'Sanguis', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'Sanguis', detail: 'Tipo inteiro (Sanguis / int)', range },
            { label: 'Sanguis_Fluens', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'Sanguis_Fluens', detail: 'Tipo decimal (Sanguis_Fluens / float)', range },
            { label: 'Veritas', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'Veritas', detail: 'Tipo lógico (Veritas / bool)', range },
            { label: 'Vazium', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'Vazium', detail: 'Tipo vazio (Vazium / void)', range },

            // Literais e constantes
            { label: 'Verum', kind: monaco.languages.CompletionItemKind.Value, insertText: 'Verum', detail: 'Verdadeiro (Verum / true)', range },
            { label: 'Falsum', kind: monaco.languages.CompletionItemKind.Value, insertText: 'Falsum', detail: 'Falso (Falsum / false)', range },
            { label: 'Ignis', kind: monaco.languages.CompletionItemKind.Constant, insertText: 'Ignis', detail: 'Estado Alto (Ignis / HIGH)', range },
            { label: 'Tenebrae', kind: monaco.languages.CompletionItemKind.Constant, insertText: 'Tenebrae', detail: 'Estado Baixo (Tenebrae / LOW)', range },
            { label: 'Entrada', kind: monaco.languages.CompletionItemKind.Constant, insertText: 'Entrada', detail: 'Modo Entrada (Entrada / INPUT)', range },
            { label: 'Saida', kind: monaco.languages.CompletionItemKind.Constant, insertText: 'Saida', detail: 'Modo Saída (Saida / OUTPUT)', range },

            // Blocos principais
            { label: 'Exordium', kind: monaco.languages.CompletionItemKind.Snippet, insertText: 'Vazium Exordium() {\n\t$0\n}', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Ritual de Inicialização (Exordium / setup)', range },
            { label: 'Inferna', kind: monaco.languages.CompletionItemKind.Snippet, insertText: 'Vazium Inferna() {\n\t$0\n}', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Ritual Contínuo (Inferna / loop)', range },

            // Controle de fluxo
            { label: 'Si', kind: monaco.languages.CompletionItemKind.Snippet, insertText: 'Si ($1) {\n\t$0\n}', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Condicional Se (Si / if)', range },
            { label: 'Aliter', kind: monaco.languages.CompletionItemKind.Snippet, insertText: 'Aliter {\n\t$0\n}', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Condicional Senão (Aliter / else)', range },
            { label: 'Tormentum', kind: monaco.languages.CompletionItemKind.Snippet, insertText: 'Tormentum ($1) {\n\t$0\n}', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Repetição Enquanto (Tormentum / while)', range },
            { label: 'Iterum', kind: monaco.languages.CompletionItemKind.Snippet, insertText: 'Iterum (Sanguis i = 0; i < $1; i = i + 1) {\n\t$0\n}', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Repetição Contada (Iterum / for)', range },
            { label: 'Redditum', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'Redditum ', detail: 'Retorno (Redditum / return)', range },

            // Funções nativas do hardware
            { label: 'Habitus', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Habitus(${1:led}, ${2:Saida});', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Configura pino (Habitus / pinMode)', range },
            { label: 'Incantare', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Incantare(${1:led}, ${2:Ignis});', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Escreve pino digital (Incantare / digitalWrite)', range },
            { label: 'Sentire', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Sentire(${1:pino})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Lê pino digital (Sentire / digitalRead)', range },
            { label: 'Anima', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Anima(${1:pino})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Lê pino analógico (Anima / analogRead)', range },
            { label: 'Mora', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Mora(${1:1000});', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Congela o tempo (Mora / delay)', range },
            { label: 'Cronos', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Cronos()', detail: 'Tempo decorrido (Cronos / millis)', range },
            { label: 'Vox', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Vox(${1:9600});', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Inicia Serial (Vox / Serial.begin)', range },
            { label: 'Revelare', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Revelare("${1:mensagem}");', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Exibe na Serial (Revelare / Serial.println)', range },
            { label: 'Susurro', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Susurro("${1:mensagem}");', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Sussurra na Serial (Susurro / Serial.print)', range },

            // Diretivas de pré-processador
            { label: 'Invocare', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'Invocare ', detail: 'Inclui biblioteca (Invocare / #include)', range },
            { label: 'Decretum', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'Decretum ', detail: 'Declara macro (Decretum / #define)', range },
            { label: 'Imutabile', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'Imutabile ', detail: 'Declara constante (Imutabile / const)', range },

            // Rituais e constantes para Pureza de Hardware
            { label: 'TemperareCronos', kind: monaco.languages.CompletionItemKind.Method, insertText: 'TemperareCronos(${1:0}, ${2:0}, "${3:pool.ntp.org}", "${4:time.nist.gov}");', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Sincroniza hora NTP (TemperareCronos / configTime)', range },
            { label: 'Aevum', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Aevum(${1:Nihil})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Lê tempo Unix Epoch (Aevum / time)', range },
            { label: 'VerbumAevum', kind: monaco.languages.CompletionItemKind.Method, insertText: 'VerbumAevum(&${1:agora})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Converte tempo Unix para texto (VerbumAevum / ctime)', range },
            { label: 'SignareCaos', kind: monaco.languages.CompletionItemKind.Method, insertText: 'SignareCaos(${1:objetoJson}, ${2:mensagemBuffer});', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Serializa JSON (SignareCaos / serializeJson)', range },
            { label: 'Inanis', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Inanis(${1:valor})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Verifica se valor é profano/indefinido (Inanis / isnan)', range },
            { label: 'Sacratum', kind: monaco.languages.CompletionItemKind.Method, insertText: 'Sacratum("${1:texto}")', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: 'Guarda texto na memória Flash sagrada (Sacratum / F)', range },
            { label: 'NexusFidelis', kind: monaco.languages.CompletionItemKind.Constant, insertText: 'NexusFidelis', detail: 'Conexão WiFi consagrada com sucesso (NexusFidelis / WL_CONNECTED)', range },
            { label: 'Albus', kind: monaco.languages.CompletionItemKind.Constant, insertText: 'Albus', detail: 'Cor branca para displays (Albus / WHITE)', range },
            { label: 'SSD1306_Tensa', kind: monaco.languages.CompletionItemKind.Constant, insertText: 'SSD1306_Tensa', detail: 'Modo de tensão SSD1306 (SSD1306_Tensa / SSD1306_SWITCHCAPVCC)', range }
          ];

          return { suggestions };
        }
      });

    // Chamar callback externo
    if (onEditorMount) {
      onEditorMount(editor, monaco);
    }
  }, [onEditorMount]);

  const handleChange = useCallback((value) => {
    if (value !== undefined) {
      lastValueRef.current = value;
      setCodigo(value);
    }
  }, [setCodigo]);

  // Limpar provedor global ao desmontar o componente para evitar vazamento de memória
  useEffect(() => {
    return () => {
      if (providerRef.current) {
        providerRef.current.dispose();
      }
    };
  }, []);

  // Sincronizar alterações que vêm de fora do editor (como templates)
  useEffect(() => {
    if (editorRef.current && codigo !== lastValueRef.current) {
      editorRef.current.setValue(codigo);
      lastValueRef.current = codigo;
    }
  }, [codigo]);

  return (
    <div
      className="w-full h-full"
      style={{
        display: 'flex',
        flexDirection: 'column',
        isolation: 'isolate'
      }}
    >
      <Editor
        height="100%"
        theme="vs-dark"
        defaultLanguage="c"
        onChange={handleChange}
        onMount={handleEditorMount}
        options={{
          // Layout
          minimap: { enabled: false },
          fontSize: 16,
          fontFamily: "'Fira Code', monospace",
          scrollBeyondLastLine: false,
          padding: { top: 32, bottom: 8 },
          wordWrap: 'on',
          automaticLayout: true,

          // Edição
          readOnly: false,
          domReadOnly: false,

          // Cursor
          smoothScrolling: true,
          cursorSmoothCaretAnimation: 'on',
          cursorStyle: 'line',
          cursorWidth: 2,
          cursorBlinking: 'blink',

          // Renderização
          renderWhitespace: 'boundary', // Mostra pontinhos nos espaços para feedback tátil/foco
          renderControlCharacters: true,
          renderLineHighlight: 'line',
          bracketPairColorization: { enabled: true },

          // Indentação
          tabSize: 2,
          insertSpaces: true,
          useTabStops: true,
          detectIndentation: false, // Impede o monaco de subscrever os tabs
          autoIndent: 'full',

          // Ativar sugestões inteligentes (VSCode Style)
          quickSuggestions: {
            other: true,
            comments: false,
            strings: false
          },
          parameterHints: { enabled: true },
          suggestOnTriggerCharacters: true,
          acceptSuggestionOnEnter: 'on',
          acceptSuggestionOnCommitCharacter: false,
          tabCompletion: 'on',
          wordBasedSuggestions: 'allDocuments',

          // Sem extras extras
          codeLens: false,
          folding: true,
          foldingHighlight: true,

          // Sem hints inline irrelevantes
          semanticHighlighting: { enabled: 'configuredByTheme' },
          inlineHints: { enabled: false },
          inlayHints: { enabled: false },

          // Comportamento de seleção
          selectionClipboard: true,
          copyWithSyntaxHighlighting: true,

          // Scroll
          scrollbar: {
            vertical: 'auto',
            horizontal: 'auto',
            useShadows: false,
            verticalScrollbarSize: 12,
            horizontalScrollbarSize: 12,
          },

          // Sem conflitos de navegação
          matchBrackets: 'always',
          renderFinalNewline: 'auto',
          trimAutoWhitespace: false, // Impede remoção abrupta de espaços ativos que o usuário digita
          trimFinalNewlines: false,

          // Importante: não scroll ao editar
          scrollPredominantAxis: true,
        }}
      />
    </div>
  );
}
