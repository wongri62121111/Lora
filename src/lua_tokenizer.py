# lua_tokenizer.py
import re
import json
from lexer import lexer  # Explicit import of lexer function

class LuaTokenizer:
    def __init__(self):
        self.reserved_words = {
            'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
            'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
            'return', 'then', 'true', 'until', 'while'
        }
        self.operators = {
            '+', '-', '*', '/', '%', '^', '#', '==', '~=', '<=', '>=', '<', '>',
            '=', ';', ':', ',', '.', '..', '...'
        }
        self.literals = []
        self.operators_used = []
        self.variables = {}
        self.reserved_words_used = []
        self.total_lines = 0
        self.tokens = []

    def tokenize(self, file_path, include_lines=False):
        with open(file_path, 'r') as file:
            source = file.read()
            lines = source.split('\n')
            self.total_lines = len([line for line in lines if not line.strip().startswith('--')])
            
            if include_lines:
                self.tokens = self._tokenize_with_lines(source)
            else:
                self.tokens = lexer(source)  # Now properly references the imported lexer function

            for token in self.tokens:
                if token["type"] in ["STRING", "NUMBER", "BOOLEAN", "NIL"]:
                    self.literals.append(token["value"])
                elif token["type"] == "OP":
                    self.operators_used.append(token["value"])
                elif token["type"] == "KEYWORD":
                    self.reserved_words_used.append(token["value"])
                elif token["type"] == "NAME":
                    var = token["value"]
                    self.variables[var] = self.variables.get(var, 0) + 1

    def _tokenize_with_lines(self, source):
        tokens = []
        lines = source.split('\n')
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('--'):
                continue  # Skip comments
                
            line_tokens = lexer(line)  # Now properly references the imported lexer function
            for token in line_tokens:
                token['lineno'] = line_num
            tokens.extend(line_tokens)
        return tokens

    def generate_report(self):
        return {
            "literals": {
                "count": len(self.literals),
                "values": list(set(self.literals))
            },
            "operators": {
                "count": len(self.operators_used),
                "values": list(set(self.operators_used))
            },
            "variables": {
                "count": len(self.variables),
                "values": list(self.variables.keys()),
                "duplicates": [var for var, count in self.variables.items() if count > 1]
            },
            "reserved_words": {
                "count": len(self.reserved_words_used),
                "values": list(set(self.reserved_words_used))
            },
            "total_lines_processed": self.total_lines
        }

if __name__ == "__main__":
    tokenizer = LuaTokenizer()
    tokenizer.tokenize("src/example.lua")
    report = tokenizer.generate_report()
    print(json.dumps(report, indent=4))