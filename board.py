from stockfish import Stockfish
import os
class Board:

    # Dictionary para traduzir as peças de chess.com para FEN (Forsyth-Edwards Notation)
    WEB_TO_FEN = {
                    "wp" : "P", "wr" : "R","wn" : "N","wb" : "B","wq" : "Q", "wk" : "K",
                    "bp" : "p","br" : "r", "bn" : "n", "bb" : "b", "bq" : "q", "bk" : "k",
                    }

    # Tamanho do tabuleiro (width e height)
    BOARD_SIZE = 8

    """ 
    Inicializar a classe Board
    Esta classe vai permitir obter as posições do jogo atual do website e converter para notações que FEN(Forsyth-Edwards Notation)
    Com estas notações poderemos comunicar melhor com o stockfish e obter a classificação atual do jogo

    :Args:
        gameSession: sessão atual do browser
    """

    def __init__(self, gameSession, stockFishFolder:str=""):
        self.gameSession = gameSession
        self.reset_board()
        self.stockfish = Stockfish(str(os.path.dirname(os.path.abspath(__file__))) + stockFishFolder + "stockfish.exe")

    
    def get_board_positions(self):
        """
        Obter posições do tabuleiro do website e guardar numa list
        
        :Returns:
            List com as posições das peças no tabuleiro
        """
        self.reset_board()

        for element in self.gameSession.get_elements("piece"):
            pieceClass = self.gameSession.get_element_attribute(element, "class")

            if pieceClass:
                pieceClass.replace("dragging", "")
                pieceData = pieceClass.split()
                pieceType = pieceData[1]
                piecePosition = pieceData[2].replace("square-", "")
                pieceX = int(piecePosition[0])
                pieceY = int(piecePosition[1])
                self.board[pieceX][pieceY] = pieceType

    def get_fen_notation(self):
        """
        Obter o tabuleiro em formato FEN(Forsyth-Edwards Notation)
        
        :Returns:
            String com o FEN Notation

        :TODO:
            Verificar possibilidade de Castle
            Verificar possibilidade de En Passant
            Verificar o valor de Halfmove Clock
            O mesmo para Fullmove

        """
        fen = ""
        emptyCounter = 0

        for y in range(1, self.BOARD_SIZE + 1):
            for x in range(self.BOARD_SIZE, 0, -1):

                if not self.board[x][y]:
                    emptyCounter += 1
                else:
                    if emptyCounter > 0:
                        fen += str(emptyCounter)
                        emptyCounter = 0
                    fen += self.WEB_TO_FEN[self.board[x][y]]

                if x == 1:
                    if emptyCounter > 0:
                        fen += str(emptyCounter)
                        emptyCounter = 0
                    
                    if y < self.BOARD_SIZE:
                        fen += "/"

        fen += " " + self.get_player_turn()
        fen += " - - "
        fen += "0 "
        fen += str(self.get_total_full_moves())

        return fen

    def get_stockfish_evaluation(self):
        """
        Obter a avaliação da posição atual stockfish
        """
        self.get_board_positions()
        fen = self.get_fen_notation()
        self.stockfish.set_fen_position(fen)
        return self.stockfish.get_evaluation()

    def get_white_total_moves(self):
        """
        Obter número de jogadas efetuadas pelo jogador de peças brancas

        :Returns:
            Total de jogadas
        """
        movesElements = self.gameSession.get_elements("node")
        whiteElements = []
        
        if not movesElements:
            return 0

        for element in movesElements:
            attribute = self.gameSession.get_element_attribute(element, "class")
            if attribute:
                if "white" in attribute:
                    whiteElements.append(element)

        return len(whiteElements)

    def get_black_total_moves(self):
        """
        Obter número de jogadas efetuadas pelo jogador de peças pretas

        :Returns:
            Total de jogadas
        """
        movesElements = self.gameSession.get_elements("node")
        blackElements = []
        
        if not movesElements:
            return 0

        for element in movesElements:
            attribute = self.gameSession.get_element_attribute(element, "class")
            if "black" in attribute:
                blackElements.append(element)

        return len(blackElements)

    """
    Obter o total de jogadas completas
    Jogada completas = brancas e pretas já jogaram

    :Returns:
        Total de jogas completas
    """
    def get_total_full_moves(self):
        whiteMoves = self.get_white_total_moves()
        blackMoves = self.get_black_total_moves()

        if whiteMoves == blackMoves:
            return whiteMoves
        else:
            return blackMoves


    def get_player_turn(self):
        """
        Com esta função vamos saber se é a vez das peças brancas de jogar ou das pretas

        :Returns:
            String lowerCase w = white e b = black
        """
        whiteMoves = self.get_white_total_moves()
        blackMoves = self.get_black_total_moves()

        if whiteMoves == blackMoves:
            return "w"
        else:
            return "b"


    def reset_board(self):
        """
        Retirar todas as peças do tabuleiro
        """
        self.board = [[""] * (self.BOARD_SIZE + 1) for i in range(self.BOARD_SIZE + 1)]