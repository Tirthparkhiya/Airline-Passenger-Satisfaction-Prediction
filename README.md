# ✈️ Airline Passenger Satisfaction Prediction

This project is an **end-to-end machine learning system** that predicts whether an airline passenger is satisfied or not, based on several travel-related and service experience features. This project uses **MLOps practices**, **LightGBM** for modeling, and tools like **MongoDB**, **TensorBoard**, **MLflow**, **DVC**, **Flask**, and **Django** for full pipeline orchestration, versioning, visualization, and deployment.

---

## 🔍 Problem Statement

Airlines want to understand factors that contribute to passenger satisfaction. With this model, we can predict satisfaction levels to help airlines improve service and operations.

---

## ✅ Objective

- Build a classification model to predict **Passenger Satisfaction**.
- Follow a full **MLOps pipeline**: data ingestion → processing → model training → evaluation → versioning → deployment.
- Track and manage experiments using **MLflow** and **TensorBoard**.
- Use **MongoDB** as a data source.
- Serve the prediction using **Flask** and a touch of **Django**.

---

## 🧠 Model Used

- **LightGBM (Light Gradient Boosting Machine)**  
Chosen for its performance on structured/tabular data and ability to handle large datasets with speed.

---

## 📊 Feature Details

Below is a table listing all features used to make predictions, along with possible input values:

| Feature                    | Description                            | Expected Input Values                                             |
|---------------------------|----------------------------------------|-------------------------------------------------------------------|
| Online boarding           | Ease of online boarding process        | Very Poor, Poor, Average, Good, Excellent, Outstanding            |
| Departure Delay           | Delay at departure (in minutes)        | Float value (e.g. 5.0, 10.3)                                      |
| Arrival Delay             | Delay at arrival (in minutes)          | Float value (e.g. 2.5, 15.0)                                      |
| Inflight wifi service     | Quality of inflight wifi               | Very Poor, Poor, Average, Good, Excellent, Outstanding            |
| Class                     | Ticket class of the passenger          | Business, Economy, Economy Plus                                   |
| Type of Travel            | Purpose of the trip                    | Business travel, Personal Travel                                  |
| Flight Distance           | Distance between source and destination| Float value (e.g. 300.0, 1250.5)                                   |
| Inflight entertainment    | Quality of inflight entertainment      | Very Poor, Poor, Average, Good, Excellent, Outstanding            |
| Seat comfort              | Comfort level of the seat              | Very Poor, Poor, Average, Good, Excellent, Outstanding            |
| Leg room service          | Quality of leg room service            | Very Poor, Poor, Average, Good, Excellent, Outstanding            |
| On-board service          | Overall onboard services               | Very Poor, Poor, Average, Good, Excellent, Outstanding            |
| Ease of Online booking    | Experience while booking               | Very Poor, Poor, Average, Good, Excellent, Outstanding            |
| Cleanliness               | Cleanliness of the plane               | Very Poor, Poor, Average, Good, Excellent, Outstanding            |

---

## 🧰 Tools & Technologies Used

| Category               | Tools/Technologies                          |
|------------------------|---------------------------------------------|
| **Modeling**           | LightGBM                                    |
| **Backend**            | Flask, Django                               |
| **Experiment Tracking**| MLflow, TensorBoard                         |
| **Data Versioning**    | DVC                                          |
| **Database**           | MongoDB                                     |
| **Logging**            | Python Logging, MLflow, TensorBoard         |
| **Deployment**         | Flask + (Optional Django frontend)      |

---

## 🚀 End-to-End Pipeline

1. **Data Ingestion**
   - Load data from MongoDB or local source
   - Store raw files in `artifacts/ingested_data`

2. **Data Preprocessing**
   - Label encoding / mapping categorical values
   - Store processed data in `artifacts/processed`

3. **Feature Engineering**
   - Feature selection and transformation
   - Stored in `artifacts/engineered_data`

4. **Model Training**
   - Trained using LightGBM
   - Model saved in `artifacts/models`
   - Logged using MLflow

5. **Evaluation**
   - Metrics: Accuracy, Precision, Recall, F1-Score
   - Visualized using TensorBoard

6. **Version Control**
   - DVC tracks data and model versions

7. **Serving**
   - Flask handles the backend REST API
   - Optional: Django for user frontend interface

