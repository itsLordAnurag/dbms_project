import streamlit as st
import pandas as pd
import plotly.express as px
import models
from database import init_db

# Initialize setup
init_db()

st.set_page_config(page_title="Neurological Database", page_icon="🧠", layout="wide")
st.title("Neurological Symptom Analysis Database")

menu = [
    "Patient Management",
    "Symptom Tracking",
    "GCS Tracker",
    "Reflex and Coordination Test",
    "Neurological Localization",
    "Advanced Reports"
]

choice = st.sidebar.radio("Navigation", menu)

if choice == "Patient Management":
    st.header("Patient Management")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Add New Patient")
        with st.form("patient_form"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            phone = st.text_input("Phone Number")
            dob = st.date_input("Date of Birth")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            submit = st.form_submit_button("Add Patient")
            if submit:
                if first_name and last_name:
                    models.add_patient(first_name, last_name, phone, dob, age)
                    st.success("Patient Added Successfully!")
                else:
                    st.error("First Name and Last Name are required.")
    
    with col2:
        st.subheader("View Patients")
        patients_df = models.get_patients()
        if not patients_df.empty:
            st.dataframe(patients_df)
        else:
            st.info("No patients found.")

elif choice == "Symptom Tracking":
    st.header("Symptom Tracking")
    patients_df = models.get_patients()
    if patients_df.empty:
        st.warning("Please add a patient first in the Patient Management section.")
    else:
        patient_options = patients_df['PatientID'].astype(str) + " - " + patients_df['FirstName'] + " " + patients_df['LastName']
        selected_patient = st.selectbox("Select Patient", patient_options)
        patient_id = selected_patient.split(" - ")[0]

        with st.form("symptom_form"):
            symptom_type = st.selectbox("Symptom Type", ["Headache", "Seizure", "Weakness", "Numbness", "Vision changes", "Other"])
            severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe", "Critical"])
            description = st.text_area("Description")
            submit = st.form_submit_button("Record Symptom")
            if submit:
                models.add_symptom(patient_id, symptom_type, severity, description)
                st.success("Symptom Recorded!")

        st.subheader("Patient's Symptoms")
        st.dataframe(models.get_symptoms(patient_id))

elif choice == "GCS Tracker":
    st.header("Glasgow Coma Scale (GCS) Tracker")
    patients_df = models.get_patients()
    if patients_df.empty:
        st.warning("Please add a patient first in the Patient Management section.")
    else:
        patient_options = patients_df['PatientID'].astype(str) + " - " + patients_df['FirstName'] + " " + patients_df['LastName']
        selected_patient = st.selectbox("Select Patient", patient_options, key="gcs")
        patient_id = selected_patient.split(" - ")[0]
    
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Record GCS")
            with st.form("gcs_form"):
                eye = st.slider("Eye Opening (1-4)", 1, 4, 4)
                verbal = st.slider("Verbal Response (1-5)", 1, 5, 5)
                motor = st.slider("Motor Response (1-6)", 1, 6, 6)
                submit = st.form_submit_button("Save GCS Score")
                if submit:
                    models.add_gcs_score(patient_id, eye, verbal, motor)
                    st.success(f"GCS Recorded! Total: {eye+verbal+motor}")

        with col2:
            st.subheader("GCS Trend Analysis")
            gcs_df = models.get_gcs_scores(patient_id)
            if not gcs_df.empty:
                fig = px.line(gcs_df, x="RecordedAt", y="TotalScore", title="GCS Total Score Over Time", markers=True, range_y=[0, 16])
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(gcs_df)
            else:
                st.info("No GCS scores recorded for this patient.")

elif choice == "Reflex & Coordination Test":
    st.header("Reflex and Coordination Tests")
    patients_df = models.get_patients()
    if patients_df.empty:
        st.warning("Please add a patient first in the Patient Management section.")
    else:
        patient_options = patients_df['PatientID'].astype(str) + " - " + patients_df['FirstName'] + " " + patients_df['LastName']
        selected_patient = st.selectbox("Select Patient", patient_options, key="reflex")
        patient_id = selected_patient.split(" - ")[0]
        
        with st.form("reflex_form"):
            test_type = st.selectbox("Exam Component", ["Cranial nerves", "Motor", "Sensory", "Coordination", "Gait"])
            body_part = st.text_input("Body Part (e.g., Left Leg, Right Arm, Face)")
            result = st.selectbox("Result", ["Normal", "Abnormal", "Absent", "Hyperreflexia", "Hyporeflexia"])
            score = st.text_input("Score (e.g., 2+, 1+, 0)")
            notes = st.text_area("Notes")
            submit = st.form_submit_button("Record Test")
            if submit:
                models.add_reflex_test(patient_id, test_type, body_part, result, score, notes)
                st.success("Reflex test recorded.")
                
        st.subheader("Patient's Test Results")
        st.dataframe(models.get_reflex_tests(patient_id))

elif choice == "Neurological Localization":
    st.header("Neurological Localization")
    patients_df = models.get_patients()
    if patients_df.empty:
        st.warning("Please add a patient first in the Patient Management section.")
    else:
        patient_options = patients_df['PatientID'].astype(str) + " - " + patients_df['FirstName'] + " " + patients_df['LastName']
        selected_patient = st.selectbox("Select Patient", patient_options, key="loc")
        patient_id = selected_patient.split(" - ")[0]
        
        with st.form("loc_form"):
            region = st.text_input("Neuroanatomical Region (e.g., Frontal Lobe, Basal Ganglia, Brainstem)")
            diagnosis = st.text_input("Diagnosis / Finding")
            algorithm = st.selectbox("Algorithm Used", ["Clinical Heuristics", "Machine Learning Model V1", "Rule-based Expert System"])
            confidence = st.slider("Confidence Score (%)", 0.0, 100.0, 85.0)
            submit = st.form_submit_button("Save Localization")
            if submit:
                models.add_localization(patient_id, region, diagnosis, algorithm, confidence)
                st.success("Localization saved.")
                
        st.subheader("Patient's Localization Records")
        st.dataframe(models.get_localizations(patient_id))

elif choice == "Advanced Reports":
    st.header("Advanced Reports & Analysis")
    
    st.subheader("1. Seizure Frequency Analysis")
    seizure_df = models.get_seizure_frequency()
    if not seizure_df.empty:
        fig = px.bar(seizure_df, x="Date", y="SeizureCount", title="Seizure Events Over Time", labels={'Date': 'Date', 'SeizureCount': 'Number of Seizures'}, color="SeizureCount", color_continuous_scale="Reds")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No seizure data found.")
        
    st.markdown("---")
    
    st.subheader("2. Critical Patients (Coma Analysis)")
    st.write("Patients with severe coma (GCS Total <= 8).")
    critical_df = models.get_critical_patients()
    if not critical_df.empty:
        st.error("⚠️ Critical patients identified based on recent GCS scores.")
        st.dataframe(critical_df)
    else:
        st.success("✅ No critical patients matching severe coma criteria at the moment.")
