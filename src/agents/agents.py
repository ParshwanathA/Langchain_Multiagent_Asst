import os, sys
sys.path.append(os.path.abspath('.'))
import src
import time
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import scrape_url
from src.tools.tools import web_search
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_classic.memory import ConversationBufferWindowMemory
import asyncio

load_dotenv()

# Model Initialization

# --- Verbose Groq wrapper with heartbeat messages ---
class VerboseGroq(ChatGroq):
    def _sleep_for_retry(self, retries_taken, timeout, response=None):
        # Show retry heartbeat in Streamlit
        st.warning(f"[Retry {retries_taken}] Rate limit hit. Sleeping {timeout:.1f}s before retry...")
        time.sleep(timeout)

# --- Safe LLM factory ---
def make_llm(model="qwen/qwen3.8-27b", max_tokens=800):
    return VerboseGroq(
        model=model,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        max_tokens=max_tokens,
        request_timeout=30,
        temperature=0.3
    )

llm = make_llm()

# --- Input guard: truncate oversized text ---
def safe_text(text, max_chars=5000):
    if len(text) > max_chars:
        st.warning(f"Input too large ({len(text)} chars). Truncating to {max_chars}.")
        return text[:max_chars]
    return text


# 1st Agent : Search agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
    )

# 2nd Agent : Reader agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
    )

# Write Chain

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be concise, factual and professional, Keep responses under 500 tokens."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()




#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()