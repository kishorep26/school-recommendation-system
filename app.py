"""
School Recommendation System - Flask API
Provides endpoints for school recommendations using trained ML models
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Load models and data
print("Loading models...")
try:
    knn_model = joblib.load('models/knn_model.pkl')
    rf_model = joblib.load('models/rf_model.pkl')
    svm_model = joblib.load('models/svm_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    city_encoder = joblib.load('models/city_encoder.pkl')
    zipcode_encoder = joblib.load('models/zipcode_encoder.pkl')
    school_raw_data = joblib.load('models/school_raw_data.pkl')
    school_data_scaled = joblib.load('models/school_data_scaled.pkl')
    feature_columns = joblib.load('models/feature_columns.pkl')
    print("Models loaded successfully!")
    print(f"Loaded {len(school_raw_data)} schools")
except Exception as e:
    print(f"Error loading models: {e}")
    print("Please run train_models.py first!")
    school_raw_data = pd.DataFrame()

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/schools', methods=['GET'])
def get_schools():
    """Get list of all schools"""
    try:
        schools = school_raw_data['School_name'].tolist()
        return jsonify({'schools': schools})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Get list of all cities"""
    try:
        cities = sorted(school_raw_data['city'].unique().tolist())
        return jsonify({'cities': cities})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/zipcodes', methods=['GET'])
def get_zipcodes():
    """Get list of all zipcodes"""
    try:
        zipcodes = sorted(school_raw_data['zipcode'].unique().tolist())
        return jsonify({'zipcodes': [str(z) for z in zipcodes]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend/by-name', methods=['POST'])
def recommend_by_name():
    """Get recommendations based on a school name"""
    try:
        data = request.json
        school_name = data.get('school_name', '').strip()
        model_type = data.get('model', 'knn')
        
        if not school_name:
            return jsonify({'error': 'School name is required'}), 400
        
        # Find the school
        matching_schools = school_raw_data[
            school_raw_data['School_name'].str.lower() == school_name.lower()
        ]
        
        if len(matching_schools) == 0:
            return jsonify({'error': 'School not found'}), 404
        
        # Get the school's index
        school_idx = matching_schools.index[0]
        
        # Get the feature vector (already scaled)
        test_sample = school_data_scaled.iloc[[school_idx]].values
        
        # Get recommendations based on model type
        if model_type == 'knn':
            distances, indices = knn_model.kneighbors(test_sample)
            recommended_indices = indices[0]
            
        elif model_type == 'rf':
            # Get predictions from each tree
            predictions = []
            for tree in rf_model.estimators_:
                pred = tree.predict(test_sample)[0]
                # Find the index of this school
                pred_idx = school_raw_data[school_raw_data['School_name'] == pred].index
                if len(pred_idx) > 0 and pred_idx[0] != school_idx:
                    predictions.append(pred_idx[0])
            
            # Take first 5 unique predictions
            recommended_indices = list(dict.fromkeys(predictions))[:5]
            
        elif model_type == 'svm':
            probabilities = svm_model.predict_proba(test_sample)
            top_indices = np.argsort(probabilities, axis=1)[:, -6:]  # Get top 6
            # Filter out the input school
            recommended_indices = [idx for idx in top_indices[0][::-1] if idx != school_idx][:5]
            
        else:
            return jsonify({'error': 'Invalid model type'}), 400
        
        # Get school details
        recommendations = school_raw_data.iloc[recommended_indices].to_dict('records')
        
        result = {
            'input_school': school_name,
            'model_used': model_type,
            'recommendations': recommendations
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in recommend_by_name: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend/by-preferences', methods=['POST'])
def recommend_by_preferences():
    """Get recommendations based on user preferences"""
    try:
        data = request.json
        model_type = data.get('model', 'knn')
        
        # Filter schools based on preferences
        filtered_data = school_raw_data.copy()
        
        # Location filter
        if data.get('location_type') == 'city' and data.get('city'):
            filtered_data = filtered_data[filtered_data['city'] == data.get('city')]
        elif data.get('location_type') == 'zipcode' and data.get('zipcode'):
            filtered_data = filtered_data[filtered_data['zipcode'] == int(data.get('zipcode'))]
        
        # Grade level filters
        if data.get('elementary'):
            filtered_data = filtered_data[filtered_data['elementary_school'] == 1]
        if data.get('intermediate'):
            filtered_data = filtered_data[filtered_data['intermediate_school'] == 1]
        if data.get('middle'):
            filtered_data = filtered_data[filtered_data['middle_school'] == 1]
        if data.get('high'):
            filtered_data = filtered_data[filtered_data['high_school'] == 1]
        
        # School grade filter
        if data.get('school_grade'):
            min_grade = int(data.get('school_grade'))
            filtered_data = filtered_data[filtered_data['school_grade'] >= min_grade]
        
        if len(filtered_data) == 0:
            return jsonify({
                'model_used': model_type,
                'recommendations': [],
                'message': 'No schools match your criteria. Try adjusting your preferences.'
            })
        
        # Get indices of filtered schools
        filtered_indices = filtered_data.index.tolist()
        
        # Use average of filtered schools as reference
        reference_vector = school_data_scaled.iloc[filtered_indices].mean(axis=0).values.reshape(1, -1)
        
        # Get recommendations
        if model_type == 'knn':
            distances, indices = knn_model.kneighbors(reference_vector, n_neighbors=min(10, len(school_data_scaled)))
            # Filter to only include schools from filtered set
            recommended_indices = [idx for idx in indices[0] if idx in filtered_indices][:5]
            
        elif model_type == 'rf':
            # Get diverse predictions
            predictions = []
            for tree in rf_model.estimators_[:10]:
                pred = tree.predict(reference_vector)[0]
                pred_idx = school_raw_data[school_raw_data['School_name'] == pred].index
                if len(pred_idx) > 0 and pred_idx[0] in filtered_indices:
                    predictions.append(pred_idx[0])
            recommended_indices = list(dict.fromkeys(predictions))[:5]
            
        elif model_type == 'svm':
            probabilities = svm_model.predict_proba(reference_vector)
            sorted_indices = np.argsort(probabilities, axis=1)[:, ::-1][0]
            recommended_indices = [idx for idx in sorted_indices if idx in filtered_indices][:5]
        
        # If we don't have enough recommendations, just return top filtered schools
        if len(recommended_indices) < 5:
            recommended_indices = filtered_indices[:5]
        
        recommendations = school_raw_data.iloc[recommended_indices].to_dict('records')
        
        result = {
            'model_used': model_type,
            'recommendations': recommendations,
            'total_matches': len(filtered_data)
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in recommend_by_preferences: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/school/<school_name>', methods=['GET'])
def get_school_details(school_name):
    """Get detailed information about a specific school"""
    try:
        school = school_raw_data[
            school_raw_data['School_name'].str.lower() == school_name.lower()
        ]
        
        if len(school) == 0:
            return jsonify({'error': 'School not found'}), 404
        
        return jsonify(school.to_dict('records')[0])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
