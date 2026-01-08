import streamlit as st
import pandas as pd
import io
import os

from data_processing import read_input, compute_totals_and_percentage, save_processed
from database_handler import init_db, insert_processed_dataframe
from visualization import (subject_average_bar, grade_distribution_pie, attendance_vs_percentage_scatter,
                          student_subject_radar, student_performance_bar)

st.set_page_config(
    page_title="Student Performance Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
        border-bottom: 3px solid #1f77b4;
    }
    h2, h3 {
        color: #2c3e50;
        margin-top: 1.5rem;
    }
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Student Performance Analysis & Management System")

# Ensure DB exists
init_db()

st.sidebar.header("⚙️ Configuration")
sidebar_choice = st.sidebar.selectbox("📁 Choose Input", ["Use sample file (Data/sample_data.xlsx)", "Upload file"])

if sidebar_choice.startswith("Use sample"):
    default_path = os.path.join('Data', 'sample_data.xlsx')
    if not os.path.exists(default_path):
        st.error(f"❌ Sample file not found at {default_path}. Please place Data/sample_data.xlsx and rerun.")
        st.stop()
    df = read_input(default_path)
    st.sidebar.success("✅ Sample file loaded")
else:
    uploaded = st.sidebar.file_uploader("📤 Upload Excel (.xlsx) or CSV", type=['xlsx','csv'])
    if uploaded is None:
        st.info("ℹ️ Upload a file to continue, or choose 'Use sample file' from the sidebar.")
        st.stop()
    if uploaded.name.endswith('.csv'):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)
    st.sidebar.success(f"✅ {uploaded.name} loaded")

st.subheader("📋 Raw Data")
st.dataframe(df, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.header("🔄 Actions")

if st.sidebar.button("🚀 Process Data"):
    with st.spinner("Processing data..."):
        processed = compute_totals_and_percentage(df)
    
    # Store processed data in session state
    st.session_state['processed_data'] = processed
    
    st.subheader("✅ Processed Data")
    
    # Download processed file
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        to_download = io.BytesIO()
        processed.to_excel(to_download, index=False, engine='openpyxl')
        to_download.seek(0)
        st.download_button("📥 Download Processed Excel", data=to_download, file_name="processed_sample_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    # Save processed file locally
    save_processed(processed)
    st.success("💾 Processed file saved to Data/processed_sample_data.xlsx")

# Display analytics if data is processed
if 'processed_data' in st.session_state:
    processed = st.session_state['processed_data']
    known = {'Roll_No','Name','Total','Percentage','Grade','Attendance(%)'}
    subj_cols = [c for c in processed.columns if c not in known]
    
    st.markdown("---")
    
    # View selector
    view_mode = st.radio("📊 Select View", ["All Students Analysis", "Individual Student Details"], horizontal=True)
    
    if view_mode == "All Students Analysis":
        st.subheader("📈 Overall Performance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if subj_cols:
                st.markdown("#### Subject-wise Average Marks")
                fig1 = subject_average_bar(processed, subj_cols)
                st.pyplot(fig1, use_container_width=True)
            
            st.markdown("#### Attendance vs Performance")
            fig3 = attendance_vs_percentage_scatter(processed)
            st.pyplot(fig3, use_container_width=True)
        
        with col2:
            st.markdown("#### Grade Distribution")
            fig2 = grade_distribution_pie(processed)
            st.pyplot(fig2, use_container_width=True)
            
            # Summary statistics
            st.markdown("#### 📊 Summary Statistics")
            stats_col1, stats_col2 = st.columns(2)
            with stats_col1:
                st.metric("Average Percentage", f"{processed['Percentage'].mean():.2f}%")
                st.metric("Total Students", len(processed))
            with stats_col2:
                st.metric("Average Attendance", f"{processed['Attendance(%)'].mean():.2f}%")
                st.metric("Pass Rate", f"{(processed['Grade'] != 'F').sum() / len(processed) * 100:.1f}%")
        
        # Display full data table
        st.markdown("---")
        st.markdown("#### 📋 Complete Student Records")
        st.dataframe(processed, use_container_width=True)
    
    else:
        st.subheader("👤 Individual Student Analysis")
        
        # Student selector
        student_options = [f"{row['Roll_No']} - {row['Name']}" for _, row in processed.iterrows()]
        selected_student = st.selectbox("Select a student:", student_options)
        
        if selected_student:
            roll_no = int(selected_student.split(' - ')[0])
            student_data = processed[processed['Roll_No'] == roll_no].iloc[0]
            
            # Student info card
            st.markdown(f"### 🎓 {student_data['Name']} (Roll No: {student_data['Roll_No']})")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Marks", f"{student_data['Total']:.0f}")
            with col2:
                grade_color = "🟢" if student_data['Grade'] in ['A+', 'A'] else "🟡" if student_data['Grade'] == 'B' else "🔴"
                st.metric("Grade", f"{grade_color} {student_data['Grade']}")
            with col3:
                st.metric("Percentage", f"{student_data['Percentage']:.2f}%")
            with col4:
                st.metric("Attendance", f"{student_data['Attendance(%)']:.1f}%")
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Subject-wise Performance")
                fig_bar = student_performance_bar(student_data, subj_cols)
                st.pyplot(fig_bar, use_container_width=True)
            
            with col2:
                st.markdown("#### 🎯 Performance vs Class Average")
                class_avg = processed[subj_cols].mean()
                fig_radar = student_subject_radar(student_data, subj_cols, class_avg)
                st.pyplot(fig_radar, use_container_width=True)
            
            # Detailed marks table
            st.markdown("---")
            st.markdown("#### 📝 Detailed Subject Marks")
            subject_data = pd.DataFrame({
                'Subject': subj_cols,
                'Marks Obtained': [student_data[s] for s in subj_cols],
                'Class Average': [class_avg[s] for s in subj_cols],
                'Difference': [student_data[s] - class_avg[s] for s in subj_cols]
            })
            subject_data['Status'] = subject_data['Difference'].apply(
                lambda x: '🟢 Above Average' if x > 0 else '🔴 Below Average' if x < 0 else '🟡 At Average'
            )
            st.dataframe(subject_data, use_container_width=True)

if st.sidebar.button("💾 Insert into Database"):
    try:
        processed = compute_totals_and_percentage(df)
        insert_processed_dataframe(processed)
        st.sidebar.success("✅ Data inserted into SQLite DB")
    except Exception as e:
        st.sidebar.error(f"❌ DB insert failed: {e}")