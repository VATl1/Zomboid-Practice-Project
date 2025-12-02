import os
from .csv_reader import CSVReader
from .json_reader import JSONReader
from .xml_reader import XMLReader

def get_reader(file_path: str):
  
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        return CSVReader()
    elif ext == ".json":
        return JSONReader()
    elif ext == ".xml":
        return XMLReader()
    else:
        raise ValueError(f"Unknown file format: {ext}")
