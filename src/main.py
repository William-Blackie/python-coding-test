from typing import Any
from fastapi import FastAPI, HTTPException
from src.pdf_service import PdfService
from src.models import Company
import os
from dotenv import load_dotenv
from src.database import DatabaseClient
from fastapi import Depends

load_dotenv()  # take environment variables from .env. mimicking the environment variables set in a Docker container/EC2/K8s or etc

API_KEY = os.environ["API_KEY"]

# Dependency Injection
def get_db_client() -> DatabaseClient:
    return DatabaseClient('data/database.csv')

def get_pdf_service() -> PdfService:
    return PdfService(API_KEY)

app = FastAPI()

@app.get("/")
def health_check() -> dict[str, str]:
    """
    A simple root endpoint to check if the API is running.
    """
    return {"Hello": "World"}

@app.get("/compare")
def compare(company_name: str, pdf: str, 
    db_client: DatabaseClient = Depends(get_db_client), 
    pdf_service: PdfService = Depends(get_pdf_service)
            ) -> dict[str, dict[str, Any]]:
    """
    A simple endpoint that compares the data extracted from a PDF with the data stored in the database.

    Attributes:
        company_name (str): the name of the company to compare.
        pdf (str): the name of the PDF file to extract data from, not including the file path or extension.
    """
    try:
        # Extract data from the PDF
        pdf_data = pdf_service.extract(file_path=f"/home/coderpad/data/{pdf}.pdf")
        
        # Get the company data from the database
        company_data = db_client.get_by_company_name(company_name=company_name)

        # Initialize Company objects with the extracted data
        current_company = Company(company_data)
        new_company = Company(csv_data=pdf_data)

        # Return a summary of the data, noting which fields did not match
        return current_company.compare(new_company)
    except (FileNotFoundError, ValueError, LookupError) as e:
        raise HTTPException(status_code=400, detail=str(e))