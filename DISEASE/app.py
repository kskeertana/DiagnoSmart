import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import webbrowser

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Function to load CSS from a file
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the custom CSS
load_css(os.path.join(os.path.dirname(__file__), "styles.css"))

# Getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# Loading the saved models
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))


# Styling for DiagnoSmart header
st.markdown(
    "<h1 style='text-align: center; color: #0ad0ee; font-weight: bold;'>DiagnoSmart</h1>",
    unsafe_allow_html=True
)

# Sidebar for navigation with custom styling
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',
                           ['Diabetes Prediction', 'Heart Disease Prediction', 'Back'],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart', 'arrow-left-circle'],
                           default_index=0,
                           styles={
                               "container": {"padding": "5px", "background-color": "#333"},
                               "icon": {"color": "white", "font-size": "25px"},
                               "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#0ad0ee"},
                               "nav-link-selected": {"background-color": "#0ad0ee"},
                           })

def open_localhost():
    webbrowser.open_new_tab('http://localhost:5000/')

# Handle the Back button
if selected == 'Back':
    open_localhost()

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    # Page title
    st.title('Diabetes Prediction using ML')

    # Input fields
    col1, col2, col3 = st.columns(3)
    with col1:
        Pregnancies = st.text_input('Number of Pregnancies', key='pregnancies')
        SkinThickness = st.text_input('Skin Thickness value', key='skin_thickness')
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value', key='dpf')

    with col2:
        Glucose = st.text_input('Glucose Level', key='glucose')
        Insulin = st.text_input('Insulin Level', key='insulin')
        BMI = st.text_input('BMI value', key='bmi')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value', key='blood_pressure')
        Age = st.text_input('Age of the Person', key='age')

    # Prediction button
    if st.button('Diabetes Test Result', key='diabetes_button'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                      BMI, DiabetesPedigreeFunction, Age]
        user_input = [float(x) for x in user_input]

        diab_prediction = diabetes_model.predict([user_input])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person is diabetic'
        else:
            diab_diagnosis = 'The person is not diabetic'

        st.success(diab_diagnosis)

# Heart Disease Prediction Page
elif selected == 'Heart Disease Prediction':
    # Page title
    st.title('Heart Disease Prediction using ML')

    # Input fields
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.text_input('Age', key='heart_age')
        restecg = st.text_input('Resting Electrocardiographic results', key='restecg')
        oldpeak = st.text_input('ST depression induced by exercise', key='oldpeak')
        ca = st.text_input('Major vessels colored by flourosopy', key='ca')
        RPDE = st.text_input('RPDE', key='RPDE')
        spread1 = st.text_input('spread1', key='spread1')

    with col2:
        sex = st.text_input('Sex', key='heart_sex')
        thalach = st.text_input('Maximum Heart Rate achieved', key='thalach')
        slope = st.text_input('Slope of the peak exercise ST segment', key='slope')
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect', key='thal')
        DFA = st.text_input('DFA', key='DFA')
        spread2 = st.text_input('spread2', key='spread2')

    with col3:
        cp = st.text_input('Chest Pain types', key='cp')
        exang = st.text_input('Exercise Induced Angina', key='exang')
        ca = st.text_input('Major vessels colored by flourosopy', key='ca_duplicate')
        NHR = st.text_input('NHR', key='NHR')
        HNR = st.text_input('HNR', key='HNR')
        D2 = st.text_input('D2', key='D2')
        PPE = st.text_input('PPE', key='PPE')

    # Prediction button
    if st.button('Heart Disease Test Result', key='heart_button'):
        user_input = [age, sex, cp, restecg, thalach, exang, oldpeak, slope, ca, thal, NHR, HNR, RPDE, DFA, spread1, spread2]
        user_input = [float(x) for x in user_input]

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
        else:
            heart_diagnosis = 'The person does not have any heart disease'

        st.success(heart_diagnosis)
