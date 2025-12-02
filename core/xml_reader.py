import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from .base_reader import BaseReader

class XMLReader(BaseReader):
   

    def read_file(self, file_path: str) -> List[Dict[str, Any]]:
        tree = ET.parse(file_path)
        root = tree.getroot()

        items = []
        for item in root.findall("item"):
            record = {child.tag: child.text for child in item}
            items.append(record)
        return items
