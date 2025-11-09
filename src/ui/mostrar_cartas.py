import random
import pygame
from pathlib import Path

# Configurações
CARD_SCALE = 0.5  # Escala da carta

# Diretórios
BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_CARDS_DIR = BASE_DIR / 'assets' / 'cards_sorte'

# Cache das imagens
CARDS_SORTE = []
CARDS_AZAR = []

if ASSETS_CARDS_DIR.exists():
    for f in ASSETS_CARDS_DIR.iterdir():
        if f.suffix.lower() != '.png':
            continue
        name_upper = f.name.upper()
        if 'SORTE' in name_upper:
            CARDS_SORTE.append(str(f))
        elif 'AZAR' in name_upper:
            CARDS_AZAR.append(str(f))


def mostrar_carta(carta, screen, clock, jogador=None, jogadores=None):
    """
    Exibe UMA única carta SOBREPOSTA na tela de jogo e executa sua ação.
    
    Args:
        carta: Objeto Carta do módulo Cartas.py
        screen: Surface do pygame onde a carta será desenhada
        clock: Clock do pygame para controlar FPS
        jogador: Jogador que puxou a carta (opcional)
        jogadores: Lista de jogadores (opcional)
    
    Returns:
        bool: True se a ação foi executada, False se cancelado
    """
    # Seleciona UMA imagem baseada no tipo da carta
    if carta.tipo == 'Sorte':
        imagens_disponiveis = CARDS_SORTE
    else:
        imagens_disponiveis = CARDS_AZAR if CARDS_AZAR else CARDS_SORTE
    
    # Carrega a imagem da carta
    if not imagens_disponiveis:
        print(f"[ERRO] Nenhuma imagem encontrada para cartas do tipo {carta.tipo}")
        return False
    
    # Seleciona UMA imagem aleatória
    imagem_path = random.choice(imagens_disponiveis)
    
    try:
        carta_img = pygame.image.load(imagem_path).convert_alpha()
        # Redimensiona a carta
        orig_w, orig_h = carta_img.get_size()
        new_w = int(orig_w * CARD_SCALE)
        new_h = int(orig_h * CARD_SCALE)
        if new_w <= 0: new_w = 1
        if new_h <= 0: new_h = 1
        carta_img = pygame.transform.smoothscale(carta_img, (new_w, new_h))
        
        # Centraliza na tela
        screen_w, screen_h = screen.get_size()
        carta_x = (screen_w - new_w) // 2
        carta_y = (screen_h - new_h) // 2
        
    except Exception as e:
        print(f"[ERRO] Falha ao carregar imagem: {e}")
        return False
    
    # Configura fonte para texto

    fonte_instrucao = pygame.font.SysFont("arial", 16, bold=True)
    fundo_salvo = screen.copy()

    # Loop de exibição
    mostrando = True
    acao_executada = False
    
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                    mostrando = False
                    acao_executada = True
        
        # A tela já foi desenhada pelo loop principal do game
        # Apenas desenha a carta por cima
        screen.blit(fundo_salvo, (0, 0))
        screen.blit(carta_img, (carta_x, carta_y))
        
        # Instruções com fundo pequeno apenas para legibilidade
        instrucao = "Pressione espaço ou enter para continuar"
        texto_instrucao = fonte_instrucao.render(instrucao, True, (255, 255, 255))
        texto_rect = texto_instrucao.get_rect(center=(screen_w // 2, screen_h - 50))
        
        # Fundo preto pequeno apenas atrás do texto
        fundo_texto = pygame.Surface((texto_rect.width + 20, texto_rect.height + 10))
        fundo_texto.fill((70, 70, 70))
        fundo_texto.set_alpha(200)
        screen.blit(fundo_texto, (texto_rect.x - 10, texto_rect.y - 5))
        screen.blit(texto_instrucao, texto_rect)
        
        texto_u = str(carta.nome)[6::]
        fonte= pygame.font.get_default_font()              ##### carrega com a fonte padrão
        fontesys=pygame.font.SysFont("helvetica", 12, bold=True)           ##### usa a fonte padrão
        txttela = fontesys.render(texto_u, 1, (255,255,255))  ##### renderiza o texto na cor desejada
        screen.blit(txttela,((screen_w//2 - 100), screen_h - 270))

        pygame.display.flip()
        clock.tick(60)
    
    # Executa a ação da carta
    if acao_executada and jogador:
        carta.acao.executar(jogador, jogadores)
    
    return acao_executada


# Exemplo de uso standalone (para testes)
if __name__ == "__main__":
    from src.engine.Cartas import gerar_baralho
    from src.engine.Jogador import Jogador
    
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Teste Carta")
    clock = pygame.time.Clock()
    
    # Simula um fundo de jogo
    background = pygame.Surface((1280, 720))
    background.fill((50, 100, 50))
    
    jogadores_teste = [
        Jogador("Fernando", "Jogador 1"),
        Jogador("Luiza", "Jogador 2")
    ]
    
    baralho = gerar_baralho(10)
    carta_sorteada = baralho.tirar_carta()
    jogador_atual = jogadores_teste[0]
    
    print(f"Carta sorteada: {carta_sorteada.nome}")
    print(f"Tipo: {carta_sorteada.tipo}")
    
    # Loop principal de teste
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Desenha o fundo primeiro
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                    
                    # Mostra a carta sobreposta
                    mostrar_carta(carta_sorteada, screen, clock, jogador_atual, jogadores_teste)
        
        screen.blit(background, (0, 0))
        
        # Texto de instrução
        font = pygame.font.Font(None, 36)
        texto = font.render("Pressione ESPAÇO para ver a carta", True, (255, 255, 255))
        screen.blit(texto, (400, 350))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()