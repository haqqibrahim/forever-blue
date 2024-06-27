import streamlit as st
import shelve
from ai.related_papers import related_papers

st.subheader("Find Related Papers")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

groq_api_key = st.secrets["GROQ_API_KEY"]
exa_api_key = st.secrets["EXA_API_KEY"]

if "papers_message" not in st.session_state:
    st.session_state["papers_message"] = []


# Load chat history from shelve file
def load_chat_history():
    with shelve.open("related_papers") as db:
        return db.get("messages", [])
    
# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("related_papers") as db:
        db["messages"] = messages



# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state["papers_message"] = load_chat_history()
    
  
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state["papers_message"]  = []
        save_chat_history([])

state = st.session_state["auth"] 

def main() -> None:
    if state == False:
        st.error("Please login or signup")
        
    else:
        # Display chat messages
        for message in st.session_state["papers_message"]:
            avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
                
        # Main chat interface
        if prompt := st.chat_input("How can I help?"):
            st.session_state["papers_message"].append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(prompt)
                
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                message_placeholder = st.empty()
                reason = "Forever Blue Reasoning, give me a minute please....."
                message_placeholder.markdown(reason + "|")
                message_placeholder.markdown(reason)
                full_response = ""
                full_response = related_papers(prompt)
                
                message_placeholder.markdown(full_response + "|")
                message_placeholder.markdown(full_response)
            st.session_state["papers_message"].append({"role": "assistant", "content": full_response})

        # Save chat history after each interaction
        save_chat_history(st.session_state["papers_message"])



main()