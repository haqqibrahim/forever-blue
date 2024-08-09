import os
from phi.assistant import Assistant
from phi.llm.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.exa import ExaTools
import streamlit as st


groq_api_key = st.secrets["GROQ_API_KEY"]
exa_api_key = st.secrets["EXA_API_KEY"]

  
def ai(prompt):
    assistant = Assistant(
    llm=Groq(model="llama3-70b-8192",api_key=groq_api_key, max_tokens=6000),
    description="You are a World Class researcher assigned a very important task. Given a subject or context or topic, your job is to create two(2) spinoff ideas based on the subject or context or topic.",
    instructions=[
        "Getting information of what research has been done based on the topic/context/subject",
        "Provide existing papers that relate to the topic/context/subjects, maximum of 8",
        "Come up with 2 spinoff ideas to improve upon the past or exisitng research",
        "generate description for the 2 spinoff project in a bullet point format",
       
    ],
    tools=[ExaTools(api_key=exa_api_key)]
    # debug_mode=True,
    )
    
    response = assistant.run(prompt, stream=False)
    return response
