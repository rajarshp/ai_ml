#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, make_response, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from flask_cors import CORS, cross_origin


# In[2]:


app = Flask(__name__)
CORS(app)
# Load the pre-trained models and encoder
with open('.venv/models/base_model.pkl', 'rb') as f:
    base_model = pickle.load(f)

with open('.venv/models/min_price_model.pkl', 'rb') as f:
    lower_model = pickle.load(f)

with open('.venv/models/max_price_model.pkl', 'rb') as f:
    upper_model = pickle.load(f)


# In[3]:


# read json response to create the data

def process_data_from_json(data):

    try:
        # Initialize lists to store extracted data
        product_id = data[0]['title']

        # Initialize an empty list to store the competitor prices
        competitor_prices = []
        
        # Iterate through the JSON data to collect competitor prices (limit to the first 5 records with price > 0)
        for record in data:
            price = float(record['price'].replace('$',''))
            if price > 0:
                competitor_prices.append(price)
            if len(competitor_prices) == 5:
                break
        
        # Create dynamic column names for competitors (comp1, comp2, ...)
        competitor_columns = [f"comp{i+1}" for i in range(len(competitor_prices))]
        
        # Create DataFrame
        data = {'product_id': [product_id]}
        for i, price in enumerate(competitor_prices):
            data[f'comp{i+1}'] = [price]
        
        data_final = pd.DataFrame(data)
        print(data_final)
        return data_final
    except Exception as e:
        print("Error in process_data_from_json", str(e))
    

    


# In[4]:


# Define preprocessing
def preprocess_input(data):
    try:
        print("Raw Data", str(data))
        competitor_columns = competitor_columns = [col for col in data.columns if col.startswith('competitor')][:5]
        other_columns = [col for col in data.columns if not col.startswith('competitor')]
        keep_columns = other_columns + competitor_columns

        data[competitor_columns] = data[competitor_columns].apply(lambda x: x.fillna(x.mean()), axis=1)
        data = data[keep_columns]
        data['actual_price'] = data[competitor_columns].max(axis=1)
        data['max_discount'] = np.round(data['actual_price'] - data[competitor_columns].min(axis=1), 2)
    
        data['min_price'] = data[competitor_columns].min(axis=1)
        # numeric_features = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col])]
        # preprocessor = ColumnTransformer(
        #     transformers=[
        #         ('num', StandardScaler(), numeric_features)
        #     ])
        # print("Transformed Data", data)
        # preprocessor.fit(data)
        # return preprocessor.transform(data)
        #print('TRANSFORMED DATA', data)
        return data.drop(columns=['product_id'])
    except Exception as e:
        print("Error", str(e))
    


# In[ ]:


# Endpoint to predict promotional price
@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        # Get JSON request data
        json_data = request.get_json()

        # Check if the input data is in the correct format
        if not isinstance(json_data, list):
            raise ValueError("Input data should be a list of dictionaries")
        
        for item in json_data:
            if not isinstance(item, dict):
                raise ValueError("Each item in the input data should be a dictionary")

        json_data = process_data_from_json(json_data)
                
        # Convert JSON to DataFrame
        input_data = pd.DataFrame(json_data)
       # input_data = input_data.drop(columns=['product_id', 'product_type', 'timestamp', 'promotional_price'])
        # Preprocess input data
        X_input = preprocess_input(input_data)

        # Predict the base price
        base_predictions = base_model.predict(X_input)
        
        # Predict the quantiles
        lower_bound = lower_model.predict(X_input)
        upper_bound = upper_model.predict(X_input)
        
        # Create a response JSON
        response = []
        for idx, row in input_data.iterrows():
            result = {
                'product_ID': row['product_id'],
                'predicted_price': base_predictions[idx],
                'predicted_min_price': lower_bound[idx],
                'predicted_max_price': upper_bound[idx]
            }
            response.append(result)

        final_response = make_response(jsonify(response))   
        final_response.headers['Access-Control-Allow-Origin'] = '*' 
        final_response.headers['Access-Control-Allow-Methods'] = '*'
        final_response.headers['Access-Control-Allow-Headers'] = '*'
        return final_response

    except Exception as e:
        print(str(e))
        return jsonify({'error: something went wrong': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=6767, use_reloader=False)




