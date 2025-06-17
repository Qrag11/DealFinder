from abc import ABC, abstractmethod
from typing import List,Dict

class BazowyScraper(ABC):
    @abstractmethod
    def szukaj(self, query: str, kategoria: str) -> List[Dict]:
        """
               Szuka ofert na stronie, zwraca listę słowników z kluczami:
               'title', 'price', 'url', 'timestamp', 'site'
               """
        pass