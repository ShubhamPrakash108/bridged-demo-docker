# ## 🛠️ Run FastAPI Server

# ```bash
# uvicorn app_fastapi:app --host 0.0.0.0 --port 8000 --reload
# ```

# ---

# ## 🌐 Access Swagger UI

# Open this URL in your browser:

# ```
# http://127.0.0.1:8000/docs
# ```

# ---

# ## 📋 How to Use Swagger UI

# 1. Scroll to find `POST /query`.
# 2. Click **"Try it out"**.
# 3. Enter the JSON body:

# ```json
# {
#   "query": "Show me all articles by Jane Doe",
#   "top_k": 3
# }
# ```

# 4. Click **"Execute"**.
# 5. View the **"Response body"** section for results.

# ---

# ## 🧪 Terminal Command to Call API

# Use this `curl` command in your terminal:

# ### PowerShell or Linux/macOS/WSL:

# ```bash
# curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d "{\"query\": \"Show me all articles by Jane Doe\", \"top_k\": 3}"
# ```

# You’ll see the response directly in the terminal.

# ---

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

