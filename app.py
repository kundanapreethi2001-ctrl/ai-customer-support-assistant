from openai import OpenAI
from dotenv import load_dotenv
import os
import chromadb

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="support_docs"
)

support_docs = [
    "Password resets are completed using OTP verification.",
    "Refunds are processed within 5 to 7 business days.",
    "Orders can be tracked from the My Orders section.",
    "Premium users get 24/7 support access.",
    "Subscription cancellations become effective next billing cycle."
]

for i, doc in enumerate(support_docs):

    embedding_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=doc
    )

    collection.add(
        documents=[doc],
        embeddings=[embedding_response.data[0].embedding],
        ids=[f"doc{i}"]
    )

question = input("Customer: ")

query_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)

results = collection.query(
    query_embeddings=[
        query_embedding.data[0].embedding
    ],
    n_results=1
)

retrieved_doc = results["documents"][0][0]

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": """
            You are a professional customer support assistant.

            Answer ONLY using provided support information.

            If information is unavailable,
            say you could not find the information.
            """
        },
        {
            "role": "user",
            "content": f"""
            Support Information:
            {retrieved_doc}

            Customer Question:
            {question}
            """
        }
    ]
)
print(
    response.choices[0].message.content
)
