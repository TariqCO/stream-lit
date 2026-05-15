import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import os
import re
import hashlib
import uuid

st.set_page_config(
    page_title="Course Registration",
    page_icon="📋",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background-color: #f5f5f4;
}

#MainMenu, footer { visibility: hidden; }

/* Metric cards */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e7e5e4;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] p { color: #78716c !important; font-size: 0.78rem !important; font-weight: 500 !important; }
[data-testid="stMetricValue"]   { color: #1c1917 !important; font-size: 1.7rem !important; font-weight: 600 !important; }

/* Buttons */
.stButton > button {
    background: #1c1917 !important;
    color: #fafaf9 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.6rem !important;
    letter-spacing: 0.01em !important;
    transition: background 0.15s ease !important;
    width: 100%;
}
.stButton > button:hover {
    background: #292524 !important;
}

/* Download button */
.stDownloadButton > button {
    background: #ffffff !important;
    color: #44403c !important;
    border: 1px solid #d6d3d1 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    width: auto !important;
}
.stDownloadButton > button:hover {
    background: #fafaf9 !important;
    border-color: #a8a29e !important;
}

/* Inputs */
input[type="text"], input[type="password"], input[type="number"] {
    border: 1px solid #d6d3d1 !important;
    border-radius: 8px !important;
    background: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1c1917 !important;
    font-size: 0.9rem !important;
}
input:focus {
    border-color: #78716c !important;
    box-shadow: 0 0 0 2px rgba(120,113,108,0.12) !important;
}

/* Selectbox */
[data-baseweb="select"] > div {
    border: 1px solid #d6d3d1 !important;
    border-radius: 8px !important;
    background: #ffffff !important;
}

/* Labels */
label, .stTextInput label, .stSelectbox label, .stNumberInput label {
    color: #57534e !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

/* Headings */
h1 { color: #1c1917 !important; font-weight: 600 !important; font-size: 1.5rem !important; letter-spacing: -0.02em !important; }
h2 { color: #292524 !important; font-weight: 600 !important; font-size: 1.2rem !important; }
h3 { color: #44403c !important; font-weight: 500 !important; }
p, .stMarkdown p { color: #57534e !important; font-size: 0.9rem !important; }

/* Alert boxes */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border: 1px solid #e7e5e4 !important;
    font-size: 0.88rem !important;
}

/* Tabs */
[data-testid="stTabs"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: #78716c !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #1c1917 !important;
    border-bottom-color: #1c1917 !important;
}

/* Form container */
[data-testid="stForm"] {
    background: #ffffff;
    border: 1px solid #e7e5e4;
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #e7e5e4 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* Caption */
.stCaption, [data-testid="stCaption"] {
    color: #a8a29e !important;
    font-size: 0.78rem !important;
}

/* ID card */
.id-card {
    background: #ffffff;
    border: 1px solid #e7e5e4;
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    margin: 1rem 0;
}
.id-card-name {
    font-size: 1.15rem;
    font-weight: 600;
    color: #1c1917;
    margin-bottom: 4px;
}
.id-card-id {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: #a8a29e;
    letter-spacing: 0.06em;
    margin-bottom: 12px;
}
.id-card-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}
.id-card-badge {
    background: #f5f5f4;
    border: 1px solid #e7e5e4;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.78rem;
    color: #57534e;
    font-weight: 500;
}

/* Outline grid */
.outline-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 12px;
}
.outline-item {
    background: #ffffff;
    border: 1px solid #e7e5e4;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 0.83rem;
    color: #44403c;
    display: flex;
    align-items: center;
    gap: 8px;
}
.outline-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #a8a29e;
    min-width: 18px;
}

/* Section label */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #a8a29e;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
CSV_FILE = "user_reg.csv"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

CITIES     = ["Karachi", "Islamabad", "Lahore", "Peshawar", "Rawalpindi", "Multan", "Quetta", "Faisalabad"]
COURSES    = ["Web Development", "AI/ML", "Digital Marketing", "Power BI", "Cyber Security", "Data Analyst"]
GENDERS    = ["Male", "Female", "Prefer not to say"]
EDUCATIONS = ["Matric", "Intermediate", "Bachelor's", "Master's", "PhD"]

COURSE_OUTLINES = {
    "Web Development":   ["HTML & CSS Fundamentals", "JavaScript Essentials", "Responsive Design", "React Basics", "Backend (Node/Express)", "REST APIs", "Deployment"],
    "AI/ML":             ["Python Refresher", "NumPy & Pandas", "Data Preprocessing", "Supervised Learning", "Unsupervised Learning", "Model Evaluation", "Deep Learning Intro"],
    "Digital Marketing": ["Marketing Fundamentals", "SEO & SEM", "Social Media Strategy", "Email Marketing", "Google Analytics", "Content Marketing", "Paid Ads"],
    "Power BI":          ["Data Sources & Import", "Power Query (ETL)", "Data Modeling", "DAX Basics", "Building Reports", "Dashboards & Visuals", "Publishing"],
    "Cyber Security":    ["Networking Fundamentals", "Linux Basics", "Threats & Attacks", "Cryptography", "Ethical Hacking Intro", "Firewalls & IDS", "Security Auditing"],
    "Data Analyst":      ["Excel for Data", "SQL Fundamentals", "Python (Pandas/Matplotlib)", "Data Cleaning", "Exploratory Analysis", "Storytelling with Data", "Capstone Project"],
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def load_data():
    return pd.read_csv(CSV_FILE) if os.path.exists(CSV_FILE) else pd.DataFrame()

def save_registration(name, email, cnic, city, contact, age, gender, education, course):
    reg_id = "REG-" + str(uuid.uuid4())[:8].upper()
    row = pd.DataFrame([{
        "ID": reg_id, "Name": name, "Email": email, "CNIC": cnic,
        "City": city, "Contact": contact, "Age": age,
        "Gender": gender, "Education": education, "Course": course
    }])
    if os.path.exists(CSV_FILE):
        pd.concat([pd.read_csv(CSV_FILE), row], ignore_index=True).to_csv(CSV_FILE, index=False)
    else:
        row.to_csv(CSV_FILE, index=False)
    return reg_id

def is_duplicate(email, cnic):
    data = load_data()
    return not data.empty and ((data["Email"] == email) | (data["CNIC"] == cnic)).any()

def valid_email(v):   return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", v))
def valid_cnic(v):    return bool(re.match(r"^\d{5}-\d{7}-\d$", v))
def valid_contact(v): return bool(re.match(r"^(03\d{9}|\+923\d{9})$", v))

def chart_style():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#57534e",
        font_family="DM Sans",
        margin=dict(t=36, b=0, l=0, r=0)
    )

PALETTE = ["#1c1917", "#44403c", "#78716c", "#a8a29e", "#d6d3d1"]

# ── Nav ────────────────────────────────────────────────────────────────────────
select = option_menu(
    menu_title=None,
    options=["Register", "Admin"],
    icons=["person", "shield-lock"],
    orientation="horizontal",
    styles={
        "container":         {"background-color": "#ffffff", "border": "1px solid #e7e5e4", "border-radius": "10px", "padding": "4px"},
        "nav-link":          {"font-family": "DM Sans, sans-serif", "font-size": "0.88rem", "color": "#78716c", "border-radius": "7px", "font-weight": "500"},
        "nav-link-selected": {"background": "#1c1917", "color": "#fafaf9", "font-weight": "600"},
    }
)

# ══════════════════════════════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════════════════════════════
if select == "Admin":

    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## Admin Access")
        st.caption("Enter your password to continue.")
        pwd = st.text_input("Password", type="password", placeholder="••••••••")
        if st.button("Continue"):
            if hashlib.sha256(pwd.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Wrong password.")
        st.caption("Default password: `admin123`")

    else:
        col_title, col_logout = st.columns([5, 1])
        with col_title:
            st.markdown("## Dashboard")
        with col_logout:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Log out"):
                st.session_state.admin_auth = False
                st.rerun()

        tab1, tab2 = st.tabs(["Overview", "Records"])

        with tab1:
            data = load_data()
            if data.empty:
                st.info("No registrations yet.")
            else:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total",  data["CNIC"].nunique())
                c2.metric("Avg Age", f"{round(data['Age'].mean())}")
                c3.metric("Male",   int((data["Gender"] == "Male").sum()))
                c4.metric("Female", int((data["Gender"] == "Female").sum()))

                st.markdown("<br>", unsafe_allow_html=True)
                col_a, col_b = st.columns(2)

                with col_a:
                    df = data["Course"].value_counts().reset_index()
                    fig = px.pie(df, names="Course", values="count", hole=0.5,
                                 color_discrete_sequence=PALETTE)
                    fig.update_layout(**chart_style(), title_text="By course", title_font_size=13)
                    fig.update_traces(textfont_size=11)
                    st.plotly_chart(fig, use_container_width=True)

                with col_b:
                    df = data["Gender"].value_counts().reset_index()
                    fig = px.pie(df, names="Gender", values="count", hole=0.5,
                                 color_discrete_sequence=PALETTE)
                    fig.update_layout(**chart_style(), title_text="By gender", title_font_size=13)
                    fig.update_traces(textfont_size=11)
                    st.plotly_chart(fig, use_container_width=True)

                df = data["City"].value_counts().reset_index()
                fig = px.bar(df, x="City", y="count", color_discrete_sequence=["#44403c"])
                fig.update_layout(**chart_style(), title_text="By city", title_font_size=13,
                                  showlegend=False,
                                  xaxis=dict(tickfont_size=11),
                                  yaxis=dict(tickfont_size=11))
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)

                df = data["Education"].value_counts().reset_index()
                fig = px.bar(df, x="Education", y="count", color_discrete_sequence=["#78716c"])
                fig.update_layout(**chart_style(), title_text="By education", title_font_size=13,
                                  showlegend=False,
                                  xaxis=dict(tickfont_size=11),
                                  yaxis=dict(tickfont_size=11))
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            data = load_data()
            if data.empty:
                st.info("No registrations yet.")
            else:
                f1, f2 = st.columns(2)
                with f1:
                    sel_courses = st.multiselect("Course", data["Course"].unique(), default=list(data["Course"].unique()))
                with f2:
                    sel_cities = st.multiselect("City", data["City"].unique(), default=list(data["City"].unique()))

                filtered = data[data["Course"].isin(sel_courses) & data["City"].isin(sel_cities)]
                st.caption(f"{len(filtered)} of {len(data)} records")
                st.dataframe(filtered, use_container_width=True, hide_index=True)
                st.download_button("Download CSV", filtered.to_csv(index=False), "registrations.csv", "text/csv")

# ══════════════════════════════════════════════════════════════════════════════
# USER
# ══════════════════════════════════════════════════════════════════════════════
elif select == "Register":
    tab1, tab2 = st.tabs(["Registration", "My Card"])

    with tab1:
        st.markdown("## Registration")
        st.caption("All fields are required.")
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("reg_form"):
            c1, c2 = st.columns(2)
            with c1:
                name      = st.text_input("Full Name", placeholder="Muhammad Ali")
                email     = st.text_input("Email", placeholder="ali@example.com")
                cnic      = st.text_input("CNIC", placeholder="42101-1234567-1")
                city      = st.selectbox("City", CITIES)
            with c2:
                contact   = st.text_input("Contact", placeholder="03001234567")
                age       = st.number_input("Age", min_value=18, max_value=60, value=22)
                gender    = st.selectbox("Gender", GENDERS)
                education = st.selectbox("Education", EDUCATIONS)

            course    = st.selectbox("Course", COURSES)
            submitted = st.form_submit_button("Submit Registration")

        if submitted:
            errors = []
            if not name.strip():           errors.append("Name is required.")
            if not valid_email(email):     errors.append("Enter a valid email address.")
            if not valid_cnic(cnic):       errors.append("CNIC format: 42101-1234567-1")
            if not valid_contact(contact): errors.append("Enter a valid Pakistani number (03xxxxxxxxx).")

            if errors:
                for e in errors:
                    st.error(e)
            elif is_duplicate(email, cnic):
                st.warning("This email or CNIC is already registered.")
            else:
                reg_id = save_registration(name, email, cnic, city, contact, age, gender, education, course)
                st.success(f"Registered successfully. Your ID: **{reg_id}**")
                st.balloons()
                st.caption("Save this ID — you'll need it to retrieve your card.")

    with tab2:
        st.markdown("## Your Registration Card")
        st.caption("Enter the details you registered with.")
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("lookup_form"):
            l_email = st.text_input("Email", placeholder="ali@example.com")
            l_cnic  = st.text_input("CNIC", placeholder="42101-1234567-1")
            lookup  = st.form_submit_button("Retrieve")

        if lookup:
            data = load_data()
            if data.empty:
                st.info("No registrations found.")
            else:
                match = data[(data["Email"] == l_email.strip()) & (data["CNIC"] == l_cnic.strip())]
                if match.empty:
                    st.error("No record found for this email and CNIC combination.")
                else:
                    row    = match.iloc[0]
                    reg_id = row.get("ID", "—")

                    st.markdown(f"""
                    <div class="id-card">
                        <div class="id-card-name">{row['Name']}</div>
                        <div class="id-card-id">{reg_id}</div>
                        <div class="id-card-meta">
                            <span class="id-card-badge">{row['Course']}</span>
                            <span class="id-card-badge">{row['City']}</span>
                            <span class="id-card-badge">{row['Education']}</span>
                            <span class="id-card-badge">{row['Gender']}</span>
                            <span class="id-card-badge">Age {row['Age']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    outline = COURSE_OUTLINES.get(row["Course"], [])
                    if outline:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown(f'<div class="section-label">{row["Course"]} — Course Outline</div>', unsafe_allow_html=True)
                        items = "".join(
                            f'<div class="outline-item"><span class="outline-num">0{i+1}</span>{topic}</div>'
                            for i, topic in enumerate(outline)
                        )
                        st.markdown(f'<div class="outline-grid">{items}</div>', unsafe_allow_html=True)
