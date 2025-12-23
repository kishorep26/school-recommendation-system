# Phoenix School Recommendation System

An intelligent school recommendation system powered by machine learning algorithms (K-Nearest Neighbors, Random Forest, and Support Vector Machine) to help students and parents find the perfect school in the Phoenix metropolitan area.

![School Recommendation System](https://img.shields.io/badge/ML-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Flask](https://img.shields.io/badge/Flask-3.0-red)

## 🎯 Features

- **Multiple ML Models**: Choose from KNN, Random Forest, or SVM algorithms
- **Dual Search Modes**:
  - Search by school name to find similar schools
  - Search by preferences to find schools matching your criteria
- **Comprehensive Data**: Analyzes 200+ schools with detailed metrics
- **Modern UI**: Beautiful, responsive web interface
- **Real-time Recommendations**: Get instant results powered by trained models

## 📊 Dataset

The system uses the Phoenix Schools Dataset containing:
- School demographics
- Academic performance metrics
- Safety statistics
- Facility information
- Location data

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd school-recommendation-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Train the models**
```bash
python train_models.py
```

This will:
- Load the Phoenix Schools Dataset
- Train KNN, Random Forest, and SVM models
- Save trained models to the `models/` directory

4. **Run the application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🐳 Docker Deployment

### Build and run with Docker

```bash
# Build the image
docker build -t school-recommendation-system .

# Run the container
docker run -p 5000:5000 school-recommendation-system
```

Access the application at `http://localhost:5000`

## 📁 Project Structure

```
school-recommendation-system/
├── app.py                          # Flask API server
├── train_models.py                 # Model training script
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── Phoenix Schools Dataset.csv     # Main dataset
├── static/                         # Frontend files
│   ├── index.html                 # Main HTML page
│   ├── style.css                  # Styling
│   └── script.js                  # JavaScript logic
└── models/                        # Trained models (generated)
    ├── knn_model.pkl
    ├── rf_model.pkl
    ├── svm_model.pkl
    └── ...
```

## 🔧 API Endpoints

### Get all schools
```
GET /api/schools
```

### Get all cities
```
GET /api/cities
```

### Get all zipcodes
```
GET /api/zipcodes
```

### Recommend by school name
```
POST /api/recommend/by-name
Content-Type: application/json

{
  "school_name": "School Name",
  "model": "knn"  // or "rf" or "svm"
}
```

### Recommend by preferences
```
POST /api/recommend/by-preferences
Content-Type: application/json

{
  "location_type": "city",
  "city": "Phoenix",
  "elementary": 1,
  "school_grade": 4,
  "proficiency": 2,
  "model": "knn"
  // ... other preferences
}
```

## 🤖 Machine Learning Models

### K-Nearest Neighbors (KNN)
- Finds schools with the most similar characteristics
- Fast and interpretable
- Best for finding schools very similar to a reference

### Random Forest
- Ensemble of decision trees
- Provides diverse recommendations
- Robust to outliers

### Support Vector Machine (SVM)
- Advanced pattern recognition
- High accuracy for complex patterns
- Best for nuanced matching

## 🎨 Technologies Used

- **Backend**: Python, Flask, scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript
- **ML Libraries**: pandas, numpy, scikit-learn
- **Deployment**: Docker, Gunicorn

## 📈 Model Performance

The models are trained on standardized features including:
- Location (city/zipcode)
- Grade levels offered
- Academic performance metrics
- Student demographics
- Safety statistics
- Facility quality

## 🛠️ Development

### Running in development mode

```bash
python app.py
```

The server will run with debug mode enabled and auto-reload on file changes.

### Training models with custom data

If you have additional datasets, place them in the root directory and update the `train_models.py` script accordingly.

## 📝 License

This project is created for educational purposes.

## 👥 Contributors

- Kishore Prashanth

## 🙏 Acknowledgments

- Phoenix Schools Dataset
- scikit-learn community
- Flask framework

---

**Note**: Make sure to train the models before running the application for the first time!
