import csv
from typing import List, Dict


class DatabaseClient:
    """
    A quick database client that loads a CSV file into a list.
    Mimics a database client that could be used in a production environment.
    """
    def __init__(self, csv_file: str) -> None:
        """
        Initialize the database client with the path to the CSV file.
        
        Attributes:
            csv_file (str): the path to the CSV file.
        """
        self.data: List[Dict[str, str]] = []
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append(row)
        return None
    
    def get_by_company_name(self, company_name: str) -> dict[str, str]|LookupError:
        """
        Get a company's data by its name.

        Attributes:
            company_name (str): the name of a company to search.
        """
        for row in self.data:
            if row['Company Name'].lower() == company_name.lower():
                return row
        raise LookupError(f"Company {company_name} not found in the database")