import os
import sys
from langchain import hub
import streamlit as st
from langchain_core.tools import Tool
from antropic_model import ClaudeModelAntropic
from tools import GetCurrentTime
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.tools.tavily_search import TavilySearchResults



from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

api_key = os.getenv('TAVILY_API_KEY')


from tools import tradehistory,trade_history,symbol_sentiment,journalsentiment,journal_sentiment
from langchain.agents import AgentExecutor, create_xml_agent

model = ClaudeModelAntropic()
llm = model.getModel()

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/xml-agent-convo")
pipeline = '''
    {'$sort': {'open_time': -1}},
    {'$limit': 5}
'''
# Custom Tools Class
tools = [
    GetCurrentTime(),
    #TradeHistoryQueryTool(),
    TavilySearchResults(),
    #YahooFinanceNewsTool(),
    Tool(
        name="trade history",
        func=tradehistory,
        description=f"Useful to get the user Trade history details and Useful to create a mongodb aggregate pipeline for example {pipeline} is should be in list to retrivew data use this Database and document info {trade_history} to create a relevant queries in dictinoary format",
    ),
    Tool(
        name="symbol sentiment",
        func=symbol_sentiment,
        description=f"Useful to get the sentiment for the trading pair / symbol / asset",
    ),
    Tool(
        name="Trade Journal sentiment",
        func=journalsentiment,
        description=f"Useful to get the user journal note sentiment and Useful to create a mongodb aggregate pipeline for example {pipeline} is should be in list to retrivew data use this Database and document info {journal_sentiment} to create a relevant queries in dictinoary format",
    ),
]

# Construct the XML agent
agent = create_xml_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# query = "total profit i made for user_id = {user_id}"
# response = agent_executor.invoke({"input": query})
# output = response.get('output', 'No output found')


# Streamlit app
st.title('Trade Risk Assessment and Recommendations')

user_id = st.number_input('Enter User ID', min_value=1, step=1)
query = st.text_input('Enter your query')
final_q = f"{query} for user_id = {user_id}"

if st.button('Get Recommendations'):
    response = agent_executor.invoke({"input": final_q})
    output = response.get('output', 'No output found')
    st.write(output)