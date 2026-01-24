import streamlit as st
import random
import os

from analysis.video_analyzer import analyze_video
from analysis.audio_analyzer import analyze_audio
from analysis.nlp_analyzer import analyze_nlp
from scoring.scoring_engine import compute_scores
from utils.report_generator import generate_report, generate_tips

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config("Interview Intelligence System", layout="centered")

st.title("🎤 Interview Intelligence System")

candidate = st.text_input("Candidate Name")

mode = st.radio(
    "Select Interview Mode",
    ["Upload Interview Video", "Live Interview"]
)

TOPICS = [
    # Technical / Academic
    "Explain your final year project",
    "What is Data Science?",
    "Explain Machine Learning with a real-world example",
    "What is the difference between supervised and unsupervised learning?",
    "Explain overfitting and how to avoid it",
    "Describe a challenging technical problem you solved",
    "How would you explain AI to a non-technical person?",
    "What programming language are you most comfortable with and why?",

    # Problem Solving
    "Describe a real-world problem you solved",
    "Explain a situation where you optimized or improved a process",
    "How would you approach solving an unknown problem?",
    "Describe a failure and what you learned from it",

    # Behavioral / HR
    "What are your strengths and weaknesses?",
    "Tell me about a time you worked in a team",
    "Describe a situation where you handled pressure",
    "How do you manage time when facing deadlines?",
    "Tell me about a conflict you resolved",

    # Career & Thinking
    "Why should we hire you?",
    "Where do you see yourself in five years?",
    "Explain a recent technology trend you find interesting"
]

# ---------------- UPLOAD MODE ----------------
if mode == "Upload Interview Video":
    video_file = st.file_uploader("Upload Interview Video (MP4)", type=["mp4"])

    if st.button("Analyze Interview"):
        if not candidate or not video_file:
            st.warning("Please enter candidate name and upload video.")
        else:
            path = os.path.join(UPLOAD_DIR, video_file.name)
            with open(path, "wb") as f:
                f.write(video_file.read())

            with st.spinner("Analyzing interview..."):
                video = analyze_video(path)
                audio = analyze_audio(path)
                nlp = analyze_nlp(audio["transcript_words"]) if audio["has_audio"] else {}
                scores = compute_scores(video, audio, nlp)
                tips = generate_tips(scores)
                pdf = generate_report(candidate, "Uploaded Interview", scores)

            st.success("Analysis Complete")
            st.json(scores)
            for tip in tips:
                st.write("•", tip)
            st.download_button("Download PDF", open(pdf, "rb"))

# ---------------- LIVE MODE ----------------
elif mode == "Live Interview":
    topic = random.choice(TOPICS)
    time_limit = st.selectbox("Select Time Limit (minutes)", [1,2,3,5])

    st.info(f"🎯 Topic: {topic}")
    st.markdown("""
    ### Instructions
    - Maintain eye contact
    - Speak clearly
    - Avoid filler words
    - Structure: Problem → Solution → Impact
    """)

    st.markdown(
        f"""
        <a href="http://localhost:7860" target="_blank">
            <button style="
            background:#4CAF50;color:white;
            padding:12px 20px;font-size:16px;
            border:none;border-radius:5px;">
            🎥 Start Live Interview
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    if st.button("Analyze Live Interview"):
        path = os.path.join(UPLOAD_DIR, "live_interview.mp4")

        if not os.path.exists(path):
            st.error("❌ No recording found. Please complete interview first.")
        else:
            with st.spinner("Analyzing interview..."):
                video = analyze_video(path)
                audio = analyze_audio(path)
                nlp = analyze_nlp(audio["transcript_words"]) if audio["has_audio"] else {}
                scores = compute_scores(video, audio, nlp)
                tips = generate_tips(scores)
                pdf = generate_report(candidate, topic, scores)

            st.success("Live Interview Analysis Complete")
            st.json(scores)
            for tip in tips:
                st.write("•", tip)
            st.download_button("Download PDF", open(pdf, "rb"))
