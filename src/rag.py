import json
from langchain.schema import Document
import os
import sys

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


# Initialize the LLaMA model
llm = Ollama(model="llama3.2", callbacks=[StreamingStdOutCallbackHandler()])

# Load embedding model
embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cuda"}
embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model_name, model_kwargs=model_kwargs
)


# Documents ------------------------------------------------------------
def load_json_as_documents(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    docs = []
    for entry in data:
        content = f"""Function: {entry["function"]}
Description: {entry["description"]}
Parameters: {json.dumps(entry.get("parameters", {}), indent=2)}
Returns: {entry.get("returns", "None")}"""
        docs.append(Document(page_content=content))

    return docs


# Vector storage FAISS -------------------------------------------------
faiss_index_path = "faiss_index_"

# Check if the FAISS index exists
if os.path.exists(faiss_index_path):
    print("Loading existing FAISS index...")
    persisted_vectorstore = FAISS.load_local(
        faiss_index_path, embeddings, allow_dangerous_deserialization=True
    )
else:
    print("Creating new FAISS index...")
    documents = load_json_as_documents("cfdocs.json")
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(faiss_index_path)
    persisted_vectorstore = vectorstore

# -----------------------------------------------------------------------

# Retrieval -------------------------------------------------------------
# Create a retriever with increased search parameters
retriever = persisted_vectorstore.as_retriever(
    search_kwargs={
        "k": 10,  # Increase number of documents to retrieve
        "fetch_k": 20,  # Fetch more documents initially for better selection
        "maximal_marginal_relevance": True,  # Use MMR to ensure diversity
        "filter": None,  # No filtering
    }
)

# Create RetrievalQA with a better prompt template
qa = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
)
# -----------------------------------------------------------------------


def print_separator():
    print("\n" + "-" * 80 + "\n")


def analyze_query(query):
    # First, analyze what functions might be needed
    analysis_prompt = f"""Analyze this query and list all relevant functions that might be needed to implement it: {query}
List ONLY the function signatures that might be relevant, one per line. 
Each function should contain the function name, its parameters (with type) and its return type, in the following format:
function_name(parameter_name: parameter_type) -> return_type

For example:
add_cube(pos: Vec3, rot: Vec3, scale: Vec3) -> None

Do not include any other text."""

    print("\nAnalyzing required functions...")
    analysis = qa({"query": analysis_prompt})
    print()

    # Now get detailed information about these functions
    functions_info = []
    for doc in analysis["source_documents"]:
        functions_info.append(doc.page_content)

    # Create the final prompt with function information
    final_prompt = f"""Based on the following function information, provide ONLY the code implementation for: {query}

Available functions are:
---
{chr(10).join(functions_info)}
---

IMPORTANT: Respond ONLY with the code implementation inside a code block. If you cannot implement the solution, respond with 'no'.
Do not include any explanations or text outside the code block.

The template for the code block is:
```python
# Import the necessary libraries
import concept_forge as cf
from math import sin

from concept_forge import Entity
from concept_forge import Vec3

# Initialize the ConceptForge instance
forge = cf.ConceptForge()
forge.entities.clear()

# INITIALIZATION CODE
# Replace this block with code that initialiases thigs
# like creating, setting starting parameters, etc.

while not forge.window_should_close():
    forge.calc_delta_time()
    forge.calc_projection()

    # UPDATION CODE HERE
    # Replace this with all the things that should update in the loop
    # like positions, rotations, scales, etc.

    forge.gui_management()
    forge.process_input()
    forge.render()
```

only write extra code in the INITIALIZATION CODE and UPDATION CODE sections and remove these comments after filling these sections.
Keep the rest of the code as it is.

DO NOT use any functions that are not in the available functions list.
"""

    return final_prompt


# Interactive query loop ------------------------------------------------
print_separator()
print("Welcome to the Function Documentation Assistant!")
print("Ask questions about functions, their parameters, and usage.")
print("Type 'exit' to quit.")
print_separator()

while True:
    query = input("\nYour question: ").strip()
    if query.lower() == "exit":
        break
    print("\nAnswer:")
    final_prompt = analyze_query(query)
    result = qa({"query": final_prompt})
    print_separator()
# -----------------------------------------------------------------------
