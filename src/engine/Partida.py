from __future__ import annotations
from typing import List, TYPE_CHECKING
import random
from .Jogador import Jogador, JogadorFalidoState
from .Fabricas import TabuleiroAbstractFactory, TabuleiroPadraoFactory
from .Banco import Banco
from .Cartas import Baralho, gerar_baralho

if TYPE_CHECKING:
    from .Tabuleiro.Tabuleiro import Tabuleiro


class Partida:
    """
    GRASP CONTROLLER: Esta classe é responsável por gerenciar o fluxo e o estado
    geral do jogo Monopoly. Ela orquestra as interações entre os jogadores,
    o tabuleiro e o banco.
    """

    def __init__(self, nomes_jogadores: List[str], factory: TabuleiroAbstractFactory):
        print("Uma nova partida está sendo criada...")

        # GRASP CREATOR: A Partida cria os objetos que ela agrega e usa intensamente.
        self.banco = Banco()
        self.tabuleiro = factory.criar_tabuleiro()
        
        pecas = ["azul", "verde", "rosa", "roxo", "amarelo", "ciano"] # Lista de peças disponíveis
        self.jogadores = [Jogador(pecas[i], nome) for i, nome in enumerate(nomes_jogadores)]

        self.baralho_sorte = gerar_baralho(10)
        self.baralho_cofre = gerar_baralho(10)

        # Atributos para controlar o estado do jogo
        self.jogador_atual_idx: int = 0
        self.em_andamento: bool = False

        print(f"Partida criada com {len(self.jogadores)} jogadores.")

    def iniciar_jogo(self):
        """Prepara e inicia o loop principal do jogo."""
        if not self.jogadores:
            print("Não há jogadores suficientes para iniciar a partida.")
            return

        self.em_andamento = True
        print("\n--- O JOGO COMEÇOU! ---")

    def jogar_rodada(self):
        """
        Executa um turno completo para o jogador atual.
        Retorna um dicionário com o resultado do turno para a UI.
        """
        if not self.em_andamento:
            print("O jogo já terminou!")
            return None

        jogador_da_vez = self.jogadores[self.jogador_atual_idx]
        valor_dados = jogador_da_vez.jogar_round()

        if valor_dados is None: # O jogador está preso e não pagou/tirou dados iguais
            self.proximo_jogador()
            return {"jogador": jogador_da_vez, "dados": None, "acao": "preso"}

        is_double = valor_dados[0] == valor_dados[1]
        if is_double:
            jogador_da_vez.doubles_consecutivos += 1
        else:
            jogador_da_vez.doubles_consecutivos = 0

        if jogador_da_vez.doubles_consecutivos == 3:
            jogador_da_vez.ir_para_cadeia()
            jogador_da_vez.doubles_consecutivos = 0
            self.proximo_jogador()
            return {
                "jogador": jogador_da_vez,
                "dados": valor_dados,
                "acao": "foi_preso_por_doubles",
                "path": [10] # Path direto para a cadeia
            }

        # Calcula o caminho do movimento dos dados
        path = []
        posicao_anterior = jogador_da_vez.posicao
        for i in range(1, sum(valor_dados) + 1):
            path.append((posicao_anterior + i) % 40)
        
        posicao_depois_dado = path[-1] if path else posicao_anterior
        jogador_da_vez.posicao = posicao_depois_dado
        
        passou_pelo_inicio = jogador_da_vez.posicao < posicao_anterior
        if passou_pelo_inicio:
            self.banco.pagar_salario(jogador_da_vez)

        # Executa a ação da casa e verifica se houve movimento secundário
        casa_atual = self.tabuleiro.get_casa_na_posicao(posicao_depois_dado)
        if casa_atual:
            casa_atual.executar_acao(jogador_da_vez, sum(valor_dados), self.jogadores, self.baralho_sorte, self.baralho_cofre)

        posicao_final = jogador_da_vez.posicao
        if posicao_final != posicao_depois_dado:
            path.append(posicao_final) # Adiciona o 'salto' (ex: para a cadeia) ao caminho

        self.verificar_fim_de_jogo()
        
        resultado_turno = {
            "jogador": jogador_da_vez,
            "dados": valor_dados,
            "acao": "moveu",
            "path": path,
            "posicao_anterior": posicao_anterior,
            "passou_pelo_inicio": passou_pelo_inicio
        }

        if not self.em_andamento:
            resultado_turno["fim_de_jogo"] = True
        
        if not is_double:
            self.proximo_jogador()
        
        return resultado_turno

    def proximo_jogador(self):
        """Avança o turno para o próximo jogador na lista."""
        self.jogador_atual_idx = (self.jogador_atual_idx + 1) % len(self.jogadores)
        print("-" * 25)

    def verificar_fim_de_jogo(self):
        """Verifica se o jogo terminou (se resta apenas um jogador não falido)."""
        jogadores_ativos = [j for j in self.jogadores if not isinstance(j.estado_atual, JogadorFalidoState)]
        if len(jogadores_ativos) <= 1:
            self.em_andamento = False
            print("\n--- FIM DE JOGO! ---")
            if jogadores_ativos:
                print(f"O vencedor é {jogadores_ativos[0].peca}!")

