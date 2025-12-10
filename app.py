# app.py

import streamlit as st

# -------------------------------
# SCAM KEYWORDS
# -------------------------------
scam_keywords = [
    'earn money fast', 'make money', 'bank account', 
    'guaranteed income', 'no experience needed', 'work from home', 'limited spots'
]

# -------------------------------
# DETECT MONEY
# -------------------------------
def detect_money(text):
    money_indicators = ['$', 'usd', 'eur', 'inr', 'rs', '₹']
    words = text.split()
    money_words = []
    for word in words:
        for indicator in money_indicators:
            if indicator.lower() in word.lower() and any(char.isdigit() for char in word):
                money_words.append(word)
                break
    return money_words

# -------------------------------
# CHECK FAKE JOB
# -------------------------------
def check_fake_job(text):
    keywords_found = [kw for kw in scam_keywords if kw.lower() in text.lower()]
    money_words = detect_money(text)
    all_matches = keywords_found + money_words

    # Highlight keywords and money in different colors
    highlighted_text = text
    for kw in keywords_found:
        highlighted_text = highlighted_text.replace(kw, f":red[{kw}]")
    for mw in money_words:
        highlighted_text = highlighted_text.replace(mw, f":blue[{mw}]")

    is_fake = len(all_matches) > 0
    return is_fake, highlighted_text, all_matches

# -------------------------------
# STREAMLIT UI/UX DESIGN
# -------------------------------
st.set_page_config(
    page_title="Fake Job Detector",
    page_icon="🕵‍♂",
    layout="wide"
)

# Header
st.markdown("<h1 style='text-align: center; color: #1F4E79;'>🕵‍♂ Fake Job Detector</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Analyze job postings and detect potential frauds instantly</p>", unsafe_allow_html=True)
st.markdown("---")

# Input area
st.subheader("Paste Job Description")
job_description = st.text_area("", height=250, placeholder="Paste the full job posting text here...")

# Analyze button
if st.button("Analyze Job Posting", use_container_width=True):
    if job_description.strip() == "":
        st.warning("⚠ Please paste a job description to analyze.")
    else:
        is_fake, highlighted_text, all_matches = check_fake_job(job_description)

        # Result card
        if is_fake:
            st.markdown(
                f"""
                <div style='border:2px solid #FF4B4B; padding:15px; border-radius:10px; background-color:#FFF5F5'>
                <h3 style='color:#FF4B4B;'>⚠ This job posting may be fraudulent!</h3>
                <p>{highlighted_text}</p>
                <p><strong>Detected keywords/money:</strong> {', '.join(all_matches)}</p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='border:2px solid #4CAF50; padding:15px; border-radius:10px; background-color:#F5FFF5'>
                <h3 style='color:#4CAF50;'>✅ This job posting appears legitimate.</h3>
                <p>{highlighted_text}</p>
                </div>
                """, unsafe_allow_html=True
            )