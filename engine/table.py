"""
Table and Column classes for LiteSQL
Represents database tables and their structure
"""

class Column:
    def __init__(self, name, data_type, constraints=None):
        self.name = name
        self.data_type = data_type
        self.constraints = constraints or []
        
        # Validate data type
        valid_types = ['INTEGER', 'INT', 'TEXT', 'VARCHAR', 'FLOAT', 'DOUBLE']
        if self.data_type not in valid_types:
            raise ValueError(f"Invalid data type: {self.data_type}")
    
    def validate_value(self, value):
        """Validate a value against this column's type and constraints"""
        # Check for NULL constraint
        if value is None and 'NOT NULL' in self.constraints:
            return False
        
        # Type checking
        if value is not None:
            if self.data_type in ['INTEGER', 'INT']:
                if not isinstance(value, int):
                    return False
            elif self.data_type in ['FLOAT', 'DOUBLE']:
                if not isinstance(value, (int, float)):
                    return False
            elif self.data_type in ['TEXT', 'VARCHAR']:
                if not isinstance(value, str):
                    return False
        
        return True
    
    def __repr__(self):
        constraints_str = f" {self.constraints}" if self.constraints else ""
        return f"Column(name='{self.name}', type='{self.data_type}'{constraints_str})"


class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []
        self.next_row_id = 0
        
        # Check for primary key
        self.pk_column = None
        for i, col in enumerate(columns):
            if col.constraints and 'PRIMARY KEY' in col.constraints:
                self.pk_column = i
                break
    
    def insert_row(self, values):
        """Insert a row into the table"""
        if len(values) != len(self.columns):
            raise ValueError(f"Expected {len(self.columns)} values, got {len(values)}")
        
        # Validate values against column types
        for i, (value, column) in enumerate(zip(values, self.columns)):
            if not column.validate_value(value):
                raise ValueError(f"Invalid value for column '{column.name}': {value}")
        
        # Check primary key constraint
        if self.pk_column is not None:
            pk_value = values[self.pk_column]
            for row in self.rows:
                if row[self.pk_column] == pk_value:
                    raise ValueError(f"Primary key violation: {pk_value} already exists")
        
        # Add row
        self.rows.append(values)
        row_id = self.next_row_id
        self.next_row_id += 1
        
        return row_id
    
    def get_column_index(self, column_name):
        """Get the index of a column by name"""
        for i, col in enumerate(self.columns):
            if col.name == column_name:
                return i
        return None
    
    def __repr__(self):
        return f"Table(name='{self.name}', columns={len(self.columns)}, rows={len(self.rows)})"