from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseReader(ABC):
  

    @abstractmethod
    def read_file(self, file_path: str) -> List[Dict[str, Any]]:
        
        pass
