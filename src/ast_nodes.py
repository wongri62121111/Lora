# ast_nodes.py
class ASTNode:
    def __init__(self, start_line=None, end_line=None):
        self.start_line = start_line
        self.end_line = end_line
    
    def translate(self, symbol_table=None):
        raise NotImplementedError("Must be implemented in subclass.")

class VariableDeclarationNode(ASTNode):
    def translate(self, symbol_table=None):
        if not self.initializers:
            if symbol_table:
                # Check if any variables are unused
                for name in self.names:
                    sym = symbol_table.lookup(name, mark_used=False)
                    if not sym.is_used:
                        print(f"Warning: Variable '{name}' declared but never used")
            
            return "\n".join(f"{name} = None" for name in self.names)
        
        if len(self.names) == len(self.initializers):
            return ", ".join(self.names) + " = " + ", ".join(
                init.translate(symbol_table) for init in self.initializers
            )
        else:
            return f"{', '.join(self.names)} = unpack({{{', '.join(init.translate(symbol_table) for init in self.initializers)}}})"

class VariableNode(ASTNode):
    def translate(self, symbol_table=None):
        if symbol_table:
            try:
                symbol = symbol_table.lookup(self.name)
                if symbol.is_local:
                    return f"_{self.name}"  # Prefix locals for clarity
            except NameError:
                pass  # Use original name if not found
        return self.name

class FunctionNode(ASTNode):
    def __init__(self, name, parameters, body, is_local=False, start_line=None, end_line=None):
        super().__init__(start_line, end_line)
        self.name = name
        self.parameters = parameters
        self.body = body
        self.is_local = is_local
    
    def translate(self, symbol_table=None):
        # Handle varargs
        params = []
        for p in self.parameters:
            if p == "...":
                params.append("*args")  # Python varargs
            else:
                params.append(p)
        
        body_lines = []
        if symbol_table:
            # Create new symbol table for function body
            func_symbol_table = SymbolTable()
            func_symbol_table.enter_scope(is_function=True)
            
            # Add parameters
            for param in self.parameters:
                if param != "...":
                    func_symbol_table.declare(param, "any", is_param=True)
            
            # Translate body
            for stmt in self.body:
                translated = stmt.translate(func_symbol_table)
                if translated:  # Skip None statements (like parse errors)
                    body_lines.append(f"    {translated}")
            
            func_symbol_table.exit_scope()
        else:
            body_lines = [f"    {stmt.translate()}" for stmt in self.body if stmt.translate()]
        
        # Add function header comment
        header_comment = f"  # line {self.start_line}" if self.start_line else ""
        
        prefix = "def " if not self.is_local else "def _local_"
        return (f"{prefix}{self.name}({', '.join(params)}):{header_comment}\n" +
                "\n".join(body_lines))

class IfNode(ASTNode):
    def __init__(self, condition, then_branch, elif_branches=None, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.elif_branches = elif_branches or []
        self.else_branch = else_branch
    
    def translate(self):
        parts = []
        parts.append(f"if {self.condition.translate()}:\n    {self.then_branch.translate()}")
        
        for cond, body in self.elif_branches:
            parts.append(f"elif {cond.translate()}:\n    {body.translate()}")
        
        if self.else_branch:
            parts.append(f"else:\n    {self.else_branch.translate()}")
        
        return "\n".join(parts)

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def translate(self):
        body_lines = "\n".join(f"    {stmt.translate()}" for stmt in self.body)
        return f"while {self.condition.translate()}:\n{body_lines}"

class ForNumericNode(ASTNode):
    def __init__(self, var_name, start, end, step, body):
        self.var_name = var_name
        self.start = start
        self.end = end
        self.step = step
        self.body = body
    
    def translate(self):
        step = self.step.translate() if self.step else "1"
        body_lines = "\n".join(f"    {stmt.translate()}" for stmt in self.body)
        return (
            f"for {self.var_name} in range(int({self.start.translate()}), "
            f"int({self.end.translate()})+1, int({step})):\n{body_lines}"
        )

class ForGenericNode(ASTNode):
    def __init__(self, vars, iter_exprs, body):
        self.vars = vars
        self.iter_exprs = iter_exprs
        self.body = body
    
    def translate(self):
        iter_str = ", ".join(expr.translate() for expr in self.iter_exprs)
        vars_str = ", ".join(self.vars)
        body_lines = "\n".join(f"    {stmt.translate()}" for stmt in self.body)
        return f"for {vars_str} in {iter_str}:\n{body_lines}"

class ReturnNode(ASTNode):
    def __init__(self, values, start_line=None):
        super().__init__(start_line)
        self.values = values
    
    def translate(self, symbol_table=None):
        if not self.values:
            return "return None"
        if len(self.values) == 1:
            return f"return {self.values[0].translate(symbol_table)}"
        
        # Multiple returns become a tuple
        values_str = ", ".join(v.translate(symbol_table) for v in self.values)
        return f"return ({values_str})"

class AssignmentNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def translate(self):
        return f"{self.name} = {self.value.translate()}"

class ExpressionStatementNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    
    def translate(self):
        return self.expression.translate()

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def translate(self):
        op = self.operator
        if op == "~=":
            op = "!="
        return f"{self.left.translate()} {op} {self.right.translate()}"

class LogicalNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def translate(self):
        return f"{self.left.translate()} {self.operator} {self.right.translate()}"

class UnaryOpNode(ASTNode):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    
    def translate(self):
        op = self.operator
        if op == "not":
            op = "not "
        return f"{op}{self.right.translate()}"

class LiteralNode(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def translate(self):
        if isinstance(self.value, str):
            return f'"{self.value}"'
        return str(self.value)

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name
    
    def translate(self):
        return self.name

class GroupingNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    
    def translate(self):
        return f"({self.expression.translate()})"

class TableNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements
    
    def translate(self):
        items = []
        for element in self.elements:
            if isinstance(element, TableKeyNode):
                items.append(f"{element.key.translate()}: {element.value.translate()}")
            else:
                items.append(element.value.translate())
        return "{" + ", ".join(items) + "}"

class TableNode(ASTNode):
    def __init__(self, elements, start_line=None, end_line=None):
        super().__init__(start_line, end_line)
        self.elements = elements
    
    def translate(self, symbol_table=None):
        items = []
        for element in self.elements:
            if isinstance(element, TableKeyNode):
                key = element.key.translate(symbol_table)
                val = element.value.translate(symbol_table)
                # Handle string keys specially for Python dicts
                if isinstance(element.key, LiteralNode) and isinstance(element.key.value, str):
                    items.append(f"'{key}': {val}")
                else:
                    items.append(f"{key}: {val}")
            else:
                items.append(element.value.translate(symbol_table))
        
        # Add line comment if available
        line_comment = f"  # line {self.start_line}" if self.start_line else ""
        return "{" + ", ".join(items) + "}" + line_comment

class TableKeyNode(ASTNode):
    def __init__(self, key, value):
        self.key = key
        self.value = value

class TableValueNode(ASTNode):
    def __init__(self, value):
        self.value = value