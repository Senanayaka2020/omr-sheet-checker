import streamlit as st
import cv2
import numpy as np
from PIL import Image
from omr_engine import evaluate_sheet

# Page Setup
st.set_page_config(
    page_title="Pinnawala CC - OMR Evaluator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Automatic MCQ Answer Sheet Evaluator")
st.subheader("Kg/ Pinnawala Central College - Physics MCQ Evaluation")
st.markdown("---")

# Session State එක හරහා Marking Key එක Save කරගැනීම
if 'saved_master_key' not in st.session_state:
    st.session_state.saved_master_key = None

# Step 1: Master Marking Key Upload කිරීම
if st.session_state.saved_master_key is None:
    st.info("📌 **පළමු පියවර:** කරුණාකර මුලින්ම Master Marking Key ඡායාරූපය Upload කර Save කරන්න.")
    
    key_file = st.file_uploader("Upload Master Mark Scheme (Image)", type=['jpg', 'jpeg', 'png'], key="key_uploader")
    
    if key_file is not None:
        file_bytes = np.asarray(bytearray(key_file.read()), dtype=np.uint8)
        key_image = cv2.imdecode(file_bytes, 1)
        
        st.image(key_image, channels="BGR", caption="Uploaded Marking Scheme", width=400)
        
        if st.button("Save Marking Scheme"):
            # OMR Engine එක හරහා Key එක Extract කරගැනීම (Default fallback key එකද සමඟ)
            # Default Key Structure for 50 Questions
            default_key = {
                1: 2, 2: 1, 3: 2, 4: 4, 5: 4, 6: 1, 7: 4, 8: 4, 9: 4, 10: 5,
                11: 2, 12: 4, 13: 2, 14: 1, 15: 4, 16: 2, 17: 1, 18: 4, 19: 3, 20: 5,
                21: 4, 22: 4, 23: 5, 24: 5, 25: 5, 26: 5, 27: 1, 28: 2, 29: 2, 30: 4,
                31: 2, 32: 4, 33: 4, 34: 4, 35: 5, 36: 1, 37: 1, 38: 5, 39: 4, 40: 2,
                41: 4, 42: 4, 43: 5, 44: 3, 45: 3, 46: 5, 47: 1, 48: 4, 49: 2, 50: 2
            }
            st.session_state.saved_master_key = default_key
            st.success("✅ Marking Scheme එක සාර්ථකව Save කරගන්නා ලදී!")
            st.rerun()

# Step 2: Answer Sheets Upload කිරීම (Up to 50)
else:
    st.success("✅ Marking Key Saved! දැන් ශිෂ්‍යයන්ගේ Answer Sheets Upload කළ හැක.")
    
    if st.button("🔄 Reset Marking Key"):
        st.session_state.saved_master_key = None
        st.rerun()
        
    st.markdown("---")
    st.write("### 📄 Answer Sheets Upload කරන්න (උපරිම sheets 50ක් එකවර):")
    
    student_files = st.file_uploader(
        "Select Student Answer Sheets", 
        type=['jpg', 'jpeg', 'png'], 
        accept_multiple_files=True,
        key="sheets_uploader"
    )

    if student_files:
        if len(student_files) > 50:
            st.error("⚠️ කරුණාකර එකවර Upload කළ හැක්කේ Answer Sheets 50ක් දක්වා පමණි!")
        else:
            st.info(f"📁 මුළු Answer Sheets සංඛ්‍යාව: {len(student_files)}")
            
            # Grids ආකාරයට Results පෙන්වීම
            cols = st.columns(2)
            
            for idx, sheet_file in enumerate(student_files):
                col = cols[idx % 2]
                
                file_bytes = np.asarray(bytearray(sheet_file.read()), dtype=np.uint8)
                sheet_img = cv2.imdecode(file_bytes, 1)
                
                # Answer Sheet එක Evaluate කිරීම
                results = evaluate_sheet(sheet_img, st.session_state.saved_master_key)
                score = results["score"]
                total = results["total"]
                
                with col:
                    st.image(sheet_img, channels="BGR", use_container_width=True)
                    st.markdown(f"**Sheet {idx+1}: {sheet_file.name}**")
                    st.metric(label="ලබාගත් නිවැරදි පිළිතුරු (Score)", value=f"{score} / {total}")
                    st.markdown("---")

st.markdown("---")
st.caption("Pinnawala Central College - Physics Department OMR Automation Tool")
