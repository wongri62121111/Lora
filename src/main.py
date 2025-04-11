from lua_tokenizer import LuaTokenizer
from parser import parse_tokens

def main():
    # Step 1: Tokenize Lua code
    tokenizer = LuaTokenizer()
    tokenizer.tokenize("src/example.lua")  # Adjust path if needed
    tokens = tokenizer.tokens  

    # Step 2: Parse tokens into AST
    ast_nodes = parse_tokens(tokens)

    # Step 3: Translate AST to Python code
    translated_lines = [node.translate() for node in ast_nodes]
    python_code = "\n\n".join(translated_lines)

    # Step 4: Output translated code
    with open("src/output/translated.py", "w") as f:
        f.write(python_code)

    print("✅ Translation complete! Check: src/output/translated.py")

if __name__ == "__main__":
    main()
