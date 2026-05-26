import { useRef, useCallback } from 'react';
import Editor from '@monaco-editor/react';

export default function CodeEditor({ codigo, setCodigo, onEditorMount }) {
  const editorRef = useRef(null);
  const monacoRef = useRef(null);
  const isInitialMount = useRef(true);

  const handleEditorMount = useCallback((editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;

    // Inicializar com o código padrão apenas na primeira montagem
    if (isInitialMount.current) {
      editor.setValue(codigo);
      isInitialMount.current = false;
    }

    // Chamar callback externo
    if (onEditorMount) {
      onEditorMount(editor, monaco);
    }
  }, [codigo, onEditorMount]);

  const handleChange = useCallback((value) => {
    if (value !== undefined) {
      setCodigo(value);
    }
  }, [setCodigo]);

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
        defaultValue={codigo}
        onChange={handleChange}
        onMount={handleEditorMount}
        options={{
          // Layout
          minimap: { enabled: false },
          fontSize: 16,
          fontFamily: "'Fira Code', monospace",
          scrollBeyondLastLine: false,
          padding: { top: 15 },
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
          renderWhitespace: 'none',
          renderControlCharacters: false,
          renderLineHighlight: 'line',
          bracketPairColorization: { enabled: true },

          // Indentação
          tabSize: 2,
          insertSpaces: true,
          useTabStops: true,
          detectIndentation: true,
          autoIndent: 'keep',

          // Desativar interferências
          quickSuggestions: false,
          parameterHints: { enabled: false },
          suggestOnTriggerCharacters: false,
          formatOnPaste: false,
          formatOnType: false,
          formatOnSave: false,

          // Auto-fechamento simples
          autoClosingBrackets: 'languageDefined',
          autoClosingQuotes: 'languageDefined',
          autoClosingDelete: 'auto',
          autoSurround: 'languageDefined',

          // Sem extras
          codeLens: false,
          folding: true,
          foldingHighlight: true,

          // Sem hints
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

          // Sem conflitos
          matchBrackets: 'always',
          renderFinalNewline: 'auto',
          trimAutoWhitespace: true,
          trimFinalNewlines: true,

          // Importante: não scroll ao editar
          scrollPredominantAxis: true,
        }}
      />
    </div>
  );
}
