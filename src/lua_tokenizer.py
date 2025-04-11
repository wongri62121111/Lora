import re
from lexer import lexer  # You must have a lexer.py file in the same folder

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

    def tokenize(self, file_path):
        with open(file_path, 'r') as file:
            source = file.read()
            tokens = lexer(source)

            for token in tokens:
                if token["type"] in ["STRING", "NUMBER", "BOOLEAN", "NIL"]:
                    self.literals.append(token["value"])
                elif token["type"] == "OP":
                    self.operators_used.append(token["value"])
                elif token["type"] == "KEYWORD":
                    self.reserved_words_used.append(token["value"])
                elif token["type"] == "NAME":
                    var = token["value"]
                    self.variables[var] = self.variables.get(var, 0) + 1

            lines = [line for line in source.split('\n') if not line.strip().startswith('--')]
            self.total_lines = len(lines)

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
    tokenizer.tokenize("example.lua")  # Make sure this file exists!
    report = tokenizer.generate_report()

    import json
    print(json.dumps(report, indent=4))
