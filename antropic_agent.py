import os
import sys
from langchain import hub
from antropic_model import ClaudeModelAntropic
from tools import GetCurrentTime,TradeJournalQueryTool
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

from langchain.agents import AgentExecutor, create_xml_agent

model = ClaudeModelAntropic()
llm = model.getModel()

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/xml-agent-convo")

# Custom Tools Class
tools = [
    GetCurrentTime(),
    TradeJournalQueryTool(),
    YahooFinanceNewsTool()
]

# Construct the XML agent
agent = create_xml_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input": "total profit i made for user_id = 103"})

output = response.get('output', 'No output found')
print(output)
