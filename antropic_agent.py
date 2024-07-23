import os
import sys
from langchain import hub
import streamlit as st
from langchain_core.tools import Tool
from antropic_model import ClaudeModelAntropic
from tools import GetCurrentTime
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from tools import tradehistory,trade_history
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
    YahooFinanceNewsTool(),
    Tool(
        name="trade history",
        func=tradehistory,
        description=f"Useful to create a mongodb aggregate pipeline for example {pipeline} is should be in list to retrivew data use this Database and document info {trade_history} to create a relevant queries in dictinoary format",
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