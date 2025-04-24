# symbol_table.py
class SymbolTable:
    def declare(self, name, symbol_type, value=None, is_local=False, is_param=False, lineno=None):
        if isinstance(name, dict):
            name_value = name.get('value') or name.get('raw')
            lineno = name.get('lineno', lineno)
            if not name_value:
                self.add_error("Invalid token format - missing name", lineno)
                return None
            name = str(name_value)
        
        # Rest of the method remains the same
        if not isinstance(name, str):
            self.add_error(f"Invalid symbol name: {name}", lineno)
            return None
        self.name = name
        self.type = symbol_type  # 'number', 'string', 'boolean', 'table', 'function', 'any'
        self.value = value
        self.is_local = is_local
        self.is_param = is_param
        self.is_used = False
        self.lineno = lineno
        self.meta = {}  # For table metatables

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]
        self.current_scope_level = 0
        self.function_scopes = []
        self.errors = []
    
    def add_error(self, message, lineno=None):
        self.errors.append(f"Line {lineno}: {message}" if lineno else message)
    
    def enter_scope(self, is_function=False):
        self.scopes.append({})
        self.current_scope_level += 1
        if is_function:
            self.function_scopes.append(self.current_scope_level)
    
    def exit_scope(self):
        if len(self.scopes) == 1:
            self.add_error("Cannot exit global scope")
            return
        
        # Check for unused locals
        for name, sym in self.scopes[-1].items():
            if sym.is_local and not sym.is_used and not sym.is_param:
                self.add_error(f"Unused local variable '{name}'", sym.lineno)
        
        if self.function_scopes and self.function_scopes[-1] == self.current_scope_level:
            self.function_scopes.pop()
        
        self.scopes.pop()
        self.current_scope_level -= 1
    
    def declare(self, name, symbol_type, value=None, is_local=False, is_param=False, lineno=None):
        if isinstance(name, dict):  # Handle token objects
            name_value = name.get('value') or name.get('raw')
            lineno = name.get('lineno')
            if not name_value:
                self.add_error("Invalid token format - missing name", lineno)
                return None
            name = name_value
    
    def lookup(self, name, mark_used=True, lineno=None):
        for scope in reversed(self.scopes):
            if name in scope:
                if mark_used and not scope[name].is_param:
                    scope[name].is_used = True
                return scope[name]
        self.add_error(f"Undefined variable '{name}'", lineno)
        return Symbol(name, 'any')  # Return dummy symbol
    
    def assign(self, name, value, lineno=None):
        symbol = self.lookup(name, lineno=lineno)
        
        # Type checking
        if symbol.type != 'any' and value is not None:
            type_ok = (
                (symbol.type == 'number' and isinstance(value, (int, float))) or
                (symbol.type == 'string' and isinstance(value, str)) or
                (symbol.type == 'boolean' and isinstance(value, bool)) or
                (symbol.type == 'table' and isinstance(value, dict))
            )
            if not type_ok:
                self.add_error(
                    f"Type mismatch: cannot assign {type(value)} to {symbol.type} '{name}'",
                    lineno
                )
        
        symbol.value = value
        return symbol
    
    def is_in_function_scope(self):
        return bool(self.function_scopes)
    
    def print_state(self):
        print("\nSymbol Table State:")
        print("-------------------")
        for i, scope in enumerate(self.scopes):
            print(f"Scope Level {i}:")
            for name, sym in scope.items():
                flags = []
                if sym.is_local: flags.append("local")
                if sym.is_param: flags.append("param")
                if sym.is_used: flags.append("used")
                flag_str = f" ({', '.join(flags)})" if flags else ""
                print(f"  {name}: {sym.type} = {sym.value}{flag_str}")
        if self.errors:
            print("\nErrors/Warnings:")
            for error in self.errors:
                print(f"  {error}")
        print("-------------------\n")