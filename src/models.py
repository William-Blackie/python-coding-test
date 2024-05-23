from typing import Any, Dict
from pydantic import BaseModel, Field
from src.constants import CSV_TO_COMPANY_FIELD_MAPPING

class Company(BaseModel):
    """
    A Pydantic model that represents the data of a company.
    """
    company_name: str
    industry: str
    market_capitalization: int
    revenue_millions: int
    ebitda_millions: int
    net_income_millions: int
    debt_millions: int
    equity_millions: int
    enterprise_value_millions: int
    pe_ratio: int
    revenue_growth_rate_percent: int
    ebitda_margin_percent: float
    roe_percent: float
    roa_percent: float
    current_ratio: float = Field(default=0.0, title="Current Ratio") # Not included in one of the CSV rows
    debt_to_equity_ratio: float
    location: str
    ceo: str = Field(default="Unknown", title="CEO") # Not included in all of the CSV rows
    number_of_employees: int = Field(default=0, title="Number of Employees") # Not included in all of the CSV rows
    
    def __init__(self, csv_data: dict[str, Any] = None, **data: Any) -> None:
        """
        Initialize the Company model with the provided data.

        Attributes:
            csv_data (dict): a dictionary of CSV data.
            data (Any): keyword arguments of the Company model fields.
        """
    
        if csv_data:
            data = self._parse_csv_data(csv_data)
        super().__init__(**data)

    def __str__(self) -> str:
        return self.company_name
    
    def _parse_csv_data(self, csv_data: dict[str, Any]) -> ValueError|dict[str, Any]:
        """
        parse data from a CSV row into the dict.
        The CSV data does not contain all the fields, so we need to map the CSV data to the model fields.

        Attributes:
            csv_data (dict): a dictionary of CSV data.
        """
    
        data = {}
        try:
            for csv_key, model_key in CSV_TO_COMPANY_FIELD_MAPPING.items():
                if csv_key not in csv_data:
                    # Skip fields that are not present in the CSV data
                    # Let the model handle the default values
                    continue
                data[model_key] = csv_data.get(csv_key)
        except ValueError as e:
            raise ValueError(f"Error loading CSV data: {e}")
        return data
    
    def compare(self, other: 'Company') -> Dict[str, dict[str, Any]]:

        if not isinstance(other, Company):
            raise TypeError("Can only compare with another Company instance")
        
        differences = {}
        for field in self.model_fields:
            try: 
                self_value = getattr(self, field)
                other_value = getattr(other, field)
                differences[field] = {"Current": self_value, "New": other_value, "Match": self_value == other_value}  
            except AttributeError as e:
                print(f"Attribute {field} not found in the model fields: {e}")
                continue      
        return differences