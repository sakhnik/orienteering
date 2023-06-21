import csv
import sys


class CsvStorage:
    def __init__(self, fname: str):
        try:
            if not fname:
                print("WARNING: using ranks.csv from current directory",
                      file=sys.stderr)
                fname = "ranks.csv"
            with open(fname, 'r') as file:
                reader = csv.reader(file)
                self.ranks = {row[0]: row[1] for row in reader}
        except Exception:
            print("WARNING: Can't read initial ranks from a CSV file",
                  file=sys.stderr)
            self.ranks = {}

    def get_ranking(self, name: str) -> str:
        return self.ranks.get(name, "")
