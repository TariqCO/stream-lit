import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import os

st.set_page_config(
    page_title="EduReg — Course Registration",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* ─── Page Background ─── */
.stApp {
    background: #0d0f14;
    color: #e8eaf0;
}

/* ─── Top nav pills ─── */
.nav-link {
    font-family: 'Sora', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    border-radius: 8px !important;
}
.nav-link.active {
    background: #c8f54a !important;
    color: #0d0f14 !important;
}

/* ─── Metric Cards ─── */
[data-testid="metric-container"] {
    background: #161a22;
    border: 1px solid #252932;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
[data-testid="metric-container"] label {
    color: #8b90a0 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #c8f54a !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ─── Inputs ─── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #161a22 !important;
    border: 1px solid #252932 !important;
    border-radius: 8px !important;
    color: #e8eaf0 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 0.9rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #c8f54a !important;
    box-shadow: 0 0 0 2px rgba(200,245,74,0.12) !important;
}

/* ─── Select boxes ─── */
.stSelectbox > div > div {
    background: #161a22 !important;
    border: 1px solid #252932 !important;
    border-radius: 8px !important;
    color: #e8eaf0 !important;
    font-family: 'Sora', sans-serif !important;
}

/* ─── Labels ─── */
.stTextInput label, .stSelectbox label,
.stNumberInput label, .stMultiSelect label {
    color: #8b90a0 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 4px !important;
}

/* ─── Submit button ─── */
.stFormSubmitButton > button,
.stButton > button {
    background: #c8f54a !important;
    color: #0d0f14 !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.05em;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 2rem !important;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.1s;
    text-transform: uppercase;
}
.stFormSubmitButton > button:hover,
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px);
}

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: transparent;
    border-bottom: 1px solid #252932;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8b90a0;
    border-radius: 6px 6px 0 0;
    font-family: 'Sora', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 0.5rem 1.2rem;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: #161a22 !important;
    color: #c8f54a !important;
    border-top: 2px solid #c8f54a !important;
}

/* ─── Dataframe ─── */
[data-testid="stDataFrame"] {
    border: 1px solid #252932;
    border-radius: 10px;
    overflow: hidden;
}

/* ─── Alerts ─── */
.stSuccess {
    background: rgba(200,245,74,0.08) !important;
    border: 1px solid rgba(200,245,74,0.3) !important;
    border-radius: 8px !important;
    color: #c8f54a !important;
}
.stError {
    background: rgba(255,90,80,0.08) !important;
    border: 1px solid rgba(255,90,80,0.3) !important;
    border-radius: 8px !important;
}
.stInfo {
    background: rgba(100,160,255,0.08) !important;
    border: 1px solid rgba(100,160,255,0.3) !important;
    border-radius: 8px !important;
}

/* ─── Download button ─── */
.stDownloadButton > button {
    background: transparent !important;
    color: #c8f54a !important;
    border: 1px solid #c8f54a !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    text-transform: uppercase;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
    width: auto !important;
}
.stDownloadButton > button:hover {
    background: rgba(200,245,74,0.1) !important;
}

/* ─── Multiselect ─── */
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(200,245,74,0.15) !important;
    color: #c8f54a !important;
    border: 1px solid rgba(200,245,74,0.3) !important;
    border-radius: 6px !important;
}

/* ─── Section dividers ─── */
hr {
    border-color: #252932 !important;
}

/* ─── Form container ─── */
[data-testid="stForm"] {
    background: #161a22;
    border: 1px solid #252932;
    border-radius: 14px;
    padding: 1.8rem 2rem 1.4rem;
}

/* ─── Plotly charts background ─── */
.js-plotly-plot {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #252932;
}

/* ─── Page title area ─── */
.page-header {
    padding: 1.6rem 0 0.4rem;
    border-bottom: 1px solid #252932;
    margin-bottom: 1.8rem;
}
.page-header h1 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #e8eaf0;
    margin: 0;
    letter-spacing: -0.02em;
}
.page-header p {
    color: #8b90a0;
    font-size: 0.82rem;
    margin: 0.3rem 0 0;
}

/* ─── ID card ─── */
.id-card {
    background: linear-gradient(135deg, #161a22 0%, #1e2330 100%);
    border: 1px solid #252932;
    border-left: 4px solid #c8f54a;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
}
.id-card .id-label {
    font-size: 0.72rem;
    color: #8b90a0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    margin-bottom: 0.2rem;
}
.id-card .id-value {
    font-size: 1.1rem;
    color: #e8eaf0;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}
.id-card .id-badge {
    display: inline-block;
    background: rgba(200,245,74,0.15);
    color: #c8f54a;
    border: 1px solid rgba(200,245,74,0.35);
    border-radius: 20px;
    padding: 0.15rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-top: 0.6rem;
}

/* ─── Outline list ─── */
.outline-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.65rem 0;
    border-bottom: 1px solid #1e2330;
    color: #c5c8d4;
    font-size: 0.9rem;
}
.outline-num {
    width: 24px;
    height: 24px;
    background: rgba(200,245,74,0.12);
    color: #c8f54a;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    flex-shrink: 0;
}

/* ─── Stat section header ─── */
.section-label {
    font-size: 0.72rem;
    color: #8b90a0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    margin: 1.6rem 0 0.8rem;
}
</style>
""", unsafe_allow_html=True)


# ─── PLOTLY THEME ───────────────────────────────────────────────
CHART_THEME = {
    "paper_bgcolor": "#161a22",
    "plot_bgcolor": "#161a22",
    "font_color": "#8b90a0",
    "font_family": "Sora",
    "gridcolor": "#252932",
    "accent": "#c8f54a",
}
PALETTE = ["#c8f54a", "#4af5c8", "#f54a7b", "#4a8ef5", "#f5c84a", "#c84af5"]


def chart_layout(fig, title=""):
    fig.update_layout(
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"], family=CHART_THEME["font_family"]),
        title=dict(text=title, font=dict(color="#e8eaf0", size=14, family="Sora"), x=0),
        margin=dict(l=16, r=16, t=40, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8b90a0")),
        colorway=PALETTE,
    )
    fig.update_xaxes(gridcolor=CHART_THEME["gridcolor"], linecolor="#252932", tickfont=dict(color="#8b90a0"))
    fig.update_yaxes(gridcolor=CHART_THEME["gridcolor"], linecolor="#252932", tickfont=dict(color="#8b90a0"))
    return fig


# ─── CSV ────────────────────────────────────────────────────────
CSV_FILE = "user_reg.csv"

def save_to_csv(name, email, cnic, city, contact, age, gender, education, course):
    new_data = pd.DataFrame({
        "Name": [name], "Email": [email], "CNIC": [cnic],
        "City": [city], "Contact": [contact], "Age": [age],
        "Gender": [gender], "Education": [education], "Course": [course]
    })
    if os.path.exists(CSV_FILE):
        existing = pd.read_csv(CSV_FILE)
        pd.concat([existing, new_data], ignore_index=True).to_csv(CSV_FILE, index=False)
    else:
        new_data.to_csv(CSV_FILE, index=False)


COURSE_OUTLINES = {
    "Web Development": [
        "HTML & CSS Fundamentals", "JavaScript Essentials",
        "Responsive & Mobile-First Design", "React Basics",
        "Backend Intro (Node / Express)", "Databases & REST APIs", "Deployment & DevOps"
    ],
    "AI/ML": [
        "Python Refresher", "NumPy & Pandas",
        "Data Preprocessing & Feature Engineering", "Supervised Learning",
        "Unsupervised Learning", "Model Evaluation & Tuning", "Intro to Deep Learning"
    ],
    "Digital Marketing": [
        "Marketing Fundamentals", "SEO & SEM",
        "Social Media Strategy", "Email Marketing",
        "Google Analytics 4", "Content Marketing", "Paid Ads — Meta & Google"
    ],
    "Power BI": [
        "Data Sources & Import", "Power Query (ETL)",
        "Data Modeling & Relationships", "DAX Fundamentals",
        "Building Reports", "Dashboards & Visuals", "Publishing & Sharing"
    ],
    "Cyber Security": [
        "Networking Fundamentals", "Linux Essentials",
        "Threats & Attack Vectors", "Cryptography Basics",
        "Ethical Hacking Intro", "Firewalls & IDS/IPS", "Security Auditing & Compliance"
    ],
    "Data Analyst": [
        "Excel for Data Analysis", "SQL Fundamentals",
        "Python with Pandas & Matplotlib", "Data Cleaning Techniques",
        "Exploratory Data Analysis", "Storytelling with Data", "Capstone Project"
    ]
}


# ─── NAV ────────────────────────────────────────────────────────
select = option_menu(
    menu_title=None,
    options=["User", "Admin"],
    icons=["person-fill", "bar-chart-fill"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#0d0f14", "padding": "0.6rem 0"},
        "icon": {"color": "#8b90a0", "font-size": "14px"},
        "nav-link": {
            "font-family": "Sora, sans-serif",
            "font-size": "0.82rem",
            "font-weight": "600",
            "color": "#8b90a0",
            "letter-spacing": "0.06em",
            "text-transform": "uppercase",
            "border-radius": "8px",
            "padding": "0.45rem 1.4rem",
        },
        "nav-link-selected": {
            "background-color": "#c8f54a",
            "color": "#0d0f14",
        },
    }
)


# ═══════════════════════════════════════════════════════════════
# ADMIN
# ═══════════════════════════════════════════════════════════════
if select == "Admin":
    tab1, tab2 = st.tabs(["📊  Stats", "📋  Records"])

    with tab1:
        st.markdown('<div class="page-header"><h1>Registration Stats</h1><p>Live overview of all registrations</p></div>', unsafe_allow_html=True)

        if os.path.exists(CSV_FILE):
            data = pd.read_csv(CSV_FILE)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Students", data["CNIC"].nunique())
            col2.metric("Avg Age", round(data["Age"].mean()))
            col3.metric("Male", int((data["Gender"] == "Male").sum()))
            col4.metric("Female", int((data["Gender"] == "Female").sum()))

            st.markdown('<div class="section-label">Gender Breakdown</div>', unsafe_allow_html=True)
            gc = data["Gender"].value_counts().reset_index()
            fig1 = px.bar(gc, x="Gender", y="count", color="Gender", color_discrete_sequence=PALETTE,
                          text_auto=True)
            fig1.update_traces(marker_line_width=0, textfont_color="#0d0f14")
            st.plotly_chart(chart_layout(fig1), use_container_width=True)

            st.markdown('<div class="section-label">Course Enrollments</div>', unsafe_allow_html=True)
            cc = data["Course"].value_counts().reset_index()
            fig2 = px.pie(cc, names="Course", values="count", color_discrete_sequence=PALETTE,
                          hole=0.55)
            fig2.update_traces(textfont=dict(color="#0d0f14", family="Sora", size=12),
                               marker=dict(line=dict(color="#0d0f14", width=2)))
            st.plotly_chart(chart_layout(fig2), use_container_width=True)

            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown('<div class="section-label">By City</div>', unsafe_allow_html=True)
                city_c = data["City"].value_counts().reset_index()
                fig3 = px.bar(city_c, x="City", y="count", color="City",
                              color_discrete_sequence=PALETTE, text_auto=True)
                fig3.update_traces(marker_line_width=0, textfont_color="#0d0f14")
                st.plotly_chart(chart_layout(fig3), use_container_width=True)

            with col_r:
                st.markdown('<div class="section-label">Education Level</div>', unsafe_allow_html=True)
                edu_c = data["Education"].value_counts().reset_index()
                fig4 = px.pie(edu_c, names="Education", values="count",
                              color_discrete_sequence=PALETTE, hole=0.45)
                fig4.update_traces(marker=dict(line=dict(color="#0d0f14", width=2)))
                st.plotly_chart(chart_layout(fig4), use_container_width=True)

        else:
            st.info("No registrations yet — check back once users sign up.")

    with tab2:
        st.markdown('<div class="page-header"><h1>Student Records</h1><p>Filter and export registration data</p></div>', unsafe_allow_html=True)

        if os.path.exists(CSV_FILE):
            data = pd.read_csv(CSV_FILE)
            options = data["Course"].unique().tolist()
            default = [options[0]] if options else []
            selected = st.multiselect("Filter by Course", options, default)
            filtered = data[data["Course"].isin(selected)] if selected else data

            st.dataframe(
                filtered.reset_index(drop=True),
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "⬇  Export CSV",
                data=filtered.to_csv(index=False),
                file_name="registrations.csv",
                mime="text/csv"
            )
        else:
            st.info("No registrations yet.")


# ═══════════════════════════════════════════════════════════════
# USER
# ═══════════════════════════════════════════════════════════════
elif select == "User":
    tab1, tab2 = st.tabs(["✏️  Register", "🪪  My ID & Outline"])

    with tab1:
        st.markdown('<div class="page-header"><h1>Course Registration</h1><p>Fill in your details to enroll</p></div>', unsafe_allow_html=True)

        with st.form("registration_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Full Name", placeholder="Ali Hassan")
                email = st.text_input("Email", placeholder="ali@example.com")
                cnic = st.text_input("CNIC", placeholder="42101-1234567-8")
                contact = st.text_input("Contact", placeholder="0300-1234567")
            with col_b:
                city = st.selectbox("City", ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Peshawar", "Multan"])
                age = st.number_input("Age", min_value=18, max_value=60, value=22)
                gender = st.selectbox("Gender", ["Male", "Female"])
                education = st.selectbox("Education", ["Matric", "Intermediate", "Bachelor's", "Master's", "PhD"])

            course = st.selectbox(
                "Select Course",
                ["Web Development", "AI/ML", "Digital Marketing", "Power BI", "Cyber Security", "Data Analyst"]
            )

            submitted = st.form_submit_button("Submit Registration →")

        if submitted:
            if all([name, email, cnic, contact]):
                save_to_csv(name, email, cnic, city, contact, age, gender, education, course)
                st.success(f"You're registered for **{course}**. Welcome aboard, {name.split()[0]}!")
                st.balloons()
            else:
                st.error("Please complete all required fields before submitting.")

    with tab2:
        st.markdown('<div class="page-header"><h1>Your ID & Course Outline</h1><p>Enter your credentials to retrieve your registration</p></div>', unsafe_allow_html=True)

        with st.form("lookup_form"):
            lu_email = st.text_input("Email", placeholder="ali@example.com")
            lu_cnic = st.text_input("CNIC", placeholder="42101-1234567-8")
            lookup = st.form_submit_button("Retrieve →")

        if lookup:
            if os.path.exists(CSV_FILE):
                data = pd.read_csv(CSV_FILE)
                match = data[data["Email"].str.lower() == lu_email.strip().lower()]

                if match.empty:
                    st.info("No registration found with that email address.")
                else:
                    candidate = match.iloc[0]
                    student_id = f"EDU-{int(candidate['Age']) * 2:04d}-{str(candidate['CNIC'])[-4:]}"
                    course = candidate["Course"]

                    st.markdown(f"""
                    <div class="id-card">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
                            <div>
                                <div class="id-label">Student Name</div>
                                <div class="id-value">{candidate['Name']}</div>
                            </div>
                            <div>
                                <div class="id-label">Student ID</div>
                                <div class="id-value">{student_id}</div>
                            </div>
                            <div>
                                <div class="id-label">City</div>
                                <div class="id-value">{candidate['City']}</div>
                            </div>
                        </div>
                        <div style="margin-top:1rem;">
                            <span class="id-badge">🎓 {course}</span>
                            <span class="id-badge" style="margin-left:0.5rem;">📘 {candidate['Education']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    outline = COURSE_OUTLINES.get(course, [])
                    if outline:
                        st.markdown(f'<div class="section-label">{course} — Course Outline</div>', unsafe_allow_html=True)
                        items_html = "".join([
                            f'<div class="outline-item"><div class="outline-num">{i+1:02d}</div><span>{topic}</span></div>'
                            for i, topic in enumerate(outline)
                        ])
                        st.markdown(items_html, unsafe_allow_html=True)
            else:
                st.info("No registrations on file yet.")
