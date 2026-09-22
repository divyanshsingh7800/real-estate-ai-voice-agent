🏠 Real Estate AI Voice Agent

An AI-powered voice agent for real-estate lead qualification and property recommendation.

The system communicates with customers through voice, understands their property requirements, asks for missing information, searches suitable properties from a local dataset, captures qualified lead details, calculates a lead qualification score, stores the lead in SQLite, and generates a conversation summary.

🚀 Project Overview

The goal of this project is to automate the initial real-estate customer interaction.

Instead of a salesperson manually asking every customer about their requirements, the AI voice agent can:

Understand customer property requirements

Ask follow-up questions for missing information

Recommend suitable properties

Capture customer name and phone number

Qualify the lead

Store lead information in SQLite

Generate a conversation summary

Respond using AI-generated voice

The project is designed as a practical Agentic AI prototype with a simple and modular architecture.

✨ Key Features

🎤 Voice Conversation

Customers can speak through the Streamlit interface.

The voice pipeline is:

Voice → Speech-to-Text → Agent → Response → Text-to-Speech

🏠 Property Recommendation

The agent searches the property dataset based on:

Location

BHK

Property type

Maximum budget

🧠 Requirement Collection

The agent collects:

Location

BHK

Property type

Budget

Purchase timeline

Purpose

👤 Lead Capture

Once the customer selects/is interested in a property, the agent collects:

Name

Phone number

📊 Lead Qualification Score

The project uses a 100-point qualification score:

Requirement

Points

Location

20

BHK

15

Budget

20

Timeline

20

Purpose

10

Phone

15

Total

100

📝 Conversation Summary

A summary of the customer's requirements and selected property is generated and stored with the lead.

💾 SQLite Database

Qualified leads are stored locally in:

real_estate.db

🏗️ Architecture

                    Customer
                       │
                       ▼
                🎤 Voice Input
                       │
                       ▼
              Speech-to-Text
                       │
                       ▼
              Streamlit Frontend
                       │
                       ▼
                FastAPI Backend
                       │
                       ▼
             Real Estate Agent
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   Requirement     Property      Lead
    Extraction      Search     Qualification
                       │            │
                       ▼            ▼
                properties.json  SQLite DB
                       │
                       └──────┬─────┘
                              ▼
                    Conversation Summary
                              │
                              ▼
                       Agent Response
                              │
                              ▼
                       Text-to-Speech
                              │
                              ▼
                         Customer

🔄 Conversation Workflow

1. Customer speaks
        ↓
2. Speech is converted to text
        ↓
3. Agent extracts requirements
        ↓
4. Missing information is requested
        ↓
5. Property dataset is searched
        ↓
6. Suitable property is recommended
        ↓
7. Customer confirms interest
        ↓
8. Name is collected
        ↓
9. Phone number is collected
        ↓
10. Lead score is calculated
        ↓
11. Lead is saved in SQLite
        ↓
12. Conversation summary is generated
        ↓
13. AI voice response is played

🛠️ Tech Stack

Backend

Python

FastAPI

Uvicorn

Pydantic

Voice

SpeechRecognition

Google Speech Recognition

Edge TTS

Streamlit Mic Recorder

Database

SQLite 3

Python built-in sqlite3

Frontend

Streamlit

Data

JSON property dataset

APIs / Libraries

Requests

Python-dotenv

📁 Project Structure

real_estate_voice_agent/
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── memory.py
│   │   └── prompts.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py
│   │   ├── property_service.py
│   │   ├── speech_to_text.py
│   │   └── text_to_speech.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   │
│   └── schemas/
│       ├── __init__.py
│       └── lead_schema.py
│
├── data/
│   └── properties.json
│
├── frontend/
│   ├── index.html
│   └── app.py
│
├── .gitignore
├── requirements.txt
└── README.md

⚙️ Installation

1. Clone the repository

git clone <https://github.com/divyanshsingh7800/real-estate-ai-voice-agent>
cd real_estate_voice_agent

2. Create virtual environment

Windows:

python -m venv venv

Activate it:

.env\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

For voice functionality, install:

pip install SpeechRecognition pyttsx3 PyAudio

The current frontend voice/TTS implementation also uses:

pip install edge-tts pygame streamlit streamlit-mic-recorder

▶️ Run the Backend

From the project root:

uvicorn app.main:app --reload

FastAPI will run at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

▶️ Run the Frontend

Open another terminal and activate the virtual environment.

Then run:

streamlit run frontend/app.py

Streamlit will provide the local application URL.

🔌 API Endpoints

GET /

Checks whether the API is running.

Example response:

{
  "message": "Real Estate Voice Agent API is running",
  "status": "success"
}

POST /chat

Sends a customer message to the real-estate agent.

Request:

{
  "message": "Mujhe Lucknow mein 2 BHK flat chahiye"
}

The response contains:

Agent response

Customer data

Lead ID when a lead is saved

Lead score

Conversation summary

GET /leads

Returns saved leads from the SQLite database.

💬 Sample Conversation 1 — Qualified Lead

Customer:
Mujhe Lucknow mein 2 BHK ka flat chahiye.

AI:
Aapka maximum budget kitna hai?

Customer:
60 lakh.

AI:
Aap property kab tak purchase karna chahte hain?

Customer:
3 mahine mein.

AI:
Property aap self-use ke liye le rahe hain ya investment ke liye?

Customer:
Self-use ke liye.

AI:
Aapki requirement ke according mujhe ye property mili hai.
Sunrise Enclave, 2 BHK, ₹58 lakh.
Kya aap is property mein interested hain?

Customer:
Haan, interested hoon.

AI:
Great choice. Aapka naam bata denge?

Customer:
Divyansh.

AI:
Thank you Divyansh. Aapka phone number share kar denge?

Customer:
7393847800.

AI:
Thank you Divyansh. Aapki details successfully note kar li hain.
Hamari team aapse jaldi contact karegi.

💬 Sample Conversation 2 — Different Requirement

Customer:
Mujhe Kanpur mein 3 BHK apartment chahiye.

AI:
Aapka maximum budget kitna hai?

Customer:
70 lakh.

AI:
Aap property kab tak purchase karna chahte hain?

Customer:
6 months mein.

AI:
Property aap self-use ke liye le rahe hain ya investment ke liye?

Customer:
Investment ke liye.

The agent then searches the property dataset and recommends a matching property when available.

💬 Sample Conversation 3 — No Matching Property

Customer:
Mujhe Lucknow mein 3 BHK flat chahiye.

AI:
Aapka maximum budget kitna hai?

Customer:
50 lakh.

AI:
Aap property kab tak purchase karna chahte hain?

Customer:
6 months mein.

AI:
Property aap self-use ke liye le rahe hain ya investment ke liye?

Customer:
Self-use.

If no property satisfies the collected filters, the agent informs the customer that a suitable property was not found and asks whether the budget or location can be made flexible.

🗃️ Property Dataset

Property information is maintained in:

data/properties.json

The dataset contains fields such as:

property_id
name
location
property_type
bhk
price
possession

Example:

{
  "property_id": "P003",
  "name": "Sunrise Enclave",
  "location": "Lucknow",
  "property_type": "Apartment",
  "bhk": 2,
  "price": 5800000,
  "possession": "2027"
}

💾 Lead Database

The application uses SQLite through Python's built-in sqlite3 module.

Database:

real_estate.db

The lead record stores information including:

name
phone
location
property_type
bhk
budget_min
budget_max
timeline
purpose
requirements
recommended_properties
conversation_summary
qualification_score

📊 Example Lead Record

Name: Divyansh
Phone: 7393847800
Location: Lucknow
Property Type: Apartment
BHK: 2
Budget: ₹60 lakh
Timeline: 3 months
Purpose: Self Use
Selected Property: Sunrise Enclave
Lead Score: 100

The exact score depends on which required information was successfully collected.

🧠 Agent Logic

The agent maintains conversation state using ConversationMemory.

It continuously checks which required fields are missing.

Required qualification fields:

Location
BHK
Budget
Timeline
Purpose

Once these are available, the agent searches the property dataset.

After a customer shows interest in a property, the agent collects:

Name
Phone

After the phone number is captured, the lead is stored in SQLite.

🎯 Assignment Requirements Covered

Requirement

Status

Voice Agent Demo

✅

Natural conversation flow

✅

Requirement collection

✅

Location

✅

BHK / Property Type

✅

Budget

✅

Timeline

✅

Purpose

✅

Property recommendation

✅

Name capture

✅

Phone capture

✅

Lead storage

✅

Conversation summary

✅

Lead qualification score

✅

Property dataset

✅

FastAPI backend

✅

Streamlit frontend

✅

SQLite database

✅

Sample conversation flows

✅

Architecture / workflow

✅

🚀 Deployment

The application is designed with separate frontend and backend components.

For deployment:

Streamlit Frontend
        │
        ▼
FastAPI Backend
        │
        ├── Property Dataset
        │
        └── SQLite Database

Before production deployment, environment variables, database persistence, microphone/browser permissions, and speech-recognition availability should be configured for the target hosting environment.

🔮 Future Enhancements

Possible future improvements:

Hindi + English language switching

More advanced LLM-based conversation

Real-time streaming voice interaction

Appointment booking

CRM integration

WhatsApp follow-up

Automated lead follow-up

Email notifications

Advanced property ranking

MongoDB/PostgreSQL for production

Authentication and admin dashboard

Improved lead scoring

Analytics dashboard

👨‍💻 Author

Divyansh Singh

AI/ML Developer | Python | Machine Learning | NLP | RAG | FastAPI | Streamlit

📌 Project Purpose

This project demonstrates how an Agentic AI workflow can automate the first stage of real-estate sales:

Understand → Qualify → Recommend → Capture → Store → Summarize

It combines voice interaction, conversational state management, property search, lead qualification, database storage, and text-to-speech into a single practical application.
