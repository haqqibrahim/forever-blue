import streamlit as st
import shelve
from phi.assistant import Assistant
from phi.llm.groq import Groq
from phi.tools.arxiv_toolkit import ArxivToolkit
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.exa import ExaTools
from ai.idea import ai

st.subheader("Generate ideas/topic for your Project")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

groq_api_key = st.secrets["GROQ_API_KEY"]
exa_api_key = st.secrets["EXA_API_KEY"]

# st.title("Forever Blue 💙")
# st.markdown("##### :blue_heart: built by [phidata](https://github.com/phidatahq/phidata)")

  
def ai_ai(prompt):
    assistant = Assistant(
    llm=Groq(model="llama3-70b-8192",api_key=groq_api_key),
    description="You World Class researcher assigned a very important task. Given a subject or context or topic, your job is to create two(2) spinoff ideas based on the subject or context or topic.",
    instructions=[
        "Getting information of what research has been done based on the topic/context/subject",
        "Provide existing papers that relate to the topic/context/subjects, maximum of 8",
        "Come up with 2 spinoff ideas to improve upon the past or exisitng research",
        "generate description for the 2 spinoff project in a bullet point format",
        "suggest papers to read based on the 2 spinoff"
    ],
    tools=[DuckDuckGo(), ExaTools(api_key=exa_api_key)]
    # debug_mode=True,
    )
    
    response = assistant.run(prompt, stream=False)
    return response

    

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history_2") as db:
        return db.get("messages", [])
    
# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history_2") as db:
        db["messages"] = messages



# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()
  
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

state = st.session_state["auth"] 

def main() -> None:
    if state == False:
        st.error("Please login or signup")
        
    else:
        # Display chat messages
        for message in st.session_state.messages:
            avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
                
        # Main chat interface
        if prompt := st.chat_input("How can I help?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(prompt)
                
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                message_placeholder = st.empty()
                reason = "Forever Blue Reasoning, give me a minute please....."
                message_placeholder.markdown(reason + "|")
                message_placeholder.markdown(reason)
                full_response = ""
                full_response = ai(prompt)
                
                message_placeholder.markdown(full_response + "|")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Save chat history after each interaction
        save_chat_history(st.session_state.messages)



main()