# AI Customer Support Assistant

## Project Objective

The goal of this project is to simulate a real-world AI-powered customer support workflow using Retrieval-Augmented Generation (RAG), conversational memory, intent detection, sentiment analysis, and workflow orchestration.

This project demonstrates how Large Language Models (LLMs) can be combined with vector databases, embeddings, business rules, and AI workflows to build intelligent customer support systems.

---

## Project Overview

An AI-powered customer support assistant built using OpenAI, Streamlit, ChromaDB, and Retrieval-Augmented Generation (RAG).

The application can:

* Answer customer support questions
* Retrieve information from uploaded support documents
* Detect customer intent
* Analyze customer sentiment
* Assign support priority
* Escalate difficult cases to human agents
* Maintain conversational memory
* Generate structured AI responses

---

## Features

* RAG-based support retrieval
* OpenAI embeddings
* ChromaDB vector database
* Conversational memory
* Intent detection
* Sentiment analysis
* Escalation workflow
* Priority assignment
* Structured AI outputs
* Streamlit chatbot UI
* Dynamic support file uploads
* Workflow stage visualization

---

## Architecture

```text
Customer Question
        ↓
Intent Detection
        ↓
Sentiment Analysis
        ↓
Priority Assignment
        ↓
Escalation Check
        ↓
RAG Retrieval
        ↓
GPT Response Generation
        ↓
Structured Support Response
```

---

## Tech Stack

* Python
* OpenAI API
* Streamlit
* ChromaDB
* Embeddings
* RAG (Retrieval-Augmented Generation)
* Prompt Engineering
* Vector Search
* Workflow Orchestration

---

## AI Concepts Used

### Retrieval-Augmented Generation (RAG)

The system retrieves relevant support information from a vector database before generating a response using GPT.

### Embeddings

Support documents and user questions are converted into vector embeddings for semantic similarity search.

### Vector Database

ChromaDB is used to store and retrieve document embeddings efficiently.

### Intent Detection

The LLM classifies the customer’s request type such as refund, password reset, or order tracking.

### Sentiment Analysis

The system analyzes customer emotion and detects positive, neutral, negative, or angry sentiment.

### Workflow Orchestration

The application combines multiple AI workflows including classification, retrieval, routing, escalation, and response generation.

### Conversational Memory

Previous chat messages are stored using Streamlit session state to maintain conversation context.

---

## Example Workflow

1. User uploads support knowledge file
2. Documents are converted into embeddings
3. Embeddings are stored in ChromaDB
4. User asks support question
5. Intent detection runs
6. Sentiment analysis runs
7. Priority is assigned
8. Escalation logic checks difficult cases
9. RAG retrieves relevant support information
10. GPT generates final structured response

---

## Project Structure

```text
ai-customer-support-assistant/
│
├── streamlit_app.py
├── app.py
├── support_data.txt
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/your-username/ai-customer-support-assistant.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Add OpenAI API Key

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

### Run Application

```bash
streamlit run streamlit_app.py
```

---

## Sample Support Data

```text
Password resets are completed using OTP verification.
Refunds are processed within 5 to 7 business days.
Orders can be tracked from the My Orders section.
Premium users get 24/7 support access.
Subscription cancellations become effective next billing cycle.
```

---

## What I Learned

* Building RAG pipelines
* Using embeddings and vector databases
* AI workflow orchestration
* Intent classification
* Sentiment analysis
* Conversational memory
* Streamlit frontend development
* Prompt engineering
* Structured AI outputs
* AI support system architecture
* Business rule integration
* Workflow-based AI engineering

---

## Future Improvements

* PDF support document uploads
* Voice-based customer support
* Multilingual support
* Ticket generation system
* Database integration
* Authentication system
* Analytics dashboard
* Deployment on Streamlit Cloud

---

## Key Learning Outcome

This project helped me understand how modern enterprise AI systems combine:

* LLMs
* Retrieval systems
* Embeddings
* Vector databases
* Workflow orchestration
* Business logic
* Conversational memory

to build scalable AI-powered applications.

---
