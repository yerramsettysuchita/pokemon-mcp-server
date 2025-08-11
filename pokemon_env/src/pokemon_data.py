import httpx
import asyncio
from typing import Optional, Dict, Any
from .models import Pokemon, Stats, Move, PokemonType

class PokemonDataFetcher:
    """Fetches Pokemon data from PokeAPI - like a Pokemon encyclopedia"""
    
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"
        self.cache: Dict[str, Pokemon] = {}  # Store Pokemon we've already looked up
        
    async def get_pokemon(self, name_or_id: str) -> Optional[Pokemon]:
        """
        Get a Pokemon by name or ID
        
        Args:
            name_or_id: Pokemon name (like "pikachu") or ID (like "25")
            
        Returns:
            Pokemon object with all the data, or None if not found
        """
        # Check if we already have this Pokemon in our cache
        cache_key = str(name_or_id).lower()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Increased timeout for slow connections
            timeout = httpx.Timeout(30.0)  # 30 seconds timeout
            async with httpx.AsyncClient(timeout=timeout) as client:
                print(f"Fetching {name_or_id} from Pokemon API... (this may take a moment)")
                
                # Get basic Pokemon data
                pokemon_response = await client.get(f"{self.base_url}/pokemon/{name_or_id}")
                pokemon_response.raise_for_status()
                pokemon_data = pokemon_response.json()
                
                # Get Pokemon species data (for more info)
                species_response = await client.get(pokemon_data["species"]["url"])
                species_response.raise_for_status()
                species_data = species_response.json()
                
                # Convert the API data to our Pokemon model
                pokemon = self._convert_api_data_to_pokemon(pokemon_data, species_data)
                
                # Save in cache for next time
                self.cache[cache_key] = pokemon
                print(f"✅ Successfully cached {pokemon.name}")
                return pokemon
                
        except httpx.TimeoutException:
            print(f"⏰ Timeout fetching Pokemon {name_or_id} - API is responding slowly")
            return None
        except httpx.HTTPError as e:
            print(f"🌐 Network error fetching Pokemon {name_or_id}: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error fetching {name_or_id}: {e}")
            return None
    
    def _convert_api_data_to_pokemon(self, pokemon_data: Dict[str, Any], species_data: Dict[str, Any]) -> Pokemon:
        """
        Convert the messy API data into our clean Pokemon model
        Think of this as translating from Pokemon-speak to our language
        """
        
        # Extract basic info
        pokemon_id = pokemon_data["id"]
        name = pokemon_data["name"].title()  # Make first letter uppercase
        
        # Extract types (Fire, Water, etc.)
        types = []
        for type_info in pokemon_data["types"]:
            type_name = type_info["type"]["name"]
            if type_name in [t.value for t in PokemonType]:
                types.append(PokemonType(type_name))
        
        # Extract stats (HP, Attack, etc.)
        stats_data = {}
        for stat in pokemon_data["stats"]:
            stat_name = stat["stat"]["name"]
            base_value = stat["base_stat"]
            
            # Convert API stat names to our names
            if stat_name == "hp":
                stats_data["hp"] = base_value
            elif stat_name == "attack":
                stats_data["attack"] = base_value
            elif stat_name == "defense":
                stats_data["defense"] = base_value
            elif stat_name == "special-attack":
                stats_data["special_attack"] = base_value
            elif stat_name == "special-defense":
                stats_data["special_defense"] = base_value
            elif stat_name == "speed":
                stats_data["speed"] = base_value
        
        stats = Stats(**stats_data)
        
        # Extract abilities
        abilities = []
        for ability_info in pokemon_data["abilities"]:
            abilities.append(ability_info["ability"]["name"].replace("-", " ").title())
        
        # Extract some moves (we'll limit to first 10 to keep it simple)
        moves = []
        for move_info in pokemon_data["moves"][:10]:
            move_name = move_info["move"]["name"].replace("-", " ").title()
            # For now, we'll create simple moves. In a full version, we'd fetch move details
            moves.append(Move(
                name=move_name,
                type=types[0] if types else PokemonType.NORMAL,  # Default to first type
                power=80,  # Default power
                accuracy=90,  # Default accuracy
                pp=15  # Default PP
            ))
        
        # Extract physical characteristics
        height = pokemon_data["height"] / 10.0  # API gives in decimeters, convert to meters
        weight = pokemon_data["weight"] / 10.0  # API gives in hectograms, convert to kg
        
        return Pokemon(
            id=pokemon_id,
            name=name,
            types=types,
            stats=stats,
            abilities=abilities,
            moves=moves,
            height=height,
            weight=weight
        )

# Create a global instance that can be used throughout the app
pokemon_fetcher = PokemonDataFetcher()

# Helper function for easy use
async def get_pokemon(name_or_id: str) -> Optional[Pokemon]:
    """Easy way to get a Pokemon"""
    return await pokemon_fetcher.get_pokemon(name_or_id)

# Test function to make sure everything works
async def test_pokemon_fetcher():
    """Test our Pokemon fetcher"""
    print("Testing Pokemon Data Fetcher...")
    
    # Test with Pikachu
    pikachu = await get_pokemon("pikachu")
    if pikachu:
        print(f"Successfully fetched: {pikachu.name}")
        print(f"Types: {[t.value for t in pikachu.types]}")
        print(f"HP: {pikachu.stats.hp}")
        print(f"First move: {pikachu.moves[0].name if pikachu.moves else 'No moves'}")
    else:
        print("Failed to fetch Pikachu")

# Run this to test if the file is executed directly
if __name__ == "__main__":
    asyncio.run(test_pokemon_fetcher())