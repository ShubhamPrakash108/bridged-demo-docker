from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json
from utils import (query_database_custom, data_creation, embeddings_creation, convert_to_pinecone_format, data_to_vector_db,
                   natural_language_to_pinecone_format, natural_language_to_sematic_meaning )


data_creation("./data/sample_data - itg_sports.csv.csv")
embeddings_creation()
convert_to_pinecone_format()

with open("./config.json", "r") as f:
    config = json.load(f)

api_key = config["api_key"]
index_name = config["index_name"]
metric = config["metric"]

data_to_vector_db(api_key, index_name, metric, dimension=384, cloud="aws", region="us-east-1")



app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    api_key: str
    top_k: Optional[int] = 5
    index_name: str

@app.post("/query")
def query_vector_db(request: QueryRequest):
    response = query_database_custom(request.query, request.api_key, request.top_k , request.index_name)
    return {
        "query": request.query,
        "results": [match.metadata for match in response.matches]
    }

