# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token
import os
from dotenv import load_dotenv
import requests
import streamlit as st

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.environ.get('LANGFLOW_ID')
FLOW_ID = os.environ.get('FLOW_ID')
APPLICATION_TOKEN = os.environ.get('APP_TOKEN')
ENDPOINT = "AM" # The endpoint name of the flow

def run_flow(message: str) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = None
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("NYSERDA Building Incentives Q&A Answer-Bot")
    st.markdown("""I am an AI bot trained on the information from the NYSERDA website in the Buildings section.
                In your question, include context about your building and your situation. I will do my best to make
                an automated summary from the NYSERDA website documents that I have.""")

    message = st.text_area("Message", placeholder="Ask something...")

    if st.button("Ask question"):
        if not message.strip():
            st.error("please enter a message")
            return
        
        try:
            with st.spinner("Asking...."):
                response = run_flow(message)
            response = response['outputs'][0]['outputs'][0]['results']['message']['text']
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

    
if __name__ == "__main__":
    main()