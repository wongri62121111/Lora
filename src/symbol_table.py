# symboltable.py - Standalone symbol table implementation

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scope_stack = [{}]  # Start with global scope

    def enter_scope(self):
        """Push a new scope onto the stack"""
        self.scope_stack.append({})

    def exit_scope(self):
        """Pop the current scope from the stack"""
        if len(self.scope_stack) > 1:  # Don't pop global scope
            self.scope_stack.pop()

    def current_scope(self):
        """Get the current scope dictionary"""
        return self.scope_stack[-1]

    def declare(self, name, var_type, value=None):
        """Declare a new variable in current scope"""
        if name in self.current_scope():
            raise NameError(f"Variable '{name}' already exists in this scope")
        
        self.current_scope()[name] = {
            'type': var_type,
            'value': value
        }
        return self.current_scope()[name]

    def lookup(self, name):
        """Find a variable in any scope (current to global)"""
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable '{name}' not found")

    def update(self, name, value):
        """Update a variable's value with type checking"""
        var_info = self.lookup(name)  # Will raise if not found
        
        # Simple type checking
        expected_type = var_info['type']
        if expected_type == 'number' and not isinstance(value, (int, float)):
            raise TypeError(f"Expected number for '{name}', got {type(value)}")
        elif expected_type == 'string' and not isinstance(value, str):
            raise TypeError(f"Expected string for '{name}', got {type(value)}")
        elif expected_type == 'boolean' and not isinstance(value, bool):
            raise TypeError(f"Expected boolean for '{name}', got {type(value)}")
        
        var_info['value'] = value
        return var_info

    def print_state(self):
        """Print the current state of all variables"""
        print("\nSymbol Table State:")
        print("-------------------")
        for i, scope in enumerate(self.scope_stack):
            print(f"Scope Level {i}:")
            for name, var_info in scope.items():
                print(f"  {name}: {var_info['type']} = {var_info['value']}")
        print("-------------------\n")


# Example usage as a standalone program
if __name__ == "__main__":
    st = SymbolTable()
    
    # Declare some variables in global scope
    st.declare("x", "number", 10)
    st.declare("name", "string", "Alice")
    st.declare("active", "boolean", True)
    
    print("Initial state:")
    st.print_state()
    
    # Enter a new scope
    st.enter_scope()
    st.declare("y", "number", 5)
    print("\nAfter entering new scope and declaring 'y':")
    st.print_state()
    
    # Update variables
    st.update("x", 20)
    st.update("name", "Bob")
    print("\nAfter updating variables:")
    st.print_state()
    
    # Exit scope
    st.exit_scope()
    print("\nAfter exiting scope:")
    st.print_state()
    
    # Try to update with wrong type (will raise TypeError)
    try:
        st.update("x", "not a number")
    except TypeError as e:
        print(f"\nType check working: {e}")