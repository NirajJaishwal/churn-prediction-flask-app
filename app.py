# import necessary libraries
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# load the saved model
model = joblib.load('churn_model.pkl')

# Convert categorical variables if needed
mapping_dict = {
    "Contract" : {"Month-to-month": 0, "One year": 1, "Two year": 2},
    "OnlineSecurity" : {"No": 0, "Yes": 2, "No internet service": 1},
    "InternetService" : {"DSL": 0, "Fiber optic": 1, "No": 2},
    "PaymentMethod" : {"Electronic check": 2, "Mailed check": 3, "Bank transfer (automatic)": 0, "Credit card (automatic)": 1},
    "SeniorCitizen" : {"No": 0, "Yes": 1},
    "StreamingMovies" : {"No": 0, "Yes": 2, "No internet service": 1}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [
            request.form.get('Contract', ''),
            request.form.get('OnlineSecurity', ''),
            float(request.form.get('MonthlyCharges', 0)),
            int(request.form.get('tenure', 0)),
            request.form.get('InternetService', ''),
            float(request.form.get('TotalCharges', 0)),
            request.form.get('PaymentMethod', ''),
            request.form.get('SeniorCitizen', ''),
            request.form.get('StreamingMovies', '')
        ]

        print("Raw Form Data:", features)  


        try:
            encoded_features = [
                mapping_dict['Contract'][features[0]],
                mapping_dict['OnlineSecurity'][features[1]],
                features[2],
                features[3],
                mapping_dict['InternetService'][features[4]],
                features[5],
                mapping_dict['PaymentMethod'][features[6]],
                # mapping_dict['SeniorCitizen'][features[7]],
                int(features[7]),
                mapping_dict['StreamingMovies'][features[8]]
            ]
        except KeyError as e:
            return jsonify({"error": f"Invalid input value: {str(e)}"}), 400


        # Convert to numpy array and reshape\
        final_features = np.array(encoded_features).reshape(1, -1)

        # define feature names as per training model
        columns = ['Contract', 'OnlineSecurity', 'MonthlyCharges', 'tenure', 'InternetService', 'TotalCharges', 'PaymentMethod', 'SeniorCitizen', 'StreamingMovies']

        # Create a dataframe
        df = pd.DataFrame([encoded_features], columns=columns)
        # Predict using the model
        prediction = model.predict(df)
        print("Prediction:", prediction)
        result = prediction
        result = 'Churn' if prediction[0] == 'Yes' else 'Not Churn'
        print("Result:", result)

        return render_template('result.html', prediction_text='Customer will {}'.format(result))  

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
