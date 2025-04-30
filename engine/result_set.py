"""
ResultSet class for LiteSQL
Formats and returns query results
"""

class ResultSet:
    def __init__(self, column_names, rows):
        self.column_names = column_names
        self.rows = rows
    
    def __str__(self):
        """Format result set as a string table for display"""
        if not self.rows:
            return f"Empty result set ({len(self.column_names)} columns)"
        
        # Get column widths
        col_widths = [len(str(col)) for col in self.column_names]
        for row in self.rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Build header
        header = " | ".join(f"{col:{width}s}" for col, width in zip(self.column_names, col_widths))
        separator = "-+-".join("-" * width for width in col_widths)
        
        # Build rows
        result_rows = []
        for row in self.rows:
            formatted_row = " | ".join(f"{str(cell):{width}s}" for cell, width in zip(row, col_widths))
            result_rows.append(formatted_row)
        
        # Combine everything
        result = f"{header}\n{separator}\n" + "\n".join(result_rows)
        result += f"\n({len(self.rows)} rows)"
        
        return result
    
    def __repr__(self):
        return f"ResultSet(columns={self.column_names}, rows={len(self.rows)})"