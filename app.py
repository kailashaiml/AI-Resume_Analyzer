import streamlit as st
import pdfplumber
import re
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🤖 AI Resume Analyzer")
st.write("Upload your resume and get AI-powered analysis")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)

if uploaded_file:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    st.success("Resume uploaded successfully!")

    st.subheader("Resume Text")
    st.write(text)

    # Candidate Name
    lines = text.split("\n")

    if len(lines) > 0:
        name = lines[0].strip()

        st.subheader("👤 Candidate Name")
        st.write(name)

    # Email
    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)

    if email:
        st.subheader("📧 Email")
        st.write(email[0])
    else:
        st.warning("Email not found")

    # Phone Number
    phone = re.findall(r'\b\d{10}\b', text)

    if phone:
        st.subheader("📱 Phone Number")
        st.write(phone[0])
    else:
        st.warning("Phone number not found")

    st.subheader("📋 Resume Analysis")

    score = 0

    if "Python" in text:
        st.success("✅ Python skill found")
        score += 25
    else:
        st.warning("❌ Python skill not found")

    if "Machine Learning" in text:
        st.success("✅ Machine Learning skill found")
        score += 25
    else:
        st.warning("❌ Machine Learning skill not found")

    if "Communication" in text:
        st.success("✅ Communication skill found")
        score += 25
    else:
        st.warning("❌ Communication skill not found")

    if "Projects" in text:
        st.success("✅ Projects section found")
        score += 25
    else:
        st.warning("❌ Projects section not found")

    st.subheader("📊 Resume Score")

    st.progress(score / 100)

    st.write(f"Your Resume Score is: {score}/100")

    # Pie Chart

    labels = [
        "Python",
        "Machine Learning",
        "Communication",
        "Projects"
    ]

    sizes = [25, 25, 25, 25]

    fig, ax = plt.subplots()

    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%"
    )

    ax.axis("equal")

    st.subheader("📈 Skills Chart")

    st.pyplot(fig)

    # AI Suggestions

    st.subheader("💡 AI Suggestions")

    if score >= 75:
        st.success(
            "Excellent resume! Keep improving your projects and skills."
        )

    elif score >= 50:
        st.info(
            "Good resume. Add more projects and technical skills."
        )

    else:
        st.warning(
            "Resume needs improvement. Add skills, projects and certifications."
        )

    # Download Report

    report = f"""
Candidate Name : {name if len(lines)>0 else "N/A"}

Email : {email[0] if email else "N/A"}

Phone : {phone[0] if phone else "N/A"}

Resume Score : {score}/100
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="resume_report.txt",
        mime="text/plain"
    )