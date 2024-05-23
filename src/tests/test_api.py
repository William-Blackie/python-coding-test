import unittest

from fastapi.testclient import TestClient

from src.database import DatabaseClient
from src.main import app, get_db_client, get_pdf_service
from src.models import Company
from src.pdf_service import PdfService


class TestApp(unittest.TestCase):
    def setUp(self):
        # Create test instances of the dependencies
        # For simplicity, we are using the same CSV file and API key for testing
        # In a real-world scenario, you would use different test data and API keys and possible a strategy pattern for the Clients to mock them.
        self.test_db_client = DatabaseClient("data/database.csv")
        self.test_pdf_service = PdfService("TEST_KEY")

        # Override the dependencies
        app.dependency_overrides[get_db_client] = lambda: self.test_db_client
        app.dependency_overrides[get_pdf_service] = lambda: self.test_pdf_service
        self.client = TestClient(app)

    def test_health_check(self):
        """
        Sanity check to verify that the API is running.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    def test_compare_success(self):
        """
        Test the compare endpoint with valid data.
        """
        response = self.client.get("/compare?company_name=HealthInc&pdf=healthinc")
        # Add assertions to check the response JSON
        self.assertEqual(response.status_code, 200)
        company_1 = Company(
            self.test_db_client.get_by_company_name(company_name="HealthInc")
        )

        company_2 = Company(
            csv_data=self.test_pdf_service.extract("/home/coderpad/data/healthinc.pdf"),
            data={},
        )
        self.assertDictEqual(response.json(), company_1.compare(company_2))

    def test_compare_invalid_company_name(self):
        """
        Test the compare endpoint with an invalid company name.
        """
        response = self.client.get(
            "/compare?company_name=Invalid Company&pdf=healthinc"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Company Invalid Company not found in the database"},
        )

    def test_compare_invalid_pdf(self):
        """
        Test the compare endpoint with an invalid PDF file.
        """
        response = self.client.get("/compare?company_name=ABC Corp&pdf=invalid_pdf")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "Cannot extract data. Invalid file provided."}
        )


if __name__ == "__main__":
    unittest.main()
