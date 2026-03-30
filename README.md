# Abyssus Compiler

## 🎯 Intuito do Projeto

O **Abyssus** é uma linguagem de programação esotérica e educacional, criada para abstrair e gamificar o desenvolvimento de sistemas embarcados. O projeto funciona como um compilador completo que traduz lógicas escritas em um "latim místico" (rituais) diretamente para código **C++ de microcontroladores (Arduino)**.

A arquitetura é dividida em dois serviços principais:

1. **Backend (Python/Flask + SLY):** Atua como o motor do compilador, realizando a Análise Léxica, Análise Sintática (geração da AST) e a Transpilação.
2. **Frontend (React + Vite + TailwindCSS):** Atua como a IDE Web interativa, comunicando-se com o motor para exibir os resultados da compilação em tempo real.

---

## ⚙️ Como Rodar o Backend Corretamente

**Pré-requisito:** Python 3.10 ou superior instalado.

O backend é o coração do compilador. Para iniciá-lo, abra um terminal na raiz do projeto e siga os passos:

1. Navegue até a pasta do backend:
   ```bash
   cd backend
   ```

2. Crie e ative um ambiente virtual (recomendado para isolar as dependências):

   **No Windows:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **No Linux/Mac:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

4. Inicie o servidor da API:
   ```bash
   python run.py
   ```

   **Sucesso:** O terminal exibirá que o servidor está rodando em [http://localhost:5000](http://localhost:5000). Deixe este terminal aberto.

---

## 💻 Como Rodar o Frontend Corretamente

**Pré-requisito:** Node.js versão 20 ou superior. 

> **Nota:** O projeto utiliza Vite v5 para máxima compatibilidade com a versão LTS do Node.

Com o backend já rodando, abra um novo terminal na raiz do projeto e siga os passos:

1. Navegue até a pasta do frontend:
   ```bash
   cd frontend
   ```

2. Instale as dependências do projeto:
   ```bash
   npm install
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

   **Sucesso:** O terminal exibirá o endereço onde o frontend está rodando, geralmente [http://localhost:3000](http://localhost:3000). Abra este endereço no navegador.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python, Flask, SLY
- **Frontend:** React, Vite, TailwindCSS
- **Linguagem de Transpilação:** C++ (Arduino)

---

## 📂 Estrutura do Projeto

```plaintext
Linguagens-Formais/
├── backend/
│   ├── abyssus/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── lexer.py
│   │   ├── parser.py
│   │   └── transpiler.py
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
```

---