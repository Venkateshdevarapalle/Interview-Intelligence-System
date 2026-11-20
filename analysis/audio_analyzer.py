import os
import subprocess
import wave
import json
from vosk import Model, KaldiRecognizer

FFMPEG_PATH = r"C:\Tools\ffmpeg.exe"


MODEL_PATH = r"C:\Interview_Intelligence_System\models\vosk-model-small-en-us-0.15"

def analyze_audio(video_path):
    uploads_dir = os.path.dirname(video_path)
    wav_path = os.path.join(uploads_dir, "temp.wav")

    # Try extracting audio
    cmd = f'"{FFMPEG_PATH}" -y -i "{video_path}" -ac 1 -ar 16000 "{wav_path}"'
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # If FFmpeg failed or WAV not created → NO AUDIO
    if result.returncode != 0 or not os.path.exists(wav_path):
        return {
            "has_audio": False,
            "speech_confidence": None,
            "transcript_words": []
        }

    # Load speech model
    #load
    model = Model(MODEL_PATH)
    wf = wave.open(wav_path, "rb")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    words = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            words.extend(res.get("result", []))

    final = json.loads(rec.FinalResult())
    words.extend(final.get("result", []))

    transcript_words = [w["word"] for w in words]

    return {
        "has_audio": True,
        "speech_confidence": round(min(len(transcript_words) / 120, 1.0) * 10, 2),
        "transcript_words": transcript_words
    }
