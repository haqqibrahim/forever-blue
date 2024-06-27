import os
from phi.assistant import Assistant
from phi.llm.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.exa import ExaTools
import streamlit as st


groq_api_key = st.secrets["GROQ_API_KEY"]
exa_api_key = st.secrets["EXA_API_KEY"]

  
def related_papers(prompt):
    assistant = Assistant(
    llm=Groq(model="llama3-70b-8192",api_key=groq_api_key, max_tokens=6000),
    description="You are a World Class researcher assigned a very important task. Given a subject or context or topic, your job is find related papers",
    instructions=[
       "Find related papers to the given topic/context/subject",
       "Provide a detailed summary of the papers found",
       "generate at least 3 key insights per paper",
       "Provided the papers should have: title, writer, date publised, publisher"
    ],
    tools=[DuckDuckGo(), ExaTools(api_key=exa_api_key)]
    # debug_mode=True,
    )
    
    response = assistant.run(prompt, stream=False)
    return response
