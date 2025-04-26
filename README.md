![image](https://github.com/user-attachments/assets/48458c05-a4b2-42cc-a5e2-6e8143730384)

# Lora - Lua to Python Cross-Compiler

A compiler that translates Lua source code into equivalent Python code while preserving functionality.

## Features
- Full Lua syntax support
- Type preservation
- Scope-aware symbol table
- Error reporting with line numbers
- Standard library stubs

## Installation
```bash
git clone https://github.com/wongri62121111/Lora
cd Lora/src
```

## Usage
1. Place your Lua files in the src directory
2. Run the compiler:
```bash
python main.py
```
3. Generated Python code will be in output.py

## Examples
**Lua Input:**
```lua
local t = {name = "Lua", version = 5.4}
```

**Python Output:**
```python
t = {'name': 'Lua', 'version': 5.4}  # line 1
```

## File Structure
```
src/
├── ast_nodes.py       # AST node definitions
├── lexer.py           # Lexical analyzer
├── lua_tokenizer.py   # Tokenizer interface
├── main.py            # Main compiler script
├── parser.py          # Syntax parser
└── symbol_table.py    # Symbol table implementation
```

## Testing
Run test cases:
```bash
python test_tokenizer.py
```

## Limitations
- No metatable support
- Limited standard library
- No coroutine support

## Contributors
- Tommy Lu
- Ishraq Syed
- Richard Wong
