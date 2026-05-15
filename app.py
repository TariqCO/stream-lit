import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import os
import re
import hashlib
import uuid

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduReg · Course Registration",
    page_icon="🎓",
    layout="centered"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #1a1a4e, #24243e);
    min-height: 100vh;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Top nav override */
section[data-testid="stSidebar"] { display: none; }

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 1rem;
    backdrop-filter: blur(10px);
}

[data-testid="stMetricLabel"] { color: #a0aec0 !important; font-size: 0.78rem; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 1.8rem; font-weight: 700; }

/* Form inputs */
input, select, textarea {
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    transition: opacity 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Download button */
.stDownloadButton > button {
    background: rgba(255,255,255,0.08) !important;
    color: #a0aec0 !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
}

/* ID card */
.id-card {
    background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
    border: 1px solid rgba(102,126,234,0.4);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    backdrop-filter: blur(12px);
}
.id-card h3 { color: #e2e8f0; margin-bottom: 0.3rem; font-size: 1.4rem; }
.id-card .id-number {
    font-family: 'JetBrains Mono', monospace;
    color: #667eea;
    font-size: 1rem;
    letter-spacing: 0.08em;
}
.id-card .meta { color: #a0aec0; font-size: 0.85rem; margin-top: 0.6rem; }

/* Outline topic pill */
.topic-pill {
    display: inline-block;
    background: rgba(102,126,234,0.15);
    border: 1px solid rgba(102,126,234,0.3);
    border-radius: 20px;
    padding: 0.35rem 0.9rem;
    margin: 0.25rem;
    color: #c3d0ff;
    font-size: 0.82rem;
}

/* Tabs */
[data-testid="stTab"] button {
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Info/success/error */
[data-testid="stAlert"] { border-radius: 12px !important; }

/* Section headers */
h1 { color: #e2e8f0 !important; font-weight: 700 !important; }
h2, h3 { color: #cbd5e0 !important; }
label { color: #a0aec0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
CSV_FILE = "user_reg.csv"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()  # Change this!

CITIES = ["Karachi", "Islamabad", "Lahore", "Peshawar", "Rawalpindi", "Multan", "Quetta", "Faisalabad"]
COURSES = ["Web Development", "AI/ML", "Digital Marketing", "Power BI", "Cyber Security", "Data Analyst"]
GENDERS = ["Male", "Female", "Prefer not to say"]
EDUCATIONS = ["Matric", "Intermediate", "Bachelor's", "Master's", "PhD"]

COURSE_OUTLINES = {
    "Web Development": [
        "HTML & CSS Fundamentals", "JavaScript Essentials", "Responsive Design",
        "React Basics", "Backend Intro (Node/Express)", "REST APIs", "Deployment & DevOps"
    ],
    "AI/ML": [
        "Python Refresher", "NumPy & Pandas", "Data Preprocessing",
        "Supervised Learning", "Unsupervised Learning", "Model Evaluation", "Intro to Deep Learning"
    ],
    "Digital Marketing": [
        "Marketing Fundamentals", "SEO & SEM", "Social Media Strategy",
        "Email Marketing", "Google Analytics", "Content Marketing", "Paid Ads (Meta/Google)"
    ],
    "Power BI": [
        "Data Sources & Import", "Power Query (ETL)", "Data Modeling",
        "DAX Basics", "Building Reports", "Dashboards & Visuals", "Publishing & Sharing"
    ],
    "Cyber Security": [
        "Networking Fundamentals", "Linux Basics", "Threats & Attack Types",
        "Cryptography", "Ethical Hacking Intro", "Firewalls & IDS", "Security Auditing"
    ],
    "Data Analyst": [
        "Excel for Data", "SQL Fundamentals", "Python (Pandas/Matplotlib)",
        "Data Cleaning", "Exploratory Data Analysis", "Storytelling with Data", "Capstone Project"
    ]
}

# ─── Helpers ─────────────────────────────────────────────────────────────────

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()

def save_to_csv(name, email, cnic, city, contact, age, gender, education, course):
    reg_id = "EDU-" + str(uuid.uuid4())[:8].upper()
    new_data = pd.DataFrame({
        "ID": [reg_id], "Name": [name], "Email": [email], "CNIC": [cnic],
        "City": [city], "Contact": [contact], "Age": [age],
        "Gender": [gender], "Education": [education], "Course": [course]
    })
    if os.path.exists(CSV_FILE):
        existing = pd.read_csv(CSV_FILE)
        pd.concat([existing, new_data], ignore_index=True).to_csv(CSV_FILE, index=False)
    else:
        new_data.to_csv(CSV_FILE, index=False)
    return reg_id

def is_duplicate(email, cnic):
    data = load_data()
    if data.empty:
        return False
    return ((data["Email"] == email) | (data["CNIC"] == cnic)).any()

def validate_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email)

def validate_cnic(cnic):
    return re.match(r"^\d{5}-\d{7}-\d$", cnic)

def validate_contact(contact):
    return re.match(r"^(03\d{9}|\+923\d{9})$", contact)

def plotly_style():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#a0aec0",
        font_family="Sora",
    )

# ─── Nav ─────────────────────────────────────────────────────────────────────
select = option_menu(
    menu_title=None,
    options=["Registration", "Admin"],
    icons=["person-fill", "shield-lock-fill"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "rgba(255,255,255,0.04)", "border-radius": "12px", "padding": "6px"},
        "nav-link": {"font-family": "Sora, sans-serif", "color": "#a0aec0", "border-radius": "8px"},
        "nav-link-selected": {"background": "linear-gradient(135deg,#667eea,#764ba2)", "color": "white", "font-weight": "600"},
    }
)

# ═══════════════════════════════════════════════════════════════════════
# ADMIN
# ═══════════════════════════════════════════════════════════════════════
if select == "Admin":

    # Simple session-based auth
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        st.markdown("## 🔐 Admin Login")
        pwd = st.text_input("Password", type="password", placeholder="Enter admin password")
        if st.button("Login"):
            if hashlib.sha256(pwd.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        st.caption("Default password: `admin123` — change `ADMIN_PASSWORD_HASH` in the code.")
    else:
        if st.button("Logout"):
            st.session_state.admin_auth = False
            st.rerun()

        tab1, tab2 = st.tabs(["📊 Statistics", "🗂 Data"])

        with tab1:
            st.markdown("## Course Registration Statistics")
            data = load_data()
            if data.empty:
                st.info("No registrations yet.")
            else:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Registrations", data["CNIC"].nunique())
                col2.metric("Average Age", f"{round(data['Age'].mean())} yrs")
                col3.metric("Male", int((data["Gender"] == "Male").sum()))
                col4.metric("Female", int((data["Gender"] == "Female").sum()))

                st.markdown("---")
                c1, c2 = st.columns(2)

                with c1:
                    gender_df = data["Gender"].value_counts().reset_index()
                    fig1 = px.pie(gender_df, names="Gender", values="count",
                                  title="Gender Distribution",
                                  color_discrete_sequence=px.colors.sequential.Purpor)
                    fig1.update_layout(**plotly_style())
                    st.plotly_chart(fig1, use_container_width=True)

                with c2:
                    course_df = data["Course"].value_counts().reset_index()
                    fig2 = px.pie(course_df, names="Course", values="count",
                                  title="Course Breakdown",
                                  color_discrete_sequence=px.colors.sequential.Plasma)
                    fig2.update_layout(**plotly_style())
                    st.plotly_chart(fig2, use_container_width=True)

                city_df = data["City"].value_counts().reset_index()
                fig3 = px.bar(city_df, x="City", y="count", title="Registrations by City",
                              color="count", color_continuous_scale="Purpor")
                fig3.update_layout(**plotly_style(), showlegend=False)
                st.plotly_chart(fig3, use_container_width=True)

                edu_df = data["Education"].value_counts().reset_index()
                fig4 = px.bar(edu_df, x="Education", y="count", title="Education Level",
                              color="count", color_continuous_scale="Plasma")
                fig4.update_layout(**plotly_style(), showlegend=False)
                st.plotly_chart(fig4, use_container_width=True)

        with tab2:
            st.markdown("## Registered Candidates")
            data = load_data()
            if data.empty:
                st.info("No registrations yet.")
            else:
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    selected_courses = st.multiselect("Filter by Course", data["Course"].unique(),
                                                      default=list(data["Course"].unique()))
                with col_f2:
                    selected_cities = st.multiselect("Filter by City", data["City"].unique(),
                                                     default=list(data["City"].unique()))

                filtered = data[data["Course"].isin(selected_courses) & data["City"].isin(selected_cities)]
                st.caption(f"Showing **{len(filtered)}** of **{len(data)}** records")
                st.dataframe(filtered, use_container_width=True, hide_index=True)

                st.download_button(
                    label="⬇ Download as CSV",
                    data=filtered.to_csv(index=False),
                    file_name="registrations.csv",
                    mime="text/csv"
                )

# ═══════════════════════════════════════════════════════════════════════
# USER
# ═══════════════════════════════════════════════════════════════════════
elif select == "Registration":
    tab1, tab2 = st.tabs(["📋 Register", "🪪 My Card & Outline"])

    with tab1:
        st.markdown("## 🎓 Course Registration")
        st.caption("Fill in the form below to register for a course.")

        with st.form("reg_form", clear_on_submit=False):
            c1, c2 = st.columns(2)
            with c1:
                name    = st.text_input("Full Name *", placeholder="Muhammad Ali")
                email   = st.text_input("Email *", placeholder="ali@example.com")
                cnic    = st.text_input("CNIC *", placeholder="42101-1234567-1")
                city    = st.selectbox("City *", CITIES)
            with c2:
                contact = st.text_input("Contact *", placeholder="03001234567")
                age     = st.number_input("Age *", min_value=18, max_value=60, value=22)
                gender  = st.selectbox("Gender *", GENDERS)
                education = st.selectbox("Education *", EDUCATIONS)

            course = st.selectbox("Course *", COURSES)
            submitted = st.form_submit_button("Register Now →")

        if submitted:
            errors = []
            if not name.strip():             errors.append("Name is required.")
            if not validate_email(email):    errors.append("Invalid email format.")
            if not validate_cnic(cnic):      errors.append("CNIC must be in format `42101-1234567-1`.")
            if not validate_contact(contact):errors.append("Contact must be a valid Pakistani number (e.g. 03001234567).")
            if not city:                     errors.append("City is required.")

            if errors:
                for e in errors:
                    st.error(e)
            elif is_duplicate(email, cnic):
                st.warning("⚠️ A registration with this Email or CNIC already exists.")
            else:
                reg_id = save_to_csv(name, email, cnic, city, contact, age, gender, education, course)
                st.success(f"✅ Registration successful! Your ID: **{reg_id}**")
                st.balloons()
                st.info("Save your ID — you'll need it to retrieve your card and course outline.")

    with tab2:
        st.markdown("## 🪪 Retrieve Your Card & Outline")
        with st.form("lookup_form"):
            l_email = st.text_input("Registered Email *", placeholder="ali@example.com")
            l_cnic  = st.text_input("CNIC *", placeholder="42101-1234567-1")
            lookup  = st.form_submit_button("Retrieve →")

        if lookup:
            data = load_data()
            if data.empty:
                st.info("No registrations found yet.")
            else:
                match = data[(data["Email"] == l_email.strip()) & (data["CNIC"] == l_cnic.strip())]
                if match.empty:
                    st.error("No registration found for the provided Email and CNIC combination.")
                else:
                    row = match.iloc[0]
                    # ID Card
                    reg_id = row.get("ID", "EDU-LEGACY")
                    st.markdown(f"""
                    <div class="id-card">
                        <h3>🎓 {row['Name']}</h3>
                        <div class="id-number">{reg_id}</div>
                        <div class="meta">
                            📚 {row['Course']} &nbsp;|&nbsp; 🏙 {row['City']} &nbsp;|&nbsp;
                            🎓 {row['Education']} &nbsp;|&nbsp; 📅 Age {row['Age']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Course Outline
                    course = row["Course"]
                    outline = COURSE_OUTLINES.get(course, [])
                    if outline:
                        st.markdown(f"### 📖 {course} — Course Outline")
                        pills_html = "".join(
                            f'<span class="topic-pill">✦ {topic}</span>'
                            for topic in outline
                        )
                        st.markdown(f"<div style='line-height:2.2'>{pills_html}</div>", unsafe_allow_html=True)
