# src/parser.py

from ast_nodes import FunctionNode, ReturnNode, IfNode

def parse_tokens(tokens):
    ast = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        # --- FUNCTION BLOCK ---
        if token["type"] == "KEYWORD" and token["value"] == "function":
            func_name = tokens[i + 1]["value"]
            i += 3  # Skip 'function', name, and '('

            # Parse parameters
            params = []
            while tokens[i]["value"] != ")":
                if tokens[i]["type"] == "NAME":
                    params.append(tokens[i]["value"])
                i += 1
            i += 1  # skip ')'

            # Parse function body
            body = []
            while i < len(tokens) and not (tokens[i]["type"] == "KEYWORD" and tokens[i]["value"] == "end"):
                if tokens[i]["type"] == "KEYWORD" and tokens[i]["value"] == "if":
                    i += 1
                    condition = ""
                    while tokens[i]["value"] != "then":
                        condition += tokens[i]["value"] + " "
                        i += 1
                    i += 1  # skip 'then'
                    condition = condition.strip()

                    # Handle single return inside if
                    if tokens[i]["type"] == "KEYWORD" and tokens[i]["value"] == "return":
                        return_expr = tokens[i + 1]["value"]
                        if_body = [ReturnNode(return_expr)]
                        body.append(IfNode(condition, if_body))
                        i += 2
                elif tokens[i]["type"] == "KEYWORD" and tokens[i]["value"] == "return":
                    left = tokens[i + 1]["value"]
                    op = tokens[i + 2]["value"]
                    right = tokens[i + 3]["value"]
                    expr = f"{left} {op} {right}"
                    body.append(ReturnNode(expr))
                    i += 4
                else:
                    i += 1

            # Skip 'end' of function
            if i < len(tokens) and tokens[i]["value"] == "end":
                i += 1

            ast.append(FunctionNode(func_name, params, body))

        else:
            i += 1  # Skip anything not a function for now

    return ast
