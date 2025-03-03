import csv 
from typing import List, Optional

class CSVProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_csv(self, filter_column: Optional[int] = None,
                filter_value: Optional[str] = None) -> List[list]:
        """Lee el CSV y opcionalmente filtra por columna y valor."""

        results = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                print(f"Columnas {headers}")

                for row in reader:
                    if filter_column is not None and filter_value is not None:
                        if row[filter_column] == filter_value:
                            results.append(row)
                    else:
                        results.append(row)                 
                return results
            
        except Exception as e:
            print(f"Error: {e}")
            return []
                
if __name__ == "__main__":
    processor =  CSVProcessor('file.csv')
    # Read all
    all_rows = processor.read_csv()
    for row in all_rows:
        print(row)
               