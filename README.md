# Car Price Prediction Web App

A production-ready machine learning web application that estimates car prices based on features like company, model, year, and kms driven.

## Features
- **Accurate Predictions**: Uses a Linear Regression model trained on a clean dataset.
- **Production-Ready**: Refactored with standardized logging, robust error handling, and security headers.
- **Configurable**: Managed via environment variables strategy.
- **Containerized**: Ready for deployment with Docker and Docker Compose.
- **Automated Tests**: Includes a suite of units tests to ensure reliability.

## Quick Start (Docker)
1. Ensure you have Docker and Docker Compose installed.
2. Clone the repository.
3. Run `docker-compose up -d`.
4. Access the app at `http://localhost:5000`.

## Local Development
1. Create a virtual environment: `python3 -m venv venv`.
2. Activate it: `source venv/bin/activate`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Create a `.env` file based on `.env.example`.
5. Run the app: `python app.py`.

## Configuration (.env)
- `SECRET_KEY`: Flask secret key for security.
- `MODEL_PATH`: Path to the `.pkl` model file.
- `DATASET_PATH`: Path to the `.csv` dataset.
- `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, ERROR).
- `PORT`: Port to run the application on.

## Running Tests
Run tests using pytest:
```bash
PYTHONPATH=. pytest tests/test_app.py
```

## Production Deployment
The application is configured to run behind Gunicorn for production:
```bash
gunicorn -c gunicorn_config.py app:app
```
