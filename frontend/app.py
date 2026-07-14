import streamlit as st
import requests

# Set up the page layout and title
st.set_page_config(page_title="TechMart AI Support", page_icon="🤖")
st.title("🤖 TechMart AI Support Agent")
st.write("Welcome! How can I help you today?")

# Initialize chat history in session state so it remembers the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous chat messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Wait for the user to type something in the chat box at the bottom
user_query = st.chat_input("Type your message here...")

if user_query:
    # 1. Display the user's message in the chat interface
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 2. Send the message to your FastAPI backend
    backend_url = "http://localhost:8000/api/v1/chat"
    
    try:
        # Show a spinning loader while waiting for the backend
        with st.spinner("Thinking..."):
            response = requests.post(backend_url, json={"query": user_query})
            
        if response.status_code == 200:
            data = response.json()
            answer = data.get("ai_response", "Error getting response.")
            department = data.get("handled_by", "Unknown")
            
            # Format the answer with a little badge showing which Agent handled it
            formatted_answer = f"**[{department}]**\n\n{answer}"
            
            # 3. Display the AI's response
            with st.chat_message("assistant"):
                st.markdown(formatted_answer)
                
            # Add AI message to history
            st.session_state.messages.append({"role": "assistant", "content": formatted_answer})
            
        else:
            st.error(f"Backend Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend. Make sure your FastAPI server is running!")