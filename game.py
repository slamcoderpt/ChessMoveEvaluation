from web import WebAuto
from board import Board
import time
class Game:

    """ 
    Inicializar website para o jogador jogar.
    Após abertura esperar que o jogador inicie um jogo e a partir de aí irá aparecer um barra com a avaliação da jogada de ambos os jogadores

    :Args:
        - website: url do website

    """
    def __init__(self, driverFolder:str, website:str = ""):
        self.websession = WebAuto(driverFolder, website)
        self.board = Board(self.websession, driverFolder)

    
    def is_playing(self):
        """
        Verificar se algum jogo está a decorrer
        
        :Returns:
            True se estiver um jogo a decorrer e False caso contrário
        """
        return self.websession.does_element_exist(element_class="opening-component") and not self.is_game_over()

    def is_game_over(self):
        """
        Verificar se o jogo já acabou

        :Returns:
            True se o jogo tiver acabado ou false caso ainda esteja a jogar
            Apenas conta se o jogo estiver acabado mas ainda tiver na mesma página do tabuleiro
        """
        return self.websession.does_element_exist(element_class="rcn-game-buttons-game-over")

    def is_connected(self):
        """
        Verifica se o jogador ainda se encontra com o browser aberto
        Aqui uso a função do obter o titulo da janela do browser porque a mesma retorna vazio caso não exista janela aberta

        :Returns:
            True se a janela do browser se encontrar aberta, caso contrário False
        """
        return self.websession.get_window_title()

    
    def gaming(self):
        """
        Função central onde vai ocorrer todos os processos de lógica e de renderização
        """
        self.update()
        self.render()
   
    def update(self):
        """
        Todo o processo de lógica vai passar por aqui
        """
        if self.is_playing() :
            print(self.board.get_stockfish_evaluation())
            time.sleep(1)
        elif self.is_game_over() :
            self.board.reset_board()
            print("O JOGO TERMINOU!!!")
        else:
            print("JOGO AINDA NÃO COMEÇOU")

    def render(self):
        """
        Todo o processo de renderização vai passar por aqui
        """
        print("GRAFICOS!!!")

    def end_game(self):
        """
        Terminar o jogo
        """
        print("A fechar o jogo...")
        self.websession.close()


