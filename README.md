# 🏦 ExpenseAnalyzer

**ExpenseAnalyzer** is a Python-based CLI application that allows users to track their expenses from a CSV file. It provides category-based expense reports, budget monitoring, and the ability to export reports in CSV or TXT format.

---

## 📖 Features
✅ **Read expenses from a CSV file**  
✅ **Filter expenses by category**  
✅ **Calculate total expenses by category**  
✅ **Set a monthly budget and get alerts if exceeded**  
✅ **Export reports in CSV or TXT format**  
✅ **Handles missing data and incorrect formats**  

---

## 📌 Requirements
- Python 3.x
- A CSV file containing **expenses with category and amount columns**

---

## 🛠️ Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

---

## 📂 CSV Format Example
```Your CSV file should have at least these columns:
  date,category,amount,description
  2025-03-01,Food,5000,Groceries
  2025-03-02,Transport,2500,Uber ride
  2025-03-03,Entertainment,10000,Movie ticket
  2025-03-04,Food,4500,Restaurant
```
If the required columns ("category" and "amount") are missing, the program will show an error.

---

## 🏆 How to Use
1. **Run the program**
 ```
  python expense_analyzer.py
```
2. **Enter your monthly budget**
The system will compare your expenses against the budget and show alerts if exceeded.

3. **Choose to export the report**
You can save the report in CSV or TXT format.

---





