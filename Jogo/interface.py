import sys
from view_utils import  WidgetHelper, CaixaConfirmacao, ViewHelper
from jogo_da_velha import JogoDaVelha
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
   QApplication, QMainWindow, QWidget, QLabel, QDialog,
   QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget, QSizePolicy, QPushButton
)

class MensagemVencedor(QWidget):
    def __init__(self, parent=None, mensagem="", on_reiniciar=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(parent.rect())

        self.setStyleSheet("background-color: rgba(0, 0, 0, 180);")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setStyleSheet("background-color: white; border-radius: 20px;")
        
        container.setMinimumSize(500, 160)  # menor altura mínima
        container.setMaximumHeight(300)     # limite máximo

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(mensagem)
        self.label.setStyleSheet("color: red;")
        font = QFont()
        font.setPointSize(32)  # menor fonte
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.label.setMaximumWidth(520)
        self.label.setMaximumHeight(150)

        self.botao_reiniciar = QPushButton("Reiniciar")
        self.botao_reiniciar.setFixedSize(250, 60)  # menor botão
        self.botao_reiniciar.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 28px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.botao_reiniciar.clicked.connect(lambda: on_reiniciar() if on_reiniciar else None)

        container_layout.addWidget(self.label)
        container_layout.addWidget(self.botao_reiniciar)

        layout.addWidget(container)

class JogoDaVelhaInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jogo da Velha")
        self.setGeometry(100, 100, 1000, 600)
        self.showMaximized()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.view = ViewHelper()
        self.jogo = JogoDaVelha()
        self.jogo.init_player(self.jogo.player_1)
        self.view.abrir_tela(self.stack, self.tela_inicial)

    def closeEvent(self, event):
        dialogo = CaixaConfirmacao(self, titulo="Confirmar saída", mensagem="Você tem certeza que deseja sair?")
        resposta = dialogo.exec()

        if resposta == QDialog.DialogCode.Accepted:
            event.accept()
        else:
            event.ignore()
    
    def toggle_menu(self):
        if self.barra_lateral.isVisible():
            self.barra_lateral.hide()
        else:
            self.barra_lateral.show()

    #############  BLOCOS  #################
    def bloco(self, num, largura, altura):
        bloco = WidgetHelper.bloco(largura, altura)

        layout = QVBoxLayout(bloco)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        bloco.mousePressEvent = lambda e: self.adicionarJogada(num, layout)
        return bloco
    
    def adicionarJogada(self, num: int, layout: QVBoxLayout):
        bolinha_label = WidgetHelper.imagem(WidgetHelper.caminho_absoluto("Images/bolinha.png"), scaled=150)
        x_label = WidgetHelper.imagem(WidgetHelper.caminho_absoluto("Images/x.jpg"), scaled=150)
        x = num // 3
        y = num % 3

        if not self.jogo.posicao_marcada(x, y):
            imagem = bolinha_label if self.jogo.current_player() == 2 else x_label
            self.jogo.marcar_matriz(x, y)
            layout.addWidget(imagem, alignment=Qt.AlignmentFlag.AlignHCenter)
            vencedor = self.jogo.confere_vencedor()
            if vencedor != 0:
                self.mostrar_vencedor(vencedor)

            self.jogo.change_player()
            self.atualizar_label_jogador()
    
    def atualizar_label_jogador(self):
        if self.label_jogador:
            jogador = self.jogo.current_player()
            texto = f"Jogador: {'X' if jogador == 1 else 'O'}"
            self.label_jogador.setText(texto)

    def mostrar_vencedor(self, vencedor):
        if vencedor == 1:
            texto = "Jogador X venceu!"
        elif vencedor == 2:
            texto = "Jogador O venceu!"
        elif vencedor == -1:
            texto = "Empate!"
        else:
            return

        self.mensagem_vencedor = MensagemVencedor(self, texto, on_reiniciar=self._reiniciar_jogo)
        self.mensagem_vencedor.show()

    def _reiniciar_jogo(self):
        self.jogo.reiniciar_jogo()

        # Limpar as imagens dos blocos (supondo que você tenha referência para eles)
        for i in range(self.grid.count()):
            bloco = self.grid.itemAt(i).widget()
            layout = bloco.layout()
            if layout is not None:
                # Remove todos os widgets (bolinha, X) do layout
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

        if hasattr(self, 'mensagem_vencedor'):
            self.mensagem_vencedor.hide()
            self.mensagem_vencedor.deleteLater()
            del self.mensagem_vencedor

        self.view.abrir_tela(self.stack, self.tela_opcao)

    ###################  TELAS  ########################
    def tela_lista_blocos(self, largura=190, altura=190):
        scroll, self.grid = WidgetHelper.lista_grid()

        for i in range(9):
            bloco = self.bloco(i, largura, altura)
            self.grid.addWidget(bloco, i // 3, i % 3)
        return scroll

    def tela_jogo(self):
        tela = QWidget()

        # Layout horizontal principal (menu + conteúdo)
        layout_h = QHBoxLayout(tela)

        # Adiciona a barra lateral ao layout principal (inicialmente oculta)
        self.barra_lateral = self.menu_lateral()
        layout_h.addWidget(self.barra_lateral)
        
        # Layout vertical para o conteúdo da tela
        layout_conteudo = QVBoxLayout()

        barra_superior = self.barra_superior()
        layout_conteudo.addLayout(barra_superior)

        tela_lista = self.tela_lista_blocos()
        layout_conteudo.addWidget(tela_lista)

        # Agora adiciona o conteúdo principal no layout horizontal
        layout_h.addLayout(layout_conteudo)

        return tela
    
    ##############  TELAS DE CRIAÇÃO  #################

    def tela_inicial(self):
        tela = QWidget()
        layout_vertical = QVBoxLayout(tela)

        titulo = WidgetHelper.label_b("JOGO DA VELHA", font_size=80)
        layout_vertical.addWidget(titulo)

        botao_jogar = WidgetHelper.botao(
            nome="JOGAR",
            largura=400, altura= 100,
            fonte= 80,
            backcolor="#D12A2A",
            hover='#FF4C4C',
            pressed='#E04343',
            border='solid #FF4C4C',
            acao= lambda: self.view.abrir_tela(self.stack, self.tela_opcao)
        )
        layout_vertical.addWidget(botao_jogar, alignment=Qt.AlignmentFlag.AlignCenter)

        return tela
    
    def tela_opcao(self):
        tela = QWidget()
        layout_vertical = QVBoxLayout(tela)

        titulo = WidgetHelper.label_b("Começar com qual?", font_size=50)
        layout_vertical.addWidget(titulo)

        layout_horizontal = QHBoxLayout()

        botao_X = WidgetHelper.botao(
            nome="X",
            largura=400, altura= 100,
            fonte= 80,
            backcolor="#D12A2A",
            hover='#FF4C4C',
            pressed='#E04343',
            border='solid #FF4C4C',
            acao= lambda: (self.jogo.init_player(1), self.view.abrir_tela(self.stack, self.tela_jogo))
        )
        layout_horizontal.addWidget(botao_X)

        botao_O = WidgetHelper.botao(
            nome="O",
            largura=400, altura= 100,
            fonte= 80,
            backcolor="#D12A2A",
            hover='#FF4C4C',
            pressed='#E04343',
            border='solid #FF4C4C', 
            acao= lambda: (self.jogo.init_player(2), self.view.abrir_tela(self.stack, self.tela_jogo))
        )
        layout_horizontal.addWidget(botao_O)
        layout_vertical.addLayout(layout_horizontal, Qt.AlignmentFlag.AlignCenter)
        layout_vertical.addSpacing(100)

        return tela
    
    def reiniciar_jogo(self):
        dialogo = CaixaConfirmacao(self, titulo="Confirmar saída", mensagem="Você tem certeza que deseja reiniciar o jogo?")
        resposta = dialogo.exec()

        if resposta == QDialog.DialogCode.Accepted:
            self.jogo.reiniciar_jogo()
            self._reiniciar_jogo()

    ##########  PARTES DE TELAS  #############
    def menu_lateral(self):
        # Crie o menu lateral e esconda no início
        menu_lateral = QFrame()
        menu_lateral.setFrameShape(QFrame.Shape.StyledPanel)
        menu_lateral.setFixedWidth(250)
        menu_lateral.hide()

        # Layout para a barra lateral
        menu_layout = QVBoxLayout(menu_lateral)
        menu_layout.setSpacing(0)  # Definir o espaçamento entre os botões como 0
        menu_layout.setContentsMargins(0, 0, 0, 0)  # Remove as margens

        botao_reiniciar = WidgetHelper.botao(
            nome="Reiniciar Jogo", fontcolor="gray",
            backcolor="", hover="#3a3a3a", border="", pressed='#000000',
            largura=250, altura=100,
            acao= self.reiniciar_jogo
        )

        # Adicionando os botões ao layout da barra lateral
        menu_layout.addWidget(botao_reiniciar, alignment=Qt.AlignmentFlag.AlignHCenter)
        menu_layout.addStretch()  # Adiciona um espaçador para empurrar os botões para cima

        return menu_lateral
    
    def barra_superior(self):
        # Barra superior com botões
        barra_superior = QHBoxLayout()

        botao_menu = WidgetHelper.botao(
            nome="≡", fonte=40,
            largura=50, altura=50,
            backcolor="", hover="#3a3a3a", border="",
            pressed='#000000', fontcolor="gray",
            acao= self.toggle_menu
        )

        self.label_jogador  = WidgetHelper.label_b(f"Jogador: {'X' if self.jogo.current_player() == 1 else 'O'}")

        barra_superior.addWidget(botao_menu)
        barra_superior.addWidget(self.label_jogador)

        return barra_superior

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JogoDaVelhaInterface()
    window.show()
    sys.exit(app.exec())
