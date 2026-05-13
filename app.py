import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from org_data import CUAC_INFO

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config={
        "temperature": 0.4,
        "max_output_tokens": 900,
    }
)

st.title("CUAC AI Grant Writing Agent")
st.write("Generate fast, professional grant application sections using CUAC information.")

st.sidebar.header("CUAC Information")
st.sidebar.write(f"**Organization:** {CUAC_INFO['registered_name']}")
st.sidebar.write(f"**RJSC #:** {CUAC_INFO['rjsc_number']}")
st.sidebar.write(f"**Website:** {CUAC_INFO['website']}")

section = st.selectbox(
    "Choose what to generate:",
    [
        "Event Description",
        "Target Audience",
        "Promotion Plan",
        "Success Measurement",
        "Visitor Impact",
        "Budget Table",
        "Concise Full Draft"
    ]
)

user_input = st.text_area(
    "Paste grant questions or event details:",
    height=260
)

def build_prompt(section, user_input):
    return f"""
You are a grant writing assistant for Celebrate Unity and Community Society.

CUAC Information:
Name: {CUAC_INFO['registered_name']}
RJSC Number: {CUAC_INFO['rjsc_number']}
Address: {CUAC_INFO['address']}
Website: {CUAC_INFO['website']}
Mission: {CUAC_INFO['mission']}
Goals: {', '.join(CUAC_INFO['goals'])}

Task:
Generate only this section: {section}

Event / Grant Details:
{user_input}

Rules:
- Be concise and professional.
- Use real grant application style.
- Use professional grant-writing structure and formatting.
- If section is "Concise Full Draft", generate a detailed but concise grant draft between 700–1200 words.
- Otherwise keep answers under 350 words.
- If generating a budget, use a simple table.
- If information is missing, write [NEEDS CONFIRMATION].
"""

if st.button("Generate"):
    if not api_key:
        st.error("Missing GEMINI_API_KEY. Add it in Streamlit Secrets.")
    elif not user_input.strip():
        st.warning("Please paste event or grant details first.")
    else:
        try:
            with st.spinner("Generating fast draft..."):
                response = model.generate_content(build_prompt(section, user_input))

            st.subheader(section)
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
