import csv

class CSV:
    def __init__(self):
        self.data = []

    def read_csv(filepath='uploads/2025_q3_dividendhistory.csv'):
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)
        return
    
if __name__ == '__main__':
    CSV.read_csv()