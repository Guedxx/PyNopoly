from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional, Dict, Any
import random
from .Jogador import Jogador, JogadorFalidoState
from .Fabricas import TabuleiroAbstractFactory
from .Banco import Banco
from .Cartas import Baralho, gerar_baralho
from .Imovel import Imovel
from .Imposto import Imposto

if TYPE_CHECKING:
    from .Tabuleiro.Tabuleiro import Tabuleiro


class Partida:
    def __init__(self, nomes_jogadores: List[str], factory: TabuleiroAbstractFactory):
        print("Uma nova partida está sendo criada...")

        self.banco = Banco()
        self.tabuleiro = factory.criar_tabuleiro()
        
        pecas = ["azul", "verde", "rosa", "roxo", "amarelo", "ciano"]
        self.jogadores = [Jogador(pecas[i], nome) for i, nome in enumerate(nomes_jogadores)]

        self.baralho_sorte = gerar_baralho(10)
        self.baralho_cofre = gerar_baralho(10)

        self.jogador_atual_idx: int = 0
        self.em_andamento: bool = False
        self.dados_rolados_neste_turno: bool = False

    def iniciar_jogo(self):
        if not self.jogadores:
            print("Não há jogadores suficientes para iniciar a partida.")
            return
        self.em_andamento = True
        print("\n--- O JOGO COMEÇOU! ---")

    def iniciar_turno(self):
        if not self.em_andamento:
            return None

        jogador_da_vez = self.jogadores[self.jogador_atual_idx]
        valor_dados = jogador_da_vez.jogar_round()

        if valor_dados is None:
            self.proximo_jogador()
            return {"jogador": jogador_da_vez, "dados": None, "acao": "preso"}

        self.dados_rolados_neste_turno = True
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
                "path": [30]
            }

        path = []
        posicao_anterior = jogador_da_vez.posicao
        for i in range(1, sum(valor_dados) + 1):
            path.append((posicao_anterior + i) % 40)
        
        posicao_final_movimento = path[-1] if path else posicao_anterior
        jogador_da_vez.posicao = posicao_final_movimento
        
        passou_pelo_inicio = jogador_da_vez.posicao < posicao_anterior
        if passou_pelo_inicio:
            self.banco.pagar_salario(jogador_da_vez)

        return {
            "jogador": jogador_da_vez,
            "dados": valor_dados,
            "acao": "moveu",
            "path": path,
            "posicao_anterior": posicao_anterior,
            "passou_pelo_inicio": passou_pelo_inicio,
            "is_double": is_double
        }

    def executar_acao_pos_movimento(self):
        jogador_da_vez = self.jogadores[self.jogador_atual_idx]
        casa_atual = self.tabuleiro.get_casa_na_posicao(jogador_da_vez.posicao)

        if casa_atual:
            if isinstance(casa_atual, Imovel) and casa_atual.dono is None:
                if jogador_da_vez.dinheiro >= casa_atual.preco:
                    return {
                        "acao": "proposta_compra",
                        "jogador": jogador_da_vez,
                        "imovel": casa_atual
                    }
                else:
                    print(f"{jogador_da_vez.nome} não tem dinheiro para comprar. Leilão deveria começar.")
                    return {"acao": "turno_finalizado"}
            
            elif isinstance(casa_atual, Imposto):
                return {
                    "acao": "pagar_imposto",
                    "jogador": jogador_da_vez,
                    "imposto": casa_atual
                }

            casa_atual.executar_acao(jogador_da_vez, 0, self.jogadores, self.baralho_sorte, self.baralho_cofre)
            
            posicao_final = jogador_da_vez.posicao
            if posicao_final != casa_atual.pos:
                return {
                    "acao": "movido_por_carta",
                    "path": [posicao_final]
                }

        return {"acao": "turno_finalizado"}

    def resolver_compra(self, decision: bool):
        jogador = self.jogadores[self.jogador_atual_idx]
        casa_atual = self.tabuleiro.get_casa_na_posicao(jogador.posicao)

        if not isinstance(casa_atual, Imovel):
            return

        if decision:
            jogador.comprar_imovel(casa_atual)
            print(f"{jogador.nome} comprou {casa_atual.nome}.")
        else:
            # TODO: Iniciar leilão
            print(f"{jogador.nome} recusou a compra de {casa_atual.nome}. Leilão deveria começar.")

    def resolver_pagamento_imposto(self):
        jogador = self.jogadores[self.jogador_atual_idx]
        casa_atual = self.tabuleiro.get_casa_na_posicao(jogador.posicao)

        if not isinstance(casa_atual, Imposto):
            return
        
        jogador.enviar_dinheiro(casa_atual.valor_imposto)
        print(f"{jogador.nome} pagou ${casa_atual.valor_imposto} de imposto.")


    def finalizar_turno(self, is_double: bool):
        self.verificar_fim_de_jogo()
        if not self.em_andamento:
            return {"acao": "fim_de_jogo"}

        if not is_double:
            self.proximo_jogador()
        else:
            print(f"{self.jogadores[self.jogador_atual_idx].nome} tirou um duplo e joga de novo!")
        
        self.dados_rolados_neste_turno = False
        return {"acao": "turno_pronto_para_iniciar"}


    def proximo_jogador(self):
        self.jogador_atual_idx = (self.jogador_atual_idx + 1) % len(self.jogadores)
        print("-" * 25)

    def verificar_fim_de_jogo(self):
        jogadores_ativos = [j for j in self.jogadores if not isinstance(j.estado_atual, JogadorFalidoState)]
        if len(jogadores_ativos) <= 1:
            self.em_andamento = False
            print("\n--- FIM DE JOGO! ---")
            if jogadores_ativos:
                print(f"O vencedor é {jogadores_ativos[0].peca}!")