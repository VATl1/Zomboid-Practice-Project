import csv
from typing import List, Dict, Any
from .base_reader import BaseReader

class CSVReader(BaseReader):
   

    def read_file(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            
            sample = csvfile.read(1024)
            csvfile.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=[',', ';', '\t'])
            reader = csv.DictReader(csvfile, dialect=dialect)
            return [row for row in reader]
