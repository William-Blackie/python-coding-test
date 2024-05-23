from typing import Any
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
    current_ratio: float = Field(default=0, title="Current Ratio") # Not included in one of the CSV rows
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
                data[model_key] = csv_data.get(csv_key)
        except AttributeError as e:
            raise ValueError(f"Error loading CSV data: {e}")
        return data
    
    def compare_csv_data(self, other: BaseModel) -> dict:
        """
        Compare two Company instances and return a dictionary of differences.
        """
        self_dict = self.model_dump()
        other_dict = other.model_dump()

        diff_dict = {}

        for key in set(self_dict.keys()) | set(other_dict.keys()):
            self_value = self_dict.get(key)
            other_value = other_dict.get(key)

            if isinstance(self_value, (int, float)) and isinstance(other_value, (int, float)):
                diff_dict[key] = self_value - other_value
            elif self_value != other_value:
                diff_dict[key] = (self_value, other_value)

        return diff_dict