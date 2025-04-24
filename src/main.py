# main.py
from lua_tokenizer import LuaTokenizer
from parser import Parser
import os

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lua_file = os.path.join(script_dir, "example.lua")  # Updated path
    
    # Tokenize with line numbers
    tokenizer = LuaTokenizer()
    tokenizer.tokenize(lua_file, include_lines=True)  # Use the full path
    
    # Rest of your code remains the same...
    parser = Parser(tokenizer.tokens)
    ast = parser.parse()
    
    # Show symbol table and errors
    parser.symbol_table.print_state()
    
    # Generate Python code
    python_code = "\n\n".join(
        node.translate(parser.symbol_table) 
        for node in ast 
        if node is not None
    )
    
    # Add standard library stubs
    stdlib = """
# Lua standard library stubs
def print(*args):
    print(' '.join(str(arg) for arg in args))
"""
    
    with open("output.py", "w") as f:
        f.write(stdlib + "\n\n" + python_code)

if __name__ == "__main__":
    main()