import pandas as pd
from datetime import datetime
from database import get_db
from bson import ObjectId

# Helper function to convert mongo cursor to pandas dataframe
def cursor_to_df(cursor, id_field='_id', rename_id_to=None):
    df = pd.DataFrame(list(cursor))
    if not df.empty and id_field in df.columns:
        df[id_field] = df[id_field].astype(str)
        if rename_id_to:
            df.rename(columns={id_field: rename_id_to}, inplace=True)
    return df

# --- Patient Operations ---
def add_patient(first_name, last_name, phone, dob, age):
    db = get_db()
    db.patients.insert_one({
        "FirstName": first_name,
        "LastName": last_name,
        "PhoneNumber": phone,
        "DateOfBirth": dob.strftime("%Y-%m-%d") if hasattr(dob, 'strftime') else str(dob),
        "Age": age
    })

def get_patients():
    db = get_db()
    cursor = db.patients.find()
    return cursor_to_df(cursor, rename_id_to='PatientID')

# --- Symptom Operations ---
def add_symptom(patient_id, symptom_type, severity, description):
    db = get_db()
    db.symptoms.insert_one({
        "PatientID": str(patient_id),
        "SymptomType": symptom_type,
        "Severity": severity,
        "Description": description,
        "RecordedAt": datetime.now()
    })

def get_symptoms(patient_id):
    db = get_db()
    cursor = db.symptoms.find({"PatientID": str(patient_id)})
    return cursor_to_df(cursor, rename_id_to='SymptomID')

# --- GCS Score Operations ---
def add_gcs_score(patient_id, eye, verbal, motor):
    total = eye + verbal + motor
    db = get_db()
    db.gcs_scores.insert_one({
        "PatientID": str(patient_id),
        "EyeScore": eye,
        "VerbalScore": verbal,
        "MotorScore": motor,
        "TotalScore": total,
        "RecordedAt": datetime.now()
    })

def get_gcs_scores(patient_id):
    db = get_db()
    cursor = db.gcs_scores.find({"PatientID": str(patient_id)}).sort("RecordedAt", 1)
    return cursor_to_df(cursor, rename_id_to='GCSID')

# --- Reflex Test Operations ---
def add_reflex_test(patient_id, test_type, body_part, result, score, notes):
    db = get_db()
    db.reflex_tests.insert_one({
        "PatientID": str(patient_id),
        "TestType": test_type,
        "BodyPart": body_part,
        "Result": result,
        "Score": score,
        "Notes": notes,
        "TestTime": datetime.now()
    })

def get_reflex_tests(patient_id):
    db = get_db()
    cursor = db.reflex_tests.find({"PatientID": str(patient_id)})
    return cursor_to_df(cursor, rename_id_to='TestID')

# --- Localization Operations ---
def add_localization(patient_id, region, diagnosis, algorithm, confidence):
    db = get_db()
    db.localizations.insert_one({
        "PatientID": str(patient_id),
        "Region": region,
        "Diagnosis": diagnosis,
        "AlgorithmUsed": algorithm,
        "ConfidenceScore": confidence,
        "GeneratedAt": datetime.now()
    })

def get_localizations(patient_id):
    db = get_db()
    cursor = db.localizations.find({"PatientID": str(patient_id)})
    return cursor_to_df(cursor, rename_id_to='LocalizationID')

# --- Advanced Analytical Queries ---
def get_seizure_frequency():
    """Group seizures by day/month for trend analysis"""
    db = get_db()
    pipeline = [
        {"$match": {"SymptomType": "Seizure"}},
        {"$project": {
            "Date": {
                "$dateToString": {"format": "%Y-%m-%d", "date": "$RecordedAt"}
            }
        }},
        {"$group": {
            "_id": "$Date",
            "SeizureCount": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    cursor = db.symptoms.aggregate(pipeline)
    df = pd.DataFrame(list(cursor))
    if not df.empty:
        df.rename(columns={'_id': 'Date'}, inplace=True)
    return df

def get_critical_patients():
    """Returns patients with low GCS scores (Total < 8 indicates severe coma)"""
    db = get_db()
    pipeline = [
        {"$match": {"TotalScore": {"$lte": 8}}},
        {"$sort": {"RecordedAt": -1}},
        {
            "$addFields": {
                "PatientObjectId": {"$toObjectId": "$PatientID"}
            }
        },
        {"$lookup": {
            "from": "patients",
            "localField": "PatientObjectId",
            "foreignField": "_id",
            "as": "patient_info"
        }},
        {"$unwind": "$patient_info"},
        {"$project": {
            "FirstName": "$patient_info.FirstName",
            "LastName": "$patient_info.LastName",
            "Age": "$patient_info.Age",
            "TotalScore": 1,
            "RecordedAt": 1,
            "_id": 0
        }},
        {"$sort": {"TotalScore": 1, "RecordedAt": -1}}
    ]
    cursor = db.gcs_scores.aggregate(pipeline)
    df = pd.DataFrame(list(cursor))
    return df
