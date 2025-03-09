import streamlit as st
import requests

st.set_page_config(page_title="Healthcare Navigator", page_icon="🏥")

api_url = "http://127.0.0.1:5000/search_doctors"
page = st.sidebar.radio("Navigate", ["User Information", "Symptoms"])

st.markdown("<h1 style='text-align: center; color: #24B0BA;'>Healthcare Navigator</h1>", unsafe_allow_html=True)

if page == "User Information":
    st.markdown("<h2 style='text-align: center;'>Please fill out the form below</h2>", unsafe_allow_html=True)
    
    with st.form(key="info_form"):
        name = st.text_input("Enter your Name")
        age = st.number_input("Enter your Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Select Gender", ["Man", "Woman", "Non-Binary", "Would Rather Not Say"])
        insurance = st.selectbox("Select Insurance Provider", 
                                 ["Cigna", "Aetna", "Blue Cross Blue Shield", "United Healthcare"])
        submit_button = st.form_submit_button(label="Submit Information")

    if submit_button:
        st.success(f"Form submitted successfully! \n\n**Name:** {name}\n**Age:** {age}\n**Gender:** {gender}\n**Insurance:** {insurance}")
        
        payload = {
            "name": name,
            "age": age,
            "gender": gender,
            "insurance": insurance
        }
        
        response = requests.post(api_url, json=payload)
        
        # error if no doc recs
        if response.status_code == 200:
            st.write("### Recommended Doctors:")
            st.write(response.json())
        else:
            st.error("Failed to fetch doctor recommendations. Please try again later.")

elif page == "Symptoms":
    st.markdown("<h2 style='text-align: center;'>Please Tell Us Your Symptoms</h2>", unsafe_allow_html=True)
    symptoms = st.text_area("Describe your symptoms in detail")
    
    if st.button("Submit Symptoms"):
        st.success("Symptoms submitted successfully! We will analyze your input and provide recommendations.")
        
        symptoms_payload = {"symptoms": symptoms}
        response = requests.post(api_url, json=symptoms_payload)

        if response.status_code == 200:
            st.write("### Recommended Doctors:")
            st.write(response.json())
        else:
            st.error("Failed to fetch doctor recommendations. Please try again later.")

