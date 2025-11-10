from __future__ import annotations
from typing import List, TYPE_CHECKING
from .Leilao import Leilao

# Usamos TYPE_CHECKING para evitar importações circulares com Jogador e Terreno
if TYPE_CHECKING:
    from .Jogador import Jogador
    from .Tabuleiro.Terreno import Terreno
from .Imovel import Imovel

class Banco:
    def __init__(self):
        # Podemos mudar o numero aqui depois, mas tem algo de casas disponiveis no .pdf das regras.
        self._casas_disponiveis: int = 32
        self._hoteis_disponiveis: int = 12
        self._leilao = Leilao()

    @property
    def casas_disponiveis(self) -> int:
        return self._casas_disponiveis

    @property
    def hoteis_disponiveis(self) -> int:
        return self._hoteis_disponiveis

    def pagar_salario(self, jogador: Jogador):
        """Paga o salário de $200 ao jogador por passar pelo Ponto de Partida."""
        print(f"Banco pagou $200 de salário para {jogador.peca}.")
        jogador.receber_dinheiro(200)

    def hipotecar_imovel(self, imovel: Terreno, jogador: Jogador):
        """
        Empresta dinheiro ao jogador com base no valor de hipoteca do imóvel.
        Vende todas as casas do imóvel pela metade do preço antes de hipotecar.
        """
        if isinstance(imovel, Imovel) and imovel.casas > 0:
            casas_vendidas = imovel.casas
            valor_venda_casas = int((casas_vendidas * imovel.preco_casa) / 2)
            jogador.receber_dinheiro(valor_venda_casas)
            
            if casas_vendidas == 5: # Hotel
                self._hoteis_disponiveis += 1
            else:
                self._casas_disponiveis += casas_vendidas
            
            imovel.casas = 0
            print(f"{jogador.peca} vendeu {casas_vendidas} casas em {imovel.nome} por ${valor_venda_casas}.")

        jogador.receber_dinheiro(imovel.hipoteca)
        imovel.set_hipotecado(True)
        print(f"{jogador.peca} hipotecou {imovel.nome} por ${imovel.hipoteca}.")


    def resgatar_hipoteca(self, imovel: Terreno, jogador: Jogador):
        """
        Recebe o pagamento do jogador para liberar a hipoteca de um imóvel, ou seja, 
        depois disso o imóvel não está mais hipotecado.
        A regra é o valor da hipoteca + 10% de juros.
        """
        custo_resgate = int(imovel.hipoteca * 1.1)
        jogador.enviar_dinheiro(custo_resgate)
        imovel.set_hipotecado(False)
        print(f"{jogador.peca} resgatou {imovel.nome} por ${custo_resgate}.")

    def iniciar_leilao(self, imovel: Terreno, jogadores: List[Jogador]):
        """
        Inicia um leilão para uma propriedade não comprada. [cite: 1555]
        Delega a responsabilidade para o objeto Leilao.
        """
        self._leilao.realizar_leilao(imovel, jogadores)
