# AI Based Fake KYC Detection System

## About the Project

This project is developed to detect fake KYC verification attempts using artificial intelligence and image processing techniques. The system takes a KYC document as input, extracts the text using OCR, detects the face present in the document, and compares it with a live face captured through the webcam.

The project uses OpenCV for face detection, Pytesseract for OCR and DeepFace for face verification. Based on the verification result, the system displays the verification status and risk level.

## Technologies Used

- Python
- Streamlit
- OpenCV
- Pytesseract
- DeepFace
- TensorFlow

## Main Features

- KYC document upload
- OCR text extraction
- Face detection
- Live face capture
- Face verification
- Risk assessment
- Verification report generation

## Project Files

- `app.py` - Main application
- `face_compare.py` - Face comparison
- `test_deepface.py` - Tests DeepFace installation
- `test_ocr.py` - Tests Tesseract OCR
- `requirements.txt` - Required libraries

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt

Run the application:
streamlit run app.py

The application will open in the browser.
