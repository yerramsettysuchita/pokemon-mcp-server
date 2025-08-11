import random
import asyncio
from typing import Tuple, List
from .models import Pokemon, BattlePokemon, BattleResult, BattleLog, PokemonType
from .pokemon_data import get_pokemon

class BattleSimulator:
    """Simulates Pokemon battles - like a virtual battle arena"""
    
    def __init__(self):
        # Type effectiveness chart - which types are strong against which
        # 2.0 = super effective, 0.5 = not very effective, 0.0 = no effect
        self.type_effectiveness = {
            PokemonType.FIRE: {
                PokemonType.GRASS: 2.0, PokemonType.ICE: 2.0, PokemonType.BUG: 2.0, PokemonType.STEEL: 2.0,
                PokemonType.FIRE: 0.5, PokemonType.WATER: 0.5, PokemonType.ROCK: 0.5, PokemonType.DRAGON: 0.5
            },
            PokemonType.WATER: {
                PokemonType.FIRE: 2.0, PokemonType.GROUND: 2.0, PokemonType.ROCK: 2.0,
                PokemonType.WATER: 0.5, PokemonType.GRASS: 0.5, PokemonType.DRAGON: 0.5
            },
            PokemonType.ELECTRIC: {
                PokemonType.WATER: 2.0, PokemonType.FLYING: 2.0,
                PokemonType.ELECTRIC: 0.5, PokemonType.GRASS: 0.5, PokemonType.DRAGON: 0.5,
                PokemonType.GROUND: 0.0
            },
            PokemonType.GRASS: {
                PokemonType.WATER: 2.0, PokemonType.GROUND: 2.0, PokemonType.ROCK: 2.0,
                PokemonType.FIRE: 0.5, PokemonType.GRASS: 0.5, PokemonType.POISON: 0.5, PokemonType.FLYING: 0.5, PokemonType.BUG: 0.5, PokemonType.DRAGON: 0.5, PokemonType.STEEL: 0.5
            },
            # Add more type matchups as needed...
        }
    
    async def simulate_battle(self, pokemon1_name: str, pokemon2_name: str, level1: int = 50, level2: int = 50) -> BattleResult:
        """
        Simulate a battle between two Pokemon
        
        Args:
            pokemon1_name: Name of first Pokemon
            pokemon2_name: Name of second Pokemon
            level1: Level of first Pokemon (default 50)
            level2: Level of second Pokemon (default 50)
            
        Returns:
            BattleResult with winner, turns, and detailed log
        """
        
        # Get Pokemon data from our fetcher
        pokemon1_data = await get_pokemon(pokemon1_name)
        pokemon2_data = await get_pokemon(pokemon2_name)
        
        if not pokemon1_data or not pokemon2_data:
            raise ValueError("One or both Pokemon not found!")
        
        # Create battle-ready Pokemon
        pokemon1 = BattlePokemon(pokemon=pokemon1_data, level=level1, current_hp=pokemon1_data.stats.hp)
        pokemon2 = BattlePokemon(pokemon=pokemon2_data, level=level2, current_hp=pokemon2_data.stats.hp)
        
        # Initialize battle log
        battle_log: List[BattleLog] = []
        turn = 1
        
        print(f"⚔️ BATTLE START! {pokemon1.pokemon.name} vs {pokemon2.pokemon.name}")
        print(f"{pokemon1.pokemon.name} HP: {pokemon1.current_hp}")
        print(f"{pokemon2.pokemon.name} HP: {pokemon2.current_hp}")
        print("=" * 50)
        
        # Battle loop - continues until one Pokemon faints
        while pokemon1.current_hp > 0 and pokemon2.current_hp > 0:
            
            # Determine turn order based on speed
            first, second = self._determine_turn_order(pokemon1, pokemon2)
            
            # First Pokemon attacks
            if first.current_hp > 0:
                damage = self._perform_attack(first, second)
                log_entry = BattleLog(
                    turn=turn,
                    attacker=first.pokemon.name,
                    defender=second.pokemon.name,
                    move_used="Tackle",  # Simplified - using basic move
                    damage_dealt=damage,
                    message=f"{first.pokemon.name} attacks {second.pokemon.name} for {damage} damage!",
                    attacker_hp=first.current_hp,
                    defender_hp=second.current_hp
                )
                battle_log.append(log_entry)
                print(f"Turn {turn}: {log_entry.message}")
                
                # Apply status effects
                self._apply_status_effects(first)
                self._apply_status_effects(second)
            
            # Second Pokemon attacks (if still alive)
            if second.current_hp > 0 and first.current_hp > 0:
                damage = self._perform_attack(second, first)
                log_entry = BattleLog(
                    turn=turn,
                    attacker=second.pokemon.name,
                    defender=first.pokemon.name,
                    move_used="Tackle",  # Simplified - using basic move
                    damage_dealt=damage,
                    message=f"{second.pokemon.name} attacks {first.pokemon.name} for {damage} damage!",
                    attacker_hp=second.current_hp,
                    defender_hp=first.current_hp
                )
                battle_log.append(log_entry)
                print(f"Turn {turn}: {log_entry.message}")
                
                # Apply status effects
                self._apply_status_effects(first)
                self._apply_status_effects(second)
            
            turn += 1
            
            # Safety check to prevent infinite battles
            if turn > 50:
                print("Battle ended in a draw after 50 turns!")
                break
        
        # Determine winner
        if pokemon1.current_hp <= 0:
            winner = pokemon2.pokemon.name
            loser = pokemon1.pokemon.name
        elif pokemon2.current_hp <= 0:
            winner = pokemon1.pokemon.name
            loser = pokemon2.pokemon.name
        else:
            winner = "Draw"
            loser = "Draw"
        
        print("=" * 50)
        print(f"🏆 BATTLE END! Winner: {winner}")
        
        return BattleResult(
            winner=winner,
            loser=loser,
            total_turns=turn - 1,
            battle_log=battle_log
        )
    
    def _determine_turn_order(self, pokemon1: BattlePokemon, pokemon2: BattlePokemon) -> Tuple[BattlePokemon, BattlePokemon]:
        """Determine which Pokemon goes first based on speed"""
        speed1 = self._calculate_actual_stat(pokemon1.pokemon.stats.speed, pokemon1.level)
        speed2 = self._calculate_actual_stat(pokemon2.pokemon.stats.speed, pokemon2.level)
        
        if speed1 > speed2:
            return pokemon1, pokemon2
        elif speed2 > speed1:
            return pokemon2, pokemon1
        else:
            # If speeds are equal, choose randomly
            return (pokemon1, pokemon2) if random.random() < 0.5 else (pokemon2, pokemon1)
    
    def _perform_attack(self, attacker: BattlePokemon, defender: BattlePokemon) -> int:
        """Calculate and apply attack damage"""
        
        # Check if Pokemon can attack (paralysis might prevent it)
        if attacker.status == "paralysis" and random.random() < 0.25:
            print(f"{attacker.pokemon.name} is paralyzed and can't move!")
            return 0
        
        # Simplified damage calculation
        attack_stat = self._calculate_actual_stat(attacker.pokemon.stats.attack, attacker.level)
        defense_stat = self._calculate_actual_stat(defender.pokemon.stats.defense, defender.level)
        
        # Base damage calculation (simplified Pokemon formula)
        base_damage = ((2 * attacker.level + 10) / 250) * (attack_stat / defense_stat) * 80 + 2
        
        # Type effectiveness (simplified - just check first types)
        effectiveness = self._get_type_effectiveness(
            attacker.pokemon.types[0] if attacker.pokemon.types else PokemonType.NORMAL,
            defender.pokemon.types[0] if defender.pokemon.types else PokemonType.NORMAL
        )
        
        base_damage *= effectiveness
        
        # Add some randomness (85% to 100% of calculated damage)
        damage = int(base_damage * random.uniform(0.85, 1.0))
        
        # Critical hit chance (6.25% chance for 2x damage)
        if random.random() < 0.0625:
            damage *= 2
            print(f"Critical hit!")
        
        # Apply damage
        defender.current_hp = max(0, defender.current_hp - damage)
        
        # Chance to inflict status effects
        self._maybe_inflict_status(attacker, defender)
        
        return damage
    
    def _calculate_actual_stat(self, base_stat: int, level: int) -> int:
        """Calculate actual stat value based on level"""
        return int((2 * base_stat * level) / 100) + 5
    
    def _get_type_effectiveness(self, attack_type: PokemonType, defend_type: PokemonType) -> float:
        """Get type effectiveness multiplier"""
        if attack_type in self.type_effectiveness:
            return self.type_effectiveness[attack_type].get(defend_type, 1.0)
        return 1.0
    
    def _maybe_inflict_status(self, attacker: BattlePokemon, defender: BattlePokemon):
        """Maybe inflict a status condition"""
        if defender.status is None and random.random() < 0.1:  # 10% chance
            possible_statuses = ["burn", "poison", "paralysis"]
            status = random.choice(possible_statuses)
            defender.status = status
            print(f"{defender.pokemon.name} is now {status}ed!")
    
    def _apply_status_effects(self, pokemon: BattlePokemon):
        """Apply ongoing status effects"""
        if pokemon.status == "burn":
            damage = max(1, pokemon.pokemon.stats.hp // 16)
            pokemon.current_hp = max(0, pokemon.current_hp - damage)
            print(f"{pokemon.pokemon.name} takes {damage} burn damage!")
        
        elif pokemon.status == "poison":
            damage = max(1, pokemon.pokemon.stats.hp // 8)
            pokemon.current_hp = max(0, pokemon.current_hp - damage)
            print(f"{pokemon.pokemon.name} takes {damage} poison damage!")

# Create global battle simulator instance
battle_simulator = BattleSimulator()

# Helper function for easy use
async def simulate_pokemon_battle(pokemon1: str, pokemon2: str) -> BattleResult:
    """Easy way to simulate a battle"""
    return await battle_simulator.simulate_battle(pokemon1, pokemon2)

# Test function
async def test_battle():
    """Test our battle simulator"""
    print("Testing Battle Simulator...")
    
    try:
        result = await simulate_pokemon_battle("pikachu", "charmander")
        print(f"\nBattle completed!")
        print(f"Winner: {result.winner}")
        print(f"Total turns: {result.total_turns}")
        print(f"Number of actions logged: {len(result.battle_log)}")
    except Exception as e:
        print(f"Battle test failed: {e}")

# Run this to test if the file is executed directly
if __name__ == "__main__":
    asyncio.run(test_battle())