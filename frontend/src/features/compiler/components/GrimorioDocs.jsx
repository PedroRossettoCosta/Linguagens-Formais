import React, { useState, useMemo } from 'react';

const CATEGORIES = {
  ALL: 'Todos',
  TYPES: 'Tipos de Dados',
  HARDWARE: 'Funções de Hardware',
  FLOW: 'Controle de Fluxo',
  META: 'Diretivas e Metaprogramação'
};

const KEYWORDS = [
  // --- Tipos de Dados ---
  {
    word: 'Sanguis',
    cpp: 'int',
    category: 'TYPES',
    description: 'Declara uma variável numérica inteira. Essencial para contagens ou índices.',
    example: 'Sanguis contador = 0;'
  },
  {
    word: 'Sanguis_Fluens',
    cpp: 'float',
    category: 'TYPES',
    description: 'Declara uma variável decimal. Ideal para cálculos científicos e sensores analógicos.',
    example: 'Sanguis_Fluens temperatura = 25.5;'
  },
  {
    word: 'Veritas',
    cpp: 'bool',
    category: 'TYPES',
    description: 'Declara uma variável lógica/booleana. Armazena os estados Verum ou Falsum.',
    example: 'Veritas wifiConectado = Falsum;'
  },
  {
    word: 'Tempus',
    cpp: 'time_t',
    category: 'TYPES',
    description: 'Declara um receptáculo de tempo Unix Epoch (inteiro de 64 bits com sinal).',
    example: 'Tempus agora = Aevum(Nihil);'
  },
  {
    word: 'Verbum',
    cpp: 'String',
    category: 'TYPES',
    description: 'Declara uma cadeia de caracteres dinâmica (objeto String do Arduino).',
    example: 'Verbum mensagem = "Consagração do ESP32";'
  },
  {
    word: 'Inscriptio',
    cpp: 'const char*',
    category: 'TYPES',
    description: 'Declara um ponteiro de caracteres imutável, economizando RAM em strings estáticas.',
    example: 'Inscriptio ssid = "MinhaRedeWiFi";'
  },
  {
    word: 'Littera',
    cpp: 'char',
    category: 'TYPES',
    description: 'Declara um único caractere ou arranjo de caracteres (byte).',
    example: 'Littera perfMsg[128];'
  },
  {
    word: 'Vazium',
    cpp: 'void',
    category: 'TYPES',
    description: 'Indica a ausência de tipo ou retorno de função.',
    example: 'Vazium Exordium() { ... }'
  },

  // --- Funções de Hardware ---
  {
    word: 'Exordium',
    cpp: 'setup()',
    category: 'HARDWARE',
    description: 'O ritual de inicialização. Executado uma única vez ao alimentar o chip.',
    example: 'Vazium Exordium() {\n  Vox(115200);\n}'
  },
  {
    word: 'Inferna',
    cpp: 'loop()',
    category: 'HARDWARE',
    description: 'O ritual eterno. Executado em repetição cíclica infinita.',
    example: 'Vazium Inferna() {\n  Mora(1000);\n}'
  },
  {
    word: 'Habitus',
    cpp: 'pinMode()',
    category: 'HARDWARE',
    description: 'Define se um pino físico agirá como Entrada (INPUT) ou Saida (OUTPUT).',
    example: 'Habitus(4, Saida);'
  },
  {
    word: 'Incantare',
    cpp: 'digitalWrite()',
    category: 'HARDWARE',
    description: 'Envia sinal elétrico Alto (Ignis / HIGH) ou Baixo (Tenebrae / LOW) a um pino.',
    example: 'Incantare(2, Ignis);'
  },
  {
    word: 'Sentire',
    cpp: 'digitalRead()',
    category: 'HARDWARE',
    description: 'Lê o estado elétrico digital de um pino de Entrada.',
    example: 'Veritas pinoAlto = Sentire(15);'
  },
  {
    word: 'Anima',
    cpp: 'analogRead()',
    category: 'HARDWARE',
    description: 'Captura o sopro elétrico analógico de um pino (0 a 4095 no ESP32).',
    example: 'Sanguis valor = Anima(34);'
  },
  {
    word: 'Mora',
    cpp: 'delay()',
    category: 'HARDWARE',
    description: 'Congela o tempo de execução do ritual por milissegundos especificados.',
    example: 'Mora(2000); // Pausa por 2 segundos'
  },
  {
    word: 'Cronos',
    cpp: 'millis()',
    category: 'HARDWARE',
    description: 'Retorna a eternidade decorrida (em milissegundos) desde a inicialização do chip.',
    example: 'Aeternum tempoAgora = Cronos();'
  },
  {
    word: 'Vox',
    cpp: 'Serial.begin()',
    category: 'HARDWARE',
    description: 'Abre o canal de comunicação Serial na taxa especificada.',
    example: 'Vox(115200);'
  },
  {
    word: 'Revelare',
    cpp: 'Serial.println()',
    category: 'HARDWARE',
    description: 'Exibe uma revelação (mensagem) no terminal Serial com quebra de linha.',
    example: 'Revelare("Ritual Concluído!");'
  },
  {
    word: 'Susurro',
    cpp: 'Serial.print()',
    category: 'HARDWARE',
    description: 'Exibe uma revelação (mensagem) no terminal Serial de forma contínua.',
    example: 'Susurro("Aguardando.");'
  },
  {
    word: 'TemperareCronos',
    cpp: 'configTime()',
    category: 'HARDWARE',
    description: 'Configura o relógio interno do chip conectando a servidores NTP.',
    example: 'TemperareCronos(0, 0, "pool.ntp.org");'
  },
  {
    word: 'Aevum',
    cpp: 'time()',
    category: 'HARDWARE',
    description: 'Retorna a data e hora atuais do calendário Unix (Epoch) a partir da conexão NTP.',
    example: 'Tempus dataHora = Aevum(Nihil);'
  },
  {
    word: 'VerbumAevum',
    cpp: 'ctime()',
    category: 'HARDWARE',
    description: 'Converte uma variável Tempus em formato legível de texto.',
    example: 'Revelare(VerbumAevum(&agora));'
  },
  {
    word: 'SignareCaos',
    cpp: 'serializeJson()',
    category: 'HARDWARE',
    description: 'Serializa um documento JSON em um buffer de caracteres.',
    example: 'SignareCaos(jsonDoc, buffer);'
  },
  {
    word: 'Inanis',
    cpp: 'isnan()',
    category: 'HARDWARE',
    description: 'Verifica se a leitura do sensor falhou (NaN / Not-a-Number).',
    example: 'Si (Inanis(leitura)) { ... }'
  },
  {
    word: 'Sacratum',
    cpp: 'F()',
    category: 'HARDWARE',
    description: 'Consagra e guarda uma string na memória flash do chip, poupando SRAM.',
    example: 'Revelare(Sacratum("Texto Guardado na Flash"));'
  },

  // --- Controle de Fluxo ---
  {
    word: 'Si',
    cpp: 'if',
    category: 'FLOW',
    description: 'Avalia uma condição lógica. Se verdadeira, executa o bloco interno.',
    example: 'Si (temperatura > 30.0) { ... }'
  },
  {
    word: 'Aliter',
    cpp: 'else',
    category: 'FLOW',
    description: 'Cláusula executada quando a condição do "Si" falha.',
    example: 'Si (luminosidade > 500) { ... } Aliter { ... }'
  },
  {
    word: 'Tormentum',
    cpp: 'while',
    category: 'FLOW',
    description: 'Laço de tormento/repetição que dura enquanto uma condição for verdadeira.',
    example: 'Tormentum (WiFi.status() != NexusFidelis) { ... }'
  },
  {
    word: 'Iterum',
    cpp: 'for',
    category: 'FLOW',
    description: 'Laço de repetição contada clássico. Permite controle preciso de incrementos.',
    example: 'Iterum (Sanguis i = 0; i < 10; i = i + 1) { ... }'
  },
  {
    word: 'Redditum',
    cpp: 'return',
    category: 'FLOW',
    description: 'Retorna um valor ou interrompe a execução de uma função.',
    example: 'Redditum Verum;'
  },
  {
    word: 'Frangere',
    cpp: 'break',
    category: 'FLOW',
    description: 'Interrompe abruptamente a execução de um laço de repetição.',
    example: 'Si (erroGrave) { Frangere; }'
  },
  {
    word: 'Pergere',
    cpp: 'continue',
    category: 'FLOW',
    description: 'Salta para a próxima iteração do laço atual imediatamente.',
    example: 'Si (ignorarPasso) { Pergere; }'
  },

  // --- Diretivas e Metaprogramação ---
  {
    word: 'Invocare',
    cpp: '#include',
    category: 'META',
    description: 'Invoca uma biblioteca externa das brumas para o escopo atual.',
    example: 'Invocare WiFi;'
  },
  {
    word: 'Decretum',
    cpp: '#define',
    category: 'META',
    description: 'Decretos/Macros de pré-processador para mapeamento de valores rápidos.',
    example: 'Decretum DHTPIN = 4;'
  },
  {
    word: 'Imutabile',
    cpp: 'const',
    category: 'META',
    description: 'Sela uma variável como constante imutável. Previne profanações de valor.',
    example: 'Imutabile Sanguis_Fluens TEMP_MAX = 25.0;'
  },
  {
    word: 'Caos',
    cpp: 'raw C++',
    category: 'META',
    description: 'Injeta um código C++ bruto diretamente na geração de código compilado.',
    example: 'Caos "JsonDocument perfJson;";'
  },
  {
    word: 'Nihil',
    cpp: 'nullptr',
    category: 'META',
    description: 'O valor nulo místico oficial da linguagem para apontar a lugar nenhum.',
    example: 'Tempus agora = Aevum(Nihil);'
  }
];

export default function GrimorioDocs() {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState('ALL');

  const filteredKeywords = useMemo(() => {
    return KEYWORDS.filter(kw => {
      const matchSearch = 
        kw.word.toLowerCase().includes(searchTerm.toLowerCase()) ||
        kw.cpp.toLowerCase().includes(searchTerm.toLowerCase()) ||
        kw.description.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchCategory = activeCategory === 'ALL' || kw.category === activeCategory;

      return matchSearch && matchCategory;
    });
  }, [searchTerm, activeCategory]);

  return (
    <div className="flex-1 flex flex-col gap-6 overflow-hidden text-gray-200">
      {/* Topo / Busca */}
      <div className="bg-abyss-panel border border-abyss-accent/20 p-6 rounded shadow-lg flex flex-col md:flex-row justify-between items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-abyss-accent tracking-widest uppercase flex items-center gap-2">
            📖 Grimório de Feitiçaria (Documentação)
          </h2>
          <p className="text-gray-500 text-xs mt-1">
            Consulte as escrituras místicas, tipos de almas e funções do hardware do compilador Abyssus.
          </p>
        </div>

        {/* Input de Busca */}
        <div className="relative w-full md:w-80">
          <input
            type="text"
            placeholder="Buscar palavra ou função..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-[#0a0a0a] text-gray-200 placeholder-gray-600 border border-gray-800 focus:border-abyss-accent rounded px-4 py-2 text-sm font-mono focus:outline-none transition-all duration-300"
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="absolute right-3 top-2.5 text-gray-500 hover:text-abyss-accent text-xs font-bold"
            >
              LIMPAR
            </button>
          )}
        </div>
      </div>

      {/* Grid Principal */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 min-h-0 overflow-hidden">
        
        {/* Painel Esquerdo: Leis Semânticas / Anti-Heresia */}
        <div className="lg:col-span-1 bg-abyss-panel border border-abyss-accent/10 p-5 rounded overflow-auto flex flex-col gap-5">
          <h3 className="text-sm font-bold text-[#ff9f43] uppercase tracking-wider border-b border-gray-800 pb-2 flex items-center gap-1.5">
            ⚡ Leis Anti-Heresia (Regras Semânticas)
          </h3>

          <div className="space-y-4 text-xs">
            <div className="bg-[#121212] p-3 border-l-2 border-red-500 rounded">
              <h4 className="font-bold text-red-400 uppercase tracking-wide">Heresia Matemática</h4>
              <p className="text-gray-400 mt-1 leading-relaxed">
                Tentar realizar uma divisão ou resto por zero (`0`) estático causará um erro instantâneo e impedirá a transpilação. A ordem matemática do cosmos é protegida.
              </p>
            </div>

            <div className="bg-[#121212] p-3 border-l-2 border-orange-500 rounded">
              <h4 className="font-bold text-orange-400 uppercase tracking-wide">Espírito Errante</h4>
              <p className="text-gray-400 mt-1 leading-relaxed">
                Qualquer variável deve ser declarada (consagrada) antes de ser usada ou receber atribuição. O compilador rastreia rigorosamente os escopos.
              </p>
            </div>

            <div className="bg-[#121212] p-3 border-l-2 border-purple-500 rounded">
              <h4 className="font-bold text-purple-400 uppercase tracking-wide">Decreto Imutável</h4>
              <p className="text-gray-400 mt-1 leading-relaxed">
                Se declarar uma variável usando o modificador <strong className="text-abyss-accent">Imutabile</strong> (equivalente a constante), tentar reatribuir seu valor gera um erro semântico.
              </p>
            </div>

            <div className="bg-[#121212] p-3 border-l-2 border-blue-500 rounded">
              <h4 className="font-bold text-blue-400 uppercase tracking-wide">Declarações Customizadas</h4>
              <p className="text-gray-400 mt-1 leading-relaxed">
                Tipos não mapeados pelo dicionário Abyssus (como `WiFiClient`, `PubSubClient`, `Adafruit_SSD1306`) são aceitos como tipos customizados, bastando usar `Tipo variável;` para consagrá-los.
              </p>
            </div>

            <div className="bg-[#121212] p-3 border-l-2 border-green-500 rounded">
              <h4 className="font-bold text-green-400 uppercase tracking-wide">Constantes Externas</h4>
              <p className="text-gray-400 mt-1 leading-relaxed">
                Para facilitação de código com bibliotecas, qualquer identificador inteiramente em maiúsculo (ex: `WL_CONNECTED`, `INPUT`, `WHITE`) é tratado como macro implícito e não gera erro de falta de declaração.
              </p>
            </div>
          </div>
        </div>

        {/* Painel Direito: Dicionário de Palavras e Categorias */}
        <div className="lg:col-span-2 flex flex-col gap-4 min-h-0 bg-abyss-panel border border-abyss-accent/10 p-5 rounded">
          
          {/* Seletor de Categorias */}
          <div className="flex flex-wrap gap-2 border-b border-gray-800 pb-3">
            {Object.entries(CATEGORIES).map(([key, name]) => (
              <button
                key={key}
                onClick={() => setActiveCategory(key)}
                className={`px-3 py-1 text-xs font-bold uppercase transition-all duration-300 border ${
                  activeCategory === key
                    ? 'bg-abyss-accent/10 border-abyss-accent text-abyss-accent shadow-[0_0_5px_rgba(255,60,0,0.3)]'
                    : 'bg-transparent border-gray-800 text-gray-500 hover:border-gray-700 hover:text-gray-300'
                }`}
              >
                {name}
              </button>
            ))}
          </div>

          {/* Lista de Termos */}
          <div className="flex-1 overflow-auto pr-1 space-y-3">
            {filteredKeywords.length === 0 ? (
              <div className="text-center py-10 text-gray-600 italic text-sm">
                Nenhuma palavra sagrada atende aos filtros de busca...
              </div>
            ) : (
              filteredKeywords.map((kw, index) => (
                <div
                  key={index}
                  className="bg-[#0c0c0c] border border-gray-900/60 p-4 rounded hover:border-abyss-accent/30 transition-all duration-300 flex flex-col md:flex-row justify-between gap-4"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <span className="text-md font-bold text-abyss-green font-mono">{kw.word}</span>
                      <span className="text-xs bg-gray-900 text-gray-500 px-2 py-0.5 rounded font-mono border border-gray-800">
                        {kw.cpp}
                      </span>
                      <span className="text-[10px] uppercase font-bold tracking-wide text-gray-600 bg-gray-950 px-1.5 py-0.5 rounded">
                        {CATEGORIES[kw.category]}
                      </span>
                    </div>
                    <p className="text-xs text-gray-400 mt-2 leading-relaxed">
                      {kw.description}
                    </p>
                  </div>

                  <div className="md:w-72 bg-[#050505] p-2.5 rounded border border-gray-900 flex flex-col justify-center">
                    <span className="text-[10px] font-bold text-abyss-accent tracking-wider uppercase mb-1">
                      Uso Místico:
                    </span>
                    <pre className="text-[11px] text-gray-300 font-mono overflow-x-auto whitespace-pre-wrap">
                      {kw.example}
                    </pre>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
