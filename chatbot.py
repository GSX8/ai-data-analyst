import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
from pandasai.responses.streamlit_response import StreamlitResponse
import time

# load_dotenv()
# apiKey = os.getenv("OPENAI_API_KEY")



def response(df, prompt):
    llm = OpenAI(api_token=st.session_state.api_key)
    sdf = SmartDataframe(df, config={"llm": llm, "verbose": True, "response_parser": StreamlitResponse})
    result=sdf.chat(prompt)
    return result

def main(): 

    st.set_page_config(
        page_title="Doto the Analyst",
        page_icon="./assets/images/chatbot-icon.svg",
        layout='wide',
        initial_sidebar_state='expanded',
    )
    container =st.container()
    api_key = ""
    st.session_state.api_key_valid = False

    with st.sidebar:
        col1,col2 = st.columns([0.3,0.7])
        with container:
            with col1:
                st.image("./assets/images/chatbot.png",use_column_width='auto')
            with col2:
                st.title("Hey, I am DOTO!")
                st.text("AI Powered Data Analyst")
        

        api_token = st.text_input("Enter your OpenAI API token to get started.", value=st.session_state.api_key, type="password", placeholder="API Token")
        
        info = st.markdown("")
        if not api_token:
            info.error("Please Paste API Token")
            time.sleep(4)
            info.empty()
        else :
            info.success("API token loaded successfully!")
            time.sleep(5)
            info.empty()
            st.session_state.api_key_valid = True
        if st.session_state.api_key_valid :
            st.caption("You can now get started by uploading the CSV file :")
        
        input_csv = st.file_uploader("Upload your CSV DataSet Below :",type=['csv'],label_visibility='collapsed')



    st.header("🧑🏽‍💻 Your personal OpenAI-powered Data Analyst 📊📈",divider=True)
    st.text("Powered by Pandas AI & OpenAI API to provide you Analytics and Visulaization for your Data.")
    # input_csv = st.file_uploader("Upload your CSV DataSet Below :",type=['csv'],label_visibility='collapsed')

    if input_csv :
        st.info("CSV file Uploaded Successfully..!",icon='💹')
        data = pd.read_csv(input_csv)
        st.dataframe(data, use_container_width=True)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        prompt = st.chat_input("Ask me anything about the csv")
        
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            st.session_state.messages.append({"role":"user","content":prompt})
            
            result = response(data, prompt)
            with st.chat_message("assistant"):
                st.write(result)
            st.session_state.messages.append({"role":"assistant","content":result})

if __name__ == '__main__':
    main()