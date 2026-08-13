import streamlit as st
from PIL import Image
import pytesseract
import numpy as np
import cv2
from deepface import DeepFace
import tempfile
import os

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Page Config
st.set_page_config(
    page_title="AI Based Fake KYC Alarm System",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 AI Based Fake KYC Alarm System")
st.write("Upload Aadhaar Card and verify identity using Face Recognition.")

# Upload Aadhaar
uploaded_file = st.file_uploader(
    "📄 Upload Aadhaar Card",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("📄 Uploaded Aadhaar Card")
    st.image(image, use_container_width=True)

    img = np.array(image)

    # ==========================
    # OCR EXTRACTION
    # ==========================

    st.subheader("📄 OCR Extraction")

    gray_ocr = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    gray_ocr = cv2.GaussianBlur(
        gray_ocr,
        (3, 3),
        0
    )

    thresh = cv2.threshold(
        gray_ocr,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    extracted_text = pytesseract.image_to_string(
        thresh,
        config="--oem 3 --psm 11"
    )

    # ==========================
    # DOCUMENT DETECTION
    # ==========================

    st.subheader("📋 Document Analysis")

    text_upper = extracted_text.upper()

    if (
        "AADHAAR" in text_upper
        or "GOVERNMENT OF INDIA" in text_upper
        or "DOB" in text_upper
        or "FEMALE" in text_upper
        or "MALE" in text_upper
    ):
        document_type = "Aadhaar Card"
    else:
        document_type = "Unknown Document"

    st.success(f"Detected Document Type: {document_type}")

    st.text_area(
        "Extracted Text",
        extracted_text,
        height=250
    )

    # ==========================
    # FACE DETECTION
    # ==========================

    st.subheader("👤 Face Detection")

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    face_img = img.copy()

    for (x, y, w, h) in faces:
        cv2.rectangle(
            face_img,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

    st.image(
        face_img,
        caption=f"Faces Detected: {len(faces)}",
        use_container_width=True
    )

    # ==========================
    # STATUS
    # ==========================

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Faces Detected",
            len(faces)
        )

    with col2:
        st.metric(
            "OCR Status",
            "Success" if len(extracted_text.strip()) > 0 else "Failed"
        )

    # ==========================
    # LIVE CAMERA
    # ==========================

    st.subheader("📸 Live Face Verification")

    live_image = st.camera_input(
        "Capture Live Face"
    )

    # ==========================
    # FACE VERIFICATION
    # ==========================

    if live_image is not None and len(faces) > 0:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as f1:

            f1.write(uploaded_file.getvalue())
            doc_path = f1.name

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as f2:

            f2.write(live_image.getvalue())
            live_path = f2.name

        st.info("Comparing Faces...")

        try:

            result = DeepFace.verify(
                img1_path=doc_path,
                img2_path=live_path,
                enforce_detection=True
            )

            distance = result["distance"]

            if result["verified"]:

                verification_result = "VERIFIED"

                st.success(
                    "✅ VERIFIED - Same Person"
                )

                risk = "🟢 LOW RISK"

            else:

                verification_result = "FAKE KYC ALERT"

                st.error(
                    "❌ FAKE KYC ALERT - Different Person"
                )

                risk = "🔴 HIGH RISK"

            match_score = round(
                max(0, (1 - distance)) * 100,
                2
            )

            st.metric(
                "Match Score",
                f"{match_score}%"
            )

            st.subheader("🚨 Risk Assessment")
            st.write(risk)

            # ==========================
            # REPORT
            # ==========================

            report = f"""
AI BASED FAKE KYC ALARM SYSTEM

Document Type: {document_type}

Faces Detected: {len(faces)}

OCR Status: {"Success" if len(extracted_text.strip()) > 0 else "Failed"}

Verification Result: {verification_result}

Face Distance: {round(distance, 4)}

Match Score: {match_score}%

Risk Level: {risk}
"""

            st.subheader("📋 Verification Report")

            st.text_area(
                "Generated Report",
                report,
                height=250
            )

            st.download_button(
                "📥 Download Report",
                report,
                file_name="KYC_Verification_Report.txt",
                mime="text/plain"
            )

        except Exception as e:

            st.error(f"Verification Error: {e}")

        finally:

            if os.path.exists(doc_path):
                os.remove(doc_path)

            if os.path.exists(live_path):
                os.remove(live_path)

else:

    st.info("Please upload an Aadhaar Card to begin verification.")