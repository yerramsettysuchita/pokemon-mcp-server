#!/usr/bin/env python3
"""
Basic test file to make sure our Pokemon system works
Run this to test your implementation step by step
"""

import asyncio
import sys
import os

# Add the src directory to Python path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pokemon_env.src.models import Pokemon, Move, Stats, BattlePokemon
from pokemon_env.src.pokemon_data import get_pokemon
from pokemon_env.src.battle_simulator import simulate_pokemon_battle

async def test_pokemon_fetching():
    """Test if we can get Pokemon data"""
    print("🔍 Testing Pokemon Data Fetching...")
    print("-" * 40)
    
    # Test fetching Pikachu
    pikachu = await get_pokemon("pikachu")
    if pikachu:
        print("✅ Successfully fetched Pikachu!")
        print(f"   Name: {pikachu.name}")
        print(f"   Types: {[t.value for t in pikachu.types]}")
        print(f"   HP: {pikachu.stats.hp}")
        print(f"   Attack: {pikachu.stats.attack}")
        print(f"   Speed: {pikachu.stats.speed}")
        print(f"   Abilities: {', '.join(pikachu.abilities)}")
        print(f"   Height: {pikachu.height}m")
        print(f"   Weight: {pikachu.weight}kg")
        if pikachu.moves:
            print(f"   First move: {pikachu.moves[0].name}")
    else:
        print("❌ Failed to fetch Pikachu")
        return False
    
    print()
    
    # Test fetching Charizard
    charizard = await get_pokemon("charizard")
    if charizard:
        print("✅ Successfully fetched Charizard!")
        print(f"   Name: {charizard.name}")
        print(f"   Types: {[t.value for t in charizard.types]}")
        print(f"   HP: {charizard.stats.hp}")
    else:
        print("❌ Failed to fetch Charizard")
        return False
    
    return True

async def test_battle_simulation():
    """Test if we can simulate battles"""
    print("\n⚔️ Testing Battle Simulation...")
    print("-" * 40)
    
    try:
        # Test the full battle simulation
        print("   (Running full battle simulation...)")
        result = await simulate_pokemon_battle("pikachu", "charmander")
        
        print("✅ Battle simulation completed!")
        print(f"   Winner: {result.winner}")
        print(f"   Loser: {result.loser}")
        print(f"   Total turns: {result.total_turns}")
        print(f"   Actions recorded: {len(result.battle_log)}")
        
        # Show battle highlights
        if result.battle_log:
            print("\n📜 Battle highlights:")
            for i, log in enumerate(result.battle_log[:3]):  # Show first 3 actions
                print(f"   Turn {log.turn}: {log.message}")
            if len(result.battle_log) > 3:
                print(f"   ... and {len(result.battle_log) - 3} more actions")
        
        return True
        
    except Exception as e:
        print(f"❌ Battle simulation failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Starting Pokemon MCP Server Tests")
    print("=" * 50)
    
    # Test 1: Pokemon data fetching
    data_test_passed = await test_pokemon_fetching()
    
    if not data_test_passed:
        print("❌ Data fetching failed. Cannot proceed to battle tests.")
        return
    
    # Test 2: Battle simulation
    battle_test_passed = await test_battle_simulation()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Data Fetching: {'✅ PASS' if data_test_passed else '❌ FAIL'}")
    print(f"   Battle Simulation: {'✅ PASS' if battle_test_passed else '❌ FAIL'}")
    
    if data_test_passed and battle_test_passed:
        print("\n🎉 All tests passed! Your Pokemon system is working!")
        print("Next step: Run the MCP server tests with 'python test_mcp.py'")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())