import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.engine.Partida import Partida
from src.engine.Fabricas import TabuleiroPadraoFactory

def run_partida_test():
    print("--- Starting Partida Test ---")

    # Create a list of player names
    player_names = ["Alice", "Bob", "Charlie", "David"]

    # Create a board factory
    factory = TabuleiroPadraoFactory()

    # Create a Partida instance
    partida = Partida(player_names, factory)

    # Start the game
    partida.iniciar_jogo()

    # Simulate a few rounds
    for i in range(5):
        print(f"\n--- Round {i+1} ---")
        result = partida.jogar_rodada()
        if result:
            print(f"Turn Result: {result}")
            if result.get("fim_de_jogo"):
                print("Game Over!")
                break
        else:
            print("No result from jogar_rodada (game might be over or an error occurred).")

    print("\n--- Partida Test Finished ---")

if __name__ == "__main__":
    run_partida_test()
