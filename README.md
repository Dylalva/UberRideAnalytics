# 🚗 Uber Ride Analytics – Machine Learning Project (2024)

A complete **machine learning pipeline** analyzing and predicting Uber ride outcomes using real-world booking data from 2024.
The project explores ride patterns, cancellations, customer satisfaction, and operational performance — delivering a predictive model for **ride booking status classification**.

---

## 📂 Project Overview

This project uses the **Uber Ride Analytics Dataset (2024)**, which contains over **148,000 ride bookings** across multiple vehicle types.
It covers information about:

* 🚕 Booking status (completed, cancelled, incomplete, etc.)
* 🚘 Vehicle type and payment method
* 💸 Ride distance and booking value
* ⭐ Customer and driver ratings
* ⏱ Average trip times (VTAT & CTAT)
* 📅 Date and time of booking

The goal is to **predict the “Booking Status”** using operational, behavioral, and temporal variables.

---

## 🧠 Machine Learning Objective

**Target Variable:** `Booking Status`
**Type:** Multiclass classification
**Classes:**

* Completed
* Cancelled by Customer
* Cancelled by Driver
* Incomplete
* No Driver Found

**Goal:** Predict the final status of a booking before it occurs, helping Uber optimize driver allocation and reduce cancellations.

---

## ⚙️ Pipeline Overview

The project was implemented entirely in **Jupyter Notebook** using **scikit-learn**, following a modular and reproducible ML pipeline.

### 🔹 Data Preprocessing

* Missing values cleaned and categorical encoding applied
* Date and time split into components (year, month, hour, weekday)
* Rare category grouping for categorical stability
* Standardization of numerical variables
* Creation of a custom preprocessing class:

  ```python
  RidePreprocessor(date_col="date", time_col="time", min_cat_freq=0.005)
  ```

### 🔹 Models Trained

| Model               | Type                       | Purpose                          |
| :------------------ | :------------------------- | :------------------------------- |
| Logistic Regression | Baseline linear classifier | Benchmark for multiclass problem |
| Random Forest       | Ensemble model             | Final predictive model           |

### 🔹 Model Evaluation

* **Cross-validation:** 5-fold
* **Metrics:** Accuracy, F1-score (macro), and ROC-AUC
* **Validation Split:** 80% training / 20% testing

---

## 📈 Results Summary

| Metric               | Logistic Regression | Random Forest |
| :------------------- | :-----------------: | :-----------: |
| **Accuracy**         |         0.94        |    **0.99**   |
| **F1-score (macro)** |         0.93        |    **0.98**   |
| **ROC-AUC (avg)**    |         0.95        |    **0.99**   |

✅ **Random Forest achieved near-perfect performance**, handling nonlinear interactions and class imbalance effectively.

---

## 📊 Key Visualizations

### 1️⃣ Confusion Matrix – Random Forest

Shows accurate classification across all booking statuses with minimal confusion.
→ *Minor overlap between customer and driver cancellations.*

### 2️⃣ True vs Predicted Distribution

Confirms balanced class representation between actual and predicted outcomes.

### 3️⃣ Feature Importance

Highlights the most influential variables:

* **Avg VTAT** – driver arrival delay
* **Avg CTAT** – trip duration
* **Booking Value** – fare amount
* **Customer & Driver Ratings** – satisfaction indicators
* **Payment Method** – behavioral signal

---

## 💡 Insights & Business Impact

* Long **driver arrival times (VTAT)** are the strongest predictor of ride cancellations.
* Higher **fare value** and **positive ratings** correlate with completed rides.
* Payment method behaviors (UPI/Cash vs. Wallet/Cards) provide insight into customer reliability.
* The model can help Uber proactively reassign drivers or incentivize users before cancellation.

---

## 🧰 Tech Stack

| Category          | Tools & Libraries                                |
| ----------------- | ------------------------------------------------ |
| **Language**      | Python 3.11                                      |
| **Environment**   | Jupyter Notebook                                 |
| **Libraries**     | pandas, numpy, matplotlib, seaborn, scikit-learn |
| **Visualization** | Matplotlib, Seaborn                              |
| **Modeling**      | RandomForestClassifier, LogisticRegression       |
| **Evaluation**    | Confusion Matrix, ROC Curves, Feature Importance |

---

## 📦 Project Structure

```
📁 UberRideAnalytics/
│
|__ data/
|   ├── 📄 Uberdata.xlsx                  # Cleaned dataset
├── 📓 notebooks/
|    ├── 📓 001_Uber2024.ipynb             # EDA notebook
|    ├── 📓 002_Uber2024.ipynb             # Main notebook
├── 📊 figures/                       # Generated plots
│    ├── confusion_matrix_RF.png
│    ├── distVerdaderos_VS_Prediccion.png
│    ├── varImportantesRF2.png
│    ├── curvaROC_RF_multiclase.png
├── 📓 models
|    ├── 📓 booking_status_rf_model.joblib
│
├── 📄 README.md                      # Project documentation (this file)
└── 📄 requirements.txt               # Python dependencies
```

---

## 🚀 How to Run the Project

1. Clone this repository:

   ```bash
   git clone https://github.com/Dylalva/uber-ride-analytics-ml.git
   cd uber-ride-analytics-ml
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Open Jupyter Notebook:

   ```bash
   jupyter notebook
   ```
4. Run `notebooks/002_Uber2024.ipynb` to reproduce preprocessing and model training.

---

## 🧑‍💻 Author

**Dylan ELizondo Alvarado**
*Systems Engineer | Data Science & ML Enthusiast*
📧 *[dylalva1933@gmail.com]*
🔗 *GitHub: [github.com/Dylalva]*
🔗 *LinkedIn: [linkedin.com/in/]*

---

## 🏁 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute with attribution.
