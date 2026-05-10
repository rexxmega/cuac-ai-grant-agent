import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from org_data import CUAC_INFO

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("CUAC AI Grant Writing Agent")

st.write("Generate professional grant application drafts using AI.")

# Sidebar
st.sidebar.header("CUAC Information")
st.sidebar.write(f"**Organization:** {CUAC_INFO['registered_name']}")
st.sidebar.write(f"**RJSC #:** {CUAC_INFO['rjsc_number']}")
st.sidebar.write(f"**Website:** {CUAC_INFO['website']}")

# Input
user_input = st.text_area(
    "Paste grant questions or event details:",
    height=300
)

def build_prompt(user_input):
    return f"""
You are an AI Grant Writing Assistant for Celebrate Unity and Community Society.

Organization Information:
Name: {CUAC_INFO['registered_name']}
RJSC Number: {CUAC_INFO['rjsc_number']}
Address: {CUAC_INFO['address']}
Mission: {CUAC_INFO['mission']}
Goals: {', '.join(CUAC_INFO['goals'])}

User Input:
{user_input}

Instructions:
- Write professionally
- Match real grant application style
- Make responses natural and editable
- Include budget tables if needed
- Use headings
"""

if st.button("Generate Grant Draft"):

    try:
        prompt = build_prompt(user_input)

        with st.spinner("Generating..."):
            response = model.generate_content(prompt)

        st.subheader("Generated Grant Draft")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"Error: {e}")