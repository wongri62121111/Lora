# src/ast_nodes.py

class ASTNode:
    def translate(self):
        raise NotImplementedError("Must be implemented in subclass.")


class AssignmentNode(ASTNode):
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression

    def translate(self):
        return f"{self.var_name} = {self.expression}"


class FunctionNode(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body  # List of ASTNode

    def translate(self):
        body_lines = "\n".join(["    " + stmt.translate() for stmt in self.body])
        return f"def {self.name}({', '.join(self.parameters)}):\n{body_lines}"


class ReturnNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def translate(self):
        return f"return {self.expression}"

class IfNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body  # list of ASTNode

    def translate(self):
        body_lines = "\n".join(["    " + stmt.translate() for stmt in self.body])
        return f"if {self.condition}:\n{body_lines}"


