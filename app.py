import streamlit as st
import cv2
import numpy as np
from omr_engine import evaluate_sheet

# Page Configuration
st.set_page_config(
    page_title="MCQ - Evaluator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Automatic MCQ Answer Sheet Evaluator")
#st.subheader("Kg/ Pinnawala Central College - Physics Department")
st.markdown("---")

# Session State for Saving Master Key
if 'saved_master_key' not in st.session_state:
    st.session_state.saved_master_key = None

# Default Key for Pinnawala CC Physics Paper 1
DEFAULT_KEY = {
    1: 2, 2: 1, 3: 2, 4: 4, 5: 4, 6: 1, 7: 4, 8: 4, 9: 4, 10: 5,
    11: 2, 12: 4, 13: 2, 14: 1, 15: 4, 16: 2, 17: 1, 18: 4, 19: 3, 20: 5,
    21: 4, 22: 4, 23: 5, 24: 5, 25: 5, 26: 5, 27: 1, 28: 2, 29: 2, 30: 4,
    31: 2, 32: 4, 33: 4, 34: 4, 35: 5, 36: 1, 37: 1, 38: 5, 39: 4, 40: 2,
    41: 4, 42: 4, 43: 5, 44: 3, 45: 3, 46: 5, 47: 1, 48: 4, 49: 2, 50: 2
}

# ==============================================================================
# STEP 1: SELECT & SAVE MARKING SCHEME (QUESTIONS 1 - 50) - MOBILE FRIENDLY
# ==============================================================================
if st.session_state.saved_master_key is None:
    st.info("📌 **පළමු පියවර:** කරුණාකර ප්‍රශ්න 1 - 50 සඳහා නිවැරදි පිළිතුරු (1, 2, 3, 4, හෝ 5) පිළිවෙළට තෝරා Save කරන්න.")
    
    with st.form("mark_scheme_form"):
        st.write("### 📝 Enter / Verify Marking Scheme")
        
        user_key = {}
        
        # Mobile view සඳහා තනි තීරුවට පල්ලෙහාට සැකසීම
        for q in range(1, 51):
            default_val = DEFAULT_KEY.get(q, 1)
            
            selected_ans = st.selectbox(
                f"Question {q:02d}",
                options=[1, 2, 3, 4, 5],
                index=default_val - 1,
                key=f"q_{q}"
            )
            user_key[q] = selected_ans

        st.markdown("---")
        submit_button = st.form_submit_button("💾 Save Marking Scheme", use_container_width=True)
        
        if submit_button:
            st.session_state.saved_master_key = user_key
            st.success("✅ Marking Scheme එක සාර්ථකව Save කරගන්නා ලදී!")
            st.rerun()

# ==============================================================================
# STEP 2: UPLOAD & EVALUATE ANSWER SHEETS (UP TO 50)
# ==============================================================================
else:
    st.success("✅ Marking Scheme Saved! දැන් ශිෂ්‍යයන්ගේ Answer Sheets Upload කළ හැක.")
    
    col_info, col_reset = st.columns([3, 1])
    with col_reset:
        if st.button("🔄 Change Marking Key", use_container_width=True):
            st.session_state.saved_master_key = None
            st.rerun()

    st.markdown("---")
    st.write("### 📄 Upload Student Answer Sheets (උපරිම 50ක් එකවර):")
    
    student_files = st.file_uploader(
        "Select Answer Sheet Images", 
        type=['jpg', 'jpeg', 'png'], 
        accept_multiple_files=True,
        key="sheets_uploader"
    )

    if student_files:
        if len(student_files) > 50:
            st.error("⚠️ කරුණාකර එකවර Upload කළ හැක්කේ Answer Sheets 50ක් දක්වා පමණි!")
        else:
            st.info(f"📁 මුළු Answer Sheets සංඛ්‍යාව: {len(student_files)}")
            st.markdown("---")
            
            # Displaying results
            for idx, sheet_file in enumerate(student_files):
                file_bytes = np.asarray(bytearray(sheet_file.read()), dtype=np.uint8)
                sheet_img = cv2.imdecode(file_bytes, 1)
                
                results = evaluate_sheet(sheet_img, st.session_state.saved_master_key)
                score = results["score"]
                total = results["total"]
                
                st.image(sheet_img, channels="BGR", use_container_width=True)
                st.markdown(f"**📄 Sheet {idx+1}: {sheet_file.name}**")
                st.metric(
                    label="ලබාගත් නිවැරදි පිළිතුරු (Correct Answers)", 
                    value=f"{score} / {total}"
                )
                st.markdown("---")

st.markdown("---")
st.caption("Pinnawala Central College - Physics Department OMR Automation System")
