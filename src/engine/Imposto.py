from __future__ import annotations
from typing import TYPE_CHECKING, List
from .Tabuleiro.CasaTabuleiro import CasaTabuleiro

if TYPE_CHECKING:
    from src.engine.Jogador import Jogador
    from src.engine.Cartas import Baralho

class Imposto(CasaTabuleiro):
    def __init__(self, nome: str, posicao: int, valor_imposto: int):
        super().__init__(nome, posicao)
        self.valor_imposto = valor_imposto

    def executar_acao(self, jogador: Jogador, val_dados: int = 0, jogadores: List[Jogador] = None, baralho_sorte: Baralho = None, baralho_cofre: Baralho = None):
        pass