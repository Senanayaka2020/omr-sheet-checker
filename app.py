# ==============================================================================
# STEP 1: SELECT & SAVE MARKING SCHEME (QUESTIONS 1 - 50)
# ==============================================================================
if st.session_state.saved_master_key is None:
    st.info("📌 **පළමු පියවර:** කරුණාකර ප්‍රශ්න 1 - 50 සඳහා නිවැරදි පිළිතුරු (1, 2, 3, 4, හෝ 5) පිළිවෙළට තෝරා Save කරන්න.")
    
    with st.form("mark_scheme_form"):
        st.write("### 📝 Enter / Verify Marking Scheme")
        
        user_key = {}
        
        # තනි Column එකක් ලෙස පල්ලෙහාට Q1 සිට Q50 දක්වා සකසයි
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
