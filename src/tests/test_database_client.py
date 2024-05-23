import unittest
from src.database import DatabaseClient


class TestDatabaseClient(unittest.TestCase):
    def setUp(self):
        # Create a test instance of the DatabaseClient
        # For simplicity, we are using the same CSV file for testing
        # In a real-world scenario, you would use different test data
        # and possible a strategy pattern for the Client to mock with code rather than fixtures.
        self.db_client = DatabaseClient('data/database.csv')
        self.expected_data = {'Company Name': 'HealthInc', 'Industry': 'Healthcare', 'Market Capitalization': '3000', 'Revenue (in millions)': '1000', 'EBITDA (in millions)': '250', 'Net Income (in millions)': '80', 'Debt (in millions)': '150', 'Equity (in millions)': '600', 'Enterprise Value (in millions)': '3150', 'P/E Ratio': '15', 'Revenue Growth Rate (%)': '12', 'EBITDA Margin (%)': '25', 'Net Income Margin (%)': '8', 'ROE (Return on Equity) (%)': '13.33', 'ROA (Return on Assets) (%)': '10', 'Current Ratio': '2', 'Debt to Equity Ratio': '0.25', 'Location': 'New York'}

    def test_get_by_company_name_existing(self):
        """
        Test getting data for an existing company.
        """
        company_name = "HealthInc"

        result = self.db_client.get_by_company_name(company_name)
        self.assertEqual(result, self.expected_data)

    def test_get_by_company_name_non_existing(self):
        """
        Test getting data for a non-existing company.
        """
        with self.assertRaises(LookupError):
            self.db_client.get_by_company_name("invalid")
    
    def test_get_by_company_name_case_insensitive(self):
        """
        Test getting data for a company with case-insensitive search.
        """
        result = self.db_client.get_by_company_name("healthinc")
        self.assertEqual(result, self.expected_data)

if __name__ == "__main__":
    unittest.main()