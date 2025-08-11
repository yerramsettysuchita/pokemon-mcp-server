from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum

class PokemonType(str, Enum):
    """Pokemon types - like Fire, Water, etc."""
    NORMAL = "normal"
    FIRE = "fire"
    WATER = "water"
    ELECTRIC = "electric"
    GRASS = "grass"
    ICE = "ice"
    FIGHTING = "fighting"
    POISON = "poison"
    GROUND = "ground"
    FLYING = "flying"
    PSYCHIC = "psychic"
    BUG = "bug"
    ROCK = "rock"
    GHOST = "ghost"
    DRAGON = "dragon"
    DARK = "dark"
    STEEL = "steel"
    FAIRY = "fairy"

class Stats(BaseModel):
    """Pokemon's battle statistics"""
    hp: int          # Health Points - how much damage it can take
    attack: int      # Physical attack power
    defense: int     # Physical defense
    special_attack: int   # Special attack power (like fire blast)
    special_defense: int  # Special defense
    speed: int       # How fast the Pokemon is

class Move(BaseModel):
    """A Pokemon's attack move"""
    name: str
    type: PokemonType
    power: int       # How much damage it does
    accuracy: int    # How likely it is to hit (out of 100)
    pp: int         # Power Points - how many times you can use it

class Pokemon(BaseModel):
    """Complete Pokemon information"""
    id: int
    name: str
    types: List[PokemonType]  # Pokemon can have 1 or 2 types
    stats: Stats
    abilities: List[str]
    moves: List[Move]
    height: float    # in meters
    weight: float    # in kilograms
    
class BattlePokemon(BaseModel):
    """Pokemon ready for battle with current status"""
    pokemon: Pokemon
    level: int = 50
    current_hp: int
    status: Optional[str] = None  # "burn", "poison", "paralysis", etc.
    
    def __init__(self, **data):
        super().__init__(**data)
        # Calculate actual HP based on level
        if 'current_hp' not in data:
            self.current_hp = self.calculate_actual_hp()
    
    def calculate_actual_hp(self) -> int:
        """Calculate HP based on level (simplified formula)"""
        base_hp = self.pokemon.stats.hp
        return int((2 * base_hp * self.level) / 100) + self.level + 10

class BattleLog(BaseModel):
    """Records what happens in battle"""
    turn: int
    attacker: str    # Pokemon name
    defender: str    # Pokemon name
    move_used: str
    damage_dealt: int
    message: str     # Description of what happened
    attacker_hp: int
    defender_hp: int

class BattleResult(BaseModel):
    """Final battle outcome"""
    winner: str
    loser: str
    total_turns: int
    battle_log: List[BattleLog]