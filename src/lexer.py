# lexer.py

import re

def lexer(source_code, include_lines=False):
    tokens = []
    lineno = 1  # Track line numbers
    keywords = {
        'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
        'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
        'return', 'then', 'true', 'until', 'while'
    }

    token_spec = [
        ('NUMBER',   r'\b\d+(\.\d+)?\b'),
        ('STRING',   r'\".*?\"|\'.*?\''),
        ('BOOLEAN',  r'\btrue\b|\bfalse\b'),
        ('NIL',      r'\bnil\b'),
        ('OP',       r'==|~=|<=|>=|[+\-*/%^#=<>;:.,()]'),
        ('NAME',     r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('SKIP',     r'[ \t\n]+'),
        ('MISMATCH', r'.')
    ]

    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)

    for match in re.finditer(tok_regex, source_code):
        kind = match.lastgroup
        value = match.group()
        
        # Handle newlines for line counting
        if '\n' in value:
            lineno += value.count('\n')
        
        token = {
            'type': kind,
            'value': value,
            'raw': value,
            'lineno': lineno
        }
        
        if kind == 'SKIP':
            continue
        elif kind == 'NAME' and value in keywords:
            token['type'] = 'KEYWORD'
            tokens.append(token)
        elif kind == 'MISMATCH':
            continue
        else:
            tokens.append(token)
    
    return tokens