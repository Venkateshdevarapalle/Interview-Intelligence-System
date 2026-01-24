def label(score):
    if score >= 8:
        return "Strong"
    elif score >= 5:
        return "Moderate"
    else:
        return "Weak"


def compute_scores(video, audio, nlp):

    camera_presence = round(video.get("camera_presence_score", 0), 2)

    # Handle missing audio safely
    speech_confidence = audio.get("speech_confidence")
    audio_available = speech_confidence is not None

    if audio_available:
        confidence = round((camera_presence + speech_confidence) / 2, 2)
        voice_clarity = round(speech_confidence, 2)
    else:
        confidence = round(camera_presence * 0.6, 2)
        voice_clarity = None

    filler_count = nlp.get("filler_count", 0)

    interview_score = round(
        (
            camera_presence * 2 +
            (voice_clarity if voice_clarity else 0) * 2 +
            max(10 - filler_count, 0)
        ) / 6 * 10,
        2
    )

    scores = {
        "Confidence": {
            "score": confidence,
            "label": label(confidence)
        },
        "Camera Presence": {
            "score": camera_presence,
            "label": label(camera_presence)
        },
        "Voice & Clarity": (
            {
                "score": voice_clarity,
                "label": label(voice_clarity)
            } if audio_available else {
                "score": None,
                "label": "No Audio Detected"
            }
        ),
        "Filler Words": {
            "count": filler_count if audio_available else "N/A"
        },
        "Interview Score": interview_score
    }

    if not audio_available:
        scores["Audio Status"] = "No audio detected in uploaded video"

    return scores
