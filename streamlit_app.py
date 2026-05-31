import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import os

# -----------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------

load_dotenv()

# -----------------------------
# OPENAI CLIENT
# -----------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("AI Customer Support Assistant")

# Sidebar title
st.sidebar.title("Support Assistant")

# -----------------------------
# CLEAR CHAT BUTTON
# -----------------------------

if st.sidebar.button("Clear Chat"):

    st.session_state.messages = []

    st.rerun()

# -----------------------------
# SESSION MEMORY INITIALIZATION
# -----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# -----------------------------
# FILE UPLOAD
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload Support Knowledge File",
    type=["txt"]
)

support_docs = []

# -----------------------------
# READ FILE CONTENT
# -----------------------------

if uploaded_file:

    # Read uploaded txt file
    file_content = uploaded_file.read().decode("utf-8")

    # Clean lines and remove empty rows
    support_docs = [
        line.strip()
        for line in file_content.split("\n")
        if line.strip()
    ]

    # Show number of support docs loaded
    st.sidebar.success(
        f"{len(support_docs)} support documents loaded"
    )

# -----------------------------
# SHOW MESSAGE IF NO FILE
# -----------------------------

if not support_docs:

    st.info(
        "Please upload a support knowledge file first."
    )

# -----------------------------
# VECTOR DATABASE SETUP
# -----------------------------

@st.cache_resource
def setup_vector_db(docs):

    # Create ChromaDB client
    chroma_client = chromadb.Client()

    # Delete old collection if exists
    try:
        chroma_client.delete_collection("support_docs")
    except:
        pass

    # Create fresh collection
    collection = chroma_client.create_collection(
        name="support_docs"
    )

    # Convert support docs into embeddings
    for i, doc in enumerate(docs):

        embedding_response = client.embeddings.create(
            model="text-embedding-3-small",
            input=doc
        )

        # Store embeddings in vector DB
        collection.add(
            documents=[doc],
            embeddings=[
                embedding_response.data[0].embedding
            ],
            ids=[f"doc{i}"]
        )

    return collection

# -----------------------------
# LOAD VECTOR DATABASE
# -----------------------------

if support_docs:

    collection = setup_vector_db(support_docs)

# -----------------------------
# CHAT INPUT
# -----------------------------

question = st.chat_input(
    "Ask your support question"
)

# -----------------------------
# MAIN AI WORKFLOW
# -----------------------------

if question and support_docs:

    # -----------------------------
    # SAVE USER MESSAGE
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # -----------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------

    with st.chat_message("user"):

        st.write(question)

    # -----------------------------
    # INTENT DETECTION
    # -----------------------------

    intent_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
                Classify the customer intent.

                Possible intents:
                - refund
                - password_reset
                - order_tracking
                - subscription
                - premium_support
                - unknown

                Only return the intent name.
                """
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    # Extract detected intent
    detected_intent = (
        intent_response
        .choices[0]
        .message
        .content
        .strip()
    )

    st.write(
        f"Detected Intent: {detected_intent}"
    )

    st.write(
        "Workflow Stage: Intent Classification Complete"
    )

    # -----------------------------
    # SENTIMENT ANALYSIS
    # -----------------------------

    sentiment_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
                Analyze customer sentiment.

                Possible sentiments:
                - positive
                - neutral
                - negative
                - angry

                Only return the sentiment.
                """
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    # Extract detected sentiment
    detected_sentiment = (
        sentiment_response
        .choices[0]
        .message
        .content
        .strip()
    )

    st.write(
        f"Detected Sentiment: {detected_sentiment}"
    )

    st.write(
        "Workflow Stage: Sentiment Analysis Complete"
    )

    # -----------------------------
    # PRIORITY LOGIC
    # -----------------------------

    priority = "low"

    if detected_sentiment == "negative":

        priority = "medium"

    if detected_sentiment == "angry":

        priority = "high"

    if detected_intent == "refund":

        priority = "high"

    if detected_intent == "premium_support":

        priority = "high"

    st.write(
        f"Support Priority: {priority}"
    )

    # -----------------------------
    # ESCALATION LOGIC
    # -----------------------------

    escalation_needed = False

    if (
        detected_sentiment == "angry"
        or detected_intent == "unknown"
    ):

        escalation_needed = True

    # -----------------------------
    # ESCALATE TO HUMAN AGENT
    # -----------------------------

    if escalation_needed:

        escalation_message = (
            "Your issue has been escalated "
            "to a human support agent."
        )

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": escalation_message
            }
        )

        # Display assistant response
        with st.chat_message("assistant"):

            st.write(escalation_message)

        st.stop()

    # -----------------------------
    # RAG RETRIEVAL
    # -----------------------------

    # Convert question into embedding
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    # Search similar support docs
    results = collection.query(
        query_embeddings=[
            query_embedding.data[0].embedding
        ],
        n_results=1
    )

    # Extract retrieved support document
    retrieved_doc = results["documents"][0][0]

    st.write(
        "Workflow Stage: Knowledge Retrieval Complete"
    )

    # -----------------------------
    # CONVERSATION MEMORY
    # -----------------------------

    conversation_history = []

    for msg in st.session_state.messages:

        conversation_history.append(
            {
                "role": msg["role"],
                "content": msg["content"]
            }
        )

    # -----------------------------
    # FINAL GPT RESPONSE
    # -----------------------------

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a professional customer support assistant.

                Use ONLY the retrieved support information
                to answer customer questions.

                Retrieved Support Information:
                {retrieved_doc}

                Return response in this exact format:

                {{
                    "customer_response": "...",
                    "priority": "low/medium/high",
                    "requires_followup": true/false
                }}

                Be concise and professional.
                """
            }
        ] + conversation_history
    )

    # Extract final response text
    response_text = (
        response
        .choices[0]
        .message
        .content
    )

    # -----------------------------
    # SAVE ASSISTANT RESPONSE
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text
        }
    )

    # -----------------------------
    # DISPLAY ASSISTANT RESPONSE
    # -----------------------------

    with st.chat_message("assistant"):

        st.write(response_text)

    st.write(
        "Workflow Stage: Response Generation Complete"
    )