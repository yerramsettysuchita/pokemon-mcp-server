#!/usr/bin/env python3
"""
Basic usage examples for the Pokemon MCP Server
This shows how to use the Pokemon system in your own code
"""

import asyncio
import sys
import os

# Add the parent directory (pokemon-mcp-server) to path so we can import pokemon_env
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import using the same pattern as test files
from pokemon_env.src.models import Pokemon, Move, Stats, BattlePokemon
from pokemon_env.src.pokemon_data import get_pokemon
from pokemon_env.src.battle_simulator import simulate_pokemon_battle

async def example_1_get_pokemon_info():
    """Example 1: Get information about a Pokemon"""
    print("📖 Example 1: Getting Pokemon Information")
    print("-" * 40)
    
    # Get Pikachu's information
    pikachu = await get_pokemon("pikachu")
    
    if pikachu:
        print(f"Name: {pikachu.name}")
        print(f"ID: {pikachu.id}")
        print(f"Types: {', '.join([t.value for t in pikachu.types])}")
        print(f"Height: {pikachu.height}m")
        print(f"Weight: {pikachu.weight}kg")
        print(f"Base HP: {pikachu.stats.hp}")
        print(f"Base Attack: {pikachu.stats.attack}")
        print(f"Base Speed: {pikachu.stats.speed}")
        print(f"Abilities: {', '.join(pikachu.abilities)}")
        print(f"Known moves: {len(pikachu.moves)}")
        
        if pikachu.moves:
            print("First few moves:")
            for move in pikachu.moves[:3]:
                print(f"  - {move.name} ({move.type.value}) - Power: {move.power}")
    else:
        print("Could not fetch Pikachu data")
    
    print()

async def example_2_compare_pokemon():
    """Example 2: Compare two Pokemon stats"""
    print("⚖️ Example 2: Comparing Pokemon Stats")
    print("-" * 40)
    
    # Get two Pokemon to compare
    pokemon1 = await get_pokemon("charizard")
    pokemon2 = await get_pokemon("blastoise")
    
    if pokemon1 and pokemon2:
        print(f"Comparing {pokemon1.name} vs {pokemon2.name}")
        print()
        
        stats = ["hp", "attack", "defense", "special_attack", "special_defense", "speed"]
        
        for stat in stats:
            val1 = getattr(pokemon1.stats, stat)
            val2 = getattr(pokemon2.stats, stat)
            winner = pokemon1.name if val1 > val2 else pokemon2.name if val2 > val1 else "Tie"
            
            print(f"{stat.replace('_', ' ').title():15}: {pokemon1.name} {val1:3} vs {pokemon2.name} {val2:3} - Winner: {winner}")
    
    print()

async def example_3_simple_battle():
    """Example 3: Run a Pokemon battle"""
    print("⚔️ Example 3: Pokemon Battle Simulation")
    print("-" * 40)
    
    print("Simulating battle: Pikachu vs Squirtle")
    
    try:
        result = await simulate_pokemon_battle("pikachu", "squirtle")
        
        print(f"🏆 Winner: {result.winner}")
        print(f"💔 Loser: {result.loser}")
        print(f"🔄 Total turns: {result.total_turns}")
        print(f"📝 Actions logged: {len(result.battle_log)}")
        
        # Show battle summary
        print("\nBattle Summary:")
        for i, log in enumerate(result.battle_log[:5]):  # Show first 5 actions
            print(f"  Turn {log.turn}: {log.message}")
        
        if len(result.battle_log) > 5:
            print(f"  ... and {len(result.battle_log) - 5} more actions")
            
    except Exception as e:
        print(f"Battle failed: {e}")
    
    print()

async def example_4_type_effectiveness():
    """Example 4: Understanding type effectiveness"""
    print("🔥 Example 4: Type Effectiveness Examples")
    print("-" * 40)
    
    # Common type matchups
    matchups = [
        ("fire", "grass", "Fire burns Grass"),
        ("water", "fire", "Water extinguishes Fire"),
        ("electric", "water", "Electric shocks Water"),
        ("grass", "water", "Grass absorbs Water"),
        ("fire", "water", "Water resists Fire"),
        ("electric", "ground", "Electric has no effect on Ground")
    ]
    
    for attacking, defending, description in matchups:
        # Simple effectiveness lookup
        type_chart = {
            "fire": {"grass": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "grass": 0.5},
            "electric": {"water": 2.0, "ground": 0.0},
            "grass": {"water": 2.0, "fire": 0.5}
        }
        
        effectiveness = type_chart.get(attacking, {}).get(defending, 1.0)
        
        if effectiveness == 2.0:
            effect = "Super Effective (2x)"
        elif effectiveness == 0.5:
            effect = "Not Very Effective (0.5x)"
        elif effectiveness == 0.0:
            effect = "No Effect (0x)"
        else:
            effect = "Normal (1x)"
        
        print(f"{attacking.title():8} vs {defending.title():8} = {effect:20} | {description}")
    
    print()

async def example_5_team_analysis():
    """Example 5: Analyze a Pokemon team"""
    print("👥 Example 5: Pokemon Team Analysis")
    print("-" * 40)
    
    team_names = ["pikachu", "charizard", "blastoise"]
    team = []
    
    print("Loading team...")
    for name in team_names:
        pokemon = await get_pokemon(name)
        if pokemon:
            team.append(pokemon)
            print(f"✅ Added {pokemon.name} to team")
        else:
            print(f"❌ Could not load {name}")
    
    if team:
        print(f"\nTeam Analysis (Total: {len(team)} Pokemon)")
        print("-" * 30)
        
        # Calculate team stats
        total_hp = sum(p.stats.hp for p in team)
        avg_attack = sum(p.stats.attack for p in team) / len(team)
        fastest = max(team, key=lambda p: p.stats.speed)
        strongest = max(team, key=lambda p: p.stats.attack)
        
        print(f"Total Team HP: {total_hp}")
        print(f"Average Attack: {avg_attack:.1f}")
        print(f"Fastest Pokemon: {fastest.name} (Speed: {fastest.stats.speed})")
        print(f"Strongest Pokemon: {strongest.name} (Attack: {strongest.stats.attack})")
        
        # Type coverage
        all_types = set()
        for pokemon in team:
            all_types.update(t.value for t in pokemon.types)
        
        print(f"Type Coverage: {', '.join(sorted(all_types))}")
    
    print()

async def main():
    """Run all examples"""
    print("🎮 Pokemon MCP Server - Usage Examples")
    print("=" * 50)
    print("These examples show how to use the Pokemon system in your own code")
    print("=" * 50)
    
    try:
        await example_1_get_pokemon_info()
        await example_2_compare_pokemon()
        await example_3_simple_battle()
        await example_4_type_effectiveness()
        await example_5_team_analysis()
        
        print("=" * 50)
        print("🎉 All examples completed!")
        print("You can use these patterns in your own Pokemon applications.")
        
    except Exception as e:
        print(f"Example error: {e}")
        print("Make sure you have internet connection and the Pokemon API is accessible.")

if __name__ == "__main__":
    asyncio.run(main())