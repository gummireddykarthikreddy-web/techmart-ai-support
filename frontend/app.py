import streamlit as st
import requests
import uuid

# Set up the page layout and title
st.set_page_config(page_title="TechMart AI Support", page_icon="🤖")
st.title("🤖 TechMart AI Support Agent")
st.write("Welcome! How can I help you today?")

# NEW: Generate a unique session ID for this specific user's visit
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous chat messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Wait for the user to type something
user_query = st.chat_input("Type your message here...")

if user_query:
    # 1. Display the user's message
    with st.chat_message("user"):
        st.markdown(user_query)
    
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 2. Send the message TO the backend
    backend_url = "http://backend:8000/api/v1/chat"
    
    try:
        with st.spinner("Thinking..."):
            # NEW: We now send the session_id along with the query so the DB can track it!
            payload = {
                "session_id": st.session_state.session_id,
                "query": user_query
            }
            response = requests.post(backend_url, json=payload)
            
        if response.status_code == 200:
            data = response.json()
            answer = data.get("ai_response", "Error getting response.")
            department = data.get("handled_by", "Unknown")
            
            formatted_answer = f"**[{department}]**\n\n{answer}"
            
            # 3. Display the AI's response
            with st.chat_message("assistant"):
                st.markdown(formatted_answer)
                
            st.session_state.messages.append({"role": "assistant", "content": formatted_answer})
            
        else:
            st.error(f"Backend Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend. Make sure your FastAPI server is running!")