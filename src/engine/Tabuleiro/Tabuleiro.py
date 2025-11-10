from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional
from ..Imovel import Imovel

if TYPE_CHECKING:
    from .CasaTabuleiro import CasaTabuleiro
    from ..Jogador import Jogador

class Tabuleiro:
    def __init__(self, casas: List[CasaTabuleiro]):
        self.casas = casas

    def get_casa_na_posicao(self, posicao: int) -> Optional[CasaTabuleiro]:
        if 0 <= posicao < len(self.casas):
            return self.casas[posicao]
        return None
    
    def get_propriedades_da_cor(self, cor: str) -> int:
        acumulador = 0
        for casa in self.casas:
            if isinstance(casa, Imovel) and casa.cor == cor:
                acumulador += 1 
        return acumulador
