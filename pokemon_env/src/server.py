#!/usr/bin/env python3
"""
Pokemon Server - Core functionality for Pokemon operations
This provides the main functions that an MCP server would use
"""

import asyncio
import json
from typing import Any, Dict, List, Optional

# Import our Pokemon modules with relative imports
from .pokemon_data import get_pokemon, pokemon_fetcher
from .battle_simulator import simulate_pokemon_battle
from .models import Pokemon, BattleResult

class PokemonServer:
    """Core Pokemon server functionality"""
    
    def __init__(self):
        self.name = "pokemon-server"
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List available Pokemon resources"""
        return [
            {
                "uri": "pokemon://database",
                "name": "Pokemon Database",
                "description": "Complete Pokemon database with stats, types, abilities, and moves",
                "mimeType": "application/json"
            },
            {
                "uri": "pokemon://pokedex",
                "name": "Pokedex Entries", 
                "description": "Detailed information about any Pokemon",
                "mimeType": "application/json"
            }
        ]
    
    async def read_resource(self, uri: str) -> str:
        """Read a specific resource"""
        if uri == "pokemon://database":
            database_info = {
                "name": "Pokemon Database",
                "description": "Access to comprehensive Pokemon data",
                "capabilities": [
                    "Fetch individual Pokemon data by name or ID",
                    "Get Pokemon stats and battle information", 
                    "Access type effectiveness data",
                    "Retrieve move lists and abilities"
                ],
                "usage_examples": [
                    "Get Pokemon data: Use get_pokemon with a Pokemon name",
                    "Battle simulation: Use simulate_battle with two Pokemon names"
                ]
            }
            return json.dumps(database_info, indent=2)
        
        elif uri == "pokemon://pokedex":
            pokedex_info = {
                "description": "Digital Pokemon encyclopedia",
                "available_data": {
                    "basic_info": ["name", "id", "types", "height", "weight"],
                    "battle_stats": ["hp", "attack", "defense", "special_attack", "special_defense", "speed"],
                    "abilities": "List of Pokemon abilities",
                    "moves": "Available moves with power, accuracy, and type"
                },
                "supported_pokemon": "All Pokemon from the official Pokedex (900+ species)"
            }
            return json.dumps(pokedex_info, indent=2)
        
        else:
            raise ValueError(f"Unknown resource URI: {uri}")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools"""
        return [
            {
                "name": "get_pokemon",
                "description": "Get detailed information about a specific Pokemon",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name_or_id": {
                            "type": "string",
                            "description": "Pokemon name (e.g., 'pikachu') or ID number (e.g., '25')"
                        }
                    },
                    "required": ["name_or_id"]
                }
            },
            {
                "name": "simulate_battle",
                "description": "Simulate a battle between two Pokemon",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pokemon1": {"type": "string", "description": "Name of first Pokemon"},
                        "pokemon2": {"type": "string", "description": "Name of second Pokemon"},
                        "level1": {"type": "integer", "description": "Level of first Pokemon", "default": 50},
                        "level2": {"type": "integer", "description": "Level of second Pokemon", "default": 50}
                    },
                    "required": ["pokemon1", "pokemon2"]
                }
            },
            {
                "name": "get_type_effectiveness",
                "description": "Get type effectiveness information",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "attacking_type": {"type": "string", "description": "Attacking type"},
                        "defending_type": {"type": "string", "description": "Defending type"}
                    },
                    "required": ["attacking_type", "defending_type"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Call a specific tool"""
        
        if name == "get_pokemon":
            name_or_id = arguments.get("name_or_id")
            if not name_or_id:
                return json.dumps({"error": "Pokemon name or ID is required"})
            
            try:
                pokemon = await get_pokemon(name_or_id)
                if not pokemon:
                    return json.dumps({"error": f"Pokemon '{name_or_id}' not found"})
                
                pokemon_info = {
                    "name": pokemon.name,
                    "id": pokemon.id,
                    "types": [t.value for t in pokemon.types],
                    "stats": {
                        "hp": pokemon.stats.hp,
                        "attack": pokemon.stats.attack,
                        "defense": pokemon.stats.defense,
                        "special_attack": pokemon.stats.special_attack,
                        "special_defense": pokemon.stats.special_defense,
                        "speed": pokemon.stats.speed
                    },
                    "abilities": pokemon.abilities,
                    "height": f"{pokemon.height}m",
                    "weight": f"{pokemon.weight}kg",
                    "moves": [
                        {
                            "name": move.name,
                            "type": move.type.value,
                            "power": move.power,
                            "accuracy": move.accuracy
                        } for move in pokemon.moves[:5]
                    ]
                }
                return json.dumps(pokemon_info, indent=2)
                
            except Exception as e:
                return json.dumps({"error": f"Error fetching Pokemon: {str(e)}"})
        
        elif name == "simulate_battle":
            pokemon1 = arguments.get("pokemon1")
            pokemon2 = arguments.get("pokemon2")
            
            if not pokemon1 or not pokemon2:
                return json.dumps({"error": "Both Pokemon names are required"})
            
            try:
                result = await simulate_pokemon_battle(pokemon1, pokemon2)
                
                battle_summary = {
                    "battle_result": {
                        "winner": result.winner,
                        "loser": result.loser,
                        "total_turns": result.total_turns
                    },
                    "battle_log": [
                        {
                            "turn": log.turn,
                            "action": f"{log.attacker} used {log.move_used} on {log.defender}",
                            "damage": log.damage_dealt,
                            "result": log.message,
                            "remaining_hp": {
                                log.attacker: log.attacker_hp,
                                log.defender: log.defender_hp
                            }
                        } for log in result.battle_log[:10]
                    ],
                    "note": f"Showing first 10 of {len(result.battle_log)} total battle actions"
                }
                return json.dumps(battle_summary, indent=2)
                
            except Exception as e:
                return json.dumps({"error": f"Error simulating battle: {str(e)}"})
        
        elif name == "get_type_effectiveness":
            attacking_type = arguments.get("attacking_type", "").lower()
            defending_type = arguments.get("defending_type", "").lower()
            
            if not attacking_type or not defending_type:
                return json.dumps({"error": "Both attacking and defending types are required"})
            
            # Type effectiveness lookup
            type_chart = {
                "fire": {"grass": 2.0, "ice": 2.0, "bug": 2.0, "steel": 2.0, "water": 0.5, "rock": 0.5, "fire": 0.5, "dragon": 0.5},
                "water": {"fire": 2.0, "ground": 2.0, "rock": 2.0, "grass": 0.5, "water": 0.5, "dragon": 0.5},
                "electric": {"water": 2.0, "flying": 2.0, "grass": 0.5, "electric": 0.5, "dragon": 0.5, "ground": 0.0},
                "grass": {"water": 2.0, "ground": 2.0, "rock": 2.0, "fire": 0.5, "grass": 0.5, "poison": 0.5, "flying": 0.5, "bug": 0.5, "dragon": 0.5, "steel": 0.5}
            }
            
            effectiveness = type_chart.get(attacking_type, {}).get(defending_type, 1.0)
            
            if effectiveness == 2.0:
                effect_text = "Super effective! (2x damage)"
            elif effectiveness == 0.5:
                effect_text = "Not very effective... (0.5x damage)"
            elif effectiveness == 0.0:
                effect_text = "No effect! (0x damage)"
            else:
                effect_text = "Normal effectiveness (1x damage)"
            
            result = {
                "attacking_type": attacking_type.title(),
                "defending_type": defending_type.title(),
                "effectiveness_multiplier": effectiveness,
                "effect": effect_text
            }
            return json.dumps(result, indent=2)
        
        else:
            return json.dumps({"error": f"Unknown tool: {name}"})

# Create global server instance
server = PokemonServer()

# Test function
async def test_server():
    """Test the server functionality"""
    print("Testing Pokemon Server...")
    
    # Test list resources
    resources = await server.list_resources()
    print(f"Resources: {len(resources)} available")
    
    # Test get Pokemon
    result = await server.call_tool("get_pokemon", {"name_or_id": "pikachu"})
    data = json.loads(result)
    if "error" not in data:
        print(f"✅ Successfully got Pokemon: {data['name']}")
    else:
        print(f"❌ Error: {data['error']}")
    
    # Test battle simulation
    battle_result = await server.call_tool("simulate_battle", {"pokemon1": "pikachu", "pokemon2": "charmander"})
    battle_data = json.loads(battle_result)
    if "error" not in battle_data:
        print(f"✅ Battle completed - Winner: {battle_data['battle_result']['winner']}")
    else:
        print(f"❌ Battle error: {battle_data['error']}")

if __name__ == "__main__":
    asyncio.run(test_server())