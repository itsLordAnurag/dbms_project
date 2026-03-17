# Neurological Symptom Analysis Database

A Streamlit web application for tracking and analyzing neurological symptoms, powered by MongoDB Atlas.

## Features
- **Patient Management**: Register and view patient records.
- **Symptom Tracking**: Log neurological symptoms and severity.
- **GCS Tracker**: Monitor Glasgow Coma Scale scores with trend graphs.
- **Reflex & Coordination**: Record clinical reflex exams and localized coordination notes.
- **Neurological Localization**: AI/Algorithm tracking form to store system-generated diagnosis predictions.
- **Advanced Reports**: View Seizure frequency trends and identify critical coma patients.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd DBMS
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your MongoDB Atlas connection string:
   ```env
   MONGO_URI=mongodb+srv://<username>:<password>@cluster...
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```
