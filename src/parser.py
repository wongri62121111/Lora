# parser.py
from ast_nodes import *
from symbol_table import SymbolTable

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.symbol_table = SymbolTable()
    
    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements
    
    def declaration(self):
        try:
            if self.match("KEYWORD", "function"):
                return self.function_declaration()
            elif self.match("KEYWORD", "local"):
                if self.check("KEYWORD", "function"):
                    return self.function_declaration(is_local=True)
                return self.variable_declaration()
            return self.statement()
        except Exception as e:
            self.symbol_table.add_error(str(e), self.peek().get('lineno'))
            self.synchronize()
            return None
    
    def function_declaration(self, is_local=False):
        start_token = self.consume("KEYWORD", "function", "Expect 'function'")
        name = self.consume("NAME", None, "Expect function name").value
        
        # Enter function scope
        self.symbol_table.enter_scope(is_function=True)
        
        self.consume("OP", "(", "Expect '(' after function name")
        params = []
        if not self.check("OP", ")"):
            param = self.consume("NAME", None, "Expect parameter name")
            self.symbol_table.declare(param.value, "any", is_param=True, lineno=param.get('lineno'))
            params.append(param.value)
            
            while self.match("OP", ","):
                param = self.consume("NAME", None, "Expect parameter name")
                self.symbol_table.declare(param.value, "any", is_param=True, lineno=param.get('lineno'))
                params.append(param.value)
        
        self.consume("OP", ")", "Expect ')' after parameters")
        
        # Handle varargs
        if self.match("OP", "..."):
            params.append("...")
            self.symbol_table.declare("...", "any", is_param=True)
        
        body = self.block("end")
        end_token = self.consume("KEYWORD", "end", "Expect 'end' after function body")
        
        # Exit function scope
        self.symbol_table.exit_scope()
        
        return FunctionNode(name, params, body, is_local, 
                          start_line=start_token.get('lineno'),
                          end_line=end_token.get('lineno'))
    
    def variable_declaration(self):
        names = []
        first_token = self.peek()
        
        # Collect variable names
        name_token = self.consume("NAME", None, "Expect variable name")
        self.symbol_table.declare(
            name_token.value, 
            "any", 
            is_local=True,
            lineno=name_token.get('lineno')
        )
        names.append(name_token.value)
        
        while self.match("OP", ","):
            name_token = self.consume("NAME", None, "Expect variable name")
            self.symbol_table.declare(
                name_token.value,
                "any",
                is_local=True,
                lineno=name_token.get('lineno')
            )
            names.append(name_token.value)
        
        initializers = []
        if self.match("OP", "="):
            initializers.append(self.expression())
            while self.match("OP", ","):
                initializers.append(self.expression())
        
        return VariableDeclarationNode(names, initializers)
    
    def statement(self):
        if self.match("KEYWORD", "if"):
            return self.if_statement()
        elif self.match("KEYWORD", "while"):
            return self.while_statement()
        elif self.match("KEYWORD", "for"):
            return self.for_statement()
        elif self.match("KEYWORD", "return"):
            return self.return_statement()
        elif self.match("KEYWORD", "do"):
            stmts = self.block("end")
            self.consume("KEYWORD", "end", "Expect 'end' after block")
            return BlockNode(stmts)
        else:
            return self.expression_statement()
    
    def if_statement(self):
        condition = self.expression()
        self.consume("KEYWORD", "then", "Expect 'then' after if condition")
        
        then_branch = self.block("end", "elseif", "else")
        elif_branches = []
        else_branch = None
        
        while self.match("KEYWORD", "elseif"):
            elif_cond = self.expression()
            self.consume("KEYWORD", "then", "Expect 'then' after elseif condition")
            elif_body = self.block("end", "elseif", "else")
            elif_branches.append((elif_cond, elif_body))
        
        if self.match("KEYWORD", "else"):
            else_branch = self.block("end")
        
        end_token = self.consume("KEYWORD", "end", "Expect 'end' after if statement")
        return IfNode(condition, then_branch, elif_branches, else_branch, end_token.get('lineno'))
    
    def while_statement(self):
        condition = self.expression()
        self.consume("KEYWORD", "do", "Expect 'do' after while condition")
        body = self.block("end")
        self.consume("KEYWORD", "end", "Expect 'end' after while body")
        return WhileNode(condition, body)
    
    def for_statement(self):
        var_name = self.consume("NAME", None, "Expect variable name").value
        
        if self.match("OP", "="):  # Numeric for
            start = self.expression()
            self.consume("OP", ",", "Expect ',' after start value")
            end = self.expression()
            
            step = None
            if self.match("OP", ","):
                step = self.expression()
            
            self.consume("KEYWORD", "do", "Expect 'do' after for clause")
            body = self.block("end")
            self.consume("KEYWORD", "end", "Expect 'end' after for body")
            return ForNumericNode(var_name, start, end, step, body)
        else:  # Generic for
            self.consume("KEYWORD", "in", "Expect 'in' after variable")
            iter_exprs = [self.expression()]
            while self.match("OP", ","):
                iter_exprs.append(self.expression())
            
            self.consume("KEYWORD", "do", "Expect 'do' after for iterators")
            body = self.block("end")
            self.consume("KEYWORD", "end", "Expect 'end' after for body")
            return ForGenericNode([var_name], iter_exprs, body)
    
    def return_statement(self):
        values = []
        if not self.check("KEYWORD", "end") and not self.check("KEYWORD", "else"):
            values.append(self.expression())
            while self.match("OP", ","):
                values.append(self.expression())
        return ReturnNode(values)
    
    
    
    def expression_statement(self):
        expr = self.expression()
        return ExpressionStatementNode(expr)
    
    def block(self, *end_tokens):
        statements = []
        while not (self.is_at_end() or any(self.check("KEYWORD", token) for token in end_tokens)):
            statements.append(self.declaration())
        return statements
    
    def expression(self):
        return self.assignment()
    
    def assignment(self):
        expr = self.logic_or()
        
        if self.match("OP", "="):
            equals = self.previous()
            value = self.assignment()
            
            if isinstance(expr, VariableNode):
                return AssignmentNode(expr.name, value)
            
            raise RuntimeError(f"Invalid assignment target at {equals.value}")
        
        return expr
    
    def logic_or(self):
        expr = self.logic_and()
        
        while self.match("KEYWORD", "or"):
            operator = self.previous()
            right = self.logic_and()
            expr = LogicalNode(expr, operator.value, right)
        
        return expr
    
    def logic_and(self):
        expr = self.equality()
        
        while self.match("KEYWORD", "and"):
            operator = self.previous()
            right = self.equality()
            expr = LogicalNode(expr, operator.value, right)
        
        return expr
    
    def equality(self):
        expr = self.comparison()
        
        while self.match("OP", "==") or self.match("OP", "~="):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryOpNode(expr, operator.value, right)
        
        return expr
    
    def comparison(self):
        expr = self.term()
        
        while (self.match("OP", ">") or self.match("OP", ">=") or
               self.match("OP", "<") or self.match("OP", "<=")):
            operator = self.previous()
            right = self.term()
            expr = BinaryOpNode(expr, operator.value, right)
        
        return expr
    
    def term(self):
        expr = self.factor()
        
        while self.match("OP", "+") or self.match("OP", "-"):
            operator = self.previous()
            right = self.factor()
            expr = BinaryOpNode(expr, operator.value, right)
        
        return expr
    
    def factor(self):
        expr = self.unary()
        
        while self.match("OP", "*") or self.match("OP", "/") or self.match("OP", "%"):
            operator = self.previous()
            right = self.unary()
            expr = BinaryOpNode(expr, operator.value, right)
        
        return expr
    
    def unary(self):
        if self.match("OP", "-") or self.match("KEYWORD", "not"):
            operator = self.previous()
            right = self.unary()
            return UnaryOpNode(operator.value, right)
        
        return self.primary()
    
    def primary(self):
        if self.match("NUMBER"):
            return LiteralNode(float(self.previous().value))
        elif self.match("STRING"):
            return LiteralNode(self.previous().value[1:-1])  # Remove quotes
        elif self.match("BOOLEAN"):
            return LiteralNode(self.previous().value == "true")
        elif self.match("NIL"):
            return LiteralNode(None)
        elif self.match("NAME"):
            return VariableNode(self.previous().value)
        elif self.match("OP", "("):
            expr = self.expression()
            self.consume("OP", ")", "Expect ')' after expression")
            return GroupingNode(expr)
        elif self.match("OP", "{"):
            return self.table_constructor()
        
        raise RuntimeError(f"Expect expression at {self.peek().value}")
    
    def table_constructor(self):
        elements = []
        start_token = self.peek()
        
        if not self.check("OP", "}"):
            elements.append(self.table_element())
            while self.match("OP", ",") or self.match("OP", ";"):
                if self.check("OP", "}"):
                    break
                elements.append(self.table_element())
        
        end_token = self.consume("OP", "}", "Expect '}' after table elements")
        return TableNode(elements, start_line=start_token.get('lineno'), end_line=end_token.get('lineno'))
    
    def table_element(self):
        if self.check("OP", "[") and self.check_next("OP", "]"):
            self.advance()  # '['
            key = self.expression()
            self.consume("OP", "]", "Expect ']' after table key")
            self.consume("OP", "=", "Expect '=' after table key")
            value = self.expression()
            return TableKeyNode(key, value)
        elif self.check("NAME") and self.check_next("OP", "="):
            key = LiteralNode(self.consume("NAME", None, "Expect field name").value)
            self.consume("OP", "=", "Expect '=' after field name")
            value = self.expression()
            return TableKeyNode(key, value)
        else:
            return TableValueNode(self.expression())
    
    # Helper methods
    def match(self, type_, value=None):
        if self.check(type_, value):
            self.advance()
            return True
        return False
    
    def check(self, type_, value=None):
        if self.is_at_end():
            return False
        token = self.peek()
        if value is None:
            return token["type"] == type_
        return token["type"] == type_ and token["value"] == value
    
    def check_next(self, type_, value=None):
        if self.current + 1 >= len(self.tokens):
            return False
        token = self.tokens[self.current + 1]
        if value is None:
            return token["type"] == type_
        return token["type"] == type_ and token["value"] == value
    
    def consume(self, expected_type, expected_value=None, message=None):
        if self.is_at_end():
            last_token = self.tokens[-1] if self.tokens else {}
            raise RuntimeError(
                f"{message or 'Unexpected end of input'} at line {last_token.get('lineno', '?')}"
            )
        
        token = self.peek()
        if not isinstance(token, dict) or 'type' not in token:
            raise RuntimeError(f"Invalid token format at position {self.current}")
        
        if (token['type'] == expected_type and 
            (expected_value is None or token['value'] == expected_value)):
            return self.advance()
        
        raise RuntimeError(
            f"{message or f'Expected {expected_type}'} at line {token.get('lineno', '?')}"
        )
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self):
        return self.current >= len(self.tokens)
    
    def peek(self):
        if self.is_at_end():
            return {'type': 'EOF', 'value': '', 'lineno': -1}
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]
    
    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous()["type"] == "KEYWORD" and self.previous()["value"] == "end":
                return
            
            if self.peek()["type"] == "KEYWORD" and self.peek()["value"] in {
                "function", "local", "if", "while", "for", "return"
            }:
                return
            
            self.advance()

def parse_tokens(tokens):
    return Parser(tokens).parse()