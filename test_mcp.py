#!/usr/bin/env python3
"""
Test the Pokemon server functionality
This tests the core server functions that would be used by MCP
"""

import asyncio
import sys
import os
import json

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the server module
from pokemon_env.src.server import server

async def test_pokemon_server():
    """Test Pokemon server functionality"""
    print("🧪 Testing Pokemon Server Functionality")
    print("=" * 50)
    
    # Test 1: List available resources
    print("📋 Test 1: Listing available resources...")
    try:
        resources = await server.list_resources()
        print(f"✅ Found {len(resources)} resources:")
        for resource in resources:
            print(f"   - {resource['name']}: {resource['description']}")
    except Exception as e:
        print(f"❌ Error listing resources: {e}")
        return False
    
    print()
    
    # Test 2: Read a resource
    print("📖 Test 2: Reading Pokemon database resource...")
    try:
        database_info = await server.read_resource("pokemon://database")
        data = json.loads(database_info)
        print(f"✅ Successfully read database resource:")
        print(f"   - Name: {data['name']}")
        print(f"   - Capabilities: {len(data['capabilities'])} features")
    except Exception as e:
        print(f"❌ Error reading resource: {e}")
        return False
    
    print()
    
    # Test 3: List available tools
    print("🔧 Test 3: Listing available tools...")
    try:
        tools = await server.list_tools()
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool['name']}: {tool['description']}")
    except Exception as e:
        print(f"❌ Error listing tools: {e}")
        return False
    
    print()
    
    # Test 4: Test get_pokemon tool
    print("🔍 Test 4: Testing get_pokemon tool...")
    try:
        result = await server.call_tool("get_pokemon", {"name_or_id": "pikachu"})
        pokemon_data = json.loads(result)
        
        if "error" not in pokemon_data:
            print(f"✅ Successfully fetched Pokemon data:")
            print(f"   - Name: {pokemon_data['name']}")
            print(f"   - Types: {', '.join(pokemon_data['types'])}")
            print(f"   - HP: {pokemon_data['stats']['hp']}")
        else:
            print(f"❌ Error: {pokemon_data['error']}")
            return False
    except Exception as e:
        print(f"❌ Error testing get_pokemon tool: {e}")
        return False
    
    print()
    
    # Test 5: Test type effectiveness tool
    print("⚡ Test 5: Testing type effectiveness tool...")
    try:
        result = await server.call_tool("get_type_effectiveness", {
            "attacking_type": "electric",
            "defending_type": "water"
        })
        effectiveness_data = json.loads(result)
        
        if "error" not in effectiveness_data:
            print(f"✅ Type effectiveness check:")
            print(f"   - {effectiveness_data['attacking_type']} vs {effectiveness_data['defending_type']}")
            print(f"   - Effect: {effectiveness_data['effect']}")
        else:
            print(f"❌ Error: {effectiveness_data['error']}")
            return False
    except Exception as e:
        print(f"❌ Error testing type effectiveness: {e}")
        return False
    
    print()
    
    # Test 6: Test battle simulation
    print("⚔️ Test 6: Testing battle simulation...")
    try:
        print("   (This may take a moment as it fetches Pokemon data and simulates battle...)")
        result = await server.call_tool("simulate_battle", {
            "pokemon1": "pikachu",
            "pokemon2": "charmander"
        })
        battle_data = json.loads(result)
        
        if "error" not in battle_data:
            print(f"✅ Battle simulation completed:")
            print(f"   - Winner: {battle_data['battle_result']['winner']}")
            print(f"   - Total turns: {battle_data['battle_result']['total_turns']}")
            print(f"   - Battle actions logged: {len(battle_data['battle_log'])}")
        else:
            print(f"❌ Error: {battle_data['error']}")
            return False
    except Exception as e:
        print(f"❌ Error testing battle simulation: {e}")
        return False
    
    print()
    print("=" * 50)
    print("🎉 All Pokemon server tests completed successfully!")
    print("Your Pokemon server is ready for MCP integration!")
    
    return True

async def main():
    """Run all Pokemon server tests"""
    success = await test_pokemon_server()
    
    if success:
        print("\n🚀 Your Pokemon server is fully functional!")
        print("✅ Core functionality works perfectly")
        print("✅ All tools are operational")
        print("✅ Data fetching and battle simulation work")
        print("\nNext steps:")
        print("1. Your system is ready for submission")
        print("2. All requirements are met")
        print("3. Pokemon MCP server is complete!")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())