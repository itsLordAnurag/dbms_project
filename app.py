import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Neurological Database", page_icon="🎃", layout="wide")
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
                    res = requests.post(f"{API_URL}/patients", json={
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone": phone,
                        "dob": str(dob),
                        "age": age
                    })
                    if res.status_code == 200:
                        st.success("Patient Added Successfully!")
                    else:
                        st.error(res.text)
                else:
                    st.error("First Name and Last Name are required.")
    
    with col2:
        st.subheader("View Patients")
        try:
            res = requests.get(f"{API_URL}/patients")
            if res.status_code == 200 and res.json():
                st.dataframe(pd.DataFrame(res.json()))
            else:
                st.info("No patients found.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the Backend API. Make sure FastAPI is running on port 8000.")

elif choice == "Symptom Tracking":
    st.header("Symptom Tracking")
    try:
        res = requests.get(f"{API_URL}/patients")
        patients_data = res.json() if res.status_code == 200 else []
        
        if not patients_data:
            st.warning("Please add a patient first in the Patient Management section.")
        else:
            patients_df = pd.DataFrame(patients_data)
            patient_options = patients_df['PatientID'].astype(str) + " - " + patients_df['FirstName'] + " " + patients_df['LastName']
            selected_patient = st.selectbox("Select Patient", patient_options)
            patient_id = selected_patient.split(" - ")[0]

            with st.form("symptom_form"):
                symptom_type = st.selectbox("Symptom Type", ["Headache", "Seizure", "Weakness", "Numbness", "Vision changes", "Other"])
                severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe", "Critical"])
                description = st.text_area("Description")
                submit = st.form_submit_button("Record Symptom")
                if submit:
                    s_res = requests.post(f"{API_URL}/symptoms", json={
                        "patient_id": patient_id,
                        "symptom_type": symptom_type,
                        "severity": severity,
                        "description": description
                    })
                    if s_res.status_code == 200:
                        st.success("Symptom Recorded!")
                    else:
                        st.error(s_res.text)

            st.subheader("Patient's Symptoms")
            s_get = requests.get(f"{API_URL}/symptoms/{patient_id}")
            if s_get.status_code == 200 and s_get.json():
                st.dataframe(pd.DataFrame(s_get.json()))
            else:
                st.info("No symptoms recorded.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the Backend API. Make sure FastAPI is running on port 8000.")

elif choice == "GCS Tracker":
    st.header("Glasgow Coma Scale (GCS) Tracker")
    try:
        res = requests.get(f"{API_URL}/patients")
        patients_data = res.json() if res.status_code == 200 else []
        
        if not patients_data:
            st.warning("Please add a patient first in the Patient Management section.")
        else:
            patients_df = pd.DataFrame(patients_data)
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
                        g_res = requests.post(f"{API_URL}/gcs", json={
                            "patient_id": patient_id,
                            "eye": eye,
                            "verbal": verbal,
                            "motor": motor
                        })
                        if g_res.status_code == 200:
                            st.success(f"GCS Recorded! Total: {eye+verbal+motor}")
                        else:
                            st.error(g_res.text)

            with col2:
                st.subheader("GCS Trend Analysis")
                g_get = requests.get(f"{API_URL}/gcs/{patient_id}")
                gcs_data = g_get.json() if g_get.status_code == 200 else []
                if gcs_data:
                    gcs_df = pd.DataFrame(gcs_data)
                    fig = px.line(gcs_df, x="RecordedAt", y="TotalScore", title="GCS Total Score Over Time", markers=True, range_y=[0, 16])
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(gcs_df)
                else:
                    st.info("No GCS scores recorded for this patient.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the Backend API. Make sure FastAPI is running on port 8000.")

elif choice == "Reflex and Coordination Test":
    st.header("Reflex and Coordination Tests")
    try:
        res = requests.get(f"{API_URL}/patients")
        patients_data = res.json() if res.status_code == 200 else []
        
        if not patients_data:
            st.warning("Please add a patient first in the Patient Management section.")
        else:
            patients_df = pd.DataFrame(patients_data)
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
                    r_res = requests.post(f"{API_URL}/reflex", json={
                        "patient_id": patient_id,
                        "test_type": test_type,
                        "body_part": body_part,
                        "result": result,
                        "score": score,
                        "notes": notes
                    })
                    if r_res.status_code == 200:
                        st.success("Reflex test recorded.")
                    else:
                        st.error(r_res.text)
                    
            st.subheader("Patient's Test Results")
            r_get = requests.get(f"{API_URL}/reflex/{patient_id}")
            if r_get.status_code == 200 and r_get.json():
                st.dataframe(pd.DataFrame(r_get.json()))
            else:
                st.info("No reflex tests recorded.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the Backend API. Make sure FastAPI is running on port 8000.")

elif choice == "Neurological Localization":
    st.header("Neurological Localization")
    try:
        res = requests.get(f"{API_URL}/patients")
        patients_data = res.json() if res.status_code == 200 else []
        
        if not patients_data:
            st.warning("Please add a patient first in the Patient Management section.")
        else:
            patients_df = pd.DataFrame(patients_data)
            patient_options = patients_df['PatientID'].astype(str) + " - " + patients_df['FirstName'] + " " + patients_df['LastName']
            selected_patient = st.selectbox("Select Patient", options=patient_options, key="loc")
            patient_id = selected_patient.split(" - ")[0]
        
            st.subheader("Automated Localization Algorithm")
            st.write("Run the Clinical Heuristics Algorithm based on the patient's recorded symptoms.")
            if st.button("Run Diagnostic Algorithm"):
                symptoms_df = models.get_symptoms(patient_id)
                if not symptoms_df.empty:
                    symptoms_list = symptoms_df['SymptomType'].tolist() + symptoms_df['Description'].tolist()
                    symptoms_str_list = [str(x) for x in symptoms_list if x and str(x).strip() and str(x) != 'nan']
                    
                    if symptoms_str_list:
                        region, confidence = models.calculate_localization(symptoms_str_list)
                        if confidence > 0:
                            models.add_localization(patient_id, region, "Automated finding based on symptoms.", "Clinical Heuristics", confidence)
                            st.success(f"Algorithm Complete & Saved! Predicted Region: **{region}** (Confidence: {confidence}%)")
                        else:
                            st.warning("Not enough specific symptom data to run the algorithm. Please log more detailed symptoms.")
                else:
                    st.warning("No symptoms found for this patient. Please log symptoms first.")
                    
            st.markdown("---")
            st.subheader("Manual Localization Entry")
            with st.form("loc_form"):
                region = st.text_input("Neuroanatomical Region (e.g., Frontal Lobe, Basal Ganglia, Brainstem)")
                diagnosis = st.text_input("Diagnosis / Finding")
                algorithm = st.selectbox("Algorithm Used", ["Clinical Heuristics", "Machine Learning Model V1", "Rule-based Expert System"])
                confidence = st.slider("Confidence Score (%)", 0.0, 100.0, 85.0)
                submit = st.form_submit_button("Save Localization")
                if submit:
                    l_res = requests.post(f"{API_URL}/localization", json={
                        "patient_id": patient_id,
                        "region": region,
                        "diagnosis": diagnosis,
                        "algorithm": algorithm,
                        "confidence": confidence
                    })
                    if l_res.status_code == 200:
                        st.success("Localization saved.")
                    else:
                        st.error(l_res.text)
                    
            st.subheader("Patient's Localization Records")
            l_get = requests.get(f"{API_URL}/localization/{patient_id}")
            if l_get.status_code == 200 and l_get.json():
                st.dataframe(pd.DataFrame(l_get.json()))
            else:
                st.info("No localizations recorded.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the Backend API. Make sure FastAPI is running on port 8000.")

elif choice == "Advanced Reports":
    st.header("Advanced Reports & Analysis")
    try:
        st.subheader("1. Seizure Frequency Analysis")
        s_res = requests.get(f"{API_URL}/analytics/seizures")
        seizure_data = s_res.json() if s_res.status_code == 200 else []
        
        if seizure_data:
            seizure_df = pd.DataFrame(seizure_data)
            fig = px.bar(seizure_df, x="Date", y="SeizureCount", title="Seizure Events Over Time", labels={'Date': 'Date', 'SeizureCount': 'Number of Seizures'}, color="SeizureCount", color_continuous_scale="Reds")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No seizure data found.")
            
        st.markdown("---")
        
        st.subheader("2. Critical Patients (Coma Analysis)")
        st.write("Patients with severe coma (GCS Total <= 8).")
        c_res = requests.get(f"{API_URL}/analytics/critical")
        critical_data = c_res.json() if c_res.status_code == 200 else []
        
        if critical_data:
            critical_df = pd.DataFrame(critical_data)
            st.error(" Critical patients identified based on recent GCS scores.")
            st.dataframe(critical_df)
        else:
            st.success("No critical patients matching severe coma criteria at the moment.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the Backend API. Make sure FastAPI is running on port 8000.")
