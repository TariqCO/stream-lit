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

# Minimal CSS — only what Streamlit can't do on its own
st.markdown("""
<style>
.id-card {
    background: #1e293b;
    border-radius: 12px;
    padding: 24px 28px;
    color: white;
    margin: 16px 0;
}
.id-card .id-num { font-size: 0.8rem; opacity: 0.5; margin-bottom: 6px; font-family: monospace; }
.id-card .id-name { font-size: 1.4rem; font-weight: 700; margin-bottom: 16px; }
.id-card .id-grid { display: flex; gap: 32px; flex-wrap: wrap; margin-bottom: 16px; }
.id-card .id-field label { font-size: 0.7rem; opacity: 0.5; text-transform: uppercase; display: block; }
.id-card .id-field span { font-size: 0.95rem; font-weight: 500; }
.id-card .course-tag {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border-radius: 6px;
    padding: 3px 12px;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

CSV_FILE = "user_reg.csv"

COURSES = ["Web Development", "AI/ML", "Digital Marketing", "Power BI", "Cyber Security", "Data Analyst"]
CITIES  = ["Karachi", "Islamabad", "Lahore", "Peshawar", "Rawalpindi", "Multan"]
EDUS    = ["Matric", "Intermediate", "Bachelor's", "Master's", "PhD"]

COURSE_OUTLINES = {
    "Web Development":    ["HTML/CSS Fundamentals", "JavaScript Essentials", "Responsive Design", "React Basics", "Backend Intro (Node/Express)", "Deployment"],
    "AI/ML":              ["Python Refresher", "NumPy & Pandas", "Data Preprocessing", "Supervised Learning", "Unsupervised Learning", "Model Evaluation", "Intro to Deep Learning"],
    "Digital Marketing":  ["Marketing Fundamentals", "SEO & SEM", "Social Media Strategy", "Email Marketing", "Google Analytics", "Content Marketing", "Paid Ads (Meta/Google)"],
    "Power BI":           ["Data Sources & Import", "Power Query (ETL)", "Data Modeling", "DAX Basics", "Building Reports", "Dashboards & Visuals", "Publishing & Sharing"],
    "Cyber Security":     ["Networking Fundamentals", "Linux Basics", "Threats & Attack Types", "Cryptography", "Ethical Hacking Intro", "Firewalls & IDS", "Security Auditing"],
    "Data Analyst":       ["Excel for Data", "SQL Fundamentals", "Python (Pandas/Matplotlib)", "Data Cleaning", "Exploratory Data Analysis", "Storytelling with Data", "Capstone Project"],
}

def save_to_csv(name, email, cnic, city, contact, age, gender, education, course):
    new_row = pd.DataFrame({
        "Name": [name], "Email": [email], "CNIC": [cnic], "City": [city],
        "Contact": [contact], "Age": [age], "Gender": [gender],
        "Education": [education], "Course": [course]
    })
    if os.path.exists(CSV_FILE):
        existing = pd.read_csv(CSV_FILE)
        pd.concat([existing, new_row], ignore_index=True).to_csv(CSV_FILE, index=False)
    else:
        new_row.to_csv(CSV_FILE, index=False)

def make_id(cnic):
    digits = "".join(filter(str.isdigit, str(cnic)))
    return f"REG-{digits[-5:]}" if len(digits) >= 5 else "REG-00000"


# ── Nav ───────────────────────────────────────────────────────────────────────
select = option_menu(
    menu_title=None,
    options=["User", "Admin"],
    icons=["person", "shield-lock"],
    orientation="horizontal"
)


# ── ADMIN ─────────────────────────────────────────────────────────────────────
if select == "Admin":
    tab1, tab2 = st.tabs(["Stats", "Information"])

    with tab1:
        st.header("Registration Overview")

        if not os.path.exists(CSV_FILE):
            st.info("No registrations yet.")
        else:
            data = pd.read_csv(CSV_FILE)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Registrations", data["CNIC"].nunique())
            c2.metric("Avg Age", round(data["Age"].mean()))
            c3.metric("Male", int((data["Gender"] == "Male").sum()))
            c4.metric("Female", int((data["Gender"] == "Female").sum()))

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                gc = data["Gender"].value_counts().reset_index()
                fig1 = px.bar(gc, x="Gender", y="count", title="By Gender", color="Gender")
                fig1.update_layout(showlegend=False, margin=dict(t=36,b=0,l=0,r=0))
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                cc = data["Course"].value_counts().reset_index()
                fig2 = px.pie(cc, names="Course", values="count", title="By Course", hole=0.4)
                fig2.update_layout(margin=dict(t=36,b=0,l=0,r=0))
                st.plotly_chart(fig2, use_container_width=True)

            col3, col4 = st.columns(2)

            with col3:
                cityc = data["City"].value_counts().reset_index()
                fig3 = px.bar(cityc, x="City", y="count", title="By City", color="City")
                fig3.update_layout(showlegend=False, margin=dict(t=36,b=0,l=0,r=0))
                st.plotly_chart(fig3, use_container_width=True)

            with col4:
                educ = data["Education"].value_counts().reset_index()
                fig4 = px.pie(educ, names="Education", values="count", title="By Education", hole=0.4)
                fig4.update_layout(margin=dict(t=36,b=0,l=0,r=0))
                st.plotly_chart(fig4, use_container_width=True)

    with tab2:
        st.header("Registered Candidates")

        if not os.path.exists(CSV_FILE):
            st.info("No registrations yet.")
        else:
            data = pd.read_csv(CSV_FILE)
            courses = data["Course"].unique().tolist()
            selected = st.multiselect("Filter by Course", courses, default=courses)
            filtered = data[data["Course"].isin(selected)] if selected else data
            st.dataframe(filtered, use_container_width=True, hide_index=True)
            st.download_button("Download CSV", filtered.to_csv(index=False),
                               file_name="registrations.csv", mime="text/csv")


# ── USER ──────────────────────────────────────────────────────────────────────
elif select == "User":
    tab1, tab2 = st.tabs(["Registration", "ID & Outline"])

    with tab1:
        st.header("Register for a Course")

        with st.form("reg_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                name    = st.text_input("Full Name")
                cnic    = st.text_input("CNIC", placeholder="42101-1234567-1")
                contact = st.text_input("Contact", placeholder="0300-1234567")
                age     = st.number_input("Age", min_value=18, max_value=60, value=22)
                gender  = st.selectbox("Gender", ["Male", "Female"])
            with col_b:
                email     = st.text_input("Email")
                city      = st.selectbox("City", CITIES)
                education = st.selectbox("Education", EDUS)
                course    = st.selectbox("Course", COURSES)

            submitted = st.form_submit_button("Register", use_container_width=True)

        if submitted:
            if all([name, email, cnic, contact]):
                save_to_csv(name, email, cnic, city, contact, age, gender, education, course)
                st.success("Registration successful!")
                st.balloons()
            else:
                st.error("Please fill in all required fields.")

    with tab2:
        st.header("Your ID Card & Course Outline")

        with st.form("id_form"):
            email_q = st.text_input("Email Address")
            cnic_q  = st.text_input("CNIC")
            fetch   = st.form_submit_button("Look Up", use_container_width=True)

        if fetch:
            if not os.path.exists(CSV_FILE):
                st.info("No registrations found yet.")
            else:
                data  = pd.read_csv(CSV_FILE)
                match = data[data["Email"] == email_q]

                if match.empty:
                    st.warning("No registration found with that email.")
                else:
                    r   = match.iloc[0]
                    uid = make_id(cnic_q or r["CNIC"])

                    st.markdown(f"""
                    <div class="id-card">
                        <div class="id-num">{uid}</div>
                        <div class="id-name">{r['Name']}</div>
                        <div class="id-grid">
                            <div class="id-field"><label>Email</label><span>{r['Email']}</span></div>
                            <div class="id-field"><label>City</label><span>{r['City']}</span></div>
                            <div class="id-field"><label>Age</label><span>{r['Age']}</span></div>
                            <div class="id-field"><label>Gender</label><span>{r['Gender']}</span></div>
                            <div class="id-field"><label>Education</label><span>{r['Education']}</span></div>
                        </div>
                        <div class="course-tag">🎓 {r['Course']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    outline = COURSE_OUTLINES.get(r["Course"], [])
                    if outline:
                        st.subheader(f"{r['Course']} — Course Outline")
                        for i, topic in enumerate(outline, 1):
                            st.markdown(f"{i}. {topic}")
