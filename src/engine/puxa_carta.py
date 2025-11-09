'''
OK aparentemente a casa de imóveis não cabe aqui pq falta cmapo, 
então vou deixar comentado o código de verificação de tipo
'''

import os
import json
import pygame
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))


ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
ARTS_DIR = os.path.join(ASSETS_DIR, "property info")
TABULEIRO_DIR = os.path.join(BASE_DIR, "Tabuleiro")

CARTA_IMG_PATH = os.path.join(ARTS_DIR, "card-info-propriedade-default-rosa.png")
COMPANHIAS_JSON = os.path.join(TABULEIRO_DIR, "CasasAleatoriasCompanhias.json")
ESTACOES_JSON = os.path.join(TABULEIRO_DIR, "CasasAleatoriasEstacoes.json")
IMOVEIS_JSON = os.path.join(TABULEIRO_DIR, "CasasAleatoriasImoveis.json")



# dimensões da tela
width = 1280
height = 720
CARTA_OFFSET = -20

# aparência do texto na carta
TEXT_POS = {
    "dono": (28, 70),       
    "valor": (28, 110),
    "aluguel": (28, 150),
    "hipoteca": (28, 190)
}

FONTES_POSSIVEIS = [
    os.path.join(ARTS_DIR, "fonts", "Georgia.ttf"),
    os.path.join(ARTS_DIR, "fonts", "Cambria.ttf"),
    "C:\\Windows\\Fonts\\arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

FONTE_TITULO = 20
FONTE_TEXTO = 16
cor_branco = (255, 255, 255)


#procurando essa fonte Montserrat pra harmonizar com o tetxo do asset 
def achar_fonte():
    for f in FONTES_POSSIVEIS:
        if os.path.exists(f):
            return f
    return None

def carrega_json(path):
    if not os.path.exists(path):
        print(f"[ERRO] Arquivo não encontrado: {path}")
        return []
    with open(path, "r", encoding="utf-8") as arq:
        try:
            return json.load(arq)
        except Exception as e:
            print(f"[ERRO] Falha ao ler JSON {path}: {e}")
            return []

def constroi_baralho_casas():
    """
    Constrói e retorna um dicionário baralho onde cada chave é um inteiro
    e o valor é um dict representando a carta.
    """
    baralho = {}
    idx = 0

    for item in carrega_json(COMPANHIAS_JSON):
        carta = dict(item)
        carta["tipo"] = "companhia"
        baralho[idx] = carta
        idx += 1

    for item in carrega_json(ESTACOES_JSON):
        carta = dict(item)
        carta["tipo"] = "estacao"
        baralho[idx] = carta
        idx += 1

    for item in carrega_json(IMOVEIS_JSON):
        carta = dict(item)
        carta["tipo"] = "imovel"
        baralho[idx] = carta
        idx += 1

    return baralho

def encaixa_texto(texto, fonte, larg_maxima):
    palavras = texto.split()
    if not palavras:
        return []
    linhas = []
    atual = palavras[0]
    for p in palavras[1:]:
        teste = atual + " " + p
        larg, _ = fonte.size(teste)
        if larg <= larg_maxima:
            atual = teste
        else:
            linhas.append(atual)
            atual = p
    linhas.append(atual)
    return linhas

def renderiza_linhas(screen, texto_linhas, fonte, cor, x, y, larg_maxima, spacing):
    y_cursor = y
    for linha in texto_linhas:
        sublinhas = encaixa_texto(linha, fonte, larg_maxima)
        for sl in sublinhas:
            surf = fonte.render(sl, True, cor)
            screen.blit(surf, (x, y_cursor))
            y_cursor += fonte.get_linesize() + spacing
    return y_cursor

def escolhe_carta_aleatoria(baralho):
    """Retorna (chave, carta) escolhida aleatoriamente a partir do dicionário."""
    if not baralho:
        return None, None
    chave = random.choice(list(baralho.keys()))
    return chave, baralho[chave]

def mostra_uma_carta(baralho):
    pygame.init()
    pygame.display.set_caption("TESTE CARTAS")
    
    tela = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    
    #inserindo carta CENTRALIZADA no fundo "preto"
    if not os.path.exists(CARTA_IMG_PATH):
        print(f"[ERRO] Imagem de carta não encontrada: {CARTA_IMG_PATH}")
        return

    carta_asset = pygame.image.load(CARTA_IMG_PATH).convert_alpha()
    carta_alt, carta_larg = carta_asset.get_size()
    carta_x = (width - carta_larg)//2
    carta_y = (height- carta_alt)//2 + CARTA_OFFSET

    #área das fontes
    fonte = achar_fonte()
    if fonte:
        fonte_titulo = pygame.font.Font(fonte, FONTE_TITULO)
        fonte_texto = pygame.font.Font(fonte, FONTE_TEXTO)
        rod_font = pygame.font.Font(fonte, 12)
        
    else:
        fonte_titulo = pygame.font.Font(None, FONTE_TITULO, bold=True)
        fonte_texto = pygame.font.SysFont(None, FONTE_TEXTO)
        rod_font = pygame.font.SysFont(None, 12)

    # escolhe a primeira carta aleatória
    chave_atual, carta_atual = escolhe_carta_aleatoria(baralho)

    running = True
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    running = False
                elif evento.key == pygame.K_SPACE:
                    # troca para outra carta aleatória
                    chave_atual, carta_atual = escolhe_carta_aleatoria(baralho)

        fundo = pygame.Surface((width, height))
        fundo.fill((30,30,30))
        tela.blit(fundo, (0, 0))
        tela.blit(carta_asset, (carta_x, carta_y))

        if carta_atual is None:
            aviso = fonte_titulo.render("Nenhuma carta carregada", True, (0,0,20))
            tela.blit(aviso, (carta_x +10, carta_y+10))
        else:
            def abs_pos(relativo):
                return (carta_x + relativo[0], carta_y + relativo[1])
            
            #VALOR
            vx, vy = abs_pos(TEXT_POS["valor"])
            label_v = rod_font.render(" ", True, cor_branco)
            tela.blit(label_v, (vx, vy))
            preco =f"{carta_atual.get('preco', '')}"  
            tela.blit(fonte_texto.render(preco, True, cor_branco), (vx + 110, vy -2))
            
            #ALUGUEL
            ax, ay = abs_pos(TEXT_POS["aluguel"])
            label_a = rod_font.render(' ', True, cor_branco)
            tela.blit(label_a, (ax, ay))
            aluguel = carta_atual.get("aluguel")
            if isinstance(aluguel, list) and aluguel:
                primeiro = aluguel[0]
                tela.blit(fonte_texto.render(f"{primeiro} (base)", True, cor_branco), (ax + 110, ay - 22))
            else:
                tela.blit(fonte_texto.render(str(aluguel or '---'), True, cor_branco), (ax+110, ay-22))

            #Hipoteca
            hx, hy = abs_pos(TEXT_POS["hipoteca"])
            label_h = rod_font.render('', True, cor_branco)
            tela.blit(label_h, (hx, hy))
            hipoteca = f"{carta_atual.get('hipoteca', '')}"
            tela.blit(fonte_texto.render(hipoteca, True, cor_branco), (hx+110, hy -35))


            titulo = pygame.Rect(carta_x + 10, (carta_y+20), carta_larg, 40)

            nome = str(carta_atual.get('nome', ''))
            nome_tela = fonte_titulo.render(nome, True, (255,255,255))
            nt_rect = nome_tela.get_rect(center=titulo.center)

            tela.blit(nome_tela, nt_rect)
            '''
            # se por acaso carta_atual não for dict, converte para string
            if not isinstance(carta_atual, dict):
                titulo_surf = fonte_titulo.render(str(carta_atual), True, (0,0,0))
                tela.blit(titulo_surf, (TEXTO_X, 36))
            else:
                tipo = carta_atual.get("tipo", "companhia")
                titulo = carta_atual.get("nome", "")
                titulo_surf = fonte_titulo.render(titulo, True, (0,0,20))
                tela.blit(titulo_surf, (TEXTO_X, 36))

                texto_x = TEXTO_X
                texto_y = TEXTO_Y

                if tipo in ("companhia", "estacao"):
                    linhas = [
                        f"Posição: {carta_atual.get('posicao', '')}",
                        f"Preço: {carta_atual.get('preco', '')}",
                        f"Hipoteca: {carta_atual.get('hipoteca', '')}"
                    ]
                    renderiza_linhas(tela, linhas, fonte_texto, (0,0,0),
                                     texto_x, texto_y, LARGURA_MAX_TEXTO, SPACING)

                elif tipo == "imovel":
                    linhas = [
                        f"Posição: {carta_atual.get('posicao', '')}",
                        f"Preço: {carta_atual.get('preco', '')}",
                        f"Hipoteca: {carta_atual.get('hipoteca', '')}",
                        f"Cor: {carta_atual.get('cor', '')}",
                        f"Preço por casa: {carta_atual.get('preco_casa', '')}",
                        "Aluguéis:"
                    ]
                    aluguel = carta_atual.get("aluguel", [])
                    if isinstance(aluguel, list):
                        for i, valor in enumerate(aluguel, start=0):
                            linhas.append(f"  {i} casas -> {valor}")
                    else:
                        linhas.append(str(aluguel))

                    renderiza_linhas(tela, linhas, fonte_texto, (0,0,0),
                                     texto_x, texto_y, LARGURA_MAX_TEXTO, SPACING)
                else:
                    texto = json.dumps(carta_atual, ensure_ascii=False, indent=2)
                    linhas = texto.splitlines()
                    renderiza_linhas(tela, linhas, fonte_texto, (0,0,0),
                                     texto_x, texto_y, LARGURA_MAX_TEXTO, SPACING)
        '''
        # rodapé: instrução de navegação
        rodape = "[Espaço] Nova carta aleatória    [Esc] Sair"
        rod_img = rod_font.render(rodape, True, (240,240,240))
        tela.blit(rod_img, (20, height - 50))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    baralho = constroi_baralho_casas()  # retorna dict
    mostra_uma_carta(baralho)













