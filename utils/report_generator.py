from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def generate_tips(scores):
    tips = []

    # Confidence
    confidence = scores.get("Confidence", {}).get("score")
    if isinstance(confidence, (int, float)) and confidence < 6:
        tips.append("❌ Low confidence detected. Practice speaking slower and maintaining posture.")

    # Camera Presence
    cam = scores.get("Camera Presence", {}).get("score")
    if isinstance(cam, (int, float)) and cam < 6:
        tips.append("📷 Improve eye contact by looking directly into the camera.")

    # Voice & Clarity (ONLY if audio exists)
    voice = scores.get("Voice & Clarity", {}).get("score")
    if isinstance(voice, (int, float)) and voice < 6:
        tips.append("🔊 Improve voice clarity by speaking clearly and reducing pauses.")

    # Filler Words
    fillers = scores.get("Filler Words", {}).get("count")
    if isinstance(fillers, int) and fillers > 10:
        tips.append(f"🗣 High filler word usage detected ({fillers}). Try pausing instead.")

    # Overall score
    interview_score = scores.get("Interview Score")
    if isinstance(interview_score, (int, float)) and interview_score < 60:
        tips.append("💡 Structure answers as Problem → Solution → Impact.")

    if not tips:
        tips.append("✅ Strong interview performance. Keep practicing for consistency.")

    return tips


def generate_report(candidate, topic, scores):
    os.makedirs("reports", exist_ok=True)

    filename = f"reports/{candidate.replace(' ', '_')}_Interview_Report.pdf"
    c = canvas.Canvas(filename, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Interview Intelligence Report")

    c.setFont("Helvetica", 11)
    c.drawString(50, 770, f"Candidate: {candidate}")
    c.drawString(50, 750, f"Topic: {topic}")
    c.drawString(50, 730, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}")

    y = 690
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Scores")
    y -= 20

    c.setFont("Helvetica", 11)
    for key, value in scores.items():
        if isinstance(value, dict):
            score = value.get("score", value.get("count", "N/A"))
            label = value.get("label", "")
            c.drawString(50, y, f"{key}: {score} {label}")
        else:
            c.drawString(50, y, f"{key}: {value}")
        y -= 18

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Improvement Tips")
    y -= 20

    c.setFont("Helvetica", 11)
    for tip in generate_tips(scores):
        c.drawString(60, y, f"- {tip}")
        y -= 16

    c.save()
    return filename
