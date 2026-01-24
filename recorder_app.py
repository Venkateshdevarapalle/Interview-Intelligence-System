import gradio as gr
import cv2
import time
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

OUTPUT_PATH = os.path.join(UPLOAD_DIR, "live_interview.mp4")

def record_interview(topic, time_limit):
    cap = cv2.VideoCapture(0)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        OUTPUT_PATH,
        cv2.VideoWriter_fourcc(*'mp4v'),
        20,
        (width, height)
    )

    # Countdown
    for i in range(5, 0, -1):
        ret, frame = cap.read()
        cv2.putText(frame, f"Starting in {i}",
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0,0,255), 3)
        cv2.imshow("Interview Recorder", frame)
        cv2.waitKey(1000)

    start_time = time.time()
    max_time = time_limit * 60

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        elapsed = int(time.time() - start_time)
        remaining = max_time - elapsed

        cv2.putText(frame, f"Topic: {topic}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0,255,0), 2)

        cv2.putText(frame, f"Time Left: {remaining}s",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0,255,0), 2)

        out.write(frame)
        cv2.imshow("Interview Recorder", frame)

        if remaining <= 0:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return "Recording complete. You can return to Streamlit."

iface = gr.Interface(
    fn=record_interview,
    inputs=[
        gr.Textbox(label="Interview Topic"),
        gr.Number(label="Time Limit (minutes)", value=2)
    ],
    outputs="text",
    title="Live Interview Recorder",
    description="Press START, speak confidently. Press Q to end early."
)

iface.launch()
