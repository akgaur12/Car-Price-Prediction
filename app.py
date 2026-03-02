import os
import pickle
import pandas as pd
import numpy as np
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from flask_talisman import Talisman
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, model_path, dataset_path):
        self.model_path = model_path
        self.dataset_path = dataset_path
        self.model = None
        self.car_data = None
        self._load_resources()

    def _load_resources(self):
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info("Model loaded successfully.")
            else:
                logger.error(f"Model file not found at {self.model_path}")

            if os.path.exists(self.dataset_path):
                self.car_data = pd.read_csv(self.dataset_path)
                logger.info("Dataset loaded successfully.")
            else:
                logger.error(f"Dataset file not found at {self.dataset_path}")
        except Exception as e:
            logger.exception("Error loading model or dataset")

    def get_form_data(self):
        if self.car_data is None:
            return [], [], [], []
        
        companies = sorted(self.car_data['company'].unique().tolist())
        car_models = sorted(self.car_data['name'].unique().tolist())
        years = sorted(self.car_data['year'].unique().tolist(), reverse=True)
        fuel_types = self.car_data['fuel_type'].unique().tolist()
        
        return companies, car_models, years, fuel_types

    def predict(self, company, car_model, year, kms_driven, fuel_type):
        if self.model is None:
            raise ValueError("Model not loaded")
        
        try:
            input_df = pd.DataFrame(
                columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                data=np.array([car_model, company, year, kms_driven, fuel_type]).reshape(1, 5)
            )
            prediction = self.model.predict(input_df)
            return np.round(prediction[0], 2)
        except Exception as e:
            logger.exception("Prediction failed")
            raise

app = Flask(__name__)
# Security Headers
Talisman(app, content_security_policy=None) # CSP can be restrictive, disabling for now unless explicitly needed
CORS(app)

model_manager = ModelManager(
    os.getenv('MODEL_PATH', 'LinearRegressionModel.pkl'),
    os.getenv('DATASET_PATH', 'Cars_Clean_Dataset.csv')
)

@app.route('/', methods=['GET'])
def index():
    try:
        companies, car_models, years, fuel_types = model_manager.get_form_data()
        companies.insert(0, 'Select Company')
        return render_template(
            'index.html',
            companies=companies,
            car_models=car_models,
            years=years,
            fuel_types=fuel_types
        )
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return "An internal error occurred.", 500

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        data = request.form
        company = data.get('company')
        car_model = data.get('model')
        year = data.get('year')
        fuel_type = data.get('fuel_type')
        kms_driven = data.get('kms')

        # Basic validation
        if not all([company, car_model, year, fuel_type, kms_driven]):
            return "Missing input data", 400

        prediction = model_manager.predict(company, car_model, year, kms_driven, fuel_type)
        logger.info(f"Prediction made for {car_model}: {prediction}")
        return str(prediction)

    except ValueError as ve:
        return str(ve), 503
    except Exception as e:
        logger.exception("Error during prediction")
        return "Internal Server Error", 500

@app.errorhandler(404)
def not_found(e):
    return "Page not found", 404

@app.errorhandler(500)
def server_error(e):
    return "Internal server error", 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )