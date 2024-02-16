import streamlit as st

import time

st.title("MultiModal Chatbot")

st.write("This is a chatbot that can answer questions about a reaserch paper and also generate a summary of the paper.")

st.markdown("""
    <style>
    .footer {
        position: fixed;
        right: 0;
        bottom: 0;
        width: auto;
        background-color: transparent;
        color: white;
        text-align: right;
        padding-right: 20px;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


st.sidebar.title("Input Data")
uploaded_file = st.sidebar.file_uploader("Add PDF of research paper ", type=['pdf', 'txt'])

if uploaded_file is not None:
    st.sidebar.write("File Uploaded Successfully")

url = st.sidebar.text_input("Add URL of research paper")
doi = st.sidebar.text_input("Add DOI of research paper")

submit_button = st.sidebar.button("Submit")

if submit_button:
    st.sidebar.write("Data Submitted Successfully")
    if uploaded_file or url or doi:
        with st.spinner("Please wait, we are processing your data"):
            time.sleep(5)
        st.success("Data Submitted Successfully")
    else:
        st.sidebar.error("Please provide the required data")


