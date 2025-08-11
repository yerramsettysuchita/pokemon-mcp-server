#!/usr/bin/env python3
"""
MCP Client Example - How an AI model would interact with our Pokemon MCP Server
This demonstrates the actual MCP protocol usage
"""

import asyncio
import json
import sys
import os

# Add the parent directory (pokemon-mcp-server) to path so we can import pokemon_env
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import using the same pattern as test files
from pokemon_env.src.server import server

class MockAI:
    """Simulates how an AI model would use the MCP server"""
    
    def __init__(self, pokemon_server):
        self.server = pokemon_server
        self.conversation_history = []
    
    async def ask_about_pokemon(self, pokemon_name: str):
        """AI asks about a specific Pokemon"""
        print(f"🤖 AI: Tell me about {pokemon_name}")
        
        # AI uses the get_pokemon tool
        result = await self.server.call_tool("get_pokemon", {"name_or_id": pokemon_name})
        pokemon_data = json.loads(result)
        
        if "error" not in pokemon_data:
            response = f"✅ {pokemon_data['name']} is a {'/'.join(pokemon_data['types'])} type Pokemon. "
            response += f"It has {pokemon_data['stats']['hp']} HP, {pokemon_data['stats']['attack']} Attack, "
            response += f"and {pokemon_data['stats']['speed']} Speed. "
            response += f"It weighs {pokemon_data['weight']} and is {pokemon_data['height']} tall."
            
            if pokemon_data['moves']:
                response += f" Some of its moves include: {', '.join([move['name'] for move in pokemon_data['moves'][:3]])}."
        else:
            response = f"❌ Sorry, I couldn't find information about {pokemon_name}."
        
        print(f"🤖 AI Response: {response}")
        self.conversation_history.append(f"Asked about {pokemon_name}")
        return response
    
    async def predict_battle_winner(self, pokemon1: str, pokemon2: str):
        """AI predicts battle outcome"""
        print(f"🤖 AI: Who would win in a battle: {pokemon1} vs {pokemon2}?")
        
        # First, get info about both Pokemon
        result1 = await self.server.call_tool("get_pokemon", {"name_or_id": pokemon1})
        result2 = await self.server.call_tool("get_pokemon", {"name_or_id": pokemon2})
        
        data1 = json.loads(result1)
        data2 = json.loads(result2)
        
        if "error" in data1 or "error" in data2:
            return "❌ I couldn't get information about one or both Pokemon."
        
        # Analyze stats
        print(f"🤖 AI: Let me analyze their stats first...")
        print(f"   {data1['name']}: HP {data1['stats']['hp']}, Attack {data1['stats']['attack']}, Speed {data1['stats']['speed']}")
        print(f"   {data2['name']}: HP {data2['stats']['hp']}, Attack {data2['stats']['attack']}, Speed {data2['stats']['speed']}")
        
        # Check type effectiveness
        if len(data1['types']) > 0 and len(data2['types']) > 0:
            type_result = await self.server.call_tool("get_type_effectiveness", {
                "attacking_type": data1['types'][0],
                "defending_type": data2['types'][0]
            })
            type_data = json.loads(type_result)
            print(f"🤖 AI: {type_data['effect']}")
        
        # Actually simulate the battle
        print(f"🤖 AI: Let me simulate this battle to be sure...")
        battle_result = await self.server.call_tool("simulate_battle", {
            "pokemon1": pokemon1,
            "pokemon2": pokemon2
        })
        battle_data = json.loads(battle_result)
        
        if "error" not in battle_data:
            winner = battle_data['battle_result']['winner']
            turns = battle_data['battle_result']['total_turns']
            
            response = f"🏆 Based on my simulation, {winner} would win after {turns} turns! "
            response += f"The battle was {'quick' if turns <= 3 else 'intense' if turns <= 10 else 'epic'}."
        else:
            response = "❌ I couldn't simulate the battle."
        
        print(f"🤖 AI Response: {response}")
        self.conversation_history.append(f"Predicted battle: {pokemon1} vs {pokemon2}")
        return response
    
    async def recommend_team_member(self, existing_team: list):
        """AI recommends a Pokemon for the team"""
        print(f"🤖 AI: You have {', '.join(existing_team)} on your team. Let me recommend another Pokemon.")
        
        # Analyze existing team
        team_types = set()
        for pokemon_name in existing_team:
            result = await self.server.call_tool("get_pokemon", {"name_or_id": pokemon_name})
            data = json.loads(result)
            if "error" not in data:
                team_types.update(data['types'])
        
        print(f"🤖 AI: Your team currently has these types: {', '.join(team_types)}")
        
        # Simple recommendation logic
        if "water" not in team_types:
            recommendation = "squirtle"
            reason = "You need a Water-type for type coverage"
        elif "fire" not in team_types:
            recommendation = "charmander"
            reason = "A Fire-type would balance your team"
        elif "grass" not in team_types:
            recommendation = "bulbasaur"
            reason = "A Grass-type would complete the starter trio"
        else:
            recommendation = "snorlax"
            reason = "A high HP Pokemon for defense"
        
        # Get info about the recommendation
        result = await self.server.call_tool("get_pokemon", {"name_or_id": recommendation})
        data = json.loads(result)
        
        if "error" not in data:
            response = f"💡 I recommend {data['name']}! {reason}. "
            response += f"It's a {'/'.join(data['types'])} type with {data['stats']['hp']} HP and {data['stats']['attack']} Attack."
        else:
            response = f"💡 I recommend {recommendation}! {reason}."
        
        print(f"🤖 AI Response: {response}")
        return response

async def demo_ai_conversation():
    """Demonstrate how an AI would have a conversation using the MCP server"""
    print("🎭 MCP Client Demo - AI Pokemon Conversation")
    print("=" * 60)
    print("This shows how an AI model would interact with our Pokemon MCP Server")
    print("=" * 60)
    
    # Create AI instance
    ai = MockAI(server)
    
    print("\n🎬 Scene 1: User asks about a Pokemon")
    print("-" * 40)
    await ai.ask_about_pokemon("pikachu")
    
    print("\n🎬 Scene 2: User asks for battle prediction")
    print("-" * 40)
    await ai.predict_battle_winner("charizard", "blastoise")
    
    print("\n🎬 Scene 3: User asks for team recommendation")
    print("-" * 40)
    await ai.recommend_team_member(["pikachu", "charizard"])
    
    print("\n🎬 Scene 4: Complex multi-step query")
    print("-" * 40)
    print("👤 User: I want to know which is better for my team: Alakazam or Machamp?")
    
    # AI breaks down the complex query
    print("🤖 AI: Let me analyze both Pokemon for you...")
    
    # Get both Pokemon
    alakazam_result = await server.call_tool("get_pokemon", {"name_or_id": "alakazam"})
    machamp_result = await server.call_tool("get_pokemon", {"name_or_id": "machamp"})
    
    alakazam_data = json.loads(alakazam_result)
    machamp_data = json.loads(machamp_result)
    
    if "error" not in alakazam_data and "error" not in machamp_data:
        print(f"🤖 AI: Alakazam is a {'/'.join(alakazam_data['types'])} type with high Special Attack ({alakazam_data['stats']['special_attack']}) and Speed ({alakazam_data['stats']['speed']})")
        print(f"🤖 AI: Machamp is a {'/'.join(machamp_data['types'])} type with high Attack ({machamp_data['stats']['attack']}) and HP ({machamp_data['stats']['hp']})")
        
        # Check type effectiveness
        type_result = await server.call_tool("get_type_effectiveness", {
            "attacking_type": "psychic",
            "defending_type": "fighting"
        })
        type_data = json.loads(type_result)
        
        print(f"🤖 AI: Interesting! {type_data['effect']} - Psychic moves are super effective against Fighting types!")
        print("🤖 AI: Based on stats and type advantage, Alakazam would be better if you need speed and special attacks, while Machamp is better for physical power and durability.")
    
    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print("This shows how our MCP server enables rich, interactive Pokemon conversations with AI!")

async def demo_resource_access():
    """Demonstrate resource access"""
    print("\n📚 Resource Access Demo")
    print("-" * 30)
    
    # List available resources
    resources = await server.list_resources()
    print("Available resources:")
    for resource in resources:
        print(f"  📋 {resource['name']}: {resource['description']}")
    
    # Read a resource
    print("\nReading Pokemon database resource:")
    db_info = await server.read_resource("pokemon://database")
    data = json.loads(db_info)
    print(f"Database: {data['name']}")
    print(f"Capabilities: {len(data['capabilities'])} features available")

async def main():
    """Run the MCP client demo"""
    try:
        await demo_ai_conversation()
        await demo_resource_access()
        
        print("\n🚀 All MCP client examples completed successfully!")
        print("This demonstrates how AI models can use your Pokemon MCP server.")
        
    except Exception as e:
        print(f"Demo failed: {e}")
        print("Make sure the Pokemon API is accessible and your internet connection is working.")

if __name__ == "__main__":
    asyncio.run(main())