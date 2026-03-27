from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import models
from typing import List, Optional

app = FastAPI(title="Neurological Symptom Analysis API")

# --- Pydantic Data Models ---
class Patient(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    dob: Optional[str] = None
    age: Optional[int] = None

class Symptom(BaseModel):
    patient_id: str
    symptom_type: str
    severity: str
    description: Optional[str] = None

class GCSScore(BaseModel):
    patient_id: str
    eye: int
    verbal: int
    motor: int

class ReflexTest(BaseModel):
    patient_id: str
    test_type: str
    body_part: Optional[str] = None
    result: str
    score: Optional[str] = None
    notes: Optional[str] = None

class Localization(BaseModel):
    patient_id: str
    region: str
    diagnosis: Optional[str] = None
    algorithm: Optional[str] = None
    confidence: Optional[float] = None

# --- API Endpoints ---

@app.post("/patients")
def add_patient(patient: Patient):
    try:
        models.add_patient(patient.first_name, patient.last_name, patient.phone, patient.dob, patient.age)
        return {"message": "Patient added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients")
def get_patients():
    try:
        df = models.get_patients()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/symptoms")
def add_symptom(s: Symptom):
    try:
        models.add_symptom(s.patient_id, s.symptom_type, s.severity, s.description)
        return {"message": "Symptom added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/symptoms/{patient_id}")
def get_symptoms(patient_id: str):
    try:
        df = models.get_symptoms(patient_id)
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gcs")
def add_gcs_score(g: GCSScore):
    try:
        models.add_gcs_score(g.patient_id, g.eye, g.verbal, g.motor)
        return {"message": "GCS Score added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/gcs/{patient_id}")
def get_gcs_scores(patient_id: str):
    try:
        df = models.get_gcs_scores(patient_id)
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reflex")
def add_reflex_test(r: ReflexTest):
    try:
        models.add_reflex_test(r.patient_id, r.test_type, r.body_part, r.result, r.score, r.notes)
        return {"message": "Reflex test added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reflex/{patient_id}")
def get_reflex_tests(patient_id: str):
    try:
        df = models.get_reflex_tests(patient_id)
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/localization")
def add_localization(l: Localization):
    try:
        models.add_localization(l.patient_id, l.region, l.diagnosis, l.algorithm, l.confidence)
        return {"message": "Localization added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/localization/{patient_id}")
def get_localizations(patient_id: str):
    try:
        df = models.get_localizations(patient_id)
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/seizures")
def get_seizure_frequency():
    try:
        df = models.get_seizure_frequency()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/critical")
def get_critical_patients():
    try:
        df = models.get_critical_patients()
        return df.to_dict(orient="records") if not df.empty else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
