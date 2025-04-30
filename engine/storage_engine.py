"""
Storage Engine for LiteSQL
Manages in-memory tables and data storage
"""

class StorageEngine:
    def __init__(self):
        self.tables = {}  # Dictionary of table_name -> Table objects
    
    def create_table(self, table):
        """Add a new table to the database"""
        if table.name in self.tables:
            raise ValueError(f"Table '{table.name}' already exists")
        
        self.tables[table.name] = table
        return True
    
    def drop_table(self, table_name):
        """Remove a table from the database"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        del self.tables[table_name]
        return True
    
    def get_table(self, table_name):
        """Get a table by name"""
        return self.tables.get(table_name)
    
    def get_tables(self):
        """Get a list of all tables"""
        return list(self.tables.values())
    
    def table_exists(self, table_name):
        """Check if a table exists"""
        return table_name in self.tables