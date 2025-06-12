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
├── dataset/                   # Training and test CSV files (NSL-KDD)
├── ml_models/                 # Python scripts for training different ML models
│   ├── decision_tree.py
│   ├── logistic_regression.py
│   ├── random_forest.py
│   ├── naive_bayes.py
│   └── knn.py
├── preprocessing/             # Scripts for cleaning and encoding data
│   └── preprocess.py
├── visualizations/            # Charts and graphs for analysis
├── model/                     # Serialized trained models (.joblib)
├── main.py                    # Main script to run end-to-end pipeline
└── requirements.txt           # List of required Python packages
```

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

