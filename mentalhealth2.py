from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and start chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get response from Gemini model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Function to detect and respond to greetings
def respond_to_greeting(input_text):
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
    for greeting in greetings:
        if greeting in input_text.lower():
            return f"{greeting.capitalize()}! How can I assist you today?"
        
def respond_to_identity(input_text):
    identity = ['who are you', 'what is your work', 'how are you going',"what is your purpose",]
    for identity in identity:
        if identity in input_text.lower():
            return f"I am a mental health chatbot! and I am going to help you enhance your mental health"


# Initialize Streamlit app
st.set_page_config(page_title="Chatbotdemo")
st.header("Mental Health Chatbot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# List of keywords related to mental health
mental_health_keywords = ['mental health', 'anxiety', 'depression', 'therapy', 'stress',"feeling","well",
                          "What does it mean to have a mental illness?", "What is mental health illness",
                          "Describe mental health illness","Who does mental illness affect?",
                          "Who is affected by mentall illness","What causes mental illness?",
                          "What leads to mental illness?","how does one get mentally ill?",
                          "Can people with mental illness recover?","Is it possible to recover from mental illness",
                          "I know someone who appears to have such symptoms?","What are the steps to be followed incase of symptoms",
                          "How to find mental health professional for myself","How to find mental health professional?",
                          "What treatment options are available?","How can one recover?",
                          "How to become involved in treatment?","What should I keep in mind if I begin treatment?",
                          "What is the difference between mental health professionals?","What are the different types of mental health professionals present?",
                          "How can I find a mental health professional right myself?","How to find the right mental health professional?",]

# Input field for user question
input_text = st.text_input("Input:", key="input")
submit_button = st.button("Ask question")

# Process user input and fetch response
if submit_button and input_text:
    # Check if the input is a greeting
    greeting_response = respond_to_greeting(input_text)
    identity_response = respond_to_identity(input_text)
    if greeting_response:
        st.subheader("Response is:")
        st.write(greeting_response)
        st.session_state['chat_history'].append(("𝘽𝙊𝙏:", greeting_response))
    elif identity_response:
        st.subheader("Response is:")
        st.write(identity_response)
        st.session_state['chat_history'].append(("𝘽𝙊𝙏:", identity_response))
    else:
        # If not a greeting, proceed with fetching mental health-related response
        response = get_gemini_response(input_text)

        # Filter responses related to mental health
        mental_health_responses = [chunk.text for chunk in response if any(keyword in chunk.text.lower() for keyword in mental_health_keywords)]


        # Add user query and response to session chat history
        st.session_state['chat_history'].append(("𝙔𝙊𝙐:", input_text))

        
        # Display filtered response
        if mental_health_responses:
            st.subheader("Response is :")
            for text in mental_health_responses:
                st.write(text)
                st.session_state['chat_history'].append(("𝘽𝙊𝙏:", text))
                
        else:
            st.subheader("Response is")
            st.write("Sorry, I couldn't understand or provide a relevant response.")

    
    

# Display chat history
st.subheader("Chat history")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
