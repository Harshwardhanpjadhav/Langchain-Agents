# Import things that are needed generically
import json
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from typing import Optional, Type
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
mongo_uri = os.getenv('MONGODB_URI')

trade_history ={
  "user_id": "id of the user which is unique for all and the type is integer",
  "symbol": "symbol of the trade also called as asset and trading pair",
  "open_time":"date and time of the trade",
  "volume": "volume of the trade",
  "side": "buy or sell",
  "close_time":"close time of the trade",
  "open_price": "price when the trade was entered",
  "close_price": "price when the trade was closed",
  "stop_loss": "number that represent the stop loss",
  "take_profit":"number that represent the take profit",
  "net_virtual_profit": "total profit or loss of the trade",
  "date": "date on which user made the trade",
  "open_day_of_week": "Friday",
  "close_day_of_week": "Friday",
  "hour": "time on which user made the trade",
  "open_hour": "hour when the trade was entered",
  "close_hour": "hour when the trade was closed",
  "rr_ratio": "risk to reward ratio",
  "day": "day on which user made the trade",
}


class GetCurrentTimes(BaseModel):
    query: str = Field(description="should be a user's query")
class GetCurrentTime(BaseTool):
    name = "get_time"
    description = "Useful for when you need to know the current time."
    args_schema: Type[BaseModel] = GetCurrentTimes
    
    def _run(self, query: str) -> str:
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")
    


# class TradeHistoryQueryArgs(BaseModel):
#     query: str = Field(description="The mongodb query in dictinory format")
# class TradeHistoryQueryTool(BaseTool):
#     name = "Trade History Query Tool"
#     description = f"Useful to create a mongodb query to retrivew data use this Database and document info {trade_history} to create a relevant queries in dictinoary format"
#     args_schema: Type[BaseModel] = TradeHistoryQueryArgs
    
#     def _run(self, query: str) -> str:
#         f"useful to get data from the MongoDB  based on the users question"
#         from pymongo import MongoClient
#         client = MongoClient(mongo_uri)
#         db = client["processed_user_data"]
#         collection = db["trade_history_PnL_single_trade"]

#         print(f"Received query: {query}")

#         try:
#             mongo_query = json.loads(query)
#         except json.JSONDecodeError:
#             return "Invalid query format. Please provide a valid JSON query."
        
#         print(f"MongoDB query: {mongo_query}")
        
#         results = collection.find(mongo_query)
#         result_list = [str(result) for result in results]
    
#         # Return results as a formatted string
#         return "\n".join(result_list)

def tradehistory(query):
    from pymongo import MongoClient
    client = MongoClient(mongo_uri)
    db = client["processed_user_data"]
    collection = db["trade_history_PnL_single_trade"]
    print(f"Received query: {query}")

    try:
        mongo_query = json.loads(query)
    except json.JSONDecodeError:
        return "Invalid query format. Please provide a valid JSON query."

    print(f"MongoDB query: {mongo_query}")

    results = collection.aggregate(mongo_query)
    result_list = [str(result) for result in results]
    return "\n".join(result_list)
