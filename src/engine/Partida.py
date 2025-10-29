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

    def __init__(self, pecas_jogadores: List[str], factory: TabuleiroAbstractFactory):
        print("Uma nova partida está sendo criada...")

        # GRASP CREATOR: A Partida cria os objetos que ela agrega e usa intensamente.
        self.banco = Banco()
        self.tabuleiro = factory.criar_tabuleiro()
        self.jogadores = [Jogador(peca, f"Jogador {i+1}") for i, peca in enumerate(pecas_jogadores)]
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
        self.jogar_rodada()  # Inicia a primeira rodada

    def jogar_rodada(self):
        """Executa um turno completo para o jogador atual."""
        if not self.em_andamento:
            print("O jogo já terminou!")
            return

        jogador_da_vez = self.jogadores[self.jogador_atual_idx]
        valor_dados = jogador_da_vez.jogar_round()

        if valor_dados is None:
            self.proximo_jogador()
            return

        is_double = valor_dados[0] == valor_dados[1]

        if is_double:
            jogador_da_vez.doubles_consecutivos += 1
        else:
            jogador_da_vez.doubles_consecutivos = 0

        if jogador_da_vez.doubles_consecutivos == 3:
            print(f"{jogador_da_vez.peca} tirou 3 duplos consecutivos e vai para a cadeia!")
            jogador_da_vez.ir_para_cadeia()
            jogador_da_vez.doubles_consecutivos = 0
            self.proximo_jogador()
            return

        posicao_anterior = jogador_da_vez.posicao
        jogador_da_vez.mover(sum(valor_dados))

        if jogador_da_vez.posicao < posicao_anterior:
            print(f"{jogador_da_vez.peca} completou uma volta!")
            self.banco.pagar_salario(jogador_da_vez)

        casa_atual = self.tabuleiro.get_casa_na_posicao(jogador_da_vez.posicao)
        if casa_atual:
            casa_atual.executar_acao(jogador_da_vez, sum(valor_dados), self.jogadores, self.baralho_sorte, self.baralho_cofre)

        self.verificar_fim_de_jogo()
        if not self.em_andamento:
            return

        if is_double:
            print(f"{jogador_da_vez.peca} tirou dados iguais e joga de novo!")
        else:
            self.proximo_jogador()

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

