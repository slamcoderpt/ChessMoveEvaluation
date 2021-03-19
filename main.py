from game import Game

CHESS_WEBSITE = "https://www.chess.com/"
DRIVER_FOLDER = "\\drivers\\"

# Iniciar o browser e abrir o website para o jogador jogar.
gameSession =  Game(DRIVER_FOLDER, CHESS_WEBSITE)

# Enquanto tiver a janela aberta vamos processar a lógica e gráficos do jogo
while gameSession.is_connected() :
    gameSession.gaming()

gameSession.end_game()


