import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import os

st.set_page_config(
    page_title="Course Registration",
    page_icon="🎓",
    layout="centered"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f5f7fa;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
[data-testid="stMetricLabel"] {
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 700;
    color: #1e293b;
}

/* Buttons */
.stFormSubmitButton > button, .stButton > button {
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1.6rem;
    font-weight: 600;
    font-size: 0.95rem;
    transition: background 0.2s;
}
.stFormSubmitButton > button:hover, .stButton > button:hover {
    background: #4f46e5;
    color: white;
}
.stDownloadButton > button {
    background: #f1f5f9;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-weight: 500;
}
.stDownloadButton > button:hover {
    background: #e2e8f0;
    color: #1e293b;
}

/* Tabs */
[data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 2px solid #e2e8f0;
}
[data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important;
    font-weight: 500;
    color: #64748b;
}
[aria-selected="true"] {
    color: #6366f1 !important;
    border-bottom: 2px solid #6366f1 !important;
}

/* ID card */
.id-card {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 16px;
    padding: 28px 32px;
    color: white;
    margin: 20px 0;
    box-shadow: 0 8px 32px rgba(99,102,241,0.25);
}
.id-card h2 {
    margin: 0 0 4px 0;
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
}
.id-card .id-num {
    font-size: 0.85rem;
    opacity: 0.8;
    margin-bottom: 20px;
    font-family: monospace;
    letter-spacing: 0.1em;
}
.id-card .id-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
}
.id-card .id-field label {
    font-size: 0.7rem;
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    display: block;
    margin-bottom: 2px;
}
.id-card .id-field span {
    font-size: 0.95rem;
    font-weight: 600;
}
.id-card .badge {
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin-top: 16px;
    border: 1px solid rgba(255,255,255,0.3);
}

/* Course outline items */
.outline-item {
    background: white;
    border-left: 4px solid #6366f1;
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    margin: 6px 0;
    font-size: 0.93rem;
    color: #334155;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

h1 { color: #1e293b !important; font-weight: 700 !important; }
h2 { color: #334155 !important; font-weight: 600 !important; }

[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# ── Nav ──────────────────────────────────────────────────────────────────────
select = option_menu(
    menu_title=None,
    options=["User", "Admin"],
    icons=["person-fill", "shield-lock-fill"],
    orientation="horizontal",
    styles={
        "container": {"padding": "4px", "background-color": "#ffffff",
                      "border-radius": "12px", "border": "1px solid #e2e8f0",
                      "margin-bottom": "24px"},
        "icon": {"color": "#6366f1", "font-size": "16px"},
        "nav-link": {"font-size": "15px", "font-weight": "500", "color": "#64748b",
                     "border-radius": "8px"},
        "nav-link-selected": {"background-color": "#6366f1", "color": "white",
                              "font-weight": "600"},
    }
)

CSV_FILE = "user_reg.csv"

COURSES = ["Web Development", "AI/ML", "Digital Marketing", "Power BI", "Cyber Security", "Data Analyst"]
CITIES  = ["Karachi", "Islamabad", "Lahore", "Peshawar", "Rawalpindi", "Multan"]
EDUS    = ["Matric", "Intermediate", "Bachelor's", "Master's", "PhD"]

COURSE_OUTLINES = {
    "Web Development": [
        "HTML/CSS Fundamentals", "JavaScript Essentials", "Responsive Design",
        "React Basics", "Backend Intro (Node/Express)", "Deployment"
    ],
    "AI/ML": [
        "Python Refresher", "NumPy & Pandas", "Data Preprocessing",
        "Supervised Learning", "Unsupervised Learning", "Model Evaluation",
        "Intro to Deep Learning"
    ],
    "Digital Marketing": [
        "Marketing Fundamentals", "SEO & SEM", "Social Media Strategy",
        "Email Marketing", "Google Analytics", "Content Marketing",
        "Paid Ads (Meta/Google)"
    ],
    "Power BI": [
        "Data Sources & Import", "Power Query (ETL)", "Data Modeling",
        "DAX Basics", "Building Reports", "Dashboards & Visuals",
        "Publishing & Sharing"
    ],
    "Cyber Security": [
        "Networking Fundamentals", "Linux Basics", "Threats & Attack Types",
        "Cryptography", "Ethical Hacking Intro", "Firewalls & IDS",
        "Security Auditing"
    ],
    "Data Analyst": [
        "Excel for Data", "SQL Fundamentals", "Python (Pandas/Matplotlib)",
        "Data Cleaning", "Exploratory Data Analysis", "Storytelling with Data",
        "Capstone Project"
    ]
}

CHART_COLORS = ["#6366f1", "#8b5cf6", "#ec4899", "#14b8a6", "#f59e0b", "#3b82f6"]


def save_to_csv(name, email, cnic, city, contact, age, gender, education, course):
    new_data = pd.DataFrame({
        "Name": [name], "Email": [email], "CNIC": [cnic], "City": [city],
        "Contact": [contact], "Age": [age], "Gender": [gender],
        "Education": [education], "Course": [course]
    })
    if os.path.exists(CSV_FILE):
        existing = pd.read_csv(CSV_FILE)
        pd.concat([existing, new_data], ignore_index=True).to_csv(CSV_FILE, index=False)
    else:
        new_data.to_csv(CSV_FILE, index=False)


def make_id(cnic):
    digits = "".join(filter(str.isdigit, str(cnic)))
    return f"REG-{digits[-5:]}" if len(digits) >= 5 else f"REG-{digits.zfill(5)}"


def styled_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_family="Inter",
        margin=dict(t=40, b=20, l=10, r=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#f1f5f9")
    st.plotly_chart(fig, use_container_width=True)


# ── ADMIN ─────────────────────────────────────────────────────────────────────
if select == "Admin":
    tab1, tab2 = st.tabs(["📊  Stats", "📋  Information"])

    with tab1:
        st.title("Registration Statistics")
        if os.path.exists(CSV_FILE):
            data = pd.read_csv(CSV_FILE)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Registrations", data["CNIC"].nunique())
            c2.metric("Average Age", round(data["Age"].mean()))
            c3.metric("Total Male", int((data["Gender"] == "Male").sum()))
            c4.metric("Total Female", int((data["Gender"] == "Female").sum()))

            st.markdown("---")

            col_l, col_r = st.columns(2)
            with col_l:
                gc = data["Gender"].value_counts().reset_index()
                fig1 = px.bar(gc, x="Gender", y="count", color="Gender",
                              title="Gender Distribution",
                              color_discrete_sequence=CHART_COLORS)
                styled_chart(fig1)

            with col_r:
                cc = data["Course"].value_counts().reset_index()
                fig2 = px.pie(cc, names="Course", values="count",
                              title="Enrolment by Course",
                              color_discrete_sequence=CHART_COLORS, hole=0.35)
                styled_chart(fig2)

            col_l2, col_r2 = st.columns(2)
            with col_l2:
                cityc = data["City"].value_counts().reset_index()
                fig3 = px.bar(cityc, x="City", y="count", color="City",
                              title="Registrations by City",
                              color_discrete_sequence=CHART_COLORS)
                styled_chart(fig3)

            with col_r2:
                educ = data["Education"].value_counts().reset_index()
                fig4 = px.pie(educ, names="Education", values="count",
                              title="Education Level Breakdown",
                              color_discrete_sequence=CHART_COLORS, hole=0.35)
                styled_chart(fig4)
        else:
            st.info("No registrations yet.")

    with tab2:
        st.title("Registered Candidates")
        if os.path.exists(CSV_FILE):
            data = pd.read_csv(CSV_FILE)
            selected = st.multiselect("Filter by Course", data["Course"].unique(),
                                      default=list(data["Course"].unique()[:1]))
            filtered = data[data["Course"].isin(selected)] if selected else data
            st.dataframe(filtered, use_container_width=True, hide_index=True)
            st.download_button("⬇  Download CSV", filtered.to_csv(index=False),
                               file_name="registrations.csv", mime="text/csv")
        else:
            st.info("No registrations yet.")


# ── USER ──────────────────────────────────────────────────────────────────────
elif select == "User":
    tab1, tab2 = st.tabs(["📝  Registration", "🎓  ID & Outline"])

    with tab1:
        st.title("Course Registration")
        with st.form("reg_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                name    = st.text_input("Full Name", placeholder="Ali Hassan")
                cnic    = st.text_input("CNIC", placeholder="42101-1234567-1")
                contact = st.text_input("Contact", placeholder="0300-1234567")
                age     = st.number_input("Age", min_value=18, max_value=60, value=22)
                gender  = st.selectbox("Gender", ["Male", "Female"])
            with col_b:
                email     = st.text_input("Email", placeholder="ali@example.com")
                city      = st.selectbox("City", CITIES)
                education = st.selectbox("Education", EDUS)
                course    = st.selectbox("Course", COURSES)

            submitted = st.form_submit_button("✅  Register Now", use_container_width=True)

        if submitted:
            if all([name, email, cnic, contact, city, gender, education, course]):
                save_to_csv(name, email, cnic, city, contact, age, gender, education, course)
                st.success("🎉 Registration successful!")
                st.balloons()
            else:
                st.error("Please fill in all fields before submitting.")

    with tab2:
        st.title("Your ID Card & Course Outline")
        with st.form("id_form"):
            email_q = st.text_input("Email Address", placeholder="ali@example.com")
            cnic_q  = st.text_input("CNIC", placeholder="42101-1234567-1")
            fetch   = st.form_submit_button("🔍  Fetch My Details", use_container_width=True)

        if fetch:
            if not os.path.exists(CSV_FILE):
                st.info("No registrations found yet.")
            else:
                data = pd.read_csv(CSV_FILE)
                match = data[data["Email"] == email_q]
                if match.empty:
                    st.warning("No registration found for that email.")
                else:
                    r = match.iloc[0]
                    uid = make_id(cnic_q or r["CNIC"])

                    st.markdown(f"""
                    <div class="id-card">
                        <div class="id-num">{uid}</div>
                        <h2>{r['Name']}</h2>
                        <div class="id-row">
                            <div class="id-field">
                                <label>Email</label>
                                <span>{r['Email']}</span>
                            </div>
                            <div class="id-field">
                                <label>City</label>
                                <span>{r['City']}</span>
                            </div>
                            <div class="id-field">
                                <label>Age</label>
                                <span>{r['Age']}</span>
                            </div>
                            <div class="id-field">
                                <label>Gender</label>
                                <span>{r['Gender']}</span>
                            </div>
                        </div>
                        <div class="badge">🎓 {r['Course']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    outline = COURSE_OUTLINES.get(r["Course"], [])
                    if outline:
                        st.subheader(f"{r['Course']} — Course Outline")
                        for i, topic in enumerate(outline, 1):
                            num = f"0{i}" if i < 10 else str(i)
                            st.markdown(
                                f'<div class="outline-item">{num}.&nbsp;&nbsp;{topic}</div>',
                                unsafe_allow_html=True
                            )
