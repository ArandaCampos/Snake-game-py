import pygame
from pygame.locals import *
from random import randrange, randint

pygame.init()  # inicializa o PyGame
pygame.mixer.init()

# Parâmetro de jogo
game_over = False

# dimensões da tela
y_screen = 500
x_screen = 500
tela = pygame.display.set_mode((x_screen, y_screen))

# Configurações da música e imagem de fundo
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load('BoxCat_Games_CPU_Talk.mp3')
pygame.mixer.music.play(-1)

# Config da música de colisão
musica_pontos = pygame.mixer.Sound('smw_coin.wav')
musica_game_over = pygame.mixer.Sound('smw_door_opens.wav')

# Config cobrinhas
altura = 20
largura = 20
snake_x = int((x_screen / 2 - altura / 2) // 20 * 20)
snake_y = int((x_screen / 2 - largura / 2) // 20 * 20)
snake_length = 5
speed = 7
control_snake_x = speed
control_snake_y = 0

# Config  da posição da apple
apple_x = randrange(0, (x_screen - largura), largura)
apple_y = randrange(0, (y_screen - altura), altura)
apple_image = pygame.image.load('sprits/apple.png').convert_alpha()

# Config do Placar
font = pygame.font.SysFont('Arial', 20, True, False)
score = 0

# Titulo do Jogo
pygame.display.set_caption('Snake game')

# Objeto da rapidez do jogo
relogio = pygame.time.Clock()

# Lista que armazena as coordenadas do corpo
body_snake = []

# Função que aumenta o corpo da cobra
def increase_body(body_snake):
    for XeY in body_snake:
        pygame.draw.rect(tela, (20, 170, 20), (XeY[0], XeY[1], 20, 20))

# Função que reinicia o jogo
def restart():
    global score, snake_length, snake_x, snake_y, apple_x, apple_y, body_snake, head_snake, game_over, control_snake_x, control_snake_y
    score = 0
    snake_length = 5
    snake_x = int((x_screen / 2 - altura / 2) // 20 * 20)
    snake_y = int((x_screen / 2 - largura / 2) // 20 * 20)
    apple_x = (randint(0, 480) // 20 * 20)
    apple_y = (randint(0, 480) // 20 * 20)
    control_snake_x = 20
    control_snake_y = 0
    body_snake = []
    head_snake = []
    game_over = False

# loop infinito para executar o jogo
while True:

    # rapidez do jogo (frames por seg)
    relogio.tick(speed)

    # Atualização e cor da tela
    tela.fill((180, 180, 180))

    # Pontuação
    mensagem = f'PONTOS: {score}'
    text = font.render(mensagem, True, (0, 0, 0))

    # Loopping finalizar o jogo
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    # Condicionais para comandos do botão
    if event.type == KEYDOWN:
        if event.key == K_UP and control_snake_y == 0:
            control_snake_x = 0
            control_snake_y = -largura
        if event.key == K_DOWN and control_snake_y == 0:
            control_snake_x = 0
            control_snake_y = largura
        if event.key == K_LEFT and control_snake_x == 0:
            control_snake_x = -altura
            control_snake_y = 0
        if event.key == K_RIGHT and control_snake_x == 0:
            control_snake_x = altura
            control_snake_y = 0

    # Insere a cobra e a maçã no jogo
    apple_coordenada = pygame.draw.rect(tela, (180, 180, 180), (apple_x, apple_y, largura, altura))
    tela.blit(apple_image, (apple_x, apple_y))
    snake = pygame.draw.rect(tela, (15, 150, 15), (snake_x, snake_y, largura, altura))

    # controla o movimento da cobra e garante que ela não pare
    snake_x += control_snake_x
    snake_y += control_snake_y

    # Condicionais para verificar se a cobra não tocou as bordas
    if snake_x >= x_screen:
        game_over = True
        musica_game_over.play()
    elif snake_x < 0:
        game_over = True
        musica_game_over.play()
    if snake_y >= y_screen:
        game_over = True
        musica_game_over.play()
    elif snake_y < 0:
        game_over = True
        musica_game_over.play()

    # Insere a pontuação na tela
    tela.blit(text, (350, 20))

    # Condicional de colisão, recria a maçã e ativa a música de pontuação
    if snake.colliderect(apple_coordenada):
        score += 1
        musica_pontos.play()
        snake_length += 1
        apple_x = randrange(0, (x_screen - largura), largura)
        apple_y = randrange(0, (y_screen - altura), altura)

    # Lista que armazena as coordenadas atual da cabeça da cobra
    head_snake = []
    head_snake.append(snake_x)
    head_snake.append(snake_y)

    # Recebe as coordenadas da cabeça para identificar onde o corpo está
    body_snake.append(head_snake)

    # Condicional que verifica se a cobra se tocou
    if body_snake.count(head_snake) > 1:
        #musica_game_over.play()
        game_over = True

    while game_over:
        # Config da tela de Game Over
        tela.fill((18, 18, 18))

        # titulo
        font_2 = pygame.font.SysFont('Arial', 42, True, False)
        mensagem_over = f'Game Over!'
        text_over = font_2.render(mensagem_over, True, (250, 250, 250))
        text_over_format = text_over.get_rect()
        text_over_format.center = (x_screen // 2, y_screen // 2 - 18)
        tela.blit(text_over, text_over_format)

        # Subtitulo
        font_3 = pygame.font.SysFont('Arial', 20, True, True)
        mensagem_restart = f'Pressione R para jogar novamente'
        text_restart = font_3.render(mensagem_restart, True, (250, 250, 250))
        text_restart_format = text_restart.get_rect()
        text_restart_format.center = (x_screen // 2, y_screen // 2 + 18)
        tela.blit(text_restart, text_restart_format)

        # condicional para finalizar o jogo
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    restart()
        pygame.display.flip()

    if len(body_snake) > snake_length:
        del body_snake[0]

    # Chama a função que incrementa o corpo da cobra
    increase_body(body_snake)

    # Atualiza a tela
    pygame.display.flip()
