"""
Query Executor for LiteSQL
Executes parsed SQL AST against the in-memory database
"""

from engine.storage_engine import StorageEngine
from engine.table import Table, Column
from engine.result_set import ResultSet

class QueryExecutor:
    def __init__(self):
        self.storage = StorageEngine()
    
    def execute(self, ast):
        """Execute a query AST and return results"""
        if ast['type'] == 'CREATE':
            return self._execute_create(ast)
        elif ast['type'] == 'INSERT':
            return self._execute_insert(ast)
        elif ast['type'] == 'SELECT':
            return self._execute_select(ast)
        else:
            raise ValueError(f"Unsupported query type: {ast['type']}")
    
    def _execute_create(self, ast):
        """Execute CREATE TABLE statement"""
        table_name = ast['table']
        columns = []
        
        for col_def in ast['columns']:
            column = Column(
                name=col_def['name'],
                data_type=col_def['type'],
                constraints=col_def.get('constraint')
            )
            columns.append(column)
        
        table = Table(table_name, columns)
        self.storage.create_table(table)
        
        return f"Table '{table_name}' created with {len(columns)} columns"
    
    def _execute_insert(self, ast):
        """Execute INSERT statement"""
        table_name = ast['table']
        values = ast['values']
        
        # Get table
        table = self.storage.get_table(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        # Check if values match column count
        if len(values) != len(table.columns):
            raise ValueError(f"Value count ({len(values)}) doesn't match column count ({len(table.columns)})")
        
        # Insert row
        row_id = table.insert_row(values)
        
        return f"Inserted 1 row into '{table_name}' (ID: {row_id})"
    
    def _execute_select(self, ast):
        """Execute SELECT statement"""
        table_name = ast['table']
        columns = ast['columns']
        where_clause = ast.get('where')
        
        # Get table
        table = self.storage.get_table(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        # Get column indices to return
        if columns == '*':
            column_indices = list(range(len(table.columns)))
            column_names = [col.name for col in table.columns]
        else:
            column_indices = []
            column_names = []
            for col_name in columns:
                for i, col in enumerate(table.columns):
                    if col.name == col_name:
                        column_indices.append(i)
                        column_names.append(col_name)
                        break
                else:
                    raise ValueError(f"Column '{col_name}' not found in table '{table_name}'")
        
        # Filter rows based on where clause
        rows = []
        for row in table.rows:
            if where_clause:
                # Simple where clause evaluation
                where_col = where_clause['column']
                where_op = where_clause['operator']
                where_val = where_clause['value']
                
                col_idx = None
                for i, col in enumerate(table.columns):
                    if col.name == where_col:
                        col_idx = i
                        break
                
                if col_idx is None:
                    raise ValueError(f"WHERE column '{where_col}' not found")
                
                row_val = row[col_idx]
                
                # Evaluate condition
                if where_op == '=' and row_val == where_val:
                    rows.append([row[i] for i in column_indices])
                elif where_op == '!=' and row_val != where_val:
                    rows.append([row[i] for i in column_indices])
                elif where_op == '>' and row_val > where_val:
                    rows.append([row[i] for i in column_indices])
                elif where_op == '<' and row_val < where_val:
                    rows.append([row[i] for i in column_indices])
                elif where_op == '>=' and row_val >= where_val:
                    rows.append([row[i] for i in column_indices])
                elif where_op == '<=' and row_val <= where_val:
                    rows.append([row[i] for i in column_indices])
            else:
                # No where clause, return all rows
                rows.append([row[i] for i in column_indices])
        
        # Create result set
        result = ResultSet(column_names, rows)
        return result