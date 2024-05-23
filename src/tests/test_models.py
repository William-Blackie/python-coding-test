import unittest
from csv import DictReader

from src.models import Company


class TestCompany(unittest.TestCase):
    """
    A class to test the Company model.
    """

    def setUp(self):
        """
        Set up the test data.
        """
        self.company_data = {
            "company_name": "ABC Corp",
            "industry": "Technology",
            "market_capitalization": 1000,
            "revenue_millions": 500,
            "ebitda_millions": 200,
            "net_income_millions": 100,
            "debt_millions": 300,
            "equity_millions": 700,
            "enterprise_value_millions": 1200,
            "pe_ratio": 10,
            "revenue_growth_rate_percent": 5,
            "ebitda_margin_percent": 40.0,
            "roe_percent": 15.0,
            "roa_percent": 10.0,
            "current_ratio": 2,
            "debt_to_equity_ratio": 0.43,
            "location": "New York",
            "ceo": "John Doe",
            "number_of_employees": 1000,
        }
        csv_data = "Company Name,Industry,Market Capitalization,Revenue (in millions),EBITDA (in millions),Net Income (in millions),Debt (in millions),Equity (in millions),Enterprise Value (in millions),P/E Ratio,Revenue Growth Rate (%),EBITDA Margin (%),Net Income Margin (%),ROE (Return on Equity) (%),ROA (Return on Assets) (%),Current Ratio,Debt to Equity Ratio,Location\nTechCorp,Technology,5000,1500,300,100,200,800,5400,25,10,20,6.67,12.5,7.5,2.5,0.25,San Francisco"
        self.parsed_csv_data = DictReader(
            csv_data.splitlines()
        ).__next__()  # Parse the CSV data into a dictionary

    def test_init(self):
        """
        Test initializing a Company object with the provided data.
        """
        company = Company(**self.company_data)  # Initialize a Company object with
        self.assertEqual(company.company_name, "ABC Corp")
        self.assertEqual(company.industry, "Technology")
        self.assertEqual(company.market_capitalization, 1000)
        self.assertEqual(company.revenue_millions, 500)
        self.assertEqual(company.ebitda_millions, 200)
        self.assertEqual(company.net_income_millions, 100)
        self.assertEqual(company.debt_millions, 300)
        self.assertEqual(company.equity_millions, 700)
        self.assertEqual(company.enterprise_value_millions, 1200)
        self.assertEqual(company.pe_ratio, 10)
        self.assertEqual(company.revenue_growth_rate_percent, 5)
        self.assertEqual(company.ebitda_margin_percent, 40.0)
        self.assertEqual(company.roe_percent, 15.0)
        self.assertEqual(company.roa_percent, 10.0)
        self.assertEqual(company.current_ratio, 2)
        self.assertEqual(company.debt_to_equity_ratio, 0.43)
        self.assertEqual(company.location, "New York")
        self.assertEqual(company.ceo, "John Doe")
        self.assertEqual(company.number_of_employees, 1000)

    def test_init_with_missing_fields(self):
        """
        Test initializing a Company object with missing fields.
        """
        self.company_data.pop("ceo")
        self.company_data.pop("number_of_employees")
        company = Company(**self.company_data)
        self.assertEqual(company.ceo, "Unknown")
        self.assertEqual(company.number_of_employees, 0)

    def test_init_with_required_missing_fields(self):
        """
        Test initializing a Company object with missing required fields.
        """
        self.company_data.pop("company_name")
        with self.assertRaises(ValueError):
            Company(**self.company_data)

    def test_init_with_extra_fields(self):
        """
        Test initializing a Company object with extra fields.
        """
        self.company_data["extra_field"] = "Extra"
        company = Company(**self.company_data)
        self.assertFalse(hasattr(company, "extra_field"))

    def test_init_with_csv_data(self):
        """
        Test initializing a Company object with CSV data.
        CSV data does not contain all the fields, so we need to map the CSV data to the model fields.
        """

        company = Company(csv_data=self.parsed_csv_data)

        self.assertEqual(company.company_name, "TechCorp")
        self.assertEqual(company.industry, "Technology")
        self.assertEqual(company.market_capitalization, 5000)
        self.assertEqual(company.revenue_millions, 1500)
        self.assertEqual(company.ebitda_millions, 300)
        self.assertEqual(company.net_income_millions, 100)
        self.assertEqual(company.debt_millions, 200)
        self.assertEqual(company.equity_millions, 800)
        self.assertEqual(company.enterprise_value_millions, 5400)
        self.assertEqual(company.pe_ratio, 25)
        self.assertEqual(company.revenue_growth_rate_percent, 10)
        self.assertEqual(company.ebitda_margin_percent, 20.0)
        self.assertEqual(company.roe_percent, 12.5)
        self.assertEqual(company.roa_percent, 7.5)
        self.assertEqual(company.current_ratio, 2.5)
        self.assertEqual(company.debt_to_equity_ratio, 0.25)
        self.assertEqual(company.location, "San Francisco")

        # Default values as not supplied in the CSV data
        self.assertEqual(company.ceo, "Unknown")
        self.assertEqual(company.number_of_employees, 0)

    def test_str(self):
        """
        Test the string representation of a Company object.
        """
        company = Company(**self.company_data)
        self.assertEqual(str(company), "ABC Corp")

    def test_compare_same_companies(self):
        company_one = Company(**self.company_data)
        company_two = Company(**self.company_data)

        comparison = company_one.compare(company_two)

        # Check that all fields match
        for key in self.company_data:
            self.assertEqual(
                comparison[key],
                {
                    "Current": self.company_data[key],
                    "New": self.company_data[key],
                    "Match": True,
                },
            )

    def test_compare_different_companies(self):
        """
        Test comparing two different Company objects.
        """
        company_one = Company(**self.company_data)
        self.company_data["debt_millions"] = 500
        self.company_data["equity_millions"] = 900
        company_two = Company(**self.company_data)

        comparison = company_one.compare(company_two)
        # Check that the debt and equity fields do not match
        self.assertEqual(
            comparison["debt_millions"], {"Current": 300, "New": 500, "Match": False}
        )
        self.assertEqual(
            comparison["equity_millions"], {"Current": 700, "New": 900, "Match": False}
        )

        # Remove the debt and equity fields from the comparison
        comparison.pop("debt_millions")
        comparison.pop("equity_millions")

        # Check that the rest of the fields match
        for key in comparison:
            self.assertEqual(
                comparison[key],
                {
                    "Current": self.company_data[key],
                    "New": self.company_data[key],
                    "Match": True,
                },
            )


if __name__ == "__main__":
    unittest.main()
