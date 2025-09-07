import streamlit as st
from pdf_parser import parse_pdf_text
from ai_analyzer import get_ai_feedback

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="🤖",
    layout="centered",
)

# --- Main App Interface ---
st.title("🚀 AI-Powered Resume Reviewer")
st.write("Get instant, expert feedback on your resume to land your dream job. Just fill in the details below.")
st.markdown("---")

# --- INPUT FIELDS ---
st.header("1. The Job You Want")
job_title = st.text_input("🎯 Enter the Job Title you're applying for", placeholder="e.g., Senior Python Developer")
job_description = st.text_area("📄 Paste the Job Description here", height=200, placeholder="Paste the full job description for the best results.")

st.header("2. Your Resume")
resume_source = st.radio("How would you like to provide your resume?", ('Upload PDF', 'Paste Text'), horizontal=True)

resume_text = ""
if resume_source == 'Upload PDF':
    uploaded_file = st.file_uploader("📂 Upload your resume in PDF format", type=['pdf'], label_visibility="collapsed")
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        resume_text = parse_pdf_text(file_bytes)
        if resume_text is None:
            st.error("❌ Error reading the PDF file. Please ensure it's a valid, text-based PDF and not an image scan.")
        else:
            st.success("✅ PDF successfully parsed!")

elif resume_source == 'Paste Text':
    resume_text = st.text_area("✍️ Paste your full resume text below", height=300, label_visibility="collapsed")

st.markdown("---")

# --- ANALYSIS TRIGGER ---
if st.button("✨ Analyze My Resume!", use_container_width=True, type="primary"):
    if not job_title or not job_description or not resume_text:
        st.warning("Please fill in all the fields: Job Title, Job Description, and your Resume.")
    else:
        with st.spinner('🤖 Our AI is reading your resume... This may take a moment...'):
            try:
                # We now directly get the dictionary from the AI analyzer. No more json.loads().
                feedback_data = get_ai_feedback(resume_text, job_title, job_description)
                
                if feedback_data:
                    st.header("📝 Feedback Report")
                    st.success("Analysis complete! Here's your personalized feedback:")

                    # Safely get overall score
                    overall_score = feedback_data.get('overall_score', 0)
                    st.subheader(f"⭐ Overall Score: {overall_score}/100")
                    st.progress(overall_score)

                    # Safely get strengths
                    strengths = feedback_data.get('strengths', [])
                    st.subheader("👍 Strengths")
                    if strengths:
                        for strength in strengths: st.markdown(f"- {strength}")
                    else:
                        st.markdown("No specific strengths were highlighted.")

                    # Safely get areas for improvement
                    improvements = feedback_data.get('areas_for_improvement', [])
                    st.subheader("🛠️ Areas for Improvement")
                    if improvements:
                        for improvement in improvements: st.markdown(f"- {improvement}")
                    else:
                        st.markdown("No specific areas for improvement were highlighted.")

                    # Safely get keyword analysis
                    keyword_analysis = feedback_data.get('keyword_analysis', {})
                    found_keywords = keyword_analysis.get('found', [])
                    missing_keywords = keyword_analysis.get('missing', [])
                    st.subheader("🔑 Keyword Match Analysis")
                    st.markdown(f"**Keywords Found:** {', '.join(found_keywords) if found_keywords else 'None'}")
                    st.markdown(f"**Keywords Missing:** {', '.join(missing_keywords) if missing_keywords else 'None'}")
                    st.info("Tip: Weave missing keywords naturally into your experience bullet points.")

                    # Safely get suggested rewrite
                    rewrite = feedback_data.get('suggested_rewrite', {})
                    original_snippet = rewrite.get('original', "N/A")
                    improved_snippet = rewrite.get('improved', "N/A")
                    st.subheader("✍️ Suggested Rewrite Example")
                    st.markdown("**Original Snippet:**")
                    st.code(original_snippet, language='text')
                    st.markdown("**Improved Snippet:**")
                    st.code(improved_snippet, language='text')
                else:
                    st.error("Sorry, the AI returned a response in an unexpected format or an error occurred. This can happen during high traffic. Please try again.")

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                st.error("Please double-check that your API key in secrets.toml is correct.")

# --- FOOTER ---
st.markdown("---")

