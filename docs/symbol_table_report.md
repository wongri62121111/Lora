## Overview
The symbol table is a fundamental data structure in compiler design that tracks identifiers (variables, functions, etc.) and their attributes throughout the compilation process.

## Implementation Details

**Key Components:**
- **Scope Management**: Uses a stack-based approach to handle nested scopes (global/local)
- **Variable Tracking**: Stores variable names, types (number, string, boolean), and current values
- **Type Checking**: Enforces type safety during variable updates
- **Lookup Mechanism**: Searches scopes from innermost to global when resolving variables

**Data Structures Used:**
- Dictionary for symbol storage (O(1) lookup time)
- List (stack) for scope management

## Role in Lua-to-Python Compiler

**Specific Functions:**
1. **Variable Declaration Tracking**: Records all variables declared in Lua code
2. **Type Validation**: Ensures Python output maintains Lua's dynamic typing behavior
3. **Scope Resolution**: Handles Lua's block scoping rules during conversion
4. **Code Generation Support**: Provides context for proper Python variable naming

**Integration Points:**
- During AST construction when variables are declared
- During semantic analysis for type checking
- During code generation for proper variable references

## General Compiler Functions

**Core Purposes:**
1. **Identifier Storage**: Maintains all declared names and their attributes
2. **Scope Management**: Tracks which identifiers are visible in each program region
3. **Type Checking**: Enforces language typing rules
4. **Error Detection**: Cataches duplicate declarations or undefined variables
5. **Code Optimization**: Provides data for optimization passes

## Implementation in a Compiler

**Typical Workflow:**
1. **Initialization**: Create symbol table when compilation begins
2. **Processing**:
   - Add entries for each declaration
   - Validate references against existing entries
   - Manage scope transitions (function/block entry/exit)
3. **Finalization**: Verify all references were resolved

**Example Integration:**

```python
# During compilation
symbol_table = SymbolTable()

# When entering a function
symbol_table.enter_scope()

# When processing variable declaration
symbol_table.declare(var_name, var_type, initial_value)

# When processing variable reference
var_info = symbol_table.lookup(var_name)

# When exiting a function
symbol_table.exit_scope()
```