import sys
import os
import unittest
from unittest.mock import patch

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.engine.Partida import Partida
from src.engine.Fabricas import TabuleiroPadraoFactory
from src.engine.Jogador import JogadorPresoState

class TestDadosDuplos(unittest.TestCase):

    def setUp(self):
        """Configura uma partida com 2 jogadores para cada teste."""
        pecas = ["Carro", "Chapéu"]
        fabrica_tabuleiro = TabuleiroPadraoFactory()
        self.partida = Partida(pecas, fabrica_tabuleiro)
        self.partida.em_andamento = True
        self.jogador1 = self.partida.jogadores[0]
        self.jogador2 = self.partida.jogadores[1]

    @patch('src.engine.Dados.Dados.lancar')
    def test_jogar_de_novo_com_dados_duplos(self, mock_lancar):
        """Testa se o jogador joga novamente ao tirar dados duplos."""
        mock_lancar.return_value = [3, 3] # Simula dados duplos

        jogador_inicial_idx = self.partida.jogador_atual_idx
        self.assertEqual(self.jogador1.doubles_consecutivos, 0)

        print("\n--- Teste: Jogar de novo com dados duplos ---")
        self.partida.jogar_rodada()

        # O jogador não deve mudar
        self.assertEqual(self.partida.jogador_atual_idx, jogador_inicial_idx)
        # O contador de duplos deve ser 1
        self.assertEqual(self.jogador1.doubles_consecutivos, 1)
        # A posição deve mudar
        self.assertEqual(self.jogador1.posicao, 6)

        print("--- Teste concluído ---")


    @patch('src.engine.Dados.Dados.lancar')
    def test_passar_a_vez_sem_dados_duplos(self, mock_lancar):
        """Testa se o turno passa para o próximo jogador se não tirar dados duplos."""
        mock_lancar.return_value = [3, 4] # Não são duplos

        jogador_inicial_idx = self.partida.jogador_atual_idx
        self.assertEqual(self.jogador1.doubles_consecutivos, 0)

        print("\n--- Teste: Passar a vez sem dados duplos ---")
        self.partida.jogar_rodada()

        # O jogador deve mudar
        self.assertNotEqual(self.partida.jogador_atual_idx, jogador_inicial_idx)
        # O contador de duplos deve ser 0
        self.assertEqual(self.jogador1.doubles_consecutivos, 0)
        # A posição deve mudar
        self.assertEqual(self.jogador1.posicao, 7)
        print("--- Teste concluído ---")


    @patch('src.engine.Dados.Dados.lancar')
    def test_ir_para_cadeia_com_tres_duplos(self, mock_lancar):
        """Testa se o jogador vai para a cadeia após 3 lances de dados duplos."""
        mock_lancar.side_effect = [[1, 1], [2, 2], [3, 3]] # 3 lances duplos

        print("\n--- Teste: Ir para a cadeia com 3 duplos ---")
        
        # Lance 1
        self.partida.jogar_rodada()
        self.assertEqual(self.jogador1.doubles_consecutivos, 1)
        self.assertEqual(self.partida.jogador_atual_idx, 0) # Mesmo jogador
        self.assertEqual(self.jogador1.posicao, 2)

        # Lance 2
        self.partida.jogar_rodada()
        self.assertEqual(self.jogador1.doubles_consecutivos, 2)
        self.assertEqual(self.partida.jogador_atual_idx, 0) # Mesmo jogador
        self.assertEqual(self.jogador1.posicao, 6)

        # Lance 3 - Deve ir para a cadeia
        self.partida.jogar_rodada()
        
        # Verifica se foi para a cadeia
        self.assertIsInstance(self.jogador1.estado_atual, JogadorPresoState)
        self.assertEqual(self.jogador1.posicao, 10) # Posição da cadeia
        
        # O contador de duplos deve ser resetado
        self.assertEqual(self.jogador1.doubles_consecutivos, 0)
        
        # O turno deve passar para o próximo jogador
        self.assertEqual(self.partida.jogador_atual_idx, 1)
        
        print("--- Teste concluído ---")

if __name__ == '__main__':
    unittest.main()
