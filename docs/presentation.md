# Final Project Presentation: Lua to Python Cross-Compiler

## 1. Project Overview
**Project Name**: Lora - Lua to Python Cross-Compiler  
**Team Members**: Tommy Lu, Ishraq Syed, Richard Wong  
**Course**: CMPSC 470, Section 001 – Spring 2025  

A compiler that translates Lua source code into equivalent Python code, preserving functionality while adapting to Python's syntax and semantics.

## 2. Language Whitepaper
### Key Features:
- Full Lua syntax support (functions, tables, control structures)
- Type preservation during translation
- Symbol table for variable tracking and scope management
- Error reporting with line numbers
- Standard library function stubs

### Implementation Highlights:
- Token-by-token lexical analysis
- Abstract Syntax Tree (AST) generation
- Context-aware symbol table
- Python code generation from AST

## 3. Language Tutorial
### Basic Usage:
1. Place Lua files in project directory
2. Run main.py
3. Output Python code generated in output.py

### Example Translation:
**Lua Input:**
```lua
function add(a, b)
    return a + b
end
```

**Python Output:**
```python
def add(a, b):  # line 2
    return a + b
```

## 4. Language Reference Manual
### Supported Lua Features:
- Functions (local/global)
- Variables (local/global)
- Control structures (if, while, for)
- Tables (arrays/dictionaries)
- Operators (arithmetic, logical, relational)
- Standard library functions (print)

### Limitations:
- Metatables not supported
- Coroutines not supported
- Some standard library functions not implemented

## 5. Project Development Plan
### Timeline:
1. Lexical analysis (Weeks 1-3)
2. Syntax analysis (Weeks 4-6)
3. Semantic analysis (Weeks 7-9)
4. Code generation (Weeks 10-12)
5. Testing and refinement (Weeks 13-15)

### Roles:
- **Project Manager**: Richard Wong
- **Language Guru**: Tommy Lu
- **System Architect**: Ishraq Syed
- **Systems Integrator**: Team collaboration
- **Tester**: All members

## 6. Translator Architecture
### Components:
1. **Lexer**: Tokenizes Lua source code
2. **Parser**: Builds AST from tokens
3. **Symbol Table**: Tracks variables and scopes
4. **Code Generator**: Produces Python from AST

### Data Flow:
Lua Source → Tokenizer → Parser → AST → Symbol Table → Code Generator → Python Output

## 7. Development Environment
### Requirements:
- Python 3.6+
- No external dependencies

### Setup:
```bash
git clone https://github.com/wongri62121111/Lora
cd Lora/src
python main.py
```

## 8. Test Plan
### Testing Strategy:
- Unit tests for each component
- Integration tests for full translation
- Comparison of Lua and Python output behavior

### Test Cases:
1. Variable declarations
2. Function definitions
3. Control structures
4. Table operations
5. Error handling

## 9. Conclusions
### Achievements:
- Successful translation of core Lua features
- Clean Python code output
- Comprehensive error reporting
- Symbol tracking across scopes

### Challenges:
- Handling Lua's flexible syntax
- Table to dictionary conversion
- Scope management

### Future Work:
- Support for metatables
- Standard library implementation
- Performance optimizations

---
