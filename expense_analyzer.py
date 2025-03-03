import csv
from pathlib import Path
from typing import List, Dict, Optional

class ExpenseAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = []  # Almacenar los datos leídos para reutilizarlos

    def read_data(self, filter_column: Optional[str] = None, 
                  filter_value: Optional[str] = None) -> List[dict]:
        """Lee el CSV y opcionalmente filtra por columna y valor."""
        results = []
        try:
            if not Path(self.file_path).is_file():
                raise FileNotFoundError(f"El archivo {self.file_path} no existe")

            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                print(f"Columnas: {reader.fieldnames}")

                for row in reader:
                    # Limpiar y convertir monto a float
                    monto = row.get('monto', '0').strip().replace(',', '.')
                    try:
                        row['monto'] = float(monto)
                    except ValueError as e:
                        print(f"Advertencia: No se pudo convertir el monto '{monto}' a número en la fila {row}. Error: {e}. Se usará 0.")
                        row['monto'] = 0

                    # Filtrar si se especifica una columna y valor
                    if filter_column is not None and filter_value is not None:
                        if row.get(filter_column, '') == filter_value:
                            results.append(row)
                    else:
                        results.append(row)

            self.data = results  # Almacenar los datos para reutilizarlos
            return results

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return []
        except Exception as e:
            print(f"Error inesperado: {e}")
            return []
        
    def total_by_category(self) -> Dict[str, float]:
        """Calcula el total de gastos por categoría."""
        categories = {}
        if not self.data:  # Asegurarse de que los datos estén cargados
            self.read_data()

        for row in self.data:
            categoria = row.get('categoría', '')
            monto = row['monto']  # Ya está convertido a float

            if categoria not in categories:
                categories[categoria] = 0
            categories[categoria] += monto

        return categories
    
    def print_expense_report(self):
        """Imprime un reporte en consola con el total de gastos por categoría."""
        totals = self.total_by_category()
        total_general = sum(totals.values())

        print("\n========== REPORTE DE GASTOS ==========")
        for category, amount in totals.items():
            print(f"{category:<20} | ₡{amount:,.2f}")
        
        print("---------------------------------------")
        print(f"{'TOTAL GENERAL':<20} | ₡{total_general:,.2f}")
        print("=======================================\n")

        

if __name__ == "__main__":
    analyzer = ExpenseAnalyzer('file.csv')
   
    analyzer.print_expense_report()