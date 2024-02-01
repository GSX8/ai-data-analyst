import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
from pandasai.responses.streamlit_response import StreamlitResponse

load_dotenv()
apiKey = os.getenv("OPENAI_API_KEY")

def response(df, prompt):
    llm = OpenAI(api_token=apiKey)
    sdf = SmartDataframe(df, config={"llm": llm, "verbose": True, "response_parser": StreamlitResponse})
    result=sdf.chat(prompt)
    return result

def main(): 

    st.set_page_config(
        page_title="AI Data Analyst",
        page_icon="./assets/images/chatbot-icon.svg",
        layout='wide',
    )
    container =st.container()


    col1,col2 = st.columns([0.06,0.9])
    with container:
        with col1:
            st.image("./assets/images/chatbot.png",use_column_width='auto')
        with col2:
            st.title("Hey, I am DOTO!")
    st.text("Powered by Pandas AI & OpenAI API to provide you Data Analytics and Visulaization.")
    st.header("🧑🏽‍💻 Your personal AI-powered Data Analyst 📊📈",divider=True)
    input_csv = st.file_uploader("Upload your CSV DataSet Below :",type=['csv'])

    if input_csv :
        st.info("CSV Uploaded Successfully")
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