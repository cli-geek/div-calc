import csv
from models import set_cursor

HEADER_KEYWORDS = ['date', 'account', 'accrued', 'category']

class fidelityCSV:
    def __init__(self):
        self.data = []

    def read_csv(filepath='uploads/2025_q3_dividendhistory.csv'):
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)

            c = set_cursor()

            for row in reader:
                if any(any(keyword in str(cell).lower() for keyword in HEADER_KEYWORDS) for cell in row if cell):
                    #print(f"Skipping header row: {row}")
                    continue

                if len(row) > 1: #and (float(row[-3]) > 0):
                    c.execute('''INSERT INTO data (
                            run_date,
                            account,
                            ticker,
                            name,
                            amount) VALUES (?, ?, ?, ?, ?)
                    ''', (row[0], row[1], row[4], row[5], row[-2]))
                    print(row[0], row[1], row[4], row[5], row[-2])

        return
    
if __name__ == '__main__':
    fidelityCSV.read_csv()