# GenAI & AgenticAI-Recipe-Assistant-chatbot-

A RAG-powered multi-agent Generative AI recipe assistant built with CrewAI, LangChain, and Groq LLMs.

It delivers contextual chat, adaptive recipe generation, smart shopping, order tracking, and voice interaction(coming soon) — a complete Agentic AI ecosystem using Streamlit.




The README will reflect:

* The **architecture**,
  
* The **LangChain , RAG + CrewAI** integration,
  
* The **LLM models** used (Llama 3.3 70B(groq), HuggingFace(GPT2, Mixtral8x7B),FlanT5, DialoGPT
  
* The **streamlit UI & modular workflow**,
  
* **Agentic AI Chatbot concept (self-adaptive response system)**,
  
* And every single feature from chat memory to order returns.

---



## 🧾 **README.md**

```markdown
# 🍳 AI Recipe Assistant – GenAI Agentic AI Chatbot

### Developed by: **Gouthum Kharvi**

A **Generative AI-powered, Agentic AI Chatbot** built with **Streamlit**, **LangChain**, **RAG** , **CrewAI**, **ChromaDB**, and **Groq LLMs**, **Hugging Face LLMs** designed to deliver an intelligent, adaptive, and voice-enabled(coming soon..)  **AI culinary assistant**.  



This project is an advanced implementation of **Conversational AI + E-commerce Intelligence**, capable of generating recipes, managing shopping operations, handling orders, and responding intelligently through natural dialogue.

---



## 🧠 About the Project

### 🔮 What is an Agentic AI Chatbot?

An **Agentic AI**  Chatbot is a system built using autonomous AI agents that can reason, retrieve, and act based on user intent.
In this project, multiple specialized agents—powered by **CrewAI** and **LangChain**—work together to handle tasks like recipe generation, order management, and personalized interaction.

It uses **Retrieval-Augmented Generation (RAG)**  to dynamically fetch relevant data (recipes, ingredients, transactions, preferences) from a Chroma vector database, ensuring responses are factual and contextually grounded.

Unlike static chatbots, this Agentic GenAI system adapts to user behavior, learns preferences over time, and intelligently coordinates multiple tasks—making it an autonomous, context-aware, and self-improving AI assistant.

##  Project Overview
Vision Statement
Transform cooking assistance through Generative AI by creating an intelligent, context-aware chatbot that not only suggests recipes but also manages the entire cooking journey—from ingredient selection to order tracking and returns.
What Problem Does It Solve?

Information Overload: Users struggle to find personalized recipes from 231K+ recipe databases
Shopping Friction: Disconnected experience between recipe discovery and ingredient purchase
Post-Purchase Support: No integrated return/replacement system in cooking assistants
Context Loss: Traditional chatbots lack memory and personalization

Solution Approach
Agentic AI Chatbot that:

Attracts relevant context using vector similarity search (ChromaDB)
Adapts responses based on user preferences and history
Acts autonomously through CrewAI multi-agent orchestration
Assists throughout the entire customer journey
---


## 🚀 Key Highlights

| Category | Feature |
|-----------|----------|
| 💬 Conversational AI | LLM-powered natural conversation with memory & context |
| 🧠 GenAI Layer | Uses LangChain , RAG + CrewAI for reasoning, chaining & dynamic response |
| 🛒 E-Commerce System | Full shopping cart, wallet, and gift card modules |
| 🔁 Returns/Replacement | Integrated return & product replacement with tracking |
| 🔊 Voice Output(coming soon..) | Converts AI responses into audible speech |
| 📈 Analytics Dashboard | Visual insights on orders, achievements, and preferences |
| 🧑‍🍳 Recipe Generation | Personalized, diet-based recipe creation |
| ⚙️ LLM Selection | User can dynamically choose from multiple AI models (Llama, HuggingFace, Groq) |
| 💾 Persistent Session | All user data (cart, chat history, wallet) retained using Streamlit session state |
| 🧩 CrewAI Agents | Custom task orchestration for autonomous order/recipe handling |

---

## 🏗️ System Architecture


          Traditional Chatbot:  User Query → Static Response
Magnetic AI:         User Query → Context Attraction → Adaptive Response → Intelligent Action
```

**Three Pillars of Magnetic Intelligence:**

1. **Contextual Magnetism** (RAG with ChromaDB)
   - Dynamically pulls relevant recipes from 231K+ database
   - Semantic search using sentence transformers
   - Vector similarity scoring for precision

2. **Conversational Magnetism** (LangChain Memory)
   - Retains chat history across sessions
   - Builds user preference profiles
   - Context-aware response generation

3. **Action Magnetism** (CrewAI Agents)
   - Autonomous task orchestration
   - Multi-agent collaboration (Recipe Chef, Nutritionist, Shopping Assistant)
   - Self-healing workflow management

---

## 🏗️ System Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
│  (Streamlit App with Custom CSS Animations & Responsive Design) │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Conversational AI Layer                       │
│                                                                   │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │  LangChain  │──│ Memory Buffer│──│ Prompt Templates   │    │
│  │  Chain      │  │              │  │                    │    │
│  └─────────────┘  └──────────────┘  └────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Agent Orchestration                     │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐    │
│  │ Recipe Chef │  │ Nutritionist│  │ Shopping Assistant  │    │
│  │   Agent     │  │   Agent     │  │     Agent           │    │
│  └─────────────┘  └─────────────┘  └─────────────────────┘    │
│         │                 │                    │                 │
│         └─────────────────┴────────────────────┘                │
│                           │                                       │
│                    CrewAI Task Manager                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM Inference Layer                           │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐     │
│  │ Groq LLM API │  │ HuggingFace  │  │ OpenRouter API   │     │
│  │ (Llama 3.3)  │  │ Transformers │  │                  │     │
│  └──────────────┘  └──────────────┘  └──────────────────┘     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data & Storage Layer                          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐     │
│  │  ChromaDB    │  │ Session State│  │ CSV Dataset      │     │
│  │  (Vectors)   │  │ (In-Memory)  │  │ (231K Recipes)   │     │
│  └──────────────┘  └──────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────────────────────┘


---

## 💡 Functional Modules 

### 1️⃣ **Chat & Conversation Engine**

- Built using **LangChain ConversationalRetrievalChain** + **CrewAI Task Agents**

- Memory is maintained via `ConversationBufferMemory`

- Allows seamless switching between models (e.g. *Llama 3.3 70B*, *HuggingFace Transformers gpt2, mistral8x7B , DialoGPT, FLANT5)

- Supports user personalization (`Beginner`, `Vegan`, etc.)



### 2️⃣ **Recipe Generator (Core AI Module)**

- Uses Groq LLMs + LangChain prompt templates

- Retrieves relevant recipes using Chroma Vector Store

- Suggests meal prep steps, nutrition breakdown, and kitchen tools

- Integrates with voice synthesis for audible reading of steps


### 3️⃣ **Shopping Cart & Payments**

- Add items from recipe recommendations

- Handles checkout through:

  - Credit/Debit cards

  - Wallet

  - Gift cards

  - Third-party payment methods (PhonePe, GooglePay.Paytm, PayPal)

- Real-time balance updates and transaction tracking


### 4️⃣ **Wallet & Gift Card System**

- Session-based wallet ledger with transaction records

- Refill/top-up feature using secure form-based UI

- Gift card balance and redemption support



### 5️⃣ **Order Management System**

- Auto-generated sample delivered orders for testing

- Tracks:

  - Order placement

  - Payment

  - Delivery

  - Return/replacement requests

- Each order includes timeline tracking (visual step completion)


###  Complete E-Commerce System
Shopping Cart

Add ingredients/equipment from recipes
Quantity management
Real-time price calculation
Item removal/editing

Payment Gateway (8 Methods)

Credit/Debit Cards (with OTP verification)
Wallet (instant payment)
Gift Cards
PayPal
Google Pay
PhonePe
UPI
Cash on Delivery

Order Management
pythonOrder Lifecycle:
1. Order Placed → 2. Payment Confirmed → 3. Preparing Order 
→ 4. Out for Delivery → 5. Delivered


### 6️⃣ **Return & Replacement Module**

- Allows user to initiate:

  - Return request (for refund)

  - Replacement request (for damaged products)

- Tracks each request with unique ID counters (`ORD`, `RET`, `REP`)

- Simulated API response generation for status updates


### 7️⃣ **Voice Interaction(coming soon)**

- Text-to-speech response rendering

- Works dynamically with Streamlit session output

- Toggle to enable/disable via settings


### 8️⃣ **Analytics Dashboard**

- Tracks total chats, favorite recipes, total orders, and achievements

- Includes gamified milestones like:

  - 🏆 “First Chat”

  - 📚 “Knowledge Seeker”

  - 🍲 “Master Chef”

- Uses pandas DataFrame for metric computation


### 9️⃣ **UI & Aesthetic Design**

- Built in **Streamlit** with extensive **custom CSS animations**

- Components:

  - Gradient headers, animated chat bubbles, hover transitions

  - Recipe cards, progress bars, and status trackers

- Fully responsive and interactive


### 🔟 **Security & API Key Handling**

- Environment variables securely load:

  - `GROQ_API_KEY`

  - `HUGGINGFACEHUB_API_TOKEN`

  - `OPENROUTER_API_KEY`

- These APIs are used for inference through respective LLM backends

---



## 🧠 LLM Models & Frameworks Used

| Category | Library / Model |

|-----------|-----------------|

| **LLM Orchestration** | LangChain |

| **CrewAI Multi-Agent Task Manager** | CrewAI |

| **Embedding Models** | SentenceTransformer, HuggingFace |

| **Vector Database** | ChromaDB |

| **LLM Providers** | Groq, OpenRouter, HuggingFaceHub |

| **Primary Model** | Llama 3.3 70B |

| **Conversation Memory** | LangChain Buffer Memory |


## Data Processing

pythonPandas         # DataFrame operations

NumPy          # Numerical computations

AST            # Safe literal evaluation

JSON           # Data serialization

UUID           # Unique ID generation

DateTime       # Timestamp management

---


## ⚙️ Installation & Setup Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/ai-recipe-assistant.git
cd ai-recipe-assistant
````

### 2️⃣ Create Environment

```bash
python -m venv venv
source venv/bin/activate   # (Mac/Linux)
venv\Scripts\activate      # (Windows)
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Keys

Add your keys in environment variables:

```bash
# Windows
set GROQ_API_KEY=your_groq_api_key
set HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token
set OPENROUTER_API_KEY=your_openrouter_api_key

# Linux/Mac
export GROQ_API_KEY=your_groq_api_key
export HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token
export OPENROUTER_API_KEY=your_openrouter_api_key
```


### 5️⃣ Launch Streamlit App

```bash
streamlit run alternative_update_streamlit16.py
```

---


## 🧱 Directory Structure

```
AI-Recipe-Assistant/
│
├── cookingrecipies.ipynb                # Notebook for prototype logic, data setup, and testing
├── alternative_update_streamlit16.py    # Streamlit app with full GenAI chatbot system
├── requirements.txt                     # Dependencies
├── README.md                            # Project documentation
└── assets/                              # (Optional) Images, icons, or datasets
```

---



## 📊 Features Summary

| Feature               | Description                                           |
| --------------------- | ----------------------------------------------------- |
| Chatbot               | Conversational AI with memory, context, and reasoning |
| Recipe Recommendation | Personalized and LLM-generated suggestions            |
| Shopping Cart         | Full e-commerce workflow                              |
| Order Tracking        | Live status and progress visualization                |
| Wallet System         | Realtime balance updates, gift cards, transactions    |
| Voice Output(coming soon)          | Text-to-speech response                               |
| Model Switcher        | User can choose different AI models dynamically       |
| Analytics             | Session stats, achievements, and user behavior data   |
| Adaptive UI           | Context-sensitive, animated, and user-friendly        |

---


## 🧩 Model Selection Panel

Users can choose from:

* 🧠 **Llama 3.3 70B (Groq)** – Best general conversational model
* 🤗 **GPT2,Mixtral8X7B (HuggingFace Transformers)** – Open-source reasoning models
* 🧩 **Dialo GPT, FLAN-t5 (OpenRouter LLMs)** – Custom API integration for scalability

This flexibility enables experimentation with multiple LLM backends in one interface.

---


## 🧭 Workflow (Step-by-Step Logic Flow)

1️⃣ User interacts via chat →

2️⃣ Input routed to selected LLM (Groq/HuggingFace,OpenRouter) →

3️⃣ LangChain handles conversational context →

4️⃣ CrewAI agent allocates tasks (recipe creation, shopping, etc.) →

5️⃣ Vector retrieval from ChromaDB →

6️⃣ Response generation + formatting →

7️⃣ Streamlit UI displays formatted AI response →

8️⃣ User can act (add to cart, return item, etc.) →

9️⃣ Session state persists all actions (wallet, orders, chat)

---

## 🎨 UI Highlights (for GitHub Preview)

*(Add screenshots here later)*

```text
📸 Suggested images:
- Chatbot Interface
- Recipe Recommendation Screen
- Order Tracking
- Wallet / Gift Card Page
- Analytics Dashboard
```

---

## 🧩 Future Enhancements

* 🔊 Add **speech-to-text voice input**
* 🧾 Integrate **recipe image generation** using Vision-LLMs
* 📦 Connect **real-time grocery APIs**
* 🧠 Add **reinforcement learning** for dynamic recipe scoring
* 🔒 Incorporate **user authentication & database persistence**

---

## 👨‍💻 Developer Information

**Name:** Gouthum Kharvi
**Role:** GENAI Developer
**Location:** Udupi, Karnataka, India
**Specialization:** Machine Learning, Deep Learning , NLP, GenAI< AgenticAI Systems, MLOps
**Email:** [gouthumkharvi1899@gmail.com](gouthumkharvi1899@gmail.com)

---



## 🧭 Summary Statement

> “AI Recipe Assistant” is more than a chatbot — it’s a **self-adapting Generative AI and Agentic AI ecosystem** that integrates conversational reasoning, recommendation, and e-commerce intelligence into one seamless interface.

> Powered by **LangChain**, **RAG**, **CrewAI**, and **Groq LLMs**, it represents the future of *context-aware, personalized, and autonomous digital assistants*.

````



---


## ⚙️ **requirements.txt**

```txt
streamlit==1.38.0
pandas
numpy
langchain
langchain-groq
langchain-community
chromadb
sentence-transformers
huggingface-hub
crewai
python-dateutil
uuid
json5
re
base64
typing-extensions
aiohttp
pydantic
fsspec
faiss-cpu
requests
transformers
torch
tqdm
pyttsx3
SpeechRecognition
````

---

