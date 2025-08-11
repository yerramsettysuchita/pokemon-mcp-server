__version__ = "1.0.0"
__author__ = "Suchita Yerramsetty"
__description__ = "Pokemon MCP Server for AI model integration"

# Export main components
from .pokemon_data import get_pokemon, pokemon_fetcher
from .battle_simulator import simulate_pokemon_battle, battle_simulator
from .models import Pokemon, BattlePokemon, BattleResult, BattleLog, Stats, Move, PokemonType

__all__ = [
    'get_pokemon', 
    'pokemon_fetcher',
    'simulate_pokemon_battle',
    'battle_simulator',
    'Pokemon',
    'BattlePokemon', 
    'BattleResult',
    'BattleLog',
    'Stats',
    'Move',
    'PokemonType'
]