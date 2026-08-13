import streamlit as st
from deepface import DeepFace
import tempfile
import os

st.title("🔐 Face Comparison Module")

doc_image = st.file_uploader(
    "Upload Aadhaar / Document Photo",
    type=["jpg", "jpeg", "png"]
)

live_image = st.camera_input("Capture Live Face")

if doc_image and live_image:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f1:
        f1.write(doc_image.read())
        doc_path = f1.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f2:
        f2.write(live_image.getvalue())
        live_path = f2.name

    st.info("Comparing faces...")

    try:
        result = DeepFace.verify(
            img1_path=doc_path,
            img2_path=live_path,
            enforce_detection=True
        )

        if result["verified"]:
            st.success("✅ VERIFIED - Same Person")
        else:
            st.error("❌ FAKE KYC ALERT - Different Person")

        st.write("Distance:", result["distance"])

    except Exception as e:
        st.error(str(e))

    finally:
        if os.path.exists(doc_path):
            os.remove(doc_path)

        if os.path.exists(live_path):
            os.remove(live_path)