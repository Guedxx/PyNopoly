from __future__ import annotations
from typing import TYPE_CHECKING, List
from .CasaTabuleiro import CasaTabuleiro

if TYPE_CHECKING:
    from ..Jogador import Jogador
    from ..Cartas import Baralho

class PontoDePartida(CasaTabuleiro):
    def executar_acao(self, jogador: Jogador, val_dados: int = 0, jogadores: List[Jogador] = None, baralho_sorte: Baralho = None, baralho_cofre: Baralho = None):
        pass

