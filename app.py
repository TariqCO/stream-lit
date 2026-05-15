import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import os 

st.set_page_config(
    page_title="Course Registration Form",
    layout="centered"
)


select = option_menu(
    menu_title=None,
    options=["User","Admin"],
    icons=["admin","user",],
    orientation="horizontal"
)

CSV_FILE = "user_reg.csv"

def save_to_csv(name, email, cnic, city, contact, age, gender, education, course):
    new_data = pd.DataFrame({
        "Name": [name],
        "Email": [email],
        "CNIC": [cnic],
        "City": [city],
        "Contact": [contact],
        "Age": [age],
        "Gender": [gender],
        "Education": [education],
        "Course": [course]

    })
    
    if os.path.exists(CSV_FILE):
        existing_data = pd.read_csv(CSV_FILE)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_csv(CSV_FILE, index=False)
    else:
        new_data.to_csv(CSV_FILE, index=False)

    return True



if select == "Admin":
    tab1, tab2= st.tabs(["Stats", "Information"])
    with tab1:
        st.title("Course Registration Statistics")
        if os.path.exists(CSV_FILE):
            data = pd.read_csv(CSV_FILE)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label="Total Registrations", value=data["CNIC"].nunique())
            col2.metric(label="Average Age", value=round(data["Age"].mean()))
            col3.metric(label="Total Male", value=(data["Gender"] == "Male").sum())
            col4.metric(label="Total Female", value=(data["Gender"] == "Female").sum())


            genderCount = data["Gender"].value_counts().reset_index()
            fig1 = px.bar(genderCount, x="Gender", y="count", color="Gender")
            st.plotly_chart(fig1)

            courseCount = data["Course"].value_counts().reset_index()
            fig2 = px.pie(courseCount, names="Course", values="count", color="Course")
            st.plotly_chart(fig2)


            cityCount = data["City"].value_counts().reset_index()
            fig3 = px.bar(cityCount, x="City", y="count", color="City")
            st.plotly_chart(fig3)

            eduCount = data["Education"].value_counts().reset_index()
            fig4 = px.pie(eduCount, names="Education", values="count", color="Education")
            st.plotly_chart(fig4)

        else:
            st.info("No Data Saved Yet")

    with tab2:
        st.title("Information")
        if os.path.exists(CSV_FILE):
            data = pd.read_csv(CSV_FILE)

            options = data["Course"].unique() 
            selected = st.multiselect("Select Course", options , ["Web Development"])
            filtered_df = data[data['Course'].isin(selected)]
            st.dataframe(filtered_df)


            csv = filtered_df.to_csv(index=False)

            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="user_data.csv",
                mime="text/csv"
            )    
        else:
            st.info("No Data Saved Yet")    

elif select == "User":
    tab1, tab2 = st.tabs(["Registration", "Outline"])
    with tab1:
        st.title("Registration")
        with st.form("Enter Registration Form"):
            name = st.text_input("Name", placeholder="Enter your Full Name")
            email = st.text_input("Email", placeholder="Enter your Email Address")
            cnic = st.text_input("CNIC", placeholder="Enter your CNIC")
            city = st.selectbox("City",  ["Karachi", "Islamabad", "Lahore", "Peshawar", "Rawalpindi", "Multan"])
            contact = st.text_input("Contact", placeholder="Enter your Mobile Number")
            age = st.number_input("Age", min_value=18, max_value=60)
            course = st.selectbox("Course", ["Web Development", "AI/ML", "Digital Marketing", "Power BI", "Cyber Security", "Data Analyist"])
            gender = st.selectbox("Gender", ["Male", "Female"])
            education = st.selectbox("Education", ["Matric", "Intermediate", " Bachelor's" ,"Master's", "PhD"] )

            submited = st.form_submit_button("Register")

        if submited:
            if name and email and cnic and contact and age and course and gender and education and city:
                save_to_csv(name, email, cnic, city, contact, age, gender, education, course)
                st.success("Registration Successful!")
                st.balloons()
            else:
                st.error("Please fill all required fields!")
            
    with tab2:
        st.title("Get your ID and Course Outline")
        with st.form("Create your id card"):
            email = st.text_input("Enter your email", placeholder="Enter your Email Address")
            cnic = st.text_input("Enter your CNIC", placeholder="Enter your CNIC")

            create = st.form_submit_button("Create ID")

            if create:
                if os.path.exists(CSV_FILE):
                    data = pd.read_csv(CSV_FILE)

                    candidateData = data[data["Email"] == email]
                    
                    if len(candidateData) == 0:
                        st.info("No Candidate registered with this Email or CNIC")
                    else:
                        candidateData = candidateData.iloc[0]

                        st.success(f" This is your Course Registration Card ---> ID: #{candidateData["Age"] * 2}")


                        course_outlines = {
                            "Web Development": [
                                "HTML/CSS Fundamentals",
                                "JavaScript Essentials",
                                "Responsive Design",
                                "React Basics",
                                "Backend Intro (Node/Express)",
                                "Deployment"
                            ],
                            "AI/ML": [
                                "Python Refresher",
                                "NumPy & Pandas",
                                "Data Preprocessing",
                                "Supervised Learning",
                                "Unsupervised Learning",
                                "Model Evaluation",
                                "Intro to Deep Learning"
                            ],
                            "Digital Marketing": [
                                "Marketing Fundamentals",
                                "SEO & SEM",
                                "Social Media Strategy",
                                "Email Marketing",
                                "Google Analytics",
                                "Content Marketing",
                                "Paid Ads (Meta/Google)"
                            ],
                            "Power BI": [
                                "Data Sources & Import",
                                "Power Query (ETL)",
                                "Data Modeling",
                                "DAX Basics",
                                "Building Reports",
                                "Dashboards & Visuals",
                                "Publishing & Sharing"
                            ],
                            "Cyber Security": [
                                "Networking Fundamentals",
                                "Linux Basics",
                                "Threats & Attack Types",
                                "Cryptography",
                                "Ethical Hacking Intro",
                                "Firewalls & IDS",
                                "Security Auditing"
                            ],
                            "Data Analyst": [
                                "Excel for Data",
                                "SQL Fundamentals",
                                "Python (Pandas/Matplotlib)",
                                "Data Cleaning",
                                "Exploratory Data Analysis",
                                "Storytelling with Data",
                                "Capstone Project"
                            ]
                        }

                        course = candidateData["Course"]
                        outline = course_outlines[course]

                        if outline:
                            st.subheader(f"{candidateData["Course"]} — Course Outline")

                            for topic in outline:
                                st.markdown(f"- {topic}")

                else:
                    st.info("No data saved yet")    
