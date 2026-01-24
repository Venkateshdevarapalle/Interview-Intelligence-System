from utils.keras_fix import *   # MUST be first
from deepface import DeepFace
import cv2



def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    face_frames = 0
    emotions = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1

        try:
            result = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False
            )

            face_frames += 1
            emotions.append(result[0]["dominant_emotion"])

        except Exception:
            pass

    cap.release()

    # Camera presence score
    camera_presence = round(
        (face_frames / total_frames) * 10, 2
    ) if total_frames > 0 else 0

    # Environment quality (simple heuristic)
    environment_quality = (
        "Good" if camera_presence >= 6 else "Needs Improvement"
    )

    return {
        "camera_presence_score": camera_presence,
        "environment_quality": environment_quality,
        "frames_analyzed": total_frames,
        "face_detected_frames": face_frames,
        "dominant_emotion": max(set(emotions), key=emotions.count)
        if emotions else "neutral"
    }
