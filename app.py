import streamlit as st
import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

st.title("🎬 AttentionX Lite - AI Clip Generator")

uploaded_file = st.file_uploader("Upload a video", type=["mp4"])

if uploaded_file:
    with open("video.mp4", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Video uploaded successfully!")

    if st.button("Generate Clips"):
        st.write("Processing...")

        # Load Whisper model
        model = whisper.load_model("base")

        # Transcribe video
        result = model.transcribe("video.mp4")

        video = VideoFileClip("video.mp4")

        clips = []

        # Take first 3 segments (simple logic)
        for i, seg in enumerate(result['segments'][:3]):
            start = seg['start']
            end = seg['end']
            text = seg['text']

            clip = video.subclip(start, end)

            txt = TextClip(text, fontsize=40, color='white')\
                    .set_position(('center', 'bottom'))\
                    .set_duration(clip.duration)

            final = CompositeVideoClip([clip, txt])

            output = f"clip_{i}.mp4"
            final.write_videofile(output)

            clips.append(output)

        st.success("Clips Generated!")

        for c in clips:
            st.video(c)
