# 🔐 Network Security Project

This project implements various **Machine Learning algorithms** to detect and classify network intrusions using the NSL-KDD dataset. It aims to support intelligent decision-making for enhancing network security by identifying malicious patterns in traffic data.

---

## 📚 Project Description

Network security is critical in today’s digital landscape. This project applies **supervised learning** techniques to classify network activity as either **normal** or **malicious**. It leverages the **NSL-KDD dataset**, a widely used benchmark in intrusion detection research.

---

## 🧰 Technologies & Libraries Used

- **Python 3.x**
- **Pandas, NumPy** – Data preprocessing
- **Matplotlib, Seaborn** – Data visualization
- **Scikit-learn** – Model training and evaluation
- **Joblib** – Model saving and loading

---

## 📁 Project Structure

```bash
Network_Security_Project/
│
├── .github/workflows/        # GitHub Actions for CI/CD
├── NetworkData/              # Raw or sample network data files
├── NetworkSecurity/          # Core ML logic and modules
├── __pycache__/              # Python cache files
├── data_schema/              # Data validation schema definitions
├── final_models/             # Trained and serialized ML models
├── prediction_output/        # Output from prediction scripts
├── templates/                # HTML templates for the web interface
├── valid_data/               # Cleaned and validated data
│
├── .gitignore                # Files to ignore in Git
├── Dockerfile                # For containerizing the app
├── README.md                 # Project description
├── app.py                    # Flask app for model deployment
├── main.py                   # Main pipeline for training & evaluation
├── push_data.py              # Script to push data to MongoDB
├── requirements.txt          # Required Python packages
├── setup.py                  # Logging and exception handling config
└── test_mongodb.py           # MongoDB connection testing
```

---

## 🧠 Key Features

- 📊 **Data Preprocessing & Validation**
  - Schema-based validation using `data_schema/`
  - Segregation into `valid_data/` and prediction-ready datasets

- 🧪 **Model Training & Evaluation**
  - Classification models trained using structured network data
  - Saved models in `final_models/`

- 🧾 **Prediction Pipeline**
  - Input data → validation → prediction
  - Output stored in `prediction_output/`

- 🌐 **Web Interface**
  - Built with **Flask**
  - Accessible via `app.py` for real-time predictions

- 🛠 **MongoDB Integration**
  - Data pushed to MongoDB via `push_data.py`
  - Connection tested via `test_mongodb.py`

- 🐳 **Dockerized**
  - App can be deployed as a container using the included `Dockerfile`

---

## 🧠 Machine Learning Models

The following models are trained and evaluated on the dataset:

- ✅ Logistic Regression
- 🌲 Decision Tree
- 🌲🌲 Random Forest
- 📈 K-Nearest Neighbors (KNN)
- 📊 Naive Bayes

Each model outputs:
- Accuracy score
- Confusion matrix
- Precision, Recall, F1-Score

---

## 📊 Results Visualization

- **Feature correlation heatmaps**
- **Bar plots** comparing model performance
- **Attack type distribution** charts
- **Confusion matrices** for each model

Plots are saved inside the `visualizations/` folder.

---

## 🚀 How to Run

1. **Clone the repository**  
   ```bash
   git clone https://github.com/souravsharma22/Network_Security_Project.git
   cd Network_Security_Project
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the main script**  
   ```bash
   python main.py
   ```

4. **Train a specific model**  
   Example:
   ```bash
   python ml_models/decision_tree.py
   ```

---

## 📌 Dataset Used

- **NSL-KDD Dataset**  
  A refined version of the KDD'99 dataset.  
  It avoids duplicate records and provides a better benchmark for evaluating intrusion detection systems.

More info: [https://www.unb.ca/cic/datasets/nsl.html](https://www.unb.ca/cic/datasets/nsl.html)

---

## 📈 Sample Output

```
Model: Random Forest
Accuracy: 91.32%
Precision: 90.55%
Recall: 89.74%
F1-Score: 90.14%
```

---

## 🔧 Future Work

- Add deep learning models like LSTM or GRU for sequence-based detection
- Use real-time packet capture tools like Wireshark for live data analysis
- Build a dashboard to display detection stats (e.g., with Flask + Chart.js)
- Incorporate unsupervised anomaly detection methods

---

## 👨‍💻 Author

**Sourav Sharma**  
🔗 [GitHub](https://github.com/souravsharma22)

---

