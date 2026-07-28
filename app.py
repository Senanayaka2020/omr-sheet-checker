import streamlit as st
import cv2
import numpy as np
from PIL import Image
from omr_engine import evaluate_sheet

# Page Config
st.set_page_config(
    page_title="Pinnawala CC - OMR Evaluator",
    page_icon="📊",
    layout="wide"
)

# Header
st.title("📊 Automatic MCQ Answer Sheet Evaluator")
st.subheader("Kg/ Pinnawala Central College - Physics MCQ Paper 1")
st.markdown("---")

# Master Mark Scheme (ප්‍රශ්න 1 සිට 50 දක්වා නිවැරදි පිළිතුරු)
MASTER_KEY = {
    1: 2, 2: 1, 3: 2, 4: 4, 5: 4, 6: 1, 7: 4, 8: 4, 9: 4, 10: 5,
    11: 2, 12: 4, 13: 2, 14: 1, 15: 4, 16: 2, 17: 1, 18: 4, 19: 3, 20: 5,
    21: 4, 22: 4, 23: 5, 24: 5, 25: 5, 26: 5, 27: 1, 28: 2, 29: 2, 30: 4,
    31: 2, 32: 4, 33: 4, 34: 4, 35: 5, 36: 1, 37: 1, 38: 5, 39: 4, 40: 2,
    41: 4, 42: 4, 43: 5, 44: 3, 45: 3, 46: 5, 47: 1, 48: 4, 49: 2, 50: 2
}

# Sidebar for Settings
st.sidebar.header("⚙️ Options")
input_type = st.sidebar.radio("Select Input Method:", ("Upload Image Sheet", "Live Camera Scan"))

image_to_process = None

# Input Method 1: File Upload
if input_type == "Upload Image Sheet":
    uploaded_file = st.file_uploader("Upload Student's Answer Sheet (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image_to_process = cv2.imdecode(file_bytes, 1)

# Input Method 2: Live Camera
elif input_type == "Live Camera Scan":
    camera_file = st.camera_input("Take a photo of the Answer Sheet")
    if camera_file is not None:
        file_bytes = np.asarray(bytearray(camera_file.read()), dtype=np.uint8)
        image_to_process = cv2.imdecode(file_bytes, 1)

# Evaluation & Output Display
if image_to_process is not None:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image_to_process, channels="BGR", caption="Scanned Answer Sheet", use_container_width=True)
        
    with col2:
        st.write("### 🔍 Evaluation Results")
        with st.spinner("Processing Answer Sheet..."):
            # OMR Engine එක මඟින් Answer Sheet එක Evalute කිරීම
            results = evaluate_sheet(image_to_process, MASTER_KEY)
            
            # Score Cards Display කිරීම
            score = results["score"]
            total = results["total"]
            percentage = (score / total) * 100
            
            st.metric(label="Total Marks / 50", value=f"{score} / {total}")
            st.progress(percentage / 100)
            
            if score >= 35:
                st.success(f"Excellent Performance! ({percentage:.1f}%)")
            elif score >= 20:
                st.warning(f"Average Performance. ({percentage:.1f}%)")
            else:
                st.error(f"Needs Improvement. ({percentage:.1f}%)")

st.markdown("---")
st.caption("Developed for Physics Department - Kg/ Pinnawala Central College")
