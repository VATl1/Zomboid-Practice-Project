import json
from typing import List, Dict, Any
from .base_reader import BaseReader

class JSONReader(BaseReader):
   

    def read_file(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)

       
        if isinstance(data, dict):
            data = [data]
        return data
