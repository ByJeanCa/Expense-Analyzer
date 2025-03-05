import csv
from pathlib import Path
from typing import List, Dict, Optional

class ExpenseAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = []  # Almacenar los datos leídos para reutilizarlos
        self.required_columns = {"categoría", "monto"}  # ✅ Define las columnas requeridas

    def read_data(self, filter_column: Optional[str] = None, 
                  filter_value: Optional[str] = None) -> List[dict]:
        """Lee el CSV y opcionalmente filtra por columna y valor."""
        results = []
        try:
            if not Path(self.file_path).is_file():
                raise FileNotFoundError(f"El archivo {self.file_path} no existe")

            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                missing_columns = self.required_columns - set(reader.fieldnames or [])
                if missing_columns:
                    raise ValueError(f"Error: Missing required columns: {', '.join(missing_columns)}")

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
        """Imprime un reporte en consola con el total de gastos por categoría y porcentajes."""
        totals = self.total_by_category()
        percentages = self.category_percentages()
        total_general = sum(totals.values())

        print("\n========== REPORTE DE GASTOS ==========")
        for category, amount in totals.items():
            percentage = percentages.get(category, 0)
            print(f"{category:<20} | ₡{amount:,.2f} | {percentage:.2f}%")
     
        print("---------------------------------------")
        print(f"{'TOTAL GENERAL':<20} | ₡{total_general:,.2f} | 100.00%")
        print("=======================================\n")

        return total_general


    def set_monthly_budget(self, budget: float):
        """Sets a monthly budget and alerts if expenses exceed it."""
        total_expenses = self.print_expense_report()
        
        print(f"\nYour monthly budget: ₡{budget:,.2f}")
        print(f"Total expenses: ₡{total_expenses:,.2f}")

        if total_expenses >= budget:
            print("\n⚠️ ALERT: Your expenses have exceeded the budget! ⚠️\n")
        else:
            print("\n✅ You are within your budget. Good job!\n")

        return total_expenses, budget  # Returns values for further use

    def export_report(self, file_name: Optional[str] = None, file_format: str = "csv"):
        """Exports the report to a CSV or TXT file."""
        totals = self.total_by_category()
        total_expenses = sum(totals.values())

        # Set default filename
        if not file_name:
            file_name = f"expense_report.{file_format}"

        try:
            if file_format == "csv":
                with open(file_name, "w", encoding="utf-8", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Category", "Amount"])
                    for category, amount in totals.items():
                        writer.writerow([category, f"₡{amount:,.2f}"])
                    writer.writerow(["TOTAL EXPENSES", f"₡{total_expenses:,.2f}"])
                print(f"✅ Report successfully saved as '{file_name}' (CSV format).")

            elif file_format == "txt":
                with open(file_name, "w", encoding="utf-8") as file:
                    file.write("========== EXPENSE REPORT ==========\n")
                    for category, amount in totals.items():
                        file.write(f"{category:<20} | ₡{amount:,.2f}\n")
                    file.write("---------------------------------------\n")
                    file.write(f"{'TOTAL EXPENSES':<20} | ₡{total_expenses:,.2f}\n")
                    file.write("=======================================\n")
                print(f"✅ Report successfully saved as '{file_name}' (TXT format).")

            else:
                print("❌ Error: Unsupported format. Use 'csv' or 'txt'.")

        except Exception as e:
            print(f"❌ Error saving file: {e}")

    def category_percentages(self) -> Dict[str, float]:
        """Calcula el porcentaje de gastos por categoría respecto al total."""
        totals = self.total_by_category()
        total_expenses = sum(totals.values())
     
        if total_expenses == 0:  # Evitar división por cero
            return {category: 0.0 for category in totals}
     
        return {category: (amount / total_expenses) * 100 for category, amount in totals.items()}


if __name__ == "__main__":

    analyzer = ExpenseAnalyzer('expenses_sample.csv')#Name/path of the csv file

    user_budget = float(input("Enter your monthly budget: "))
    analyzer.set_monthly_budget(user_budget)

    # Ask user for export format
    format_choice = input("Do you want to export the report? (csv/txt/no): ").strip().lower()
    if format_choice in ["csv", "txt"]:
        analyzer.export_report(file_format=format_choice)