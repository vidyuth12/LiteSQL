"""
SQL Parser for LiteSQL
Uses Lark to parse SQL statements into an AST for the query executor
"""

import os
from lark import Lark, Transformer, v_args

class SQLTransformer(Transformer):
    def start(self, items):
        return items[0]
    
    def create_statement(self, items):
        table_name = items[0]
        columns = items[1]
        return {
            'type': 'CREATE',
            'table': table_name,
            'columns': columns
        }
    
    def insert_statement(self, items):
        table_name = items[0]
        values = items[1]
        return {
            'type': 'INSERT',
            'table': table_name,
            'values': values
        }
    
    def select_statement(self, items):
        result = {
            'type': 'SELECT',
            'columns': items[0],
            'table': items[1]
        }
        
        # Add where clause if it exists
        if len(items) > 2:
            result['where'] = items[2]
            
        return result
    
    def column_def_list(self, items):
        return items
    
    def column_def(self, items):
        result = {
            'name': items[0],
            'type': items[1]
        }
        
        # Add constraint if specified
        if len(items) > 2:
            result['constraint'] = items[2]
            
        return result
    
    def data_type(self, items):
        return str(items[0]).upper()
    
    def value_list(self, items):
        return items
    
    def value(self, items):
        val = items[0]
        
        # Process value based on type
        if val.type == 'STRING':
            # Remove quotes from string
            return val.value[1:-1]
        elif val.type == 'NUMBER':
            # Convert to int or float
            if '.' in val.value:
                return float(val.value)
            return int(val.value)
        elif val.type == 'NULL':
            return None
        
        return val.value
    
    def select_expr(self, items):
        if items[0] == '*':
            return '*'
        return items[0]
    
    def column_list(self, items):
        return items
    
    def where_clause(self, items):
        return items[0]
    
    def condition(self, items):
        return {
            'column': items[0],
            'operator': items[1],
            'value': items[2]
        }
    
    def comparison_op(self, items):
        return str(items[0])
    
    def table_name(self, items):
        return str(items[0])
    
    def column_name(self, items):
        return str(items[0])
    
    # Handle terminals
    def IDENTIFIER(self, token):
        return token.value
    
    def STRING(self, token):
        return token.value
    
    def NUMBER(self, token):
        return token.value
    
    def NULL(self, token):
        return None


class SQLParser:
    def __init__(self):
        # Get the directory containing this script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        grammar_file = os.path.join(current_dir, 'sql_grammar.lark')
        
        with open(grammar_file, 'r') as f:
            grammar = f.read()
        
        self.parser = Lark(grammar, parser='lalr', transformer=SQLTransformer())
    
    def parse(self, sql_string):
        """Parse an SQL string into an AST for execution"""
        try:
            return self.parser.parse(sql_string)
        except Exception as e:
            raise ValueError(f"SQL parsing error: {str(e)}")


if __name__ == "__main__":
    # Test the parser
    parser = SQLParser()
    
    # Test CREATE TABLE
    create_sql = "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
    print(parser.parse(create_sql))
    
    # Test INSERT
    insert_sql = "INSERT INTO users VALUES (1, 'John Doe', 30)"
    print(parser.parse(insert_sql))
    
    # Test SELECT
    select_sql = "SELECT * FROM users WHERE age > 25"
    print(parser.parse(select_sql))