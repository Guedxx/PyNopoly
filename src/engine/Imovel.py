from __future__ import annotations
from typing import List, TYPE_CHECKING
from .Tabuleiro.Terreno import Terreno

if TYPE_CHECKING:
    from .Jogador import Jogador
    from .Cartas import Baralho

class Imovel(Terreno):
    def __init__(self, nome: str, posicao: int, preco: int, hipoteca: int, 
                 cor: str, alugueis: List[int], preco_casa: int, hipotecado: bool = False):
        super().__init__(nome, posicao, preco, cor)
        self.hipoteca = hipoteca
        self.alugueis = alugueis
        self.cor = cor
        self.casas = 0
        self.preco_casa = preco_casa
        self.hipotecado = hipotecado  
    
    def calcular_aluguel(self, val_dados: int = 0) -> int:
        
        # Se o imóvel está hipotecado, não cobra aluguel
        if self.hipotecado:
            return 0
        # Se não há casas, retorna aluguel básico
        if self.casas == 0:
            return self.alugueis[0]
        # Se há casas, retorna aluguel correspondente
        elif 1 <= self.casas <= 4:
            return self.alugueis[self.casas]
        # Se tem hotel (5 casas), retorna aluguel de hotel
        elif self.casas == 5:
            return self.alugueis[5]
        else:
            return 0  # Caso inválido

    def set_hipotecado(self, hipotecado: bool):
        self.hipotecado = hipotecado

    def executar_acao(self, jogador: Jogador, val_dados: int = 0, jogadores: List[Jogador] = None, baralho_sorte: Baralho = None, baralho_cofre: Baralho = None):
        if self.dono is None:
            # Lógica de compra será transferida para a Partida/UI
            # Por enquanto, não faz nada
            pass
        elif self.dono is not jogador:
            aluguel = self.calcular_aluguel(val_dados)
            jogador.pagar_aluguel(self.dono, aluguel)
