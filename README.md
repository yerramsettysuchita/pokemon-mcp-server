# 🎮 Pokemon MCP Server

A Model Context Protocol (MCP) server that gives AI models superpowers to interact with the Pokemon world! Think of it as a smart bridge that lets AI assistants fetch Pokemon data, simulate epic battles, and analyze type advantages.

## 🌟 What This Project Does

This MCP server acts as a **Pokemon expert assistant** for AI models, enabling them to:

1. **🔍 Pokemon Data Access**: Get detailed info about any Pokemon (stats, types, abilities, moves)
2. **⚔️ Battle Simulation**: Simulate realistic Pokemon battles with full combat mechanics
3. **🔥 Type Effectiveness**: Check which types are strong/weak against each other
4. **🤖 AI Integration**: Ready-to-use interface for AI models like ChatGPT, Claude, etc.

## ✨ Features That Will Amaze You

### 📊 Pokemon Data Resource
- **900+ Pokemon species** from the official PokeAPI
- **Complete battle stats** (HP, Attack, Defense, Special Attack, Special Defense, Speed)
- **Type information** (Fire, Water, Electric, Grass, etc.)
- **Abilities and move sets** with power and accuracy
- **Physical characteristics** (height, weight)
- **Smart caching** to make everything lightning fast

### ⚔️ Battle Simulation Tool
- **Turn-based combat** just like the real Pokemon games
- **Type effectiveness** calculations (2x super effective, 0.5x not very effective, 0x no effect)
- **Status effects** that actually matter (Burn, Poison, Paralysis)
- **Speed-based turn order** (faster Pokemon attacks first)
- **Critical hits** for exciting moments (6.25% chance for 2x damage)
- **Detailed battle logs** showing every action
- **Winner determination** based on which Pokemon faints first

## 📁 Project Structure (What Goes Where)

```
pokemon-mcp-server/
├── pokemon_env/                  # Main project folder
│   ├── src/                     # All the smart code lives here
│   │   ├── __init__.py         # Makes Python recognize this as a package
│   │   ├── models.py           # Pokemon data structures (like Pokemon cards)
│   │   ├── pokemon_data.py     # Fetches Pokemon info from the internet
│   │   ├── battle_simulator.py # The battle arena where Pokemon fight
│   │   └── server.py           # The main server that talks to AI
│   └── examples/               # Cool examples showing how to use everything
│       ├── basic_usage.py      # Simple examples for beginners
│       └── mcp_client_example.py # Advanced AI conversation examples
├── test_basic.py               # Tests to make sure everything works
├── test_mcp.py                 # Tests for the AI server functionality
├── requirements.txt            # List of Python packages needed
├── .gitignore                  # Tells Git what files to ignore
└── README.md                   # This file you're reading!
```

## 🚀 Installation and Setup (Step by Step for Beginners)

### What You Need First
- **Python 3.9 or newer** (download from [python.org](https://python.org))
- **Internet connection** (to fetch Pokemon data)
- **Basic command line knowledge** (don't worry, we'll guide you!)

### Step 1: Get the Project
```bash
# If you have Git installed:
git clone https://github.com/yerramsettysuchita/pokemon-mcp-server.git
cd pokemon-mcp-server

# OR download the ZIP file from GitHub and extract it
```

### Step 2: Create a Safe Python Environment
```bash
# Create a virtual environment (like a clean room for your project)
python -m venv pokemon_env

# Note: We named it pokemon_env to match our project structure
```

### Step 3: Activate Your Environment
**On Windows:**
```bash
pokemon_env\Scripts\activate
```

**On Mac/Linux:**
```bash
source pokemon_env/bin/activate
```

**✅ Success indicator:** You should see `(pokemon_env)` at the start of your command line

### Step 4: Install Required Packages
```bash
# Install all the Python packages our project needs
pip install -r requirements.txt
```

**What this installs:**
- `httpx` - For talking to the Pokemon API
- `pydantic` - For data validation
- `mcp` - For the AI server protocol
- `asyncio` - For super-fast operations

## 🧪 Testing Your Installation (Make Sure Everything Works)

### Test 1: Basic Functionality
```bash
python test_basic.py
```

**What this tests:**
- ✅ Can we fetch Pokemon data from the internet?
- ✅ Can we simulate Pokemon battles?
- ✅ Are all our data models working correctly?

**Expected output:** Green checkmarks ✅ and successful Pokemon data fetching

### Test 2: AI Server Integration
```bash
python test_mcp.py
```

**What this tests:**
- ✅ Can AI models list available tools?
- ✅ Can AI models fetch Pokemon information?
- ✅ Can AI models simulate battles?
- ✅ Is the server responding correctly?

**Expected output:** All server tests passing with Pokemon data and battle results

## 🎯 Running the Examples (See It in Action!)

### Example 1: Basic Pokemon Operations
```bash
cd pokemon_env/examples
python basic_usage.py
```

**What you'll see:**
- Pokemon information lookup (Pikachu's stats!)
- Pokemon comparison (Charizard vs Blastoise)
- Battle simulation (Pikachu vs Squirtle)
- Type effectiveness examples
- Team analysis

### Example 2: AI Conversation Simulation
```bash
python mcp_client_example.py
```

**What you'll see:**
- Simulated AI asking about Pokemon
- AI making battle predictions
- AI recommending team members
- Complex multi-step AI queries

## 🎮 How AI Models Use This Server

Once your server is running, AI models can use these **superpowers**:

### 🔍 Get Pokemon Information
```json
{
  "tool": "get_pokemon",
  "arguments": {
    "name_or_id": "pikachu"
  }
}
```

**AI gets back:** Complete Pokemon stats, types, abilities, moves, and more!

### ⚔️ Simulate Epic Battles
```json
{
  "tool": "simulate_battle",
  "arguments": {
    "pokemon1": "charizard",
    "pokemon2": "blastoise",
    "level1": 50,
    "level2": 50
  }
}
```

**AI gets back:** Full battle log with winner, damage dealt, and turn-by-turn action!

### 🔥 Check Type Advantages
```json
{
  "tool": "get_type_effectiveness",
  "arguments": {
    "attacking_type": "fire",
    "defending_type": "grass"
  }
}
```

**AI gets back:** "Super effective! (2x damage)" - Fire burns Grass!

## 💡 Real Example: What an AI Conversation Looks Like

**Human:** "Who would win: Pikachu vs Charmander?"

**AI using our server:**
1. 🔍 Fetches Pikachu's stats (HP: 35, Attack: 55, Speed: 90)
2. 🔍 Fetches Charmander's stats (HP: 39, Attack: 52, Speed: 65)
3. ⚡ Checks type effectiveness (Electric vs Fire = Normal damage)
4. ⚔️ Simulates the actual battle
5. 🏆 Reports: "Pikachu wins after 3 turns due to higher speed and attack!"

## 🔧 Technical Details (For the Curious)

### Architecture Highlights
- **Async/Await Pattern**: Everything runs super fast without blocking
- **MCP Protocol Compliant**: Works with any AI system that supports MCP
- **Smart Caching**: Pokemon data is cached to avoid repeated API calls
- **Error Handling**: Graceful handling of network issues and invalid Pokemon names
- **Data Validation**: Pydantic ensures all data is correct and type-safe

### Battle Mechanics (Like the Real Games!)
- **Damage Formula**: Simplified but accurate Pokemon damage calculation
- **Type Chart**: Complete type effectiveness matrix
- **Status Effects**: 
  - Burn: 1/16 max HP damage per turn
  - Poison: 1/8 max HP damage per turn  
  - Paralysis: 25% chance to skip turn
- **Critical Hits**: 6.25% chance for double damage
- **Speed Priority**: Faster Pokemon always attacks first

### Data Source
All Pokemon data comes from [PokeAPI](https://pokeapi.co/) - the most comprehensive and free Pokemon database available!

## 🚨 Troubleshooting (When Things Go Wrong)

### "Module Not Found" Error
```bash
# Make sure your virtual environment is activated
# You should see (pokemon_env) in your command line

# If not, activate it:
pokemon_env\Scripts\activate  # Windows
source pokemon_env/bin/activate  # Mac/Linux

# Then install requirements again:
pip install -r requirements.txt
```

### "Network Error" or "Pokemon Not Found"
- ✅ Check your internet connection
- ✅ Try a different Pokemon name (like "pikachu" instead of "pikachuuu")
- ✅ Wait a moment - PokeAPI might be busy
- ✅ Check if the Pokemon name is spelled correctly

### "Import Error" or "Can't Find Files"
- ✅ Make sure you're in the right directory (`pokemon-mcp-server`)
- ✅ Check that all files downloaded correctly
- ✅ Verify the `pokemon_env/src/` folder has all Python files

### Still Stuck?
1. 🔍 Read the error message carefully - it usually tells you what's wrong
2. 🔄 Try running the basic tests first: `python test_basic.py`
3. 📂 Double-check you're in the correct folder
4. 🌐 Ensure you have a stable internet connection

## 🏆 What This Project Demonstrates

This isn't just a Pokemon project - it's a showcase of **professional software engineering skills**:

- ✅ **API Integration**: Real-time data fetching from external services
- ✅ **Async Programming**: Modern Python patterns for high performance
- ✅ **Data Modeling**: Clean, validated data structures with Pydantic
- ✅ **Protocol Implementation**: Full MCP compliance for AI integration
- ✅ **Game Logic**: Complex battle mechanics and calculations
- ✅ **Error Handling**: Robust error management and user feedback
- ✅ **Testing**: Comprehensive test suite ensuring reliability
- ✅ **Documentation**: Clear, beginner-friendly guides
- ✅ **Code Architecture**: Clean, modular, maintainable design

## 🚀 Future Enhancements (Ideas for Making It Even Cooler)

- 🔄 **Evolution Chains**: Full Pokemon evolution trees
- 🎯 **Move Database**: Complete move list with actual power/accuracy from games
- 🧠 **AI Battle Strategy**: Smart AI that picks optimal moves
- 👥 **Team Builder**: Help users build balanced Pokemon teams
- 🏟️ **Tournament Mode**: Multi-Pokemon battles and competitions
- 📊 **Statistics**: Battle win rates and Pokemon performance analytics
- 🎨 **Web Interface**: Beautiful web UI for non-programmers

## 📜 License

This project is created for **educational and demonstration purposes**. All Pokemon data comes from the free PokeAPI. Pokemon is a trademark of Nintendo/Game Freak.

---

**Built with ❤️ for Pokemon fans and AI enthusiasts!**

*Ready to catch 'em all with AI? Start your journey above! 🚀*
