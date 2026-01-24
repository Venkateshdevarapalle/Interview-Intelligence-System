import av
import time
from streamlit_webrtc import VideoProcessorBase

OUTPUT_VIDEO = "uploads/live_interview.mp4"

class LiveRecorder(VideoProcessorBase):
    def __init__(self):
        self.container = av.open(OUTPUT_VIDEO, mode="w")
        self.stream = self.container.add_stream("h264", rate=30)
        self.start_time = time.time()
        self.stopped = False

    def recv(self, frame):
        if self.stopped:
            return frame

        img = frame.to_ndarray(format="bgr24")
        video_frame = av.VideoFrame.from_ndarray(img, format="bgr24")
        packet = self.stream.encode(video_frame)

        if packet:
            self.container.mux(packet)

        return frame

    def stop(self):
        self.stopped = True
        self.container.close()
