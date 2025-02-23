import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyC_3S1DnOvip8iBpyhtp1rf08j91Scx8V0"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # Updated to a valid model name (gemini-2.0-flash doesn't exist as of now)

# Utility function for AI responses
def generate_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Initialize session state
def initialize_session_state():
    defaults = {
        "lesson_plans": [],
        "grades": {},
        "forum_posts": [],
        "pd_activities": [],
        "wellbeing_logs": [],
        "observations": [],
        "messages": [],
        "substitute_plans": [],
        "attendance": {},
        "peer_reviews": [],
        "live_observations": [],
        "student_analytics": {},
        "dark_mode": False,
        "current_page": "Home",
        "username": "teacher1",
        "role": "Teacher",
        "lesson_planning_session": [],
        "collaborative_notes": [],
        "feedback_log": []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Dynamic UI Theme with Radio Button Styling
def apply_theme():
    primary_color = "#2E86C1"
    secondary_color = "#28A745"
    accent_color = "#F59E0B"
    background_dark = "#1A2525"
    background_light = "#F8FAFC"
    
    if st.session_state['dark_mode']:
        bg_color = background_dark
        text_color = "#E2E8F0"
        card_bg = "#2D3748"
        accent = "#FBBF24"
    else:
        bg_color = background_light
        text_color = "#1A2525"
        card_bg = "#FFFFFF"
        accent = accent_color

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    :root {{
        --primary: {primary_color};
        --secondary: {secondary_color};
        --accent: {accent};
        --bg: {bg_color};
        --text: {text_color};
        --card-bg: {card_bg};
    }}

    .stApp {{
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }}

    .custom-card {{
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .custom-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
    }}

    .stButton>button {{
        background: linear-gradient(45deg, {primary_color}, {secondary_color});
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        opacity: 0.9;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background: var(--card-bg);
        padding: 0.5rem;
        border-radius: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background: var(--primary) !important;
        color: white !important;
    }}

    .divider {{
        margin: 20px 0;
        border-bottom: 2px solid rgba(229, 231, 235, 0.5);
    }}

    .sidebar-header {{
        background: linear-gradient(45deg, {primary_color}, {secondary_color});
        color: white;
        padding: 1.5rem;
        border-radius: 12px 12px 0 0;
        margin-bottom: 1rem;
    }}

    .stRadio > div {{
        display: flex;
        flex-direction: column;
    }}
    .stRadio label {{
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        transition: background 0.3s ease;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: 600;
    }}
    .stRadio label:hover {{
        background: rgba(46, 134, 193, 0.1);
    }}
    .stRadio input:checked + label {{
        background: var(--primary);
        color: white;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

# Updated Sidebar Navigation with Radio Buttons
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-header">
            <h1 style="font-size: 1.75rem; margin: 0;">
                <i class="fas fa-graduation-cap" style="margin-right: 0.5rem;"></i>EduGauge
            </h1>
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: #E2E8F0;"></div>
                <div>
                    <p style="margin: 0; font-weight: 600;">{st.session_state['username']}</p>
                    <p style="margin: 0; font-size: 0.875rem;">{st.session_state['role']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        pages = [
            ("🏠 Home", "Home"),
            ("📚 Lesson Planning", "Lesson Planning"),
            ("📊 Student Performance", "Student Performance"),
            ("🎓 Professional Development", "Professional Development"),
            ("🤝 Collaboration", "Collaboration"),
            ("💖 Well-Being", "Well-Being"),
            ("👁️ Observation and Feedback", "Observation and Feedback"),
            ("🏫 Classroom Management", "Classroom Management")
        ] if st.session_state["role"] == "Teacher" else [
            ("🏠 Home", "Home"),
            ("🛠️ Admin Tools", "Admin Tools")
        ]

        options = [display for display, _ in pages]
        current_index = next((i for i, (_, p) in enumerate(pages) if p == st.session_state["current_page"]), 0)
        selected_display = st.radio("Navigation", options, index=current_index)
        selected_page = next(p for d, p in pages if d == selected_display)
        if selected_page != st.session_state["current_page"]:
            st.session_state["current_page"] = selected_page
            st.rerun()

        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: var(--primary);"><i class="fas fa-cog"></i> Settings</h3>', unsafe_allow_html=True)
        st.checkbox("Dark Mode", value=st.session_state['dark_mode'], 
                    on_change=lambda: st.session_state.update({'dark_mode': not st.session_state['dark_mode']}), 
                    key="dark_mode_toggle")
        st.markdown('</div>', unsafe_allow_html=True)

# Main Application
def main():
    st.set_page_config(page_title="EduGauge", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
    initialize_session_state()
    apply_theme()
    render_sidebar()
    page = st.session_state["current_page"]

    if page == "Home":
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 700; color: var(--primary);"><i class="fas fa-home"></i> EduGauge Home</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.25rem; color: var(--text);">Empowering Teachers for Impactful Learning</p>', unsafe_allow_html=True)
        st.image("https://via.placeholder.com/1200x300.png?text=EduGauge+Welcome", use_column_width=True, caption="Welcome to EduGauge")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="subheader"><i class="fas fa-tachometer-alt" style="color: var(--accent); margin-right: 0.5rem;"></i>Quick Stats</h3>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Lesson Plans", len(st.session_state["lesson_plans"]), delta="New")
        with col2:
            st.metric("PD Hours", f"{sum(a['hours'] for a in st.session_state['pd_activities']):.2f}", delta="+2.5")
        with col3:
            st.metric("Observations", len(st.session_state["observations"]), delta="Recent")
        with col4:
            st.metric("Students Graded", sum(len(g) for g in st.session_state["grades"].values()), delta="Updated")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="subheader"><i class="fas fa-chart-line" style="color: var(--accent); margin-right: 0.5rem;"></i>Performance Overview</h3>', unsafe_allow_html=True)
        if st.session_state["grades"]:
            all_grades = [grade["grade"] for student_grades in st.session_state["grades"].values() for grade in student_grades]
            fig = px.histogram(all_grades, nbins=10, title="Grades Distribution", height=400)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Lesson Planning":
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 700; color: var(--primary);"><i class="fas fa-book-open"></i> Lesson Planning</h1>', unsafe_allow_html=True)
        tabs = st.tabs(["Create Lesson Plan", "AI Tools", "Substitute Plans", "AI Lesson Planning"])
        
        with tabs[0]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-plus" style="color: var(--accent); margin-right: 0.5rem;"></i>Create a New Lesson Plan</h3>', unsafe_allow_html=True)
            with st.form(key="lesson_form"):
                title = st.text_input("Lesson Title", placeholder="e.g., Introduction to Fractions")
                objectives = st.text_area("Objectives", placeholder="What students will learn...", height=100)
                activities = st.text_area("Activities", placeholder="Classroom activities...", height=150)
                materials = st.text_area("Materials Needed", placeholder="Resources required...", height=100)
                col1, col2 = st.columns([3, 1])
                with col2:
                    submit = st.form_submit_button("Save Lesson Plan")
                if submit:
                    st.session_state["lesson_plans"].append({
                        "title": title,
                        "objectives": objectives,
                        "activities": activities,
                        "materials": materials,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.success("Lesson plan saved successfully!")
            if st.session_state["lesson_plans"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Saved Lesson Plans</h3>', unsafe_allow_html=True)
                for plan in st.session_state["lesson_plans"]:
                    with st.expander(f"{plan['title']} (Saved: {plan['timestamp']})"):
                        st.markdown(f"**Objectives:** {plan['objectives']}")
                        st.markdown(f"**Activities:** {plan['activities']}")
                        st.markdown(f"**Materials:** {plan['materials']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[1]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-robot" style="color: var(--accent); margin-right: 0.5rem;"></i>AI-Enhanced Tools</h3>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Generate Lesson Ideas", key="gen_ideas"):
                    prompt = f"Generate creative lesson plan ideas for {st.session_state['username']}'s class on a topic of their choice."
                    response = generate_ai_response(prompt)
                    st.markdown('<div class="custom-card"><h4 style="color: var(--primary);">AI-Generated Ideas</h4></div>', unsafe_allow_html=True)
                    st.write(response)
            with col2:
                if st.button("Check Curriculum Alignment", key="check_align"):
                    if st.session_state["lesson_plans"]:
                        last_plan = st.session_state["lesson_plans"][-1]
                        prompt = f"Check if the following lesson plan aligns with standard curriculum: Title: {last_plan['title']}, Objectives: {last_plan['objectives']}, Activities: {last_plan['activities']}"
                        response = generate_ai_response(prompt)
                        st.markdown('<div class="custom-card"><h4 style="color: var(--primary);">AI Alignment Check</h4></div>', unsafe_allow_html=True)
                        st.write(response)
                    else:
                        st.warning("No lesson plans available to check.")
            with col3:
                if st.button("Generate Dynamic Questions", key="gen_questions"):
                    prompt = f"Create a set of varied-difficulty questions for a lesson by {st.session_state['username']}."
                    response = generate_ai_response(prompt)
                    st.markdown('<div class="custom-card"><h4 style="color: var(--primary);">AI-Generated Questions</h4></div>', unsafe_allow_html=True)
                    st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[2]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-user-cog" style="color: var(--accent); margin-right: 0.5rem;"></i>Substitute Lesson Plans</h3>', unsafe_allow_html=True)
            if st.button("Generate Substitute Plan", key="gen_sub_plan"):
                if st.session_state["lesson_plans"]:
                    last_plan = st.session_state["lesson_plans"][-1]
                    prompt = f"Generate a substitute lesson plan based on: Title: {last_plan['title']}, Objectives: {last_plan['objectives']}, Activities: {last_plan['activities']}"
                    response = generate_ai_response(prompt)
                    st.session_state["substitute_plans"].append({
                        "original_title": last_plan['title'],
                        "sub_plan": response,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.markdown('<div class="custom-card"><h4 style="color: var(--primary);">Substitute Plan Generated</h4></div>', unsafe_allow_html=True)
                    st.write(response)
                else:
                    st.warning("No lesson plans available to generate substitute plan.")
            if st.session_state["substitute_plans"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Saved Substitute Plans</h3>', unsafe_allow_html=True)
                for plan in st.session_state["substitute_plans"]:
                    with st.expander(f"Original: {plan['original_title']} (Generated: {plan['timestamp']})"):
                        st.write(plan['sub_plan'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[3]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-robot" style="color: var(--accent); margin-right: 0.5rem;"></i>AI Lesson Planning Assistant</h3>', unsafe_allow_html=True)
            if len(st.session_state["lesson_planning_session"]) == 0:
                with st.form("initial_planning_form"):
                    grade_level = st.selectbox("Grade Level", ["1", "2", "3", "4", "5"], key="grade_level")
                    subject = st.selectbox("Subject", ["Math", "Science", "English"], key="subject")
                    topic = st.text_input("Topic", key="topic")
                    objectives = st.text_area("Learning Objectives", key="objectives")
                    if st.form_submit_button("Generate Initial Lesson Plan"):
                        initial_prompt = f"Create a lesson plan for {grade_level} grade {subject} on {topic} with objectives: {objectives}"
                        response = generate_ai_response(initial_prompt)
                        st.session_state["lesson_planning_session"] = [
                            {"role": "teacher", "content": initial_prompt},
                            {"role": "ai", "content": response}
                        ]
                        st.rerun()
            else:
                current_plan = st.session_state["lesson_planning_session"][-1]["content"]
                st.markdown("**Current Lesson Plan:**")
                st.write(current_plan)
                feedback = st.text_area("Provide feedback or requests for modification", key="feedback_input")
                if st.button("Submit Feedback", key="submit_feedback"):
                    st.session_state["lesson_planning_session"].append({"role": "teacher", "content": feedback})
                    conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state["lesson_planning_session"]])
                    prompt = conversation + "\nAI: "
                    response = generate_ai_response(prompt)
                    st.session_state["lesson_planning_session"].append({"role": "ai", "content": response})
                    st.rerun()
                if st.button("Save Lesson Plan", key="save_lesson_plan"):
                    final_plan = st.session_state["lesson_planning_session"][-1]["content"]
                    st.session_state["lesson_plans"].append({
                        "title": "AI-Generated Lesson Plan",
                        "objectives": "",
                        "activities": "",
                        "materials": "",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "content": final_plan
                    })
                    st.success("Lesson plan saved!")
                    st.session_state["lesson_planning_session"] = []
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Student Performance":
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 700; color: var(--primary);"><i class="fas fa-chart-bar"></i> Student Performance</h1>', unsafe_allow_html=True)
        tabs = st.tabs(["Record Grades", "Attendance", "Analytics", "AI Feedback", "Predictive Analytics", "Automated Grading"])
        
        with tabs[0]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-plus" style="color: var(--accent); margin-right: 0.5rem;"></i>Record Student Grades</h3>', unsafe_allow_html=True)
            with st.form(key="grade_form"):
                student_name = st.text_input("Student Name", placeholder="e.g., John Doe")
                grade = st.number_input("Grade", min_value=0, max_value=100, step=1)
                assignment = st.text_input("Assignment Name", placeholder="e.g., Math Quiz 1")
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.form_submit_button("Add Grade"):
                        if student_name not in st.session_state["grades"]:
                            st.session_state["grades"][student_name] = []
                        st.session_state["grades"][student_name].append({"grade": grade, "assignment": assignment, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                        st.success(f"Grade added for {student_name}")
            if st.session_state["grades"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Recorded Grades</h3>', unsafe_allow_html=True)
                for student, grades in st.session_state["grades"].items():
                    with st.expander(f"{student}"):
                        for g in grades:
                            st.write(f"- {g['assignment']}: {g['grade']} (Logged: {g['timestamp']})")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[1]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-calendar-check" style="color: var(--accent); margin-right: 0.5rem;"></i>Record Attendance</h3>', unsafe_allow_html=True)
            with st.form(key="attendance_form"):
                student_name = st.text_input("Student Name", placeholder="e.g., John Doe")
                date = st.date_input("Date")
                status = st.selectbox("Status", ["Present", "Absent", "Tardy"])
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.form_submit_button("Record Attendance"):
                        if student_name not in st.session_state["attendance"]:
                            st.session_state["attendance"][student_name] = []
                        st.session_state["attendance"][student_name].append({"date": date, "status": status, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                        st.success(f"Attendance recorded for {student_name}")
            if st.session_state["attendance"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Attendance Records</h3>', unsafe_allow_html=True)
                for student, records in st.session_state["attendance"].items():
                    with st.expander(f"{student}"):
                        for r in records:
                            st.write(f"- {r['date']}: {r['status']} (Logged: {r['timestamp']})")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[2]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-chart-pie" style="color: var(--accent); margin-right: 0.5rem;"></i>Student Analytics</h3>', unsafe_allow_html=True)
            if st.session_state["grades"]:
                for student, grades in st.session_state["grades"].items():
                    avg_grade = sum(g["grade"] for g in grades) / len(grades)
                    st.session_state["student_analytics"][student] = avg_grade
                df_grades = pd.DataFrame(list(st.session_state["student_analytics"].items()), columns=["Student", "Average Grade"])
                fig_grade = px.bar(df_grades, x="Student", y="Average Grade", title="Average Grades per Student", color="Average Grade", 
                                   color_continuous_scale="Viridis", height=400)
                st.plotly_chart(fig_grade, use_container_width=True)
            if st.session_state["attendance"]:
                attendance_summary = {student: {"Present": 0, "Absent": 0, "Tardy": 0} for student in st.session_state["attendance"]}
                for student, records in st.session_state["attendance"].items():
                    for r in records:
                        attendance_summary[student][r["status"]] += 1
                df_attendance = pd.DataFrame(attendance_summary).T
                fig_att = px.bar(df_attendance, title="Attendance Summary", barmode="stack", height=400, 
                                 color_discrete_map={"Present": "#28A745", "Absent": "#DC3545", "Tardy": "#F59E0B"})
                st.plotly_chart(fig_att, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[3]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-robot" style="color: var(--accent); margin-right: 0.5rem;"></i>AI Feedback</h3>', unsafe_allow_html=True)
            if st.session_state["grades"]:
                selected_student = st.selectbox("Select Student for AI Feedback", list(st.session_state["grades"].keys()), key="student_select")
                if st.button("Generate Feedback", key="gen_grade_feedback"):
                    grades = [g["grade"] for g in st.session_state["grades"][selected_student]]
                    avg_grade = sum(grades) / len(grades)
                    prompt = f"Provide constructive feedback for {selected_student} with grades: {grades} and average: {avg_grade:.2f}"
                    response = generate_ai_response(prompt)
                    st.markdown('<div class="custom-card"><h4 style="color: var(--primary);">AI-Generated Feedback</h4></div>', unsafe_allow_html=True)
                    st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[4]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-brain" style="color: var(--accent); margin-right: 0.5rem;"></i>Predictive Analytics</h3>', unsafe_allow_html=True)
            if st.session_state["grades"] and st.session_state["attendance"]:
                data_summary = "\n".join([f"{student}: Grades - {', '.join([str(g['grade']) for g in grades])}, Attendance - {sum(1 for r in st.session_state['attendance'].get(student, []) if r['status'] == 'Present')} out of {len(st.session_state['attendance'].get(student, []))}" for student, grades in st.session_state["grades"].items()])
                prompt = f"Analyze the following student data and predict their future performance. Identify any students at risk and suggest interventions.\n\n{data_summary}"
                response = generate_ai_response(prompt)
                st.write(response)
            else:
                st.info("No data available for predictive analytics.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[5]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-robot" style="color: var(--accent); margin-right: 0.5rem;"></i>Automated Grading</h3>', unsafe_allow_html=True)
            with st.form("grading_form"):
                assignment_prompt = st.text_area("Assignment Prompt", placeholder="e.g., Write a short essay on the causes of World War I.")
                student_response = st.text_area("Student Response", height=200)
                if st.form_submit_button("Grade Assignment"):
                    if assignment_prompt and student_response:
                        prompt = f"Grade the following student response based on the assignment prompt. Provide a score out of 10 and constructive feedback.\n\nAssignment Prompt: {assignment_prompt}\n\nStudent Response: {student_response}"
                        response = generate_ai_response(prompt)
                        st.write(response)
                    else:
                        st.warning("Please provide both the assignment prompt and student response.")
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Professional Development":
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 700; color: var(--primary);"><i class="fas fa-graduation-cap"></i> Professional Development</h1>', unsafe_allow_html=True)
        tabs = st.tabs(["Log Activities", "AI Recommendations", "Progress Tracker"])
        
        with tabs[0]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-plus" style="color: var(--accent); margin-right: 0.5rem;"></i>Log PD Activities</h3>', unsafe_allow_html=True)
            with st.form(key="pd_form"):
                activity = st.text_input("PD Activity", placeholder="e.g., Workshop on Classroom Management")
                hours = st.number_input("Hours Spent", min_value=0.0, step=0.5)
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.form_submit_button("Log Activity"):
                        st.session_state["pd_activities"].append({
                            "activity": activity,
                            "hours": hours,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.success("Activity logged successfully!")
            if st.session_state["pd_activities"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Logged Activities</h3>', unsafe_allow_html=True)
                for act in st.session_state["pd_activities"]:
                    st.markdown(f"""
                    <div class="custom-card">
                        {act['activity']} - {act['hours']} hours (Logged: {act['timestamp']})
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[1]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-robot" style="color: var(--accent); margin-right: 0.5rem;"></i>AI Recommendations</h3>', unsafe_allow_html=True)
            if st.button("Get AI PD Recommendations", key="gen_pd_recommend"):
                activities = [a["activity"] for a in st.session_state["pd_activities"]]
                prompt = f"Suggest professional development modules for {st.session_state['username']} based on recent activities: {', '.join(activities)}."
                response = generate_ai_response(prompt)
                st.markdown('<div class="custom-card"><h4 style="color: var(--primary);">AI-Suggested PD Modules</h4></div>', unsafe_allow_html=True)
                st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[2]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-chart-line" style="color: var(--accent); margin-right: 0.5rem;"></i>Progress Tracker</h3>', unsafe_allow_html=True)
            if st.session_state["pd_activities"]:
                total_hours = sum(a["hours"] for a in st.session_state["pd_activities"])
                st.metric("Total PD Hours", f"{total_hours:.2f}", delta="+2.5 this week")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=total_hours,
                    title={'text': "PD Hours Progress"},
                    gauge={'axis': {'range': [0, 50]},
                           'bar': {'color': "var(--secondary)"},
                           'steps': [{'range': [0, 25], 'color': "#DC3545"},
                                     {'range': [25, 40], 'color': "#F59E0B"},
                                     {'range': [40, 50], 'color': "#28A745"}]}
                ))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No PD activities logged yet. Start by logging an activity!")
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Collaboration":
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 700; color: var(--primary);"><i class="fas fa-users"></i> Collaboration</h1>', unsafe_allow_html=True)
        tabs = st.tabs(["Discussion Forum", "Messages", "Peer Review", "Collaborative Notes"])
        
        with tabs[0]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-comments" style="color: var(--accent); margin-right: 0.5rem;"></i>Discussion Forum</h3>', unsafe_allow_html=True)
            with st.form(key="forum_form"):
                post = st.text_area("Write a new post", placeholder="Share your thoughts or ask a question...", height=150)
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.form_submit_button("Post"):
                        st.session_state["forum_posts"].append({
                            "author": st.session_state["username"],
                            "content": post,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.success("Post added successfully!")
            if st.session_state["forum_posts"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Forum Posts</h3>', unsafe_allow_html=True)
                for post in st.session_state["forum_posts"]:
                    st.markdown(f"""
                    <div class="custom-card">
                        <strong style="color: var(--primary);">{post['author']} ({post['timestamp']})</strong>
                        <p>{post['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[1]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-envelope" style="color: var(--accent); margin-right: 0.5rem;"></i>Messages</h3>', unsafe_allow_html=True)
            recipient = st.selectbox("Select Recipient", ["teacher1", "teacher2"], help="Choose who to message")
            message = st.text_area("Write your message", placeholder="Type your message here...", height=150)
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("Send Message", key="send_msg"):
                    st.session_state["messages"].append({
                        "sender": st.session_state["username"],
                        "recipient": recipient,
                        "message": message,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.success("Message sent successfully!")
            st.markdown('<h3 class="subheader"><i class="fas fa-inbox" style="color: var(--accent); margin-right: 0.5rem;"></i>Inbox</h3>', unsafe_allow_html=True)
            for msg in st.session_state["messages"]:
                if msg["recipient"] == st.session_state["username"]:
                    st.markdown(f"""
                    <div class="custom-card">
                        <strong style="color: var(--primary);">From {msg['sender']} ({msg['timestamp']})</strong>
                        <p>{msg['message']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[2]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-user-friends" style="color: var(--accent); margin-right: 0.5rem;"></i>Peer Review Scheduling</h3>', unsafe_allow_html=True)
            with st.form(key="peer_review_form"):
                colleague = st.selectbox("Select Colleague", ["teacher1", "teacher2"], help="Choose a colleague to review")
                date = st.date_input("Observation Date")
                time = st.time_input("Observation Time")
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.form_submit_button("Schedule Peer Review"):
                        st.session_state["peer_reviews"].append({
                            "reviewer": st.session_state["username"],
                            "colleague": colleague,
                            "date": date,
                            "time": time,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.success("Peer review scheduled successfully!")
            if st.session_state["peer_reviews"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Scheduled Peer Reviews</h3>', unsafe_allow_html=True)
                for review in st.session_state["peer_reviews"]:
                    st.markdown(f"""
                    <div class="custom-card">
                        Reviewer: {review['reviewer']} for {review['colleague']} on {review['date']} at {review['time']}
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[3]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-file-alt" style="color: var(--accent); margin-right: 0.5rem;"></i>Collaborative Notes</h3>', unsafe_allow_html=True)
            with st.form("notes_form"):
                note = st.text_area("Add a note", height=100)
                if st.form_submit_button("Submit Note"):
                    st.session_state["collaborative_notes"].append({
                        "author": st.session_state["username"],
                        "note": note,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "votes": 0,
                        "comments": []
                    })
                    st.success("Note added successfully!")
            if st.session_state["collaborative_notes"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Shared Notes</h3>', unsafe_allow_html=True)
                for idx, note in enumerate(st.session_state["collaborative_notes"]):
                    st.markdown(f"""
                    <div class="custom-card">
                        <strong>{note['author']} ({note['timestamp']})</strong>
                        <p>{note['note']}</p>
                        <div>Votes: {note['votes']}</div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Upvote", key=f"upvote_{idx}"):
                        st.session_state["collaborative_notes"][idx]["votes"] += 1
                        st.rerun()
                    comment = st.text_input(f"Comment on this note", key=f"comment_{idx}")
                    if st.button(f"Add Comment", key=f"add_comment_{idx}"):
                        st.session_state["collaborative_notes"][idx]["comments"].append({
                            "author": st.session_state["username"],
                            "comment": comment,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.rerun()
                    for c in note["comments"]:
                        st.markdown(f"""
                        <div class="custom-card" style="margin-left: 2rem;">
                            <strong>{c['author']} ({c['timestamp']})</strong>
                            <p>{c['comment']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Well-Being":
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 700; color: var(--primary);"><i class="fas fa-heart"></i> Teacher Well-Being</h1>', unsafe_allow_html=True)
        tabs = st.tabs(["Mood Tracker", "AI Support"])
        
        with tabs[0]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-smile" style="color: var(--accent); margin-right: 0.5rem;"></i>Mood Tracker</h3>', unsafe_allow_html=True)
            with st.form(key="wellbeing_form"):
                mood = st.text_area("How are you feeling today?", placeholder="Describe your mood or day...", height=150)
                stress_level = st.slider("Stress Level", 0, 10, 5, help="Rate your stress from 0 (low) to 10 (high)")
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.form_submit_button("Log Mood"):
                        st.session_state["wellbeing_logs"].append({
                            "mood": mood,
                            "stress": stress_level,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.success("Mood logged successfully!")
            if st.session_state["wellbeing_logs"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-history" style="color: var(--accent); margin-right: 0.5rem;"></i>Mood History</h3>', unsafe_allow_html=True)
                for log in st.session_state["wellbeing_logs"]:
                    st.markdown(f"""
                    <div class="custom-card">
                        <strong>{log['timestamp']}</strong>
                        <p>Mood: {log['mood']}</p>
                        <p>Stress: {log['stress']}/10</p>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[1]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-robot" style="color: var(--accent); margin-right: 0.5rem;"></i>AI Support</h3>', unsafe_allow_html=True)
            if st.button("Get AI Well-Being Tips", key="gen_wellbeing_tips"):
                logs = [f"{l['mood']} (Stress: {l['stress']})" for l in st.session_state["wellbeing_logs"]]
                prompt = f"Provide well-being tips for a teacher based on recent mood logs: {', '.join(logs)}."
                response = generate_ai_response(prompt)
                st.markdown('<div class="custom-card"><h4 style="color: var(--primary);">AI Tips</h4></div>', unsafe_allow_html=True)
                st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Observation and Feedback":
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 700; color: var(--primary);"><i class="fas fa-eye"></i> Observation & Feedback</h1>', unsafe_allow_html=True)
        tabs = st.tabs(["Record Observation", "AI Analysis", "Real-Time Observation"])
        
        with tabs[0]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-plus" style="color: var(--accent); margin-right: 0.5rem;"></i>Record Classroom Observation</h3>', unsafe_allow_html=True)
            with st.form(key="observation_form"):
                observation = st.text_area("Observation Notes", placeholder="e.g., teaching style, student engagement...", height=150)
                uploaded_file = st.file_uploader("Upload Video/Audio (optional)", type=["mp4", "mp3"])
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.form_submit_button("Save Observation"):
                        observation_data = {
                            "notes": observation,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "file": uploaded_file.name if uploaded_file else None
                        }
                        st.session_state["observations"].append(observation_data)
                        st.success("Observation saved successfully!")
            if st.session_state["observations"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Saved Observations</h3>', unsafe_allow_html=True)
                for obs in st.session_state["observations"]:
                    with st.expander(f"{obs['timestamp']}"):
                        st.markdown(f"**Notes:** {obs['notes']}")
                        if obs["file"]:
                            st.markdown(f"**Attached File:** {obs['file']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[1]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-robot" style="color: var(--accent); margin-right: 0.5rem;"></i>AI Analysis</h3>', unsafe_allow_html=True)
            if st.session_state["observations"]:
                selected_observation = st.selectbox("Select Observation", [o["timestamp"] for o in st.session_state["observations"]], key="obs_select")
                if st.button("Analyze with AI", key="analyze_obs"):
                    obs = next(o for o in st.session_state["observations"] if o["timestamp"] == selected_observation)
                    prompt = f"Analyze the following classroom observation and provide detailed feedback: {obs['notes']}"
                    if obs["file"]:
                        prompt += f" (Note: Includes a {obs['file']} file, assume it supports the notes)."
                    response = generate_ai_response(prompt)
                    st.markdown('<div class="custom-card"><h4 style="color: var(--primary);">AI Analysis</h4></div>', unsafe_allow_html=True)
                    st.write(response)
            else:
                st.info("No observations available for analysis yet.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[2]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-video" style="color: var(--accent); margin-right: 0.5rem;"></i>Real-Time Observation</h3>', unsafe_allow_html=True)
            st.write("Get AI-driven insights during live classroom sessions.")
            live_notes = st.text_area("Enter live observation notes", placeholder="e.g., Students are engaged with group work...", height=150)
            col1, col2 = st.columns([2, 1])
            with col2:
                if st.button("Analyze Live Session", key="analyze_live"):
                    if live_notes:
                        prompt = f"Analyze these live classroom observation notes and provide real-time feedback: {live_notes}"
                        response = generate_ai_response(prompt)
                        st.session_state["live_observations"].append({
                            "notes": live_notes,
                            "feedback": response,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.markdown('<div class="custom-card"><h4 style="color: var(--primary);">AI Real-Time Feedback</h4></div>', unsafe_allow_html=True)
                        st.write(response)
                    else:
                        st.warning("Please enter some notes to analyze.")
            if st.session_state["live_observations"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-history" style="color: var(--accent); margin-right: 0.5rem;"></i>Live Observation History</h3>', unsafe_allow_html=True)
                for obs in st.session_state["live_observations"]:
                    with st.expander(f"{obs['timestamp']}"):
                        st.markdown(f"**Notes:** {obs['notes']}")
                        st.markdown(f"**AI Feedback:** {obs['feedback']}")
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Classroom Management":
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 700; color: var(--primary);"><i class="fas fa-chalkboard-teacher"></i> Classroom Management</h1>', unsafe_allow_html=True)
        tabs = st.tabs(["Live Attendance", "Instant Feedback"])
        
        with tabs[0]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-calendar-check" style="color: var(--accent); margin-right: 0.5rem;"></i>Live Attendance</h3>', unsafe_allow_html=True)
            student_list = list(st.session_state["grades"].keys())
            if not student_list:
                st.info("No students registered yet. Add student grades first.")
            else:
                with st.form("live_attendance_form"):
                    attendance_data = {}
                    for student in student_list:
                        attendance_data[student] = st.selectbox(f"Status for {student}", ["Present", "Absent", "Tardy"], key=f"att_{student}")
                    if st.form_submit_button("Record Attendance"):
                        date = datetime.now().date()
                        for student, status in attendance_data.items():
                            if student not in st.session_state["attendance"]:
                                st.session_state["attendance"][student] = []
                            st.session_state["attendance"][student].append({
                                "date": date,
                                "status": status,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                        st.success("Attendance recorded successfully!")
            if st.session_state["attendance"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Today\'s Attendance</h3>', unsafe_allow_html=True)
                today = datetime.now().date()
                for student, records in st.session_state["attendance"].items():
                    today_records = [r for r in records if r["date"] == today]
                    if today_records:
                        with st.expander(f"{student}"):
                            for r in today_records:
                                st.write(f"- {r['date']}: {r['status']} (Logged: {r['timestamp']})")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tabs[1]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subheader"><i class="fas fa-comment" style="color: var(--accent); margin-right: 0.5rem;"></i>Instant Feedback</h3>', unsafe_allow_html=True)
            student_list = list(st.session_state["grades"].keys())
            if not student_list:
                st.info("No students registered yet. Add student grades first.")
            else:
                with st.form("feedback_form"):
                    student = st.selectbox("Select Student", student_list, key="feedback_student")
                    predefined_feedback = st.selectbox("Predefined Feedback", [
                        "Great participation!",
                        "Needs improvement in engagement.",
                        "Excellent work on the assignment.",
                        "Please focus more during class."
                    ], key="predefined_feedback")
                    custom_feedback = st.text_area("Custom Feedback (optional)", height=100, key="custom_feedback")
                    if st.form_submit_button("Send Feedback"):
                        feedback = custom_feedback if custom_feedback else predefined_feedback
                        if "feedback_log" not in st.session_state:
                            st.session_state["feedback_log"] = []
                        st.session_state["feedback_log"].append({
                            "student": student,
                            "feedback": feedback,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.success(f"Feedback sent to {student}!")
            if "feedback_log" in st.session_state and st.session_state["feedback_log"]:
                st.markdown('<h3 class="subheader"><i class="fas fa-list" style="color: var(--accent); margin-right: 0.5rem;"></i>Feedback Log</h3>', unsafe_allow_html=True)
                for fb in st.session_state["feedback_log"]:
                    st.markdown(f"""
                    <div class="custom-card">
                        <strong>To {fb['student']} ({fb['timestamp']})</strong>
                        <p>{fb['feedback']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Admin Tools":
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 700; color: var(--primary);"><i class="fas fa-tools"></i> Admin Tools</h1>', unsafe_allow_html=True)
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="subheader"><i class="fas fa-tachometer-alt" style="color: var(--accent); margin-right: 0.5rem;"></i>Dashboard</h3>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Teachers", 3, delta="Static")
        with col2:
            st.metric("PD Activities", len(st.session_state["pd_activities"]), delta="+1 this week")
        with col3:
            st.metric("Observations", len(st.session_state["observations"]), delta="Recent")
        with col4:
            st.metric("Grades", sum(len(g) for g in st.session_state["grades"].values()), delta="Updated")
        
        st.markdown('<h3 class="subheader"><i class="fas fa-chart-bar" style="color: var(--accent); margin-right: 0.5rem;"></i>Teacher Performance Analytics</h3>', unsafe_allow_html=True)
        if st.session_state["pd_activities"]:
            pd_data = pd.DataFrame(st.session_state["pd_activities"])
            pd_data["teacher"] = st.session_state["username"]
            fig = px.bar(pd_data.groupby("teacher")["hours"].sum(), title="PD Hours by Teacher", color="hours", 
                         color_continuous_scale="Blues", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        if st.button("Generate Intervention Plan", key="gen_intervention"):
            prompt = f"Generate an intervention plan based on teacher PD activities, observations, and student performance data for {st.session_state['username']}."
            response = generate_ai_response(prompt)
            st.markdown('<div class="custom-card"><h4 style="color: var(--primary);">AI-Generated Intervention Plan</h4></div>', unsafe_allow_html=True)
            st.write(response)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()