# Pokemon MCP Server

A Model Context Protocol (MCP) server that provides AI models with access to comprehensive Pokemon data and battle simulation capabilities.

## What This Project Does

This MCP server acts as a bridge between AI models and the Pokemon world, enabling:

1. **Pokemon Data Access**: Get detailed information about any Pokemon including stats, types, abilities, and moves
2. **Battle Simulation**: Simulate realistic battles between any two Pokemon with detailed combat mechanics
3. **Type Effectiveness**: Check type advantages and disadvantages for strategic planning

## Features

### Pokemon Data Resource
- Comprehensive Pokemon database with 900+ species
- Base stats (HP, Attack, Defense, Special Attack, Special Defense, Speed)
- Type information (Fire, Water, Electric, etc.)
- Abilities and move sets
- Physical characteristics (height, weight)
- Real-time data fetching from PokeAPI

### Battle Simulation Tool
- Full turn-based battle mechanics
- Type effectiveness calculations (2x, 0.5x, 0x damage)
- Status effects (Burn, Poison, Paralysis)
- Speed-based turn order
- Critical hit mechanics
- Detailed battle logging
- Realistic damage calculations

## Project Structure

```
pokemon-mcp-server/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── server.py                # Main MCP server
│   ├── models.py                # Data models (Pokemon, Battle, etc.)
│   ├── pokemon_data.py          # Pokemon data fetcher
│   └── battle_simulator.py      # Battle simulation engine
├── examples/                     # Example usage
├── tests/                        # Test files
├── requirements.txt              # Python dependencies
├── test_basic.py                # Basic functionality tests
├── test_mcp.py                  # MCP server tests
└── README.md                    # This file
```

## Installation and Setup

### Prerequisites
- Python 3.9 or higher
- Internet connection (for Pokemon data fetching)

### Step 1: Clone or Download
Download this project to your computer and navigate to the project directory.

### Step 2: Create Virtual Environment
```bash
python -m venv pokemon_env
```

### Step 3: Activate Virtual Environment
**Windows:**
```bash
pokemon_env\Scripts\activate
```

**Mac/Linux:**
```bash
source pokemon_env/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

## Testing Your Installation

### Test Basic Functionality
```bash
python test_basic.py
```

This will test:
- Pokemon data fetching from PokeAPI
- Battle simulation mechanics
- Data model validation

### Test MCP Server
```bash
python test_mcp.py
```

This will test:
- MCP resource listing
- MCP tool functionality
- Complete server integration

## Running the MCP Server

### Start the Server
```bash
cd src
python server.py
```

The server will start and wait for MCP client connections via standard input/output.

### Integration with AI Models
Once running, AI models can interact with the server using these tools:

#### 1. Get Pokemon Data
```json
{
  "tool": "get_pokemon",
  "arguments": {
    "name_or_id": "pikachu"
  }
}
```

#### 2. Simulate Battle
```json
{
  "tool": "simulate_battle", 
  "arguments": {
    "pokemon1": "pikachu",
    "pokemon2": "charizard",
    "level1": 50,
    "level2": 50
  }
}
```

#### 3. Check Type Effectiveness
```json
{
  "tool": "get_type_effectiveness",
  "arguments": {
    "attacking_type": "electric",
    "defending_type": "water"
  }
}
```

## Example Usage

### Getting Pokemon Information
When an AI asks "What are Pikachu's stats?", the server will return:

```json
{
  "name": "Pikachu",
  "id": 25,
  "types": ["electric"],
  "stats": {
    "hp": 35,
    "attack": 55,
    "defense": 40,
    "special_attack": 50,
    "special_defense": 50,
    "speed": 90
  },
  "abilities": ["Static", "Lightning Rod"],
  "height": "0.4m",
  "weight": "6.0kg"
}
```

### Battle Simulation
When an AI requests "Simulate Pikachu vs Charmander", the server returns detailed battle results including turn-by-turn combat log, damage calculations, and the winner.

## Technical Implementation

### Architecture
- **MCP Protocol Compliance**: Full implementation of MCP resource and tool interfaces
- **Async Architecture**: All operations use async/await for optimal performance
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Data Validation**: Pydantic models ensure data integrity
- **Caching**: Pokemon data caching to reduce API calls

### Battle Mechanics
- **Damage Formula**: Simplified Pokemon damage calculation
- **Type Chart**: Comprehensive type effectiveness matrix
- **Status Effects**: Burn (1/16 max HP per turn), Poison (1/8 max HP per turn), Paralysis (25% chance to skip turn)
- **Critical Hits**: 6.25% chance for 2x damage
- **Speed Priority**: Faster Pokemon attacks first

### Data Source
Primary data source is [PokeAPI](https://pokeapi.co/), a free and comprehensive Pokemon database.

## Troubleshooting

### Common Issues

**Import Errors**
- Ensure you're in the correct directory
- Check that virtual environment is activated
- Verify all files are in the correct folders

**Network Errors**
- Check internet connection
- PokeAPI might be temporarily unavailable
- Try with different Pokemon names

**Module Not Found**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check that `src/__init__.py` exists

### Getting Help
If you encounter issues:
1. Check the error message carefully
2. Ensure all setup steps were followed
3. Try running the basic tests first
4. Check that all files are in the correct locations

## Development Notes

This project was designed as a technical assessment demonstrating:
- MCP protocol implementation
- API integration skills
- Data modeling and validation
- Async programming patterns
- Game mechanics implementation
- Clean code architecture

## Future Enhancements

Potential improvements for production use:
- Complete move database with actual power/accuracy values
- Full evolution chain implementation
- More sophisticated AI battle strategies
- Pokemon team building tools
- Competitive battling features
- Move learning and TM compatibility

## License

This project is for educational and demonstration purposes.