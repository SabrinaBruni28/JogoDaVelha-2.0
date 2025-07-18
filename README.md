# 🎮 Jogo da Velha (Tic-Tac-Toe) em PyQt6

Este é um jogo da velha com interface gráfica moderna construída em **Python** utilizando **PyQt6**. Dois jogadores se alternam marcando `X` ou `O` em um tabuleiro 3x3 até que um deles vença ou a partida termine em empate.

---

## 🚀 Funcionalidades

- Interface gráfica elegante com botões personalizados.
- Escolha de jogador inicial (`X` ou `O`).
- Embaçamento de fundo com mensagem visual de vencedor.
- Botão para reiniciar o jogo a qualquer momento.
- Detecção de vitória por linha, coluna ou diagonal.
- Detecção de empate.

---

## 📁 Estrutura do Projeto

```
.
├── Jogo/
│   ├── interface.py         # Interface principal do jogo
│   ├── jogo_da_velha.py     # Lógica do jogo
│   └── view_utils.py        # Componentes reutilizáveis (botões, imagens etc.)
├── Images/                  # Imagens dos símbolos (X e O)
├── requirements.txt         # Dependências do projeto
└── Makefile                 # Automação de comandos
```
---

## 🛠️ Como rodar o projeto

Siga os passos abaixo para configurar e executar o jogo:


### Utilize o Makefile

Use os comandos abaixo para gerenciar o ambiente virtual e executar o projeto:

#### 🧱 Criar ambiente virtual

```bash
make criar_ambiente
```

#### 📦 Instalar as dependências

```bash
make instalar_bibliotecas
```

#### ▶️ Rodar o jogo

```bash
make run
```

#### ▶️ Gerar um executável Linux

```bash
make executavel_linux
```
#### ▶️ Gerar um executável Windows

```bash
make executavel_windows
```
---

## 🧑‍💻 Autor

Desenvolvido por [Sabrina Bruni](https://github.com/SabrinaBruni28)
