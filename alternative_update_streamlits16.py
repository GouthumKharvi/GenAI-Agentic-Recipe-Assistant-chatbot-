"""
🍳 AI RECIPE ASSISTANT - COMPLETE UPDATED VERSION
Developed By: Gouthum
All Features Working | Voice Output | Shopping Cart | Favorites | Analytics
"""

import streamlit as st
import os
from datetime import datetime
import pandas as pd
import ast
import re
import base64
import json
import uuid
from io import BytesIO
from datetime import datetime, timedelta


# =======================🔹 CORE LANGCHAIN + GENAI IMPORTS =======================

# 🧠 Core LangChain Components
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# ✅ Retrieval + Combination (modern universal import)
from langchain_experimental.chains import create_retrieval_chain, create_stuff_documents_chain


# 🧩 Vector & Embedding Components
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 🤖 LLM & Multi-Agent AI
from langchain_groq import ChatGroq
from crewai import Agent, Task, Crew
from langgraph import Graph
from autogen import AssistantAgent, UserProxyAgent

# 🧠 Support Packages
import chromadb
from sentence_transformers import SentenceTransformer

# ⚙️ System Configuration
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Disable GPU if necessary





# ================== Set API keys=======================================================================
os.environ["GROQ_API_KEY"] = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
os.environ["OPENROUTER_API_KEY"] = "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"





# ==================== SESSION STATE INITIALIZATION ====================

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'shopping_cart' not in st.session_state:
    st.session_state.shopping_cart = []

if 'cart_items_count' not in st.session_state:
    st.session_state.cart_items_count = 0

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if 'total_messages' not in st.session_state:
    st.session_state.total_messages = 0

if 'achievements' not in st.session_state:
    st.session_state.achievements = ['🏆 First Chat', '📚 Knowledge Seeker']

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'chat'

if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = True

if 'preferences' not in st.session_state:
    st.session_state.preferences = {
        'user_name': 'Gouthum Kharvi',
        'dietary': 'None',
        'skill_level': 'Beginner'
    }

if 'redirect_to_shopping' not in st.session_state:
    st.session_state.redirect_to_shopping = False

if 'recipe_results' not in st.session_state:
    st.session_state.recipe_results = []

if 'current_recipe_page' not in st.session_state:
    st.session_state.current_recipe_page = 0

if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "Llama 3.3 70B (Best)"

if 'show_export' not in st.session_state:
    st.session_state.show_export = False

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'order_counter' not in st.session_state:
    st.session_state.order_counter = 1000

if 'wallet_balance' not in st.session_state:
    st.session_state.wallet_balance = 0.0
    
if 'wallet_transactions' not in st.session_state:
    st.session_state.wallet_transactions = []

if 'gift_card_balance' not in st.session_state:
    st.session_state.gift_card_balance = 0.0
    
if 'gift_card_transactions' not in st.session_state:
    st.session_state.gift_card_transactions = []

if 'show_wallet_topup' not in st.session_state:
    st.session_state.show_wallet_topup = False

if 'show_giftcard_topup' not in st.session_state:
    st.session_state.show_giftcard_topup = False

if 'order_history' not in st.session_state:
    st.session_state.order_history = []
    
if 'return_items' not in st.session_state:
    st.session_state.return_items = []
    
if 'replaced_items' not in st.session_state:
    st.session_state.replaced_items = {}


# ==================== NEW: RETURN & REPLACEMENT SESSION STATES ====================
if 'return_requests' not in st.session_state:
    st.session_state.return_requests = []

if 'return_counter' not in st.session_state:
    st.session_state.return_counter = 5000

if 'replacement_requests' not in st.session_state:
    st.session_state.replacement_requests = []

if 'replacement_counter' not in st.session_state:
    st.session_state.replacement_counter = 6000




# ==================== AUTO-DELIVERED SAMPLE ORDERS (for testing Return/Replacement) ====================
import random
from datetime import datetime, timedelta

if 'sample_orders_created' not in st.session_state:
    st.session_state.sample_orders_created = True

    # Only create 5 sample delivered orders (looks real)
    sample_customer = {
        'name': st.session_state.preferences['user_name'],
        'email': 'your@email.com',
        'phone': '+1 555-0123',
        'address': '456 Shopping Lane',
        'city': 'Your City',
        'state': 'YS',
        'zip': '12345'
    }

    # Kitchen equipment dictionary (with emojis)
    kitchen_equipment = {
        "knife": "🔪",
        "frying pan": "🍳",
        "blender": "🥤",
        "microwave": "📡",
        "refrigerator": "🧊",
        "oven": "🔥",
        "toaster": "🍞",
        "pressure cooker": "🍲",
        "cutting board": "🪵",
        "spoon": "🥄",
        "fork": "🍴",
        "plate": "🍽️",
        "mug": "☕",
        "kettle": "🫖",
        "whisk": "🍰",
        "rolling pin": "🪵",
        "measuring cup": "🧪",
        "bowl": "🥣",
        "grater": "🧀",
        "colander": "🕳️",
        "pizza cutter": "🍕",
        "tongs": "🤏",
        "ladle": "🍲",
        "peeler": "🥕",
        "ice cream scoop": "🍨",
        "refrigerator thermometer": "🌡️"
    }

    # Assign random prices for each item (100–1000 range)
    prices = {item: random.randint(100, 1000) for item in kitchen_equipment}

    # Pick 5 random items for random sample orders
    random_items = random.sample(list(kitchen_equipment.items()), 5)

    # Generate random sample orders using random kitchen items
    sample_orders = []
    for name, emoji in random_items:
        sample_orders.append({
            'items': [{'ingredient': f"{emoji} {name}", 'quantity': 1}],
            'total': float(prices[name])
        })

    # Delivered 2 days ago (eligible for return)
    delivered_time = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

    # Create 5 random orders
    sample_order_start = 5000
    for idx, sample in enumerate(sample_orders):
        order = {
            'order_id': f"ORD-{sample_order_start + idx}",  
            'date': delivered_time,
            'customer': sample_customer.copy(),
            'payment_method': 'credit_card',
            'items': sample['items'],
            'total': sample['total'],
            'status': 'Delivered',
            'tracking': [
                {'step': 'Order Placed', 'completed': True, 'time': delivered_time},
                {'step': 'Payment Confirmed', 'completed': True, 'time': delivered_time},
                {'step': 'Preparing Order', 'completed': True, 'time': delivered_time},
                {'step': 'Out for Delivery', 'completed': True, 'time': delivered_time},
                {'step': 'Delivered', 'completed': True, 'time': delivered_time}
            ]
        }
        st.session_state.orders.append(order)
    



# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="🤖 AI Recipe Assistant",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)





# ==================== CUSTOM CSS ====================

st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        animation: fadeIn 1s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 5px 15px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        animation: slideInRight 0.3s;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .chat-bot {
        background: #f8f9fa;
        color: #333;
        padding: 1rem;
        border-radius: 15px 15px 15px 5px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        animation: slideInLeft 0.3s;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .recipe-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .recipe-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .ingredient-item {
        background: #f0f4ff;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        border-left: 3px solid #667eea;
        font-size: 0.95rem;
        color: #333333;
    }
    
    .highlight {
        background-color: #ffeb3b;
        font-weight: bold;
        padding: 2px 4px;
        border-radius: 3px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)






# ==================== INGREDIENT DATA (500+ Items) ====================
ingredient_data = {
    # ==================== PASTA & GRAINS (25 items) ====================
    'pasta': {'price': 2.99, 'quantity': '500g', 'icon': '🍝'},
    'spaghetti': {'price': 3.49, 'quantity': '500g', 'icon': '🍝'},
    'penne': {'price': 3.29, 'quantity': '500g', 'icon': '🍝'},
    'macaroni': {'price': 2.89, 'quantity': '500g', 'icon': '🍝'},
    'linguine': {'price': 3.79, 'quantity': '500g', 'icon': '🍝'},
    'fettuccine': {'price': 3.99, 'quantity': '500g', 'icon': '🍝'},
    'lasagna': {'price': 4.49, 'quantity': '500g', 'icon': '🍝'},
    'ravioli': {'price': 5.99, 'quantity': '400g', 'icon': '🍝'},
    'tortellini': {'price': 6.49, 'quantity': '400g', 'icon': '🍝'},
    'fusilli': {'price': 3.19, 'quantity': '500g', 'icon': '🍝'},
    'rigatoni': {'price': 3.39, 'quantity': '500g', 'icon': '🍝'},
    'orzo': {'price': 3.99, 'quantity': '400g', 'icon': '🍝'},
    'rice': {'price': 4.99, 'quantity': '1 kg', 'icon': '🍚'},
    'basmati rice': {'price': 6.99, 'quantity': '1 kg', 'icon': '🍚'},
    'jasmine rice': {'price': 7.49, 'quantity': '1 kg', 'icon': '🍚'},
    'brown rice': {'price': 5.99, 'quantity': '1 kg', 'icon': '🍚'},
    'wild rice': {'price': 9.99, 'quantity': '500g', 'icon': '🍚'},
    'arborio rice': {'price': 8.49, 'quantity': '500g', 'icon': '🍚'},
    'quinoa': {'price': 7.99, 'quantity': '500g', 'icon': '🌾'},
    'couscous': {'price': 4.99, 'quantity': '500g', 'icon': '🌾'},
    'bulgur wheat': {'price': 4.49, 'quantity': '500g', 'icon': '🌾'},
    'barley': {'price': 3.99, 'quantity': '500g', 'icon': '🌾'},
    'farro': {'price': 6.99, 'quantity': '400g', 'icon': '🌾'},
    'millet': {'price': 5.49, 'quantity': '500g', 'icon': '🌾'},
    'buckwheat': {'price': 5.99, 'quantity': '500g', 'icon': '🌾'},
    
    # ==================== VEGETABLES (50 items) ====================
    'tomato': {'price': 3.99, 'quantity': '1 kg', 'icon': '🍅'},
    'cherry tomato': {'price': 5.49, 'quantity': '500g', 'icon': '🍅'},
    'roma tomato': {'price': 4.49, 'quantity': '1 kg', 'icon': '🍅'},
    'onion': {'price': 2.49, 'quantity': '1 kg', 'icon': '🧅'},
    'red onion': {'price': 2.99, 'quantity': '1 kg', 'icon': '🧅'},
    'green onion': {'price': 1.99, 'quantity': '1 bunch', 'icon': '🧅'},
    'shallots': {'price': 4.99, 'quantity': '500g', 'icon': '🧅'},
    'leek': {'price': 3.99, 'quantity': '500g', 'icon': '🧅'},
    'garlic': {'price': 3.49, 'quantity': '200g', 'icon': '🧄'},
    'carrot': {'price': 2.99, 'quantity': '1 kg', 'icon': '🥕'},
    'baby carrot': {'price': 3.99, 'quantity': '500g', 'icon': '🥕'},
    'potato': {'price': 3.49, 'quantity': '2 kg', 'icon': '🥔'},
    'sweet potato': {'price': 4.49, 'quantity': '1 kg', 'icon': '🍠'},
    'yam': {'price': 4.99, 'quantity': '1 kg', 'icon': '🍠'},
    'spinach': {'price': 3.99, 'quantity': '500g', 'icon': '🥬'},
    'kale': {'price': 4.49, 'quantity': '500g', 'icon': '🥬'},
    'lettuce': {'price': 2.99, 'quantity': '1 head', 'icon': '🥬'},
    'romaine lettuce': {'price': 3.49, 'quantity': '1 head', 'icon': '🥬'},
    'arugula': {'price': 4.99, 'quantity': '200g', 'icon': '🥬'},
    'broccoli': {'price': 3.99, 'quantity': '500g', 'icon': '🥦'},
    'cauliflower': {'price': 4.49, 'quantity': '1 head', 'icon': '🥦'},
    'brussels sprouts': {'price': 5.49, 'quantity': '500g', 'icon': '🥬'},
    'cabbage': {'price': 2.99, 'quantity': '1 head', 'icon': '🥬'},
    'red cabbage': {'price': 3.49, 'quantity': '1 head', 'icon': '🥬'},
    'bell pepper': {'price': 4.99, 'quantity': '500g', 'icon': '🫑'},
    'red bell pepper': {'price': 5.49, 'quantity': '500g', 'icon': '🫑'},
    'yellow bell pepper': {'price': 5.49, 'quantity': '500g', 'icon': '🫑'},
    'green bell pepper': {'price': 4.49, 'quantity': '500g', 'icon': '🫑'},
    'jalapeño': {'price': 3.99, 'quantity': '200g', 'icon': '🌶️'},
    'serrano pepper': {'price': 4.49, 'quantity': '200g', 'icon': '🌶️'},
    'habanero': {'price': 5.99, 'quantity': '100g', 'icon': '🌶️'},
    'cucumber': {'price': 2.99, 'quantity': '500g', 'icon': '🥒'},
    'english cucumber': {'price': 3.99, 'quantity': '1 piece', 'icon': '🥒'},
    'zucchini': {'price': 3.49, 'quantity': '500g', 'icon': '🥒'},
    'yellow squash': {'price': 3.49, 'quantity': '500g', 'icon': '🥒'},
    'eggplant': {'price': 4.99, 'quantity': '500g', 'icon': '🍆'},
    'mushroom': {'price': 5.99, 'quantity': '400g', 'icon': '🍄'},
    'shiitake mushroom': {'price': 8.99, 'quantity': '300g', 'icon': '🍄'},
    'portobello mushroom': {'price': 7.49, 'quantity': '400g', 'icon': '🍄'},
    'oyster mushroom': {'price': 6.99, 'quantity': '300g', 'icon': '🍄'},
    'asparagus': {'price': 6.99, 'quantity': '500g', 'icon': '🥒'},
    'green beans': {'price': 4.99, 'quantity': '500g', 'icon': '🫘'},
    'snap peas': {'price': 5.49, 'quantity': '400g', 'icon': '🫛'},
    'snow peas': {'price': 5.49, 'quantity': '400g', 'icon': '🫛'},
    'corn': {'price': 3.99, 'quantity': '4 ears', 'icon': '🌽'},
    'baby corn': {'price': 4.99, 'quantity': '400g', 'icon': '🌽'},
    'celery': {'price': 2.99, 'quantity': '1 bunch', 'icon': '🥬'},
    'bok choy': {'price': 3.99, 'quantity': '500g', 'icon': '🥬'},
    'napa cabbage': {'price': 4.49, 'quantity': '1 head', 'icon': '🥬'},
    'radish': {'price': 2.99, 'quantity': '500g', 'icon': '🔴'},
    
    # ==================== FRUITS (50 items) ====================
    'apple': {'price': 4.49, 'quantity': '1 kg', 'icon': '🍎'},
    'green apple': {'price': 4.49, 'quantity': '1 kg', 'icon': '🍏'},
    'red apple': {'price': 4.49, 'quantity': '1 kg', 'icon': '🍎'},
    'banana': {'price': 2.99, 'quantity': '1 kg', 'icon': '🍌'},
    'plantain': {'price': 3.49, 'quantity': '1 kg', 'icon': '🍌'},
    'orange': {'price': 4.99, 'quantity': '1 kg', 'icon': '🍊'},
    'blood orange': {'price': 6.49, 'quantity': '1 kg', 'icon': '🍊'},
    'mandarin': {'price': 5.49, 'quantity': '1 kg', 'icon': '🍊'},
    'tangerine': {'price': 5.49, 'quantity': '1 kg', 'icon': '🍊'},
    'clementine': {'price': 5.99, 'quantity': '1 kg', 'icon': '🍊'},
    'lemon': {'price': 3.99, 'quantity': '500g', 'icon': '🍋'},
    'lime': {'price': 3.49, 'quantity': '500g', 'icon': '🍋'},
    'grapefruit': {'price': 5.99, 'quantity': '1 kg', 'icon': '🍊'},
    'grape': {'price': 5.99, 'quantity': '500g', 'icon': '🍇'},
    'red grape': {'price': 6.49, 'quantity': '500g', 'icon': '🍇'},
    'green grape': {'price': 6.49, 'quantity': '500g', 'icon': '🍇'},
    'strawberry': {'price': 6.99, 'quantity': '500g', 'icon': '🍓'},
    'blueberry': {'price': 7.99, 'quantity': '300g', 'icon': '🫐'},
    'raspberry': {'price': 8.49, 'quantity': '300g', 'icon': '🍇'},
    'blackberry': {'price': 8.49, 'quantity': '300g', 'icon': '🫐'},
    'cranberry': {'price': 6.99, 'quantity': '400g', 'icon': '🔴'},
    'watermelon': {'price': 6.99, 'quantity': '1 whole', 'icon': '🍉'},
    'cantaloupe': {'price': 5.99, 'quantity': '1 whole', 'icon': '🍈'},
    'honeydew': {'price': 6.49, 'quantity': '1 whole', 'icon': '🍈'},
    'mango': {'price': 3.99, 'quantity': '2 pieces', 'icon': '🥭'},
    'papaya': {'price': 4.99, 'quantity': '1 piece', 'icon': '🍈'},
    'pineapple': {'price': 5.99, 'quantity': '1 whole', 'icon': '🍍'},
    'kiwi': {'price': 5.49, 'quantity': '6 pieces', 'icon': '🥝'},
    'dragon fruit': {'price': 7.99, 'quantity': '2 pieces', 'icon': '🐉'},
    'passion fruit': {'price': 6.99, 'quantity': '6 pieces', 'icon': '🟣'},
    'avocado': {'price': 5.99, 'quantity': '4 pieces', 'icon': '🥑'},
    'peach': {'price': 5.99, 'quantity': '1 kg', 'icon': '🍑'},
    'nectarine': {'price': 6.49, 'quantity': '1 kg', 'icon': '🍑'},
    'plum': {'price': 5.49, 'quantity': '1 kg', 'icon': '🍑'},
    'apricot': {'price': 6.99, 'quantity': '500g', 'icon': '🍑'},
    'cherry': {'price': 9.99, 'quantity': '500g', 'icon': '🍒'},
    'pear': {'price': 5.49, 'quantity': '1 kg', 'icon': '🍐'},
    'asian pear': {'price': 6.99, 'quantity': '1 kg', 'icon': '🍐'},
    'fig': {'price': 8.99, 'quantity': '400g', 'icon': '🟤'},
    'date': {'price': 7.99, 'quantity': '500g', 'icon': '🟤'},
    'pomegranate': {'price': 6.99, 'quantity': '2 pieces', 'icon': '🟣'},
    'persimmon': {'price': 7.49, 'quantity': '500g', 'icon': '🟠'},
    'lychee': {'price': 8.99, 'quantity': '500g', 'icon': '🔴'},
    'rambutan': {'price': 9.49, 'quantity': '500g', 'icon': '🔴'},
    'star fruit': {'price': 6.99, 'quantity': '400g', 'icon': '⭐'},
    'guava': {'price': 5.99, 'quantity': '500g', 'icon': '🟢'},
    'coconut': {'price': 4.99, 'quantity': '1 piece', 'icon': '🥥'},
    'jackfruit': {'price': 12.99, 'quantity': '1 kg', 'icon': '🟡'},
    'durian': {'price': 19.99, 'quantity': '1 kg', 'icon': '🟡'},
    'longan': {'price': 7.99, 'quantity': '500g', 'icon': '🟤'},
    
    # ==================== MEAT & POULTRY (40 items) ====================
    'chicken': {'price': 8.99, 'quantity': '1 kg', 'icon': '🍗'},
    'chicken breast': {'price': 12.99, 'quantity': '1 kg', 'icon': '🍗'},
    'chicken thigh': {'price': 10.99, 'quantity': '1 kg', 'icon': '🍗'},
    'chicken wings': {'price': 9.99, 'quantity': '1 kg', 'icon': '🍗'},
    'chicken drumstick': {'price': 9.49, 'quantity': '1 kg', 'icon': '🍗'},
    'whole chicken': {'price': 14.99, 'quantity': '1.5 kg', 'icon': '🍗'},
    'chicken liver': {'price': 6.99, 'quantity': '500g', 'icon': '🍗'},
    'chicken gizzard': {'price': 5.99, 'quantity': '500g', 'icon': '🍗'},
    'ground chicken': {'price': 11.49, 'quantity': '500g', 'icon': '🍗'},
    'turkey': {'price': 11.99, 'quantity': '1 kg', 'icon': '🦃'},
    'turkey breast': {'price': 14.99, 'quantity': '1 kg', 'icon': '🦃'},
    'ground turkey': {'price': 12.49, 'quantity': '500g', 'icon': '🦃'},
    'duck': {'price': 16.99, 'quantity': '1 kg', 'icon': '🦆'},
    'duck breast': {'price': 19.99, 'quantity': '500g', 'icon': '🦆'},
    'quail': {'price': 14.99, 'quantity': '4 pieces', 'icon': '🐦'},
    'ground beef': {'price': 11.99, 'quantity': '500g', 'icon': '🥩'},
    'beef steak': {'price': 19.99, 'quantity': '500g', 'icon': '🥩'},
    'ribeye steak': {'price': 24.99, 'quantity': '500g', 'icon': '🥩'},
    'sirloin steak': {'price': 22.99, 'quantity': '500g', 'icon': '🥩'},
    'tenderloin': {'price': 29.99, 'quantity': '500g', 'icon': '🥩'},
    'beef ribs': {'price': 15.99, 'quantity': '1 kg', 'icon': '🥩'},
    'beef brisket': {'price': 17.99, 'quantity': '1 kg', 'icon': '🥩'},
    'beef shank': {'price': 13.99, 'quantity': '1 kg', 'icon': '🥩'},
    'beef chuck': {'price': 12.99, 'quantity': '1 kg', 'icon': '🥩'},
    'beef liver': {'price': 8.99, 'quantity': '500g', 'icon': '🥩'},
    'pork': {'price': 10.99, 'quantity': '1 kg', 'icon': '🥓'},
    'pork chop': {'price': 12.99, 'quantity': '1 kg', 'icon': '🥓'},
    'pork tenderloin': {'price': 14.99, 'quantity': '500g', 'icon': '🥓'},
    'pork ribs': {'price': 13.99, 'quantity': '1 kg', 'icon': '🥓'},
    'pork belly': {'price': 11.99, 'quantity': '1 kg', 'icon': '🥓'},
    'ground pork': {'price': 9.99, 'quantity': '500g', 'icon': '🥓'},
    'bacon': {'price': 7.99, 'quantity': '400g', 'icon': '🥓'},
    'canadian bacon': {'price': 9.49, 'quantity': '400g', 'icon': '🥓'},
    'sausage': {'price': 8.99, 'quantity': '500g', 'icon': '🌭'},
    'italian sausage': {'price': 9.99, 'quantity': '500g', 'icon': '🌭'},
    'chorizo': {'price': 10.49, 'quantity': '400g', 'icon': '🌭'},
    'bratwurst': {'price': 11.99, 'quantity': '500g', 'icon': '🌭'},
    'ham': {'price': 9.99, 'quantity': '500g', 'icon': '🍖'},
    'lamb': {'price': 18.99, 'quantity': '1 kg', 'icon': '🍖'},
    'lamb chop': {'price': 22.99, 'quantity': '500g', 'icon': '🍖'},
    
    # ==================== SEAFOOD (40 items) ====================
    'fish': {'price': 12.99, 'quantity': '500g', 'icon': '🐟'},
    'salmon': {'price': 16.99, 'quantity': '500g', 'icon': '🐟'},
    'atlantic salmon': {'price': 18.99, 'quantity': '500g', 'icon': '🐟'},
    'smoked salmon': {'price': 22.99, 'quantity': '400g', 'icon': '🐟'},
    'tuna': {'price': 14.99, 'quantity': '500g', 'icon': '🐟'},
    'yellowfin tuna': {'price': 17.99, 'quantity': '500g', 'icon': '🐟'},
    'ahi tuna': {'price': 19.99, 'quantity': '500g', 'icon': '🐟'},
    'cod': {'price': 13.99, 'quantity': '500g', 'icon': '🐟'},
    'tilapia': {'price': 11.99, 'quantity': '500g', 'icon': '🐟'},
    'halibut': {'price': 19.99, 'quantity': '500g', 'icon': '🐟'},
    'mahi mahi': {'price': 17.99, 'quantity': '500g', 'icon': '🐟'},
    'snapper': {'price': 16.99, 'quantity': '500g', 'icon': '🐟'},
    'sea bass': {'price': 18.99, 'quantity': '500g', 'icon': '🐟'},
    'trout': {'price': 14.99, 'quantity': '500g', 'icon': '🐟'},
    'mackerel': {'price': 12.99, 'quantity': '500g', 'icon': '🐟'},
    'sardine': {'price': 9.99, 'quantity': '400g', 'icon': '🐟'},
    'anchovy': {'price': 8.99, 'quantity': '300g', 'icon': '🐟'},
    'catfish': {'price': 11.99, 'quantity': '500g', 'icon': '🐟'},
    'swordfish': {'price': 21.99, 'quantity': '500g', 'icon': '🐟'},
    'barramundi': {'price': 17.99, 'quantity': '500g', 'icon': '🐟'},
    'shrimp': {'price': 18.99, 'quantity': '500g', 'icon': '🦐'},
    'jumbo shrimp': {'price': 24.99, 'quantity': '500g', 'icon': '🦐'},
    'tiger shrimp': {'price': 22.99, 'quantity': '500g', 'icon': '🦐'},
    'prawn': {'price': 20.99, 'quantity': '500g', 'icon': '🦐'},
    'crab': {'price': 24.99, 'quantity': '500g', 'icon': '🦀'},
    'king crab': {'price': 39.99, 'quantity': '500g', 'icon': '🦀'},
    'snow crab': {'price': 34.99, 'quantity': '500g', 'icon': '🦀'},
    'blue crab': {'price': 29.99, 'quantity': '500g', 'icon': '🦀'},
    'lobster': {'price': 34.99, 'quantity': '500g', 'icon': '🦞'},
    'lobster tail': {'price': 44.99, 'quantity': '400g', 'icon': '🦞'},
    'oyster': {'price': 22.99, 'quantity': '12 pieces', 'icon': '🦪'},
    'clam': {'price': 16.99, 'quantity': '1 kg', 'icon': '🦪'},
    'mussel': {'price': 14.99, 'quantity': '1 kg', 'icon': '🦪'},
    'scallop': {'price': 26.99, 'quantity': '500g', 'icon': '🦪'},
    'squid': {'price': 13.99, 'quantity': '500g', 'icon': '🦑'},
    'octopus': {'price': 17.99, 'quantity': '500g', 'icon': '🐙'},
    'calamari': {'price': 15.99, 'quantity': '500g', 'icon': '🦑'},
    'cuttlefish': {'price': 16.99, 'quantity': '500g', 'icon': '🦑'},
    'sea urchin': {'price': 29.99, 'quantity': '200g', 'icon': '🦔'},
    'caviar': {'price': 99.99, 'quantity': '100g', 'icon': '🥚'},
    
    # ==================== DAIRY & EGGS (30 items) ====================
    'milk': {'price': 3.99, 'quantity': '1 liter', 'icon': '🥛'},
    'whole milk': {'price': 4.49, 'quantity': '1 liter', 'icon': '🥛'},
    'skim milk': {'price': 3.99, 'quantity': '1 liter', 'icon': '🥛'},
    '2% milk': {'price': 4.19, 'quantity': '1 liter', 'icon': '🥛'},
    'almond milk': {'price': 5.99, 'quantity': '1 liter', 'icon': '🥛'},
    'soy milk': {'price': 5.49, 'quantity': '1 liter', 'icon': '🥛'},
    'oat milk': {'price': 6.49, 'quantity': '1 liter', 'icon': '🥛'},
    'coconut milk': {'price': 5.99, 'quantity': '1 liter', 'icon': '🥥'},
    'evaporated milk': {'price': 4.99, 'quantity': '400ml', 'icon': '🥛'},
    'condensed milk': {'price': 5.49, 'quantity': '400ml', 'icon': '🥛'},
    'buttermilk': {'price': 4.49, 'quantity': '1 liter', 'icon': '🥛'},
    'heavy cream': {'price': 6.99, 'quantity': '500ml', 'icon': '🥛'},
    'whipping cream': {'price': 6.49, 'quantity': '500ml', 'icon': '🥛'},
    'half and half': {'price': 5.49, 'quantity': '500ml', 'icon': '🥛'},
    'sour cream': {'price': 4.49, 'quantity': '400g', 'icon': '🥛'},
    'cream cheese': {'price': 5.99, 'quantity': '250g', 'icon': '🧀'},
    'cheese': {'price': 7.99, 'quantity': '400g', 'icon': '🧀'},
    'cheddar': {'price': 8.99, 'quantity': '400g', 'icon': '🧀'},
    'mozzarella': {'price': 7.49, 'quantity': '400g', 'icon': '🧀'},
    'parmesan': {'price': 12.99, 'quantity': '300g', 'icon': '🧀'},
    'gouda': {'price': 9.99, 'quantity': '400g', 'icon': '🧀'},
    'swiss cheese': {'price': 9.49, 'quantity': '400g', 'icon': '🧀'},
    'brie': {'price': 11.99, 'quantity': '300g', 'icon': '🧀'},
    'feta': {'price': 8.99, 'quantity': '400g', 'icon': '🧀'},
    'blue cheese': {'price': 10.99, 'quantity': '300g', 'icon': '🧀'},
    'butter': {'price': 5.49, 'quantity': '250g', 'icon': '🧈'},
    'unsalted butter': {'price': 5.99, 'quantity': '250g', 'icon': '🧈'},
    'yogurt': {'price': 4.99, 'quantity': '500g', 'icon': '🥛'},
    'greek yogurt': {'price': 6.49, 'quantity': '500g', 'icon': '🥛'},
    'egg': {'price': 5.99, 'quantity': '12 pieces', 'icon': '🥚'},
    
    # ==================== OILS & CONDIMENTS (40 items) ====================
    'olive oil': {'price': 12.99, 'quantity': '750ml', 'icon': '🫒'},
    'extra virgin olive oil': {'price': 16.99, 'quantity': '750ml', 'icon': '🫒'},
    'vegetable oil': {'price': 6.99, 'quantity': '1 liter', 'icon': '🛢️'},
    'canola oil': {'price': 7.49, 'quantity': '1 liter', 'icon': '🛢️'},
    'sunflower oil': {'price': 7.99, 'quantity': '1 liter', 'icon': '🛢️'},
    'corn oil': {'price': 6.99, 'quantity': '1 liter', 'icon': '🛢️'},
    'coconut oil': {'price': 9.99, 'quantity': '500ml', 'icon': '🥥'},
    'sesame oil': {'price': 8.99, 'quantity': '400ml', 'icon': '🛢️'},
    'avocado oil': {'price': 14.99, 'quantity': '500ml', 'icon': '🥑'},
    'peanut oil': {'price': 9.99, 'quantity': '750ml', 'icon': '🥜'},
    'grapeseed oil': {'price': 11.99, 'quantity': '500ml', 'icon': '🍇'},
    'walnut oil': {'price': 13.99, 'quantity': '500ml', 'icon': '🥜'},
    'salt': {'price': 1.99, 'quantity': '500g', 'icon': '🧂'},
    'sea salt': {'price': 3.99, 'quantity': '400g', 'icon': '🧂'},
    'himalayan salt': {'price': 5.99, 'quantity': '400g', 'icon': '🧂'},
    'kosher salt': {'price': 4.49, 'quantity': '500g', 'icon': '🧂'},
    'pepper': {'price': 4.99, 'quantity': '100g', 'icon': '🌶️'},
    'black pepper': {'price': 5.49, 'quantity': '100g', 'icon': '🌶️'},
    'white pepper': {'price': 5.99, 'quantity': '100g', 'icon': '🌶️'},
    'cayenne pepper': {'price': 6.49, 'quantity': '100g', 'icon': '🌶️'},
    'sugar': {'price': 3.49, 'quantity': '1 kg', 'icon': '🍬'},
    'brown sugar': {'price': 4.49, 'quantity': '1 kg', 'icon': '🍬'},
    'powdered sugar': {'price': 4.99, 'quantity': '500g', 'icon': '🍬'},
    'honey': {'price': 8.99, 'quantity': '500g', 'icon': '🍯'},
    'maple syrup': {'price': 12.99, 'quantity': '500ml', 'icon': '🍁'},
    'agave nectar': {'price': 9.99, 'quantity': '500ml', 'icon': '🌵'},
    'vinegar': {'price': 3.99, 'quantity': '750ml', 'icon': '🧴'},
    'apple cider vinegar': {'price': 5.99, 'quantity': '750ml', 'icon': '🧴'},
    'balsamic vinegar': {'price': 9.99, 'quantity': '500ml', 'icon': '🧴'},
    'rice vinegar': {'price': 4.99, 'quantity': '500ml', 'icon': '🧴'},
    'white vinegar': {'price': 3.49, 'quantity': '1 liter', 'icon': '🧴'},
    'soy sauce': {'price': 4.99, 'quantity': '500ml', 'icon': '🧴'},
    'dark soy sauce': {'price': 5.49, 'quantity': '500ml', 'icon': '🧴'},
    'fish sauce': {'price': 5.99, 'quantity': '500ml', 'icon': '🐟'},
    'oyster sauce': {'price': 6.49, 'quantity': '500ml', 'icon': '🦪'},
    'worcestershire sauce': {'price': 5.49, 'quantity': '400ml', 'icon': '🧴'},
    'hot sauce': {'price': 4.99, 'quantity': '300ml', 'icon': '🌶️'},
    'sriracha': {'price': 5.99, 'quantity': '400ml', 'icon': '🌶️'},
    'ketchup': {'price': 3.99, 'quantity': '500g', 'icon': '🍅'},
    'mayonnaise': {'price': 4.99, 'quantity': '400g', 'icon': '🥪'},
    
    # ==================== SPICES & HERBS (50 items) ====================
    'basil': {'price': 3.99, 'quantity': '50g', 'icon': '🌿'},
    'oregano': {'price': 4.49, 'quantity': '50g', 'icon': '🌿'},
    'thyme': {'price': 4.99, 'quantity': '50g', 'icon': '🌿'},
    'rosemary': {'price': 4.99, 'quantity': '50g', 'icon': '🌿'},
    'parsley': {'price': 2.99, 'quantity': '1 bunch', 'icon': '🌿'},
    'cilantro': {'price': 2.99, 'quantity': '1 bunch', 'icon': '🌿'},
    'dill': {'price': 3.49, 'quantity': '1 bunch', 'icon': '🌿'},
    'mint': {'price': 3.49, 'quantity': '1 bunch', 'icon': '🌿'},
    'sage': {'price': 4.99, 'quantity': '50g', 'icon': '🌿'},
    'tarragon': {'price': 5.49, 'quantity': '50g', 'icon': '🌿'},
    'chives': {'price': 3.49, 'quantity': '1 bunch', 'icon': '🌿'},
    'bay leaves': {'price': 4.99, 'quantity': '50g', 'icon': '🍃'},
    'cinnamon': {'price': 5.99, 'quantity': '100g', 'icon': '🥄'},
    'cinnamon stick': {'price': 6.99, 'quantity': '50g', 'icon': '🥄'},
    'cumin': {'price': 5.49, 'quantity': '100g', 'icon': '🥄'},
    'coriander': {'price': 5.49, 'quantity': '100g', 'icon': '🥄'},
    'turmeric': {'price': 6.49, 'quantity': '100g', 'icon': '🥄'},
    'paprika': {'price': 5.99, 'quantity': '100g', 'icon': '🥄'},
    'smoked paprika': {'price': 6.99, 'quantity': '100g', 'icon': '🥄'},
    'chili powder': {'price': 5.99, 'quantity': '100g', 'icon': '🌶️'},
    'curry powder': {'price': 6.99, 'quantity': '100g', 'icon': '🥄'},
    'garam masala': {'price': 7.99, 'quantity': '100g', 'icon': '🥄'},
    'cardamom': {'price': 8.99, 'quantity': '50g', 'icon': '🥄'},
    'cloves': {'price': 7.99, 'quantity': '50g', 'icon': '🥄'},
    'nutmeg': {'price': 8.49, 'quantity': '50g', 'icon': '🥄'},
    'allspice': {'price': 6.99, 'quantity': '100g', 'icon': '🥄'},
    'ginger': {'price': 4.99, 'quantity': '200g', 'icon': '🫚'},
    'ginger powder': {'price': 5.99, 'quantity': '100g', 'icon': '🫚'},
    'garlic powder': {'price': 5.49, 'quantity': '100g', 'icon': '🧄'},
    'onion powder': {'price': 4.99, 'quantity': '100g', 'icon': '🧅'},
    'mustard powder': {'price': 5.49, 'quantity': '100g', 'icon': '🥄'},
    'mustard seeds': {'price': 4.99, 'quantity': '100g', 'icon': '🌾'},
    'fennel seeds': {'price': 5.49, 'quantity': '100g', 'icon': '🌾'},
    'caraway seeds': {'price': 5.99, 'quantity': '100g', 'icon': '🌾'},
    'poppy seeds': {'price': 6.49, 'quantity': '100g', 'icon': '🌾'},
    'sesame seeds': {'price': 4.99, 'quantity': '200g', 'icon': '🌾'},
    'celery seeds': {'price': 5.49, 'quantity': '100g', 'icon': '🌾'},
    'anise': {'price': 6.99, 'quantity': '100g', 'icon': '🌾'},
    'star anise': {'price': 7.99, 'quantity': '50g', 'icon': '⭐'},
    'saffron': {'price': 29.99, 'quantity': '10g', 'icon': '🟡'},
    'vanilla extract': {'price': 12.99, 'quantity': '100ml', 'icon': '🧴'},
    'vanilla bean': {'price': 19.99, 'quantity': '5 pieces', 'icon': '🥄'},
    'red pepper flakes': {'price': 4.99, 'quantity': '100g', 'icon': '🌶️'},
    'italian seasoning': {'price': 5.99, 'quantity': '100g', 'icon': '🌿'},
    'herbs de provence': {'price': 6.99, 'quantity': '100g', 'icon': '🌿'},
    'five spice': {'price': 6.99, 'quantity': '100g', 'icon': '🥄'},
    'za\'atar': {'price': 7.99, 'quantity': '100g', 'icon': '🌿'},
    'sumac': {'price': 8.49, 'quantity': '100g', 'icon': '🔴'},
    'fenugreek': {'price': 6.49, 'quantity': '100g', 'icon': '🌿'},
    'asafoetida': {'price': 7.99, 'quantity': '50g', 'icon': '🥄'},
    
    # ==================== NUTS & SEEDS (25 items) ====================
    'almond': {'price': 11.99, 'quantity': '400g', 'icon': '🥜'},
    'sliced almonds': {'price': 12.49, 'quantity': '400g', 'icon': '🥜'},
    'walnut': {'price': 12.99, 'quantity': '400g', 'icon': '🥜'},
    'cashew': {'price': 13.99, 'quantity': '400g', 'icon': '🥜'},
    'roasted cashew': {'price': 14.49, 'quantity': '400g', 'icon': '🥜'},
    'peanut': {'price': 8.99, 'quantity': '500g', 'icon': '🥜'},
    'roasted peanuts': {'price': 9.49, 'quantity': '500g', 'icon': '🥜'},
    'pecan': {'price': 14.99, 'quantity': '400g', 'icon': '🥜'},
    'pistachio': {'price': 15.99, 'quantity': '400g', 'icon': '🥜'},
    'macadamia': {'price': 18.99, 'quantity': '300g', 'icon': '🥜'},
    'hazelnut': {'price': 13.99, 'quantity': '400g', 'icon': '🥜'},
    'brazil nut': {'price': 16.99, 'quantity': '400g', 'icon': '🥜'},
    'pine nut': {'price': 19.99, 'quantity': '300g', 'icon': '🥜'},
    'chestnut': {'price': 11.99, 'quantity': '500g', 'icon': '🌰'},
    'sunflower seeds': {'price': 6.99, 'quantity': '400g', 'icon': '🌻'},
    'pumpkin seeds': {'price': 7.99, 'quantity': '400g', 'icon': '🎃'},
    'chia seeds': {'price': 9.99, 'quantity': '300g', 'icon': '🌾'},
    'flax seeds': {'price': 8.99, 'quantity': '400g', 'icon': '🌾'},
    'hemp seeds': {'price': 12.99, 'quantity': '300g', 'icon': '🌾'},
    'peanut butter': {'price': 8.99, 'quantity': '500g', 'icon': '🥜'},
    'almond butter': {'price': 12.99, 'quantity': '400g', 'icon': '🥜'},
    'cashew butter': {'price': 13.99, 'quantity': '400g', 'icon': '🥜'},
    'tahini': {'price': 9.99, 'quantity': '400g', 'icon': '🥄'},
    'nutella': {'price': 7.99, 'quantity': '400g', 'icon': '🍫'},
    'mixed nuts': {'price': 14.99, 'quantity': '500g', 'icon': '🥜'},
    
    # ==================== LEGUMES & BEANS (20 items) ====================
    'lentils': {'price': 4.99, 'quantity': '500g', 'icon': '🫘'},
    'red lentils': {'price': 5.49, 'quantity': '500g', 'icon': '🫘'},
    'green lentils': {'price': 5.49, 'quantity': '500g', 'icon': '🫘'},
    'chickpeas': {'price': 3.99, 'quantity': '500g', 'icon': '🫘'},
    'black beans': {'price': 3.49, 'quantity': '500g', 'icon': '🫘'},
    'kidney beans': {'price': 3.99, 'quantity': '500g', 'icon': '🫘'},
    'pinto beans': {'price': 3.49, 'quantity': '500g', 'icon': '🫘'},
    'white beans': {'price': 3.99, 'quantity': '500g', 'icon': '🫘'},
    'navy beans': {'price': 3.99, 'quantity': '500g', 'icon': '🫘'},
    'cannellini beans': {'price': 4.49, 'quantity': '500g', 'icon': '🫘'},
    'lima beans': {'price': 4.49, 'quantity': '500g', 'icon': '🫘'},
    'soybeans': {'price': 4.49, 'quantity': '500g', 'icon': '🫘'},
    'edamame': {'price': 5.99, 'quantity': '400g', 'icon': '🫛'},
    'mung beans': {'price': 4.99, 'quantity': '500g', 'icon': '🫘'},
    'adzuki beans': {'price': 5.49, 'quantity': '500g', 'icon': '🫘'},
    'fava beans': {'price': 5.99, 'quantity': '500g', 'icon': '🫘'},
    'split peas': {'price': 3.99, 'quantity': '500g', 'icon': '🫛'},
    'tofu': {'price': 4.99, 'quantity': '400g', 'icon': '🥡'},
    'tempeh': {'price': 5.99, 'quantity': '400g', 'icon': '🥡'},
    'refried beans': {'price': 4.49, 'quantity': '400g', 'icon': '🫘'},
    
    # ==================== BAKING INGREDIENTS (40 items) ====================
    'all purpose flour': {'price': 4.99, 'quantity': '1 kg', 'icon': '🥄'},
    'bread flour': {'price': 5.49, 'quantity': '1 kg', 'icon': '🍞'},
    'cake flour': {'price': 5.99, 'quantity': '1 kg', 'icon': '🎂'},
    'whole wheat flour': {'price': 5.49, 'quantity': '1 kg', 'icon': '🌾'},
    'almond flour': {'price': 12.99, 'quantity': '500g', 'icon': '🥜'},
    'coconut flour': {'price': 9.99, 'quantity': '500g', 'icon': '🥥'},
    'rice flour': {'price': 6.99, 'quantity': '500g', 'icon': '🍚'},
    'cornstarch': {'price': 3.99, 'quantity': '500g', 'icon': '🌽'},
    'corn flour': {'price': 4.49, 'quantity': '500g', 'icon': '🌽'},
    'baking powder': {'price': 4.49, 'quantity': '200g', 'icon': '🥄'},
    'baking soda': {'price': 3.49, 'quantity': '200g', 'icon': '🥄'},
    'yeast': {'price': 5.99, 'quantity': '100g', 'icon': '🍞'},
    'active dry yeast': {'price': 6.49, 'quantity': '100g', 'icon': '🍞'},
    'instant yeast': {'price': 6.99, 'quantity': '100g', 'icon': '🍞'},
    'cocoa powder': {'price': 7.99, 'quantity': '300g', 'icon': '🍫'},
    'dark chocolate': {'price': 8.99, 'quantity': '400g', 'icon': '🍫'},
    'milk chocolate': {'price': 7.99, 'quantity': '400g', 'icon': '🍫'},
    'white chocolate': {'price': 8.49, 'quantity': '400g', 'icon': '🍫'},
    'chocolate chips': {'price': 6.99, 'quantity': '400g', 'icon': '🍫'},
    'dark chocolate chips': {'price': 7.49, 'quantity': '400g', 'icon': '🍫'},
    'white chocolate chips': {'price': 7.49, 'quantity': '400g', 'icon': '🍫'},
    'gelatin': {'price': 5.99, 'quantity': '100g', 'icon': '🥄'},
    'agar agar': {'price': 8.99, 'quantity': '100g', 'icon': '🥄'},
    'cream of tartar': {'price': 6.99, 'quantity': '100g', 'icon': '🥄'},
    'molasses': {'price': 6.99, 'quantity': '500ml', 'icon': '🍯'},
    'corn syrup': {'price': 5.99, 'quantity': '500ml', 'icon': '🌽'},
    'golden syrup': {'price': 7.99, 'quantity': '500ml', 'icon': '🍯'},
    'food coloring': {'price': 5.99, 'quantity': '4-pack', 'icon': '🎨'},
    'sprinkles': {'price': 4.99, 'quantity': '200g', 'icon': '🌈'},
    'rainbow sprinkles': {'price': 5.49, 'quantity': '200g', 'icon': '🌈'},
    'chocolate sprinkles': {'price': 5.49, 'quantity': '200g', 'icon': '🍫'},
    'parchment paper': {'price': 4.99, 'quantity': '30 sheets', 'icon': '📄'},
    'wax paper': {'price': 3.99, 'quantity': '30 sheets', 'icon': '📄'},
    'aluminum foil': {'price': 5.99, 'quantity': '1 roll', 'icon': '🥈'},
    'plastic wrap': {'price': 4.99, 'quantity': '1 roll', 'icon': '📦'},
    'muffin liners': {'price': 3.99, 'quantity': 'Pack of 100', 'icon': '🧁'},
    'cupcake liners': {'price': 4.49, 'quantity': 'Pack of 100', 'icon': '🧁'},
    'puff pastry': {'price': 6.99, 'quantity': '400g', 'icon': '🥐'},
    'phyllo dough': {'price': 7.99, 'quantity': '400g', 'icon': '🥐'},
    'pie crust': {'price': 5.99, 'quantity': '2 pieces', 'icon': '🥧'},
    
    # ==================== KITCHEN EQUIPMENT (50+ items) ====================
    'pressure cooker': {'price': 89.99, 'quantity': '5L', 'icon': '💨'},
    'rice cooker': {'price': 74.99, 'quantity': '1.8L', 'icon': '🍚'},
    'slow cooker': {'price': 79.99, 'quantity': '6L', 'icon': '⏲️'},
    'mixer grinder': {'price': 89.99, 'quantity': '750W', 'icon': '🌀'},
    'hand blender': {'price': 34.99, 'quantity': '400W', 'icon': '🌀'},
    'electric kettle': {'price': 34.99, 'quantity': '1.5L', 'icon': '☕'},
    'induction cooktop': {'price': 99.99, 'quantity': '1600W', 'icon': '🔥'},
    'gas stove': {'price': 299.99, 'quantity': '4-burner', 'icon': '🔥'},
    'deep fryer': {'price': 89.99, 'quantity': '6L', 'icon': '🍟'},
    'air fryer': {'price': 129.99, 'quantity': '5L', 'icon': '🌪️'},
    'toaster': {'price': 39.99, 'quantity': '4-slice', 'icon': '🍞'},
    'toaster oven': {'price': 89.99, 'quantity': '20L', 'icon': '🍞'},
    'sandwich maker': {'price': 34.99, 'quantity': '2-slice', 'icon': '🥪'},
    'waffle maker': {'price': 44.99, 'quantity': '1 unit', 'icon': '🧇'},
    'coffee maker': {'price': 79.99, 'quantity': '12-cup', 'icon': '☕'},
    'espresso machine': {'price': 299.99, 'quantity': '1 unit', 'icon': '☕'},
    'french press': {'price': 24.99, 'quantity': '1 liter', 'icon': '☕'},
    'tea kettle': {'price': 29.99, 'quantity': '2L', 'icon': '🫖'},
    'blender': {'price': 79.99, 'quantity': '2L', 'icon': '🌀'},
    'food processor': {'price': 149.99, 'quantity': '12-cup', 'icon': '🥕'},
    'stand mixer': {'price': 279.99, 'quantity': '5L', 'icon': '⚙️'},
    'hand mixer': {'price': 39.99, 'quantity': '300W', 'icon': '🌀'},
    'immersion blender': {'price': 44.99, 'quantity': '500W', 'icon': '🌀'},
    'knife set': {'price': 79.99, 'quantity': 'Set of 6', 'icon': '🔪'},
    'chef knife': {'price': 29.99, 'quantity': '8-inch', 'icon': '🔪'},
    'paring knife': {'price': 12.99, 'quantity': '4-inch', 'icon': '🔪'},
    'bread knife': {'price': 24.99, 'quantity': '10-inch', 'icon': '🔪'},
    'carving knife': {'price': 34.99, 'quantity': '10-inch', 'icon': '🔪'},
    'kitchen shears': {'price': 18.99, 'quantity': '1 unit', 'icon': '✂️'},
    'cutting board': {'price': 19.99, 'quantity': '1 unit', 'icon': '🪵'},
    'wooden cutting board': {'price': 24.99, 'quantity': '1 unit', 'icon': '🪵'},
    'bamboo cutting board': {'price': 22.99, 'quantity': '1 unit', 'icon': '🎋'},
    'plastic cutting board': {'price': 14.99, 'quantity': 'Set of 3', 'icon': '🟦'},
    'chopping board': {'price': 19.99, 'quantity': '1 unit', 'icon': '🪵'},
    'mixing bowl set': {'price': 24.99, 'quantity': 'Set of 5', 'icon': '🥣'},
    'glass mixing bowls': {'price': 29.99, 'quantity': 'Set of 5', 'icon': '🥣'},
    'stainless steel bowls': {'price': 34.99, 'quantity': 'Set of 5', 'icon': '🥣'},
    'measuring cups': {'price': 11.99, 'quantity': 'Set of 4', 'icon': '📏'},
    'measuring spoons': {'price': 7.99, 'quantity': 'Set of 6', 'icon': '🥄'},
    'liquid measuring cup': {'price': 9.99, 'quantity': '1L', 'icon': '📏'},
    'kitchen scale': {'price': 24.99, 'quantity': '1 unit', 'icon': '⚖️'},
    'digital thermometer': {'price': 19.99, 'quantity': '1 unit', 'icon': '🌡️'},
    'meat thermometer': {'price': 24.99, 'quantity': '1 unit', 'icon': '🌡️'},
    'candy thermometer': {'price': 16.99, 'quantity': '1 unit', 'icon': '🌡️'},
    'timer': {'price': 12.99, 'quantity': '1 unit', 'icon': '⏱️'},
    'colander': {'price': 16.99, 'quantity': '1 unit', 'icon': '🥣'},
    'strainer': {'price': 14.99, 'quantity': '1 unit', 'icon': '🥣'},
    'fine mesh strainer': {'price': 19.99, 'quantity': '1 unit', 'icon': '🥣'},
    'sieve': {'price': 13.99, 'quantity': '1 unit', 'icon': '🥣'},
    'salad spinner': {'price': 24.99, 'quantity': '1 unit', 'icon': '🥗'},
    'grater': {'price': 12.99, 'quantity': '1 unit', 'icon': '🧀'},
    'box grater': {'price': 16.99, 'quantity': '1 unit', 'icon': '🧀'},
    'microplane': {'price': 13.99, 'quantity': '1 unit', 'icon': '🧀'},
    'zester': {'price': 9.99, 'quantity': '1 unit', 'icon': '🍋'},
    'garlic press': {'price': 11.99, 'quantity': '1 unit', 'icon': '🧄'},
    'potato masher': {'price': 14.99, 'quantity': '1 unit', 'icon': '🥔'},
    'can opener': {'price': 12.99, 'quantity': '1 unit', 'icon': '🥫'},
    'bottle opener': {'price': 6.99, 'quantity': '1 unit', 'icon': '🍺'},
    'corkscrew': {'price': 14.99, 'quantity': '1 unit', 'icon': '🍷'},
    'whisk': {'price': 8.99, 'quantity': '1 unit', 'icon': '🥄'},
    'balloon whisk': {'price': 10.99, 'quantity': '1 unit', 'icon': '🥄'},
    'flat whisk': {'price': 9.99, 'quantity': '1 unit', 'icon': '🥄'},
    'wooden spoon': {'price': 5.99, 'quantity': '1 unit', 'icon': '🥄'},
    'slotted spoon': {'price': 6.99, 'quantity': '1 unit', 'icon': '🥄'},
    'ladle': {'price': 7.99, 'quantity': '1 unit', 'icon': '🥄'},
    'soup ladle': {'price': 9.99, 'quantity': '1 unit', 'icon': '🥄'},
    'spatula': {'price': 6.99, 'quantity': '1 unit', 'icon': '🥄'},
    'rubber spatula': {'price': 7.99, 'quantity': '1 unit', 'icon': '🥄'},
    'silicone spatula': {'price': 8.99, 'quantity': '1 unit', 'icon': '🥄'},
    'fish spatula': {'price': 9.99, 'quantity': '1 unit', 'icon': '🐟'},
    'offset spatula': {'price': 8.99, 'quantity': '1 unit', 'icon': '🥄'},
    'tongs': {'price': 9.99, 'quantity': '1 unit', 'icon': '🔧'},
    'kitchen tongs': {'price': 11.99, 'quantity': '1 unit', 'icon': '🔧'},
    'pasta fork': {'price': 6.99, 'quantity': '1 unit', 'icon': '🍝'},
    'serving spoon': {'price': 7.99, 'quantity': '1 unit', 'icon': '🥄'},
    'serving fork': {'price': 7.99, 'quantity': '1 unit', 'icon': '🍴'},
    'basting brush': {'price': 5.99, 'quantity': '1 unit', 'icon': '🖌️'},
    'pastry brush': {'price': 6.99, 'quantity': '1 unit', 'icon': '🖌️'},
    'rolling pin': {'price': 14.99, 'quantity': '1 unit', 'icon': '🥖'},
    'marble rolling pin': {'price': 24.99, 'quantity': '1 unit', 'icon': '🥖'},
    'french rolling pin': {'price': 19.99, 'quantity': '1 unit', 'icon': '🥖'},
    'pastry cutter': {'price': 8.99, 'quantity': '1 unit', 'icon': '🥐'},
    'dough scraper': {'price': 6.99, 'quantity': '1 unit', 'icon': '🥖'},
    'bench scraper': {'price': 9.99, 'quantity': '1 unit', 'icon': '🥖'},
    'cookie cutter set': {'price': 12.99, 'quantity': 'Set of 12', 'icon': '🍪'},
    'cookie scoop': {'price': 8.99, 'quantity': '1 unit', 'icon': '🍪'},
    'ice cream scoop': {'price': 9.99, 'quantity': '1 unit', 'icon': '🍨'},
    'melon baller': {'price': 7.99, 'quantity': '1 unit', 'icon': '🍈'},
    'apple corer': {'price': 8.99, 'quantity': '1 unit', 'icon': '🍎'},
    'pizza cutter': {'price': 8.99, 'quantity': '1 unit', 'icon': '🍕'},
    'pizza stone': {'price': 34.99, 'quantity': '1 unit', 'icon': '🍕'},
    'pizza peel': {'price': 29.99, 'quantity': '1 unit', 'icon': '🍕'},
    'baking sheet': {'price': 16.99, 'quantity': '1 unit', 'icon': '🍪'},
    'cookie sheet': {'price': 14.99, 'quantity': '1 unit', 'icon': '🍪'},
    'half sheet pan': {'price': 18.99, 'quantity': '1 unit', 'icon': '🍪'},
    'quarter sheet pan': {'price': 14.99, 'quantity': '1 unit', 'icon': '🍪'},
    'jelly roll pan': {'price': 16.99, 'quantity': '1 unit', 'icon': '🍰'},
    'muffin tin': {'price': 18.99, 'quantity': '12-cup', 'icon': '🧁'},
    'mini muffin tin': {'price': 16.99, 'quantity': '24-cup', 'icon': '🧁'},
    'cake pan': {'price': 19.99, 'quantity': '9-inch', 'icon': '🎂'},
    'round cake pan': {'price': 16.99, 'quantity': '9-inch', 'icon': '🎂'},
    'square cake pan': {'price': 17.99, 'quantity': '9-inch', 'icon': '🎂'},
    'springform pan': {'price': 22.99, 'quantity': '9-inch', 'icon': '🎂'},
    'bundt pan': {'price': 24.99, 'quantity': '10-inch', 'icon': '🎂'},
    'loaf pan': {'price': 14.99, 'quantity': '9x5-inch', 'icon': '🍞'},
    'pie dish': {'price': 16.99, 'quantity': '9-inch', 'icon': '🥧'},
    'tart pan': {'price': 19.99, 'quantity': '9-inch', 'icon': '🥧'},
    'casserole dish': {'price': 29.99, 'quantity': '9x13-inch', 'icon': '🥘'},
    'baking dish': {'price': 24.99, 'quantity': '9x13-inch', 'icon': '🥘'},
    'roasting pan': {'price': 39.99, 'quantity': 'Large', 'icon': '🍗'},
    'dutch oven': {'price': 129.99, 'quantity': '6L', 'icon': '🍲'},
    'stockpot': {'price': 59.99, 'quantity': '12L', 'icon': '🍲'},
    'saucepan': {'price': 39.99, 'quantity': '2L', 'icon': '🍳'},
    'small saucepan': {'price': 29.99, 'quantity': '1L', 'icon': '🍳'},
    'large saucepan': {'price': 49.99, 'quantity': '4L', 'icon': '🍳'},
    'frying pan': {'price': 42.99, 'quantity': '10-inch', 'icon': '🍳'},
    'skillet': {'price': 44.99, 'quantity': '12-inch', 'icon': '🥘'},
    'non stick pan': {'price': 49.99, 'quantity': '10-inch', 'icon': '🍳'},
    'cast iron skillet': {'price': 54.99, 'quantity': '12-inch', 'icon': '🥘'},
    'wok': {'price': 49.99, 'quantity': '14-inch', 'icon': '🍜'},
    'carbon steel wok': {'price': 59.99, 'quantity': '14-inch', 'icon': '🍜'},
    'grill pan': {'price': 52.99, 'quantity': '11-inch', 'icon': '🍖'},
    'griddle': {'price': 44.99, 'quantity': '1 unit', 'icon': '🥞'},
    'crepe pan': {'price': 34.99, 'quantity': '10-inch', 'icon': '🥞'},
    'paella pan': {'price': 39.99, 'quantity': '15-inch', 'icon': '🥘'},
    'saute pan': {'price': 49.99, 'quantity': '12-inch', 'icon': '🥘'},
    'pot set': {'price': 149.99, 'quantity': 'Set of 10', 'icon': '🍲'},
    'cookware set': {'price': 199.99, 'quantity': 'Set of 12', 'icon': '🍳'},
    'storage containers': {'price': 24.99, 'quantity': 'Set of 10', 'icon': '🥫'},
    'glass containers': {'price': 34.99, 'quantity': 'Set of 10', 'icon': '🥫'},
    'plastic containers': {'price': 19.99, 'quantity': 'Set of 12', 'icon': '🥫'},
    'mason jars': {'price': 19.99, 'quantity': 'Set of 12', 'icon': '🫙'},
    'spice jars': {'price': 24.99, 'quantity': 'Set of 24', 'icon': '🧂'},
    'bread box': {'price': 34.99, 'quantity': '1 unit', 'icon': '🍞'},
    'cookie jar': {'price': 24.99, 'quantity': '1 unit', 'icon': '🍪'},
    'refrigerator': {'price': 799.99, 'quantity': '300L', 'icon': '🧊'},
    'microwave oven': {'price': 199.99, 'quantity': '25L', 'icon': '📟'},
    'oven': {'price': 599.99, 'quantity': '60L', 'icon': '🔥'},
    'convection oven': {'price': 399.99, 'quantity': '45L', 'icon': '🌡️'},
    'dishwasher': {'price': 699.99, 'quantity': '12-place', 'icon': '🧼'},
    'dish rack': {'price': 24.99, 'quantity': '1 unit', 'icon': '🧼'},
    'dish drainer': {'price': 19.99, 'quantity': '1 unit', 'icon': '🧼'},
    'soap dispenser': {'price': 14.99, 'quantity': '1 unit', 'icon': '🧴'},
    'sponge holder': {'price': 8.99, 'quantity': '1 unit', 'icon': '🧽'},
    'trash bin': {'price': 29.99, 'quantity': '50L', 'icon': '🗑️'},
    'compost bin': {'price': 39.99, 'quantity': '10L', 'icon': '🗑️'},
    'paper towel holder': {'price': 14.99, 'quantity': '1 unit', 'icon': '🧻'},
    'utensil holder': {'price': 16.99, 'quantity': '1 unit', 'icon': '🥄'},
    'knife block': {'price': 34.99, 'quantity': '1 unit', 'icon': '🔪'},
    'spice rack': {'price': 29.99, 'quantity': '1 unit', 'icon': '🧂'},
    'pot rack': {'price': 79.99, 'quantity': '1 unit', 'icon': '🍲'},
    'apron': {'price': 19.99, 'quantity': '1 unit', 'icon': '👕'},
    'oven mitts': {'price': 14.99, 'quantity': 'Set of 2', 'icon': '🧤'},
    'pot holders': {'price': 12.99, 'quantity': 'Set of 4', 'icon': '🧤'},
    'dish towels': {'price': 16.99, 'quantity': 'Set of 6', 'icon': '🧻'},
    'kitchen towels': {'price': 19.99, 'quantity': 'Set of 6', 'icon': '🧻'},
}




# ==================== NUTRITION DATABASE (100 Items) ====================
NUTRITION_DB_100 = {
    'chicken breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'sodium': 74, 'calcium': 11, 'iron': 0.9, 'vitamin_a': 13, 'vitamin_c': 0},
    'chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'sodium': 74, 'calcium': 11, 'iron': 0.9, 'vitamin_a': 13, 'vitamin_c': 0},
    'ground beef': {'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 15, 'fiber': 0, 'sodium': 72, 'calcium': 18, 'iron': 2.6, 'vitamin_a': 0, 'vitamin_c': 0},
    'salmon': {'calories': 208, 'protein': 20, 'carbs': 0, 'fat': 13, 'fiber': 0, 'sodium': 59, 'calcium': 9, 'iron': 0.3, 'vitamin_a': 40, 'vitamin_c': 0},
    'egg': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'fiber': 0, 'sodium': 124, 'calcium': 56, 'iron': 1.8, 'vitamin_a': 540, 'vitamin_c': 0},
    'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'fiber': 0.4, 'sodium': 1, 'calcium': 10, 'iron': 0.2, 'vitamin_a': 0, 'vitamin_c': 0},
    'pasta': {'calories': 131, 'protein': 5, 'carbs': 25, 'fat': 1.1, 'fiber': 1.8, 'sodium': 6, 'calcium': 7, 'iron': 0.5, 'vitamin_a': 0, 'vitamin_c': 0},
    'potato': {'calories': 77, 'protein': 2, 'carbs': 17, 'fat': 0.1, 'fiber': 2.1, 'sodium': 6, 'calcium': 12, 'iron': 0.8, 'vitamin_a': 2, 'vitamin_c': 19.7},
    'tomato': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'fiber': 1.2, 'sodium': 5, 'calcium': 10, 'iron': 0.3, 'vitamin_a': 833, 'vitamin_c': 13.7},
    'onion': {'calories': 40, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.1, 'fiber': 1.7, 'sodium': 4, 'calcium': 23, 'iron': 0.2, 'vitamin_a': 2, 'vitamin_c': 7.4},
    'nuts': {'calories': 607, 'protein': 20, 'carbs': 21, 'fat': 54, 'fiber': 9, 'sodium': 5, 'calcium': 114, 'iron': 2.9, 'vitamin_a': 1, 'vitamin_c': 0},
    'almonds': {'calories': 579, 'protein': 21, 'carbs': 22, 'fat': 50, 'fiber': 12.5, 'sodium': 1, 'calcium': 269, 'iron': 3.7, 'vitamin_a': 1, 'vitamin_c': 0},
    'walnuts': {'calories': 654, 'protein': 15, 'carbs': 14, 'fat': 65, 'fiber': 6.7, 'sodium': 2, 'calcium': 98, 'iron': 2.9, 'vitamin_a': 20, 'vitamin_c': 1.3},
    'cashews': {'calories': 553, 'protein': 18, 'carbs': 30, 'fat': 44, 'fiber': 3.3, 'sodium': 12, 'calcium': 37, 'iron': 6.7, 'vitamin_a': 0, 'vitamin_c': 0.5},
    'broccoli': {'calories': 34, 'protein': 2.8, 'carbs': 7, 'fat': 0.4, 'fiber': 2.6, 'sodium': 33, 'calcium': 47, 'iron': 0.7, 'vitamin_a': 623, 'vitamin_c': 89.2},
    'carrot': {'calories': 41, 'protein': 0.9, 'carbs': 10, 'fat': 0.2, 'fiber': 2.8, 'sodium': 69, 'calcium': 33, 'iron': 0.3, 'vitamin_a': 16706, 'vitamin_c': 5.9},
    'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2, 'sodium': 79, 'calcium': 99, 'iron': 2.7, 'vitamin_a': 9377, 'vitamin_c': 28.1},
    'peas': {'calories': 81, 'protein': 5, 'carbs': 14, 'fat': 0.4, 'fiber': 5, 'sodium': 5, 'calcium': 25, 'iron': 1.5, 'vitamin_a': 765, 'vitamin_c': 40},
    'corn': {'calories': 86, 'protein': 3.2, 'carbs': 19, 'fat': 1.2, 'fiber': 2.7, 'sodium': 15, 'calcium': 2, 'iron': 0.5, 'vitamin_a': 187, 'vitamin_c': 6.8},
    'beetroot': {'calories': 43, 'protein': 1.6, 'carbs': 10, 'fat': 0.2, 'fiber': 2.8, 'sodium': 78, 'calcium': 16, 'iron': 0.8, 'vitamin_a': 33, 'vitamin_c': 4.9},
    'cauliflower': {'calories': 25, 'protein': 1.9, 'carbs': 5, 'fat': 0.3, 'fiber': 2, 'sodium': 30, 'calcium': 22, 'iron': 0.4, 'vitamin_a': 13, 'vitamin_c': 48.2},
    'cabbage': {'calories': 25, 'protein': 1.3, 'carbs': 6, 'fat': 0.1, 'fiber': 2.5, 'sodium': 18, 'calcium': 40, 'iron': 0.5, 'vitamin_a': 98, 'vitamin_c': 36.6},
    'brinjal': {'calories': 25, 'protein': 1, 'carbs': 6, 'fat': 0.2, 'fiber': 3, 'sodium': 2, 'calcium': 9, 'iron': 0.2, 'vitamin_a': 23, 'vitamin_c': 2.2},
    'okra': {'calories': 33, 'protein': 1.9, 'carbs': 7.5, 'fat': 0.2, 'fiber': 3.2, 'sodium': 7, 'calcium': 82, 'iron': 0.6, 'vitamin_a': 716, 'vitamin_c': 23},
    'bottle gourd': {'calories': 14, 'protein': 0.6, 'carbs': 3.4, 'fat': 0.1, 'fiber': 0.5, 'sodium': 2, 'calcium': 26, 'iron': 0.2, 'vitamin_a': 16, 'vitamin_c': 10.1},
    'pumpkin': {'calories': 26, 'protein': 1, 'carbs': 6.5, 'fat': 0.1, 'fiber': 0.5, 'sodium': 1, 'calcium': 21, 'iron': 0.8, 'vitamin_a': 8513, 'vitamin_c': 9},
    'mushroom': {'calories': 22, 'protein': 3.1, 'carbs': 3.3, 'fat': 0.3, 'fiber': 1, 'sodium': 5, 'calcium': 3, 'iron': 0.5, 'vitamin_a': 2, 'vitamin_c': 2.1},
    'paneer': {'calories': 265, 'protein': 18, 'carbs': 1.2, 'fat': 21, 'fiber': 0, 'sodium': 22, 'calcium': 208, 'iron': 0.7, 'vitamin_a': 210, 'vitamin_c': 0},
    'tofu': {'calories': 76, 'protein': 8, 'carbs': 1.9, 'fat': 4.8, 'fiber': 0.3, 'sodium': 7, 'calcium': 350, 'iron': 5.4, 'vitamin_a': 85, 'vitamin_c': 0},
    'cheese': {'calories': 402, 'protein': 25, 'carbs': 1.3, 'fat': 33, 'fiber': 0, 'sodium': 621, 'calcium': 721, 'iron': 0.7, 'vitamin_a': 1080, 'vitamin_c': 0},
    'butter': {'calories': 717, 'protein': 0.9, 'carbs': 0.1, 'fat': 81, 'fiber': 0, 'sodium': 11, 'calcium': 24, 'iron': 0.1, 'vitamin_a': 2499, 'vitamin_c': 0},
    'yogurt': {'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'fiber': 0, 'sodium': 36, 'calcium': 110, 'iron': 0, 'vitamin_a': 27, 'vitamin_c': 1},
    'milk': {'calories': 42, 'protein': 3.4, 'carbs': 5, 'fat': 1, 'fiber': 0, 'sodium': 44, 'calcium': 125, 'iron': 0, 'vitamin_a': 162, 'vitamin_c': 0},
    'lentils': {'calories': 116, 'protein': 9, 'carbs': 20, 'fat': 0.4, 'fiber': 8, 'sodium': 2, 'calcium': 19, 'iron': 3.3, 'vitamin_a': 8, 'vitamin_c': 1.5},
    'moong dal': {'calories': 347, 'protein': 24, 'carbs': 63, 'fat': 1.2, 'fiber': 16, 'sodium': 15, 'calcium': 132, 'iron': 6.7, 'vitamin_a': 50, 'vitamin_c': 0},
    'chickpeas': {'calories': 164, 'protein': 9, 'carbs': 27, 'fat': 2.6, 'fiber': 8, 'sodium': 24, 'calcium': 49, 'iron': 2.9, 'vitamin_a': 27, 'vitamin_c': 1.3},
    'kidney beans': {'calories': 333, 'protein': 24, 'carbs': 60, 'fat': 0.8, 'fiber': 25, 'sodium': 24, 'calcium': 143, 'iron': 8.2, 'vitamin_a': 0, 'vitamin_c': 4.5},
    'black beans': {'calories': 341, 'protein': 21, 'carbs': 63, 'fat': 1.4, 'fiber': 16.6, 'sodium': 5, 'calcium': 123, 'iron': 5, 'vitamin_a': 17, 'vitamin_c': 0},
    'soybeans': {'calories': 446, 'protein': 36, 'carbs': 30, 'fat': 20, 'fiber': 9.3, 'sodium': 2, 'calcium': 277, 'iron': 15.7, 'vitamin_a': 22, 'vitamin_c': 6},
    'oats': {'calories': 389, 'protein': 17, 'carbs': 66, 'fat': 7, 'fiber': 10.6, 'sodium': 2, 'calcium': 54, 'iron': 4.7, 'vitamin_a': 0, 'vitamin_c': 0},
    'quinoa': {'calories': 120, 'protein': 4.1, 'carbs': 21, 'fat': 1.9, 'fiber': 2.8, 'sodium': 7, 'calcium': 17, 'iron': 1.5, 'vitamin_a': 14, 'vitamin_c': 0},
    'broccoli': {'calories': 34, 'protein': 2.8, 'carbs': 6.6, 'fat': 0.4, 'fiber': 2.6, 'sodium': 33, 'calcium': 47, 'iron': 0.7, 'vitamin_a': 623, 'vitamin_c': 89.2},
    'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2, 'sodium': 79, 'calcium': 99, 'iron': 2.7, 'vitamin_a': 9377, 'vitamin_c': 28.1},
    'carrot': {'calories': 41, 'protein': 0.9, 'carbs': 9.6, 'fat': 0.2, 'fiber': 2.8, 'sodium': 69, 'calcium': 33, 'iron': 0.3, 'vitamin_a': 16706, 'vitamin_c': 5.9},
    'cucumber': {'calories': 16, 'protein': 0.7, 'carbs': 3.6, 'fat': 0.1, 'fiber': 0.5, 'sodium': 2, 'calcium': 16, 'iron': 0.3, 'vitamin_a': 105, 'vitamin_c': 2.8},
    'bell pepper': {'calories': 31, 'protein': 1, 'carbs': 6, 'fat': 0.3, 'fiber': 2.1, 'sodium': 4, 'calcium': 10, 'iron': 0.4, 'vitamin_a': 157, 'vitamin_c': 127.7},
    'mushroom': {'calories': 22, 'protein': 3.1, 'carbs': 3.3, 'fat': 0.3, 'fiber': 1, 'sodium': 5, 'calcium': 3, 'iron': 0.5, 'vitamin_a': 0, 'vitamin_c': 2.1},
    'lettuce': {'calories': 15, 'protein': 1.4, 'carbs': 2.9, 'fat': 0.2, 'fiber': 1.3, 'sodium': 28, 'calcium': 36, 'iron': 0.9, 'vitamin_a': 7405, 'vitamin_c': 9.2},
    'kale': {'calories': 49, 'protein': 4.3, 'carbs': 8.8, 'fat': 0.9, 'fiber': 3.6, 'sodium': 38, 'calcium': 150, 'iron': 1.5, 'vitamin_a': 9990, 'vitamin_c': 120},
    'cauliflower': {'calories': 25, 'protein': 1.9, 'carbs': 5, 'fat': 0.3, 'fiber': 2, 'sodium': 30, 'calcium': 22, 'iron': 0.4, 'vitamin_a': 0, 'vitamin_c': 48.2},
    'peas': {'calories': 81, 'protein': 5.4, 'carbs': 14.5, 'fat': 0.4, 'fiber': 5.1, 'sodium': 5, 'calcium': 25, 'iron': 1.5, 'vitamin_a': 765, 'vitamin_c': 40},
    'corn': {'calories': 86, 'protein': 3.2, 'carbs': 19, 'fat': 1.2, 'fiber': 2.7, 'sodium': 15, 'calcium': 2, 'iron': 0.5, 'vitamin_a': 187, 'vitamin_c': 6.8},
    'zucchini': {'calories': 17, 'protein': 1.2, 'carbs': 3.1, 'fat': 0.3, 'fiber': 1, 'sodium': 8, 'calcium': 16, 'iron': 0.4, 'vitamin_a': 200, 'vitamin_c': 17.9},
    'sweet potato': {'calories': 86, 'protein': 1.6, 'carbs': 20.1, 'fat': 0.1, 'fiber': 3, 'sodium': 55, 'calcium': 30, 'iron': 0.6, 'vitamin_a': 14187, 'vitamin_c': 2.4},
    'eggplant': {'calories': 25, 'protein': 1, 'carbs': 6, 'fat': 0.2, 'fiber': 3, 'sodium': 2, 'calcium': 9, 'iron': 0.2, 'vitamin_a': 23, 'vitamin_c': 2.2},
    'beetroot': {'calories': 43, 'protein': 1.6, 'carbs': 10, 'fat': 0.2, 'fiber': 2.8, 'sodium': 78, 'calcium': 16, 'iron': 0.8, 'vitamin_a': 33, 'vitamin_c': 4.9},
    'pumpkin': {'calories': 26, 'protein': 1, 'carbs': 6.5, 'fat': 0.1, 'fiber': 0.5, 'sodium': 1, 'calcium': 21, 'iron': 0.8, 'vitamin_a': 8513, 'vitamin_c': 9},
    'green beans': {'calories': 31, 'protein': 1.8, 'carbs': 7, 'fat': 0.1, 'fiber': 3.4, 'sodium': 6, 'calcium': 37, 'iron': 1, 'vitamin_a': 690, 'vitamin_c': 12.2},
    'asparagus': {'calories': 20, 'protein': 2.2, 'carbs': 3.9, 'fat': 0.1, 'fiber': 2.1, 'sodium': 2, 'calcium': 24, 'iron': 2.1, 'vitamin_a': 756, 'vitamin_c': 5.6},
    'okra': {'calories': 33, 'protein': 1.9, 'carbs': 7.5, 'fat': 0.2, 'fiber': 3.2, 'sodium': 7, 'calcium': 82, 'iron': 0.6, 'vitamin_a': 375, 'vitamin_c': 23},
    'cabbage': {'calories': 25, 'protein': 1.3, 'carbs': 5.8, 'fat': 0.1, 'fiber': 2.5, 'sodium': 18, 'calcium': 40, 'iron': 0.5, 'vitamin_a': 98, 'vitamin_c': 36.6},
    'celery': {'calories': 16, 'protein': 0.7, 'carbs': 3, 'fat': 0.2, 'fiber': 1.6, 'sodium': 80, 'calcium': 40, 'iron': 0.2, 'vitamin_a': 449, 'vitamin_c': 3.1},
    'garlic': {'calories': 149, 'protein': 6.4, 'carbs': 33, 'fat': 0.5, 'fiber': 2.1, 'sodium': 17, 'calcium': 181, 'iron': 1.7, 'vitamin_a': 9, 'vitamin_c': 31.2},
    'ginger': {'calories': 80, 'protein': 1.8, 'carbs': 18, 'fat': 0.8, 'fiber': 2, 'sodium': 13, 'calcium': 16, 'iron': 0.6, 'vitamin_a': 0, 'vitamin_c': 5},
    'avocado': {'calories': 160, 'protein': 2, 'carbs': 9, 'fat': 15, 'fiber': 7, 'sodium': 7, 'calcium': 12, 'iron': 0.6, 'vitamin_a': 146, 'vitamin_c': 10},
    'banana': {'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'fiber': 2.6, 'sodium': 1, 'calcium': 5, 'iron': 0.3, 'vitamin_a': 64, 'vitamin_c': 8.7},
    'apple': {'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2, 'fiber': 2.4, 'sodium': 1, 'calcium': 6, 'iron': 0.1, 'vitamin_a': 54, 'vitamin_c': 4.6},
    'orange': {'calories': 47, 'protein': 0.9, 'carbs': 12, 'fat': 0.1, 'fiber': 2.4, 'sodium': 0, 'calcium': 40, 'iron': 0.1, 'vitamin_a': 225, 'vitamin_c': 53.2},
    'strawberry': {'calories': 32, 'protein': 0.7, 'carbs': 7.7, 'fat': 0.3, 'fiber': 2, 'sodium': 1, 'calcium': 16, 'iron': 0.4, 'vitamin_a': 12, 'vitamin_c': 58.8},
    'blueberry': {'calories': 57, 'protein': 0.7, 'carbs': 14.5, 'fat': 0.3, 'fiber': 2.4, 'sodium': 1, 'calcium': 6, 'iron': 0.3, 'vitamin_a': 54, 'vitamin_c': 9.7},
    'grapes': {'calories': 69, 'protein': 0.7, 'carbs': 18, 'fat': 0.2, 'fiber': 0.9, 'sodium': 2, 'calcium': 10, 'iron': 0.4, 'vitamin_a': 66, 'vitamin_c': 10.8},
    'mango': {'calories': 60, 'protein': 0.8, 'carbs': 15, 'fat': 0.4, 'fiber': 1.6, 'sodium': 1, 'calcium': 11, 'iron': 0.2, 'vitamin_a': 1082, 'vitamin_c': 36.4},
    'pineapple': {'calories': 50, 'protein': 0.5, 'carbs': 13, 'fat': 0.1, 'fiber': 1.4, 'sodium': 1, 'calcium': 13, 'iron': 0.3, 'vitamin_a': 58, 'vitamin_c': 47.8},
    'papaya': {'calories': 43, 'protein': 0.5, 'carbs': 11, 'fat': 0.3, 'fiber': 1.7, 'sodium': 8, 'calcium': 20, 'iron': 0.3, 'vitamin_a': 950, 'vitamin_c': 60.9},
    'watermelon': {'calories': 30, 'protein': 0.6, 'carbs': 8, 'fat': 0.2, 'fiber': 0.4, 'sodium': 1, 'calcium': 7, 'iron': 0.2, 'vitamin_a': 569, 'vitamin_c': 8.1},
    'pear': {'calories': 57, 'protein': 0.4, 'carbs': 15, 'fat': 0.1, 'fiber': 3.1, 'sodium': 1, 'calcium': 9, 'iron': 0.2, 'vitamin_a': 25, 'vitamin_c': 4.3},
    'pomegranate': {'calories': 83, 'protein': 1.7, 'carbs': 19, 'fat': 1.2, 'fiber': 4, 'sodium': 3, 'calcium': 10, 'iron': 0.3, 'vitamin_a': 0, 'vitamin_c': 10.2},
    'kiwi': {'calories': 41, 'protein': 1.1, 'carbs': 10, 'fat': 0.5, 'fiber': 2.1, 'sodium': 3, 'calcium': 34, 'iron': 0.3, 'vitamin_a': 87, 'vitamin_c': 92.7},
    'chickpeas': {'calories': 164, 'protein': 9, 'carbs': 27, 'fat': 2.6, 'fiber': 7.6, 'sodium': 24, 'calcium': 49, 'iron': 2.9, 'vitamin_a': 67, 'vitamin_c': 1.3},
    'kidney beans': {'calories': 127, 'protein': 8.7, 'carbs': 22.8, 'fat': 0.5, 'fiber': 6.4, 'sodium': 2, 'calcium': 28, 'iron': 2.9, 'vitamin_a': 0, 'vitamin_c': 4.5},
    'black beans': {'calories': 132, 'protein': 8.9, 'carbs': 23.7, 'fat': 0.5, 'fiber': 8.7, 'sodium': 1, 'calcium': 27, 'iron': 2.1, 'vitamin_a': 0, 'vitamin_c': 0},
    'lentils': {'calories': 116, 'protein': 9, 'carbs': 20, 'fat': 0.4, 'fiber': 8, 'sodium': 2, 'calcium': 19, 'iron': 3.3, 'vitamin_a': 8, 'vitamin_c': 1.5},
    'tofu': {'calories': 76, 'protein': 8, 'carbs': 1.9, 'fat': 4.8, 'fiber': 0.3, 'sodium': 7, 'calcium': 350, 'iron': 5.4, 'vitamin_a': 85, 'vitamin_c': 0.1},
    'paneer': {'calories': 265, 'protein': 18.3, 'carbs': 1.2, 'fat': 21.6, 'fiber': 0, 'sodium': 22, 'calcium': 208, 'iron': 0.2, 'vitamin_a': 210, 'vitamin_c': 0},
    'almonds': {'calories': 579, 'protein': 21.2, 'carbs': 21.6, 'fat': 49.9, 'fiber': 12.5, 'sodium': 1, 'calcium': 269, 'iron': 3.7, 'vitamin_a': 1, 'vitamin_c': 0},
    'cashews': {'calories': 553, 'protein': 18.2, 'carbs': 30.2, 'fat': 43.8, 'fiber': 3.3, 'sodium': 12, 'calcium': 37, 'iron': 6.7, 'vitamin_a': 0, 'vitamin_c': 0.5},
    'walnuts': {'calories': 654, 'protein': 15.2, 'carbs': 13.7, 'fat': 65.2, 'fiber': 6.7, 'sodium': 2, 'calcium': 98, 'iron': 2.9, 'vitamin_a': 20, 'vitamin_c': 1.3},
    'peanuts': {'calories': 567, 'protein': 25.8, 'carbs': 16.1, 'fat': 49.2, 'fiber': 8.5, 'sodium': 18, 'calcium': 92, 'iron': 4.6, 'vitamin_a': 0, 'vitamin_c': 0},
    'soybeans': {'calories': 446, 'protein': 36.5, 'carbs': 30.2, 'fat': 20, 'fiber': 9.3, 'sodium': 2, 'calcium': 277, 'iron': 15.7, 'vitamin_a': 22, 'vitamin_c': 6},
    'oats': {'calories': 389, 'protein': 16.9, 'carbs': 66.3, 'fat': 6.9, 'fiber': 10.6, 'sodium': 2, 'calcium': 54},
    'wheat flour': {'calories': 364, 'protein': 10.3, 'carbs': 76, 'fat': 1, 'fiber': 2.7, 'sodium': 2, 'calcium': 15, 'iron': 1.2, 'vitamin_a': 0, 'vitamin_c': 0},
    'bread': {'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3.2, 'fiber': 2.7, 'sodium': 491, 'calcium': 144, 'iron': 4.9, 'vitamin_a': 0, 'vitamin_c': 0},
    'milk': {'calories': 42, 'protein': 3.4, 'carbs': 5, 'fat': 1, 'fiber': 0, 'sodium': 44, 'calcium': 125, 'iron': 0, 'vitamin_a': 47, 'vitamin_c': 0},
    'yogurt': {'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'fiber': 0, 'sodium': 36, 'calcium': 110, 'iron': 0.1, 'vitamin_a': 27, 'vitamin_c': 0.8},

    # 🍹 DRINKS
    'orange juice': {'calories': 45, 'carbs': 10.4, 'sugar': 8.4, 'vitamin_c': 50, 'protein': 0.7, 'fat': 0.2, 'sodium': 1, 'calcium': 11, 'iron': 0.2},
    'apple juice': {'calories': 46, 'carbs': 11.3, 'sugar': 9.6, 'vitamin_c': 0.9, 'protein': 0.1, 'fat': 0.1, 'sodium': 4, 'calcium': 8, 'iron': 0.2},
    'grape juice': {'calories': 60, 'carbs': 14.8, 'sugar': 13.9, 'vitamin_c': 25, 'protein': 0.4, 'fat': 0.1, 'sodium': 2, 'calcium': 10, 'iron': 0.3},
    'pineapple juice': {'calories': 53, 'carbs': 13, 'sugar': 10, 'vitamin_c': 47.8, 'protein': 0.4, 'fat': 0.1, 'sodium': 2, 'calcium': 13, 'iron': 0.3},
    'mango juice': {'calories': 57, 'carbs': 14, 'sugar': 13, 'vitamin_c': 36, 'protein': 0.4, 'fat': 0.2, 'sodium': 1, 'calcium': 10, 'iron': 0.1},
    'lemon juice': {'calories': 22, 'carbs': 6.9, 'sugar': 2.5, 'vitamin_c': 38.7, 'protein': 0.4, 'fat': 0.2, 'sodium': 1, 'calcium': 6, 'iron': 0.1},
    'tomato juice': {'calories': 17, 'carbs': 3.5, 'sugar': 2.6, 'vitamin_c': 70.1, 'protein': 0.9, 'fat': 0.2, 'sodium': 10, 'calcium': 10, 'iron': 0.4},
    'carrot juice': {'calories': 39, 'carbs': 9.3, 'sugar': 3.9, 'vitamin_c': 8.5, 'protein': 0.6, 'fat': 0.2, 'sodium': 66, 'calcium': 24, 'iron': 0.3},
    'watermelon juice': {'calories': 30, 'carbs': 8, 'sugar': 6.2, 'vitamin_c': 8.1, 'protein': 0.6, 'fat': 0.1, 'sodium': 1, 'calcium': 7, 'iron': 0.2},
    'coconut water': {'calories': 19, 'carbs': 3.7, 'sugar': 2.6, 'vitamin_c': 2.4, 'protein': 0.7, 'fat': 0.2, 'sodium': 105, 'calcium': 24, 'iron': 0.3},
    'pomegranate juice': {'calories': 54, 'carbs': 13, 'sugar': 12, 'vitamin_c': 10.2, 'protein': 0.2, 'fat': 0.1, 'sodium': 3, 'calcium': 11, 'iron': 0.3},
    'cranberry juice': {'calories': 46, 'carbs': 12.2, 'sugar': 11, 'vitamin_c': 9.3, 'protein': 0.4, 'fat': 0.1, 'sodium': 2, 'calcium': 8, 'iron': 0.2},
    'beetroot juice': {'calories': 43, 'carbs': 10, 'sugar': 8, 'vitamin_c': 4.9, 'protein': 1.6, 'fat': 0.2, 'sodium': 78, 'calcium': 16, 'iron': 0.8},
    'guava juice': {'calories': 63, 'carbs': 16, 'sugar': 14, 'vitamin_c': 125, 'protein': 0.9, 'fat': 0.4, 'sodium': 4, 'calcium': 12, 'iron': 0.3},
    'papaya juice': {'calories': 40, 'carbs': 10, 'sugar': 7, 'vitamin_c': 60, 'protein': 0.5, 'fat': 0.1, 'sodium': 2, 'calcium': 15, 'iron': 0.2},
    'strawberry shake': {'calories': 95, 'carbs': 15, 'sugar': 13, 'vitamin_c': 40, 'protein': 2.9, 'fat': 2.2, 'sodium': 30, 'calcium': 100, 'iron': 0.3},
    'banana shake': {'calories': 120, 'carbs': 27, 'sugar': 22, 'vitamin_c': 6, 'protein': 4, 'fat': 1.5, 'sodium': 45, 'calcium': 150, 'iron': 0.2},
    'coffee': {'calories': 2, 'carbs': 0, 'sugar': 0, 'vitamin_c': 0, 'protein': 0.3, 'fat': 0, 'sodium': 5, 'calcium': 4, 'iron': 0.1},
    'tea': {'calories': 1, 'carbs': 0.2, 'sugar': 0, 'vitamin_c': 0, 'protein': 0, 'fat': 0, 'sodium': 3, 'calcium': 3, 'iron': 0.1},
    'milkshake': {'calories': 210, 'carbs': 28, 'sugar': 25, 'vitamin_c': 2, 'protein': 6, 'fat': 8, 'sodium': 120, 'calcium': 200, 'iron': 0.2},
    'energy drink': {'calories': 45, 'carbs': 11, 'sugar': 10, 'vitamin_c': 8, 'protein': 0, 'fat': 0, 'sodium': 105, 'calcium': 5, 'iron': 0.1},
    'protein shake': {'calories': 180, 'carbs': 8, 'sugar': 2, 'vitamin_c': 4, 'protein': 30, 'fat': 2, 'sodium': 150, 'calcium': 120, 'iron': 0.8},
    'hot chocolate': {'calories': 190, 'carbs': 25, 'sugar': 23, 'vitamin_c': 1, 'protein': 8, 'fat': 6, 'sodium': 120, 'calcium': 200, 'iron': 1},
    'soy milk': {'calories': 54, 'carbs': 6.3, 'sugar': 3, 'vitamin_c': 0.9, 'protein': 3.3, 'fat': 1.8, 'sodium': 51, 'calcium': 25, 'iron': 0.6},
    'almond milk': {'calories': 15, 'carbs': 0.6, 'sugar': 0.2, 'vitamin_c': 0, 'protein': 0.6, 'fat': 1.2, 'sodium': 65, 'calcium': 17, 'iron': 0.1},
    'buttermilk': {'calories': 40, 'carbs': 4.8, 'sugar': 4.8, 'vitamin_c': 1, 'protein': 3.3, 'fat': 1, 'sodium': 105, 'calcium': 116, 'iron': 0.1},
    'lassi': {'calories': 75, 'carbs': 9.8, 'sugar': 8, 'vitamin_c': 2, 'protein': 3, 'fat': 3, 'sodium': 100, 'calcium': 120, 'iron': 0.2},
    'green smoothie': {'calories': 65, 'carbs': 13, 'sugar': 9, 'vitamin_c': 85, 'protein': 2, 'fat': 0.5, 'sodium': 20, 'calcium': 40, 'iron': 0.7},
    'cola': {'calories': 39, 'carbs': 10.6, 'sugar': 10.6, 'vitamin_c': 0, 'protein': 0, 'fat': 0, 'sodium': 7, 'calcium': 2, 'iron': 0},
    'beer': {'calories': 43, 'carbs': 3.6, 'sugar': 0.2, 'vitamin_c': 0, 'protein': 0.5, 'fat': 0, 'sodium': 4, 'calcium': 4, 'iron': 0},
    'wine': {'calories': 85, 'carbs': 2.6, 'sugar': 0.9, 'vitamin_c': 0, 'protein': 0.1, 'fat': 0, 'sodium': 4, 'calcium': 8, 'iron': 0.5},

    # 🍖 MEAT & FISH
    'chicken breast': {'calories': 165, 'protein': 31, 'fat': 3.6, 'vitamin_c': 0, 'carbs': 0, 'sodium': 74, 'calcium': 12, 'iron': 1},
    'chicken thigh': {'calories': 209, 'protein': 26, 'fat': 10.9, 'vitamin_c': 0, 'carbs': 0, 'sodium': 81, 'calcium': 11, 'iron': 1.3},
    'chicken liver': {'calories': 167, 'protein': 24, 'fat': 6.5, 'vitamin_c': 27, 'carbs': 0.9, 'sodium': 71, 'calcium': 11, 'iron': 9},
    'turkey breast': {'calories': 135, 'protein': 29, 'fat': 1.6, 'vitamin_c': 0, 'carbs': 0, 'sodium': 48, 'calcium': 14, 'iron': 1.1},
    'duck meat': {'calories': 337, 'protein': 19, 'fat': 28, 'vitamin_c': 0, 'carbs': 0, 'sodium': 63, 'calcium': 11, 'iron': 2.7},
    'beef steak': {'calories': 271, 'protein': 25, 'fat': 19, 'vitamin_c': 0, 'carbs': 0, 'sodium': 58, 'calcium': 18, 'iron': 2.6},
    'beef liver': {'calories': 191, 'protein': 29, 'fat': 5.3, 'vitamin_c': 33, 'carbs': 5, 'sodium': 69, 'calcium': 5, 'iron': 6.5},
    'pork chop': {'calories': 231, 'protein': 25.7, 'fat': 13.9, 'vitamin_c': 0, 'carbs': 0, 'sodium': 59, 'calcium': 19, 'iron': 0.8},
    'pork liver': {'calories': 165, 'protein': 26, 'fat': 4.4, 'vitamin_c': 25, 'carbs': 3.8, 'sodium': 73, 'calcium': 9, 'iron': 15},
    'lamb meat': {'calories': 294, 'protein': 25.6, 'fat': 21, 'vitamin_c': 0, 'carbs': 0, 'sodium': 70, 'calcium': 18, 'iron': 2.1},
    'mutton': {'calories': 294, 'protein': 26, 'fat': 21, 'vitamin_c': 0, 'carbs': 0, 'sodium': 72, 'calcium': 17, 'iron': 2.3},
    'fish salmon': {'calories': 208, 'protein': 20, 'fat': 13, 'vitamin_c': 0, 'carbs': 0, 'sodium': 59, 'calcium': 9, 'iron': 0.3},
    'tuna': {'calories': 132, 'protein': 28, 'fat': 0.6, 'vitamin_c': 0, 'carbs': 0, 'sodium': 47, 'calcium': 8, 'iron': 1.3},
    'sardine': {'calories': 208, 'protein': 25, 'fat': 11, 'vitamin_c': 0, 'carbs': 0, 'sodium': 505, 'calcium': 382, 'iron': 2.9},
    'prawn': {'calories': 99, 'protein': 24, 'fat': 0.3, 'vitamin_c': 0, 'carbs': 0.2, 'sodium': 111, 'calcium': 64, 'iron': 0.5},
    'crab': {'calories': 87, 'protein': 18, 'fat': 1.5, 'vitamin_c': 3, 'carbs': 0, 'sodium': 295, 'calcium': 91, 'iron': 0.8},
    'lobster': {'calories': 90, 'protein': 19, 'fat': 0.9, 'vitamin_c': 3, 'carbs': 0.1, 'sodium': 423, 'calcium': 96, 'iron': 0.4},
    'egg': {'calories': 155, 'protein': 13, 'fat': 11, 'vitamin_c': 0, 'carbs': 1.1, 'sodium': 124, 'calcium': 50, 'iron': 1.2},
    'egg white': {'calories': 52, 'protein': 11, 'fat': 0.2, 'vitamin_c': 0, 'carbs': 0.7, 'sodium': 166, 'calcium': 7, 'iron': 0.1},
    'egg yolk': {'calories': 322, 'protein': 16, 'fat': 27, 'vitamin_c': 0, 'carbs': 3.6, 'sodium': 48, 'calcium': 129, 'iron': 2.7},
    'goat meat': {'calories': 143, 'protein': 27, 'fat': 3, 'vitamin_c': 0, 'carbs': 0, 'sodium': 75, 'calcium': 11, 'iron': 3.7},
    'quail': {'calories': 134, 'protein': 21.8, 'fat': 4.5, 'vitamin_c': 0, 'carbs': 0, 'sodium': 47, 'calcium': 15, 'iron': 4.5},
    'venison': {'calories': 158, 'protein': 30.2, 'fat': 3.2, 'vitamin_c': 0, 'carbs': 0, 'sodium': 66, 'calcium': 9, 'iron': 4},
    'bacon': {'calories': 541, 'protein': 37, 'fat': 42, 'vitamin_c': 0, 'carbs': 1.4, 'sodium': 1717, 'calcium': 11, 'iron': 1.4},
    'ham': {'calories': 145, 'protein': 20.9, 'fat': 5.5, 'vitamin_c': 0, 'carbs': 1.5, 'sodium': 1203, 'calcium': 8, 'iron': 0.9}
}




NUTRITION_DB = NUTRITION_DB_100


# ==================== EQUIPMENT DATABASE FOR RECIPES (500+ Recipe Types) ====================
COOKING_EQUIPMENT = {
    # ==================== CHICKEN DISHES (40 recipes) ====================
    'chicken_curry': ['Pressure cooker', 'Wooden spoon', "Chef's knife", 'Cutting board', 'Mixing bowl', 'Spatula', 'Measuring spoons'],
    'chicken': ['Pressure cooker', 'Wooden spoon', "Chef's knife", 'Cutting board', 'Mixing bowl', 'Spatula', 'Measuring spoons'],
    'grilled_chicken': ['Grill pan', 'Tongs', 'Mixing bowl', 'Meat thermometer', 'Basting brush', 'Oven', "Chef's knife"],
    'chicken_soup': ['Stockpot', 'Ladle', 'Cutting board', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'chicken_stir_fry': ['Wok', 'Spatula', 'Cutting board', "Chef's knife", 'Mixing bowl', 'Tongs', 'Rice cooker'],
    'fried_chicken': ['Deep fryer', 'Tongs', 'Mixing bowl', 'Meat thermometer', 'Paper towels', 'Wire rack'],
    'roast_chicken': ['Roasting pan', 'Meat thermometer', 'Basting brush', 'Oven', "Chef's knife", 'Carving fork'],
    'chicken_tikka': ['Grill', 'Mixing bowl', 'Bamboo skewers', 'Basting brush', 'Tongs', 'Oven'],
    'chicken_alfredo': ['Pasta pot', 'Skillet', 'Whisk', 'Cheese grater', 'Tongs', 'Serving bowl'],
    'chicken_parmesan': ['Skillet', 'Baking dish', 'Oven', 'Meat thermometer', 'Cheese grater', 'Spatula'],
    'chicken_marsala': ['Skillet', 'Wooden spoon', "Chef's knife", 'Cutting board', 'Measuring cups', 'Serving platter'],
    'chicken_piccata': ['Skillet', 'Tongs', "Chef's knife", 'Whisk', 'Measuring spoons', 'Serving platter'],
    'buffalo_chicken': ['Deep fryer', 'Mixing bowl', 'Tongs', 'Serving platter', 'Dipping bowl'],
    'chicken_satay': ['Grill', 'Bamboo skewers', 'Mixing bowl', "Chef's knife", 'Basting brush', 'Serving platter'],
    'chicken_enchiladas': ['Baking dish', 'Oven', 'Skillet', "Chef's knife", 'Spatula', 'Cheese grater'],
    'chicken_quesadilla': ['Skillet', 'Spatula', "Chef's knife", 'Pizza cutter', 'Cheese grater', 'Serving platter'],
    'chicken_kebab': ['Grill', 'Metal skewers', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving platter'],
    'chicken_biryani': ['Pressure cooker', "Chef's knife", 'Mixing bowl', 'Rice cooker', 'Ladle', 'Serving bowl'],
    'chicken_wings': ['Baking sheet', 'Oven', 'Mixing bowl', 'Tongs', 'Wire rack', 'Serving platter'],
    'chicken_nuggets': ['Deep fryer', 'Mixing bowl', 'Tongs', 'Paper towels', 'Serving platter'],
    'chicken_teriyaki': ['Skillet', "Chef's knife", 'Mixing bowl', 'Spatula', 'Rice cooker', 'Serving bowl'],
    'orange_chicken': ['Wok', "Chef's knife", 'Mixing bowl', 'Spatula', 'Whisk', 'Serving bowl'],
    'chicken_fajitas': ['Skillet', "Chef's knife", 'Cutting board', 'Tongs', 'Serving platter', 'Mixing bowl'],
    'chicken_cordon_bleu': ['Baking dish', 'Oven', 'Meat thermometer', 'Mixing bowl', 'Spatula', 'Serving platter'],
    'chicken_salad': ['Mixing bowl', "Chef's knife", 'Cutting board', 'Salad spinner', 'Tongs', 'Serving bowl'],
    'chicken_tacos': ['Skillet', "Chef's knife", 'Spatula', 'Mixing bowl', 'Serving platter', 'Tongs'],
    'bbq_chicken': ['Grill', 'Basting brush', 'Tongs', 'Meat thermometer', "Chef's knife", 'Serving platter'],
    'kung_pao_chicken': ['Wok', 'Spatula', "Chef's knife", 'Mixing bowl', 'Rice cooker', 'Serving bowl'],
    'general_tso_chicken': ['Wok', "Chef's knife", 'Mixing bowl', 'Spatula', 'Deep fryer', 'Serving bowl'],
    'chicken_cacciatore': ['Dutch oven', 'Wooden spoon', "Chef's knife", 'Cutting board', 'Oven', 'Serving bowl'],
    'lemon_chicken': ['Skillet', "Chef's knife", 'Whisk', 'Mixing bowl', 'Tongs', 'Serving platter'],
    'honey_mustard_chicken': ['Baking dish', 'Oven', 'Whisk', 'Mixing bowl', 'Basting brush', 'Serving platter'],
    'sesame_chicken': ['Wok', "Chef's knife", 'Mixing bowl', 'Spatula', 'Whisk', 'Serving bowl'],
    'chicken_pot_pie': ['Pie dish', 'Oven', 'Pot', "Chef's knife", 'Rolling pin', 'Pastry brush'],
    'chicken_schnitzel': ['Skillet', 'Meat tenderizer', 'Mixing bowl', 'Tongs', 'Paper towels', 'Serving platter'],
    'chicken_shawarma': ['Grill', "Chef's knife", 'Mixing bowl', 'Bamboo skewers', 'Tongs', 'Serving platter'],
    'tandoori_chicken': ['Oven', 'Mixing bowl', "Chef's knife", 'Basting brush', 'Tongs', 'Serving platter'],
    'jerk_chicken': ['Grill', 'Mixing bowl', "Chef's knife", 'Basting brush', 'Tongs', 'Serving platter'],
    'chicken_noodle_soup': ['Stockpot', 'Ladle', "Chef's knife", 'Colander', 'Wooden spoon', 'Soup bowl'],
    'chicken_burrito': ['Skillet', "Chef's knife", 'Mixing bowl', 'Spatula', 'Serving platter', 'Rice cooker'],
    
    # ==================== BEEF DISHES (50 recipes) ====================
    'beef_stew': ['Dutch oven', 'Wooden spoon', "Chef's knife", 'Cutting board', 'Oven', 'Ladle'],
    'beef_curry': ['Pressure cooker', 'Wooden spoon', "Chef's knife", 'Mixing bowl', 'Ladle', 'Serving bowl'],
    'steak': ['Cast iron skillet', 'Tongs', 'Meat thermometer', "Chef's knife", 'Serving platter', 'Cutting board'],
    'beef_tacos': ['Skillet', 'Spatula', "Chef's knife", 'Mixing bowl', 'Serving platter', 'Tongs'],
    'beef_burger': ['Grill pan', 'Spatula', 'Mixing bowl', "Chef's knife", 'Tongs', 'Serving platter'],
    'pot_roast': ['Dutch oven', 'Meat thermometer', 'Tongs', "Chef's knife", 'Ladle', 'Serving platter'],
    'beef_stroganoff': ['Skillet', 'Wooden spoon', "Chef's knife", 'Mixing bowl', 'Pasta pot', 'Serving bowl'],
    'meatballs': ['Mixing bowl', 'Baking sheet', 'Oven', "Chef's knife", 'Cookie scoop', 'Spatula'],
    'beef_wellington': ['Baking sheet', 'Oven', 'Rolling pin', "Chef's knife", 'Meat thermometer', 'Pastry brush'],
    'beef_bourguignon': ['Dutch oven', 'Wooden spoon', "Chef's knife", 'Oven', 'Ladle', 'Serving bowl'],
    'corned_beef': ['Large pot', 'Wooden spoon', "Chef's knife", 'Slotted spoon', 'Cutting board', 'Serving platter'],
    'beef_enchiladas': ['Baking dish', 'Oven', 'Skillet', "Chef's knife", 'Spatula', 'Cheese grater'],
    'beef_kebab': ['Grill', 'Metal skewers', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving platter'],
    'beef_fajitas': ['Skillet', "Chef's knife", 'Tongs', 'Mixing bowl', 'Serving platter', 'Cutting board'],
    'beef_teriyaki': ['Skillet', "Chef's knife", 'Mixing bowl', 'Spatula', 'Whisk', 'Serving bowl'],
    'mongolian_beef': ['Wok', "Chef's knife", 'Mixing bowl', 'Spatula', 'Whisk', 'Serving bowl'],
    'beef_bulgogi': ['Grill pan', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving platter', 'Rice cooker'],
    'beef_brisket': ['Smoker', 'Meat thermometer', "Chef's knife", 'Tongs', 'Basting brush', 'Serving platter'],
    'prime_rib': ['Roasting pan', 'Oven', 'Meat thermometer', "Chef's knife", 'Carving fork', 'Serving platter'],
    'beef_chili': ['Dutch oven', 'Wooden spoon', "Chef's knife", 'Ladle', 'Mixing bowl', 'Serving bowl'],
    'beef_short_ribs': ['Dutch oven', 'Oven', "Chef's knife", 'Tongs', 'Ladle', 'Serving platter'],
    'shepherd_pie': ['Skillet', 'Baking dish', 'Oven', 'Potato masher', "Chef's knife", 'Serving spoon'],
    'salisbury_steak': ['Skillet', 'Mixing bowl', "Chef's knife", 'Spatula', 'Whisk', 'Serving platter'],
    'beef_rendang': ['Pot', 'Wooden spoon', "Chef's knife", 'Blender', 'Ladle', 'Serving bowl'],
    'philly_cheesesteak': ['Skillet', "Chef's knife", 'Spatula', 'Tongs', 'Cheese grater', 'Serving platter'],
    'beef_nachos': ['Baking sheet', 'Oven', 'Skillet', "Chef's knife", 'Cheese grater', 'Serving platter'],
    'beef_stir_fry': ['Wok', "Chef's knife", 'Spatula', 'Mixing bowl', 'Rice cooker', 'Serving bowl'],
    'beef_empanadas': ['Baking sheet', 'Oven', 'Skillet', "Chef's knife", 'Rolling pin', 'Fork'],
    'beef_ragu': ['Sauce pan', 'Wooden spoon', "Chef's knife", 'Ladle', 'Pasta pot', 'Serving bowl'],
    'beef_pho': ['Stockpot', 'Ladle', "Chef's knife", 'Strainer', 'Chopsticks', 'Soup bowl'],
    'beef_satay': ['Grill', 'Bamboo skewers', "Chef's knife", 'Mixing bowl', 'Basting brush', 'Serving platter'],
    'beef_goulash': ['Dutch oven', 'Wooden spoon', "Chef's knife", 'Ladle', 'Oven', 'Serving bowl'],
    'beef_shawarma': ['Grill', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving platter', 'Bamboo skewers'],
    'carne_asada': ['Grill', "Chef's knife", 'Mixing bowl', 'Tongs', 'Cutting board', 'Serving platter'],
    'beef_quesadilla': ['Skillet', "Chef's knife", 'Spatula', 'Cheese grater', 'Pizza cutter', 'Serving platter'],
    'beef_lasagna': ['Lasagna pan', 'Oven', 'Skillet', "Chef's knife", 'Spatula', 'Cheese grater'],
    'swiss_steak': ['Dutch oven', 'Meat tenderizer', "Chef's knife", 'Oven', 'Ladle', 'Serving platter'],
    'beef_tartare': ['Mixing bowl', "Chef's knife", 'Cutting board', 'Fork', 'Serving platter', 'Small bowls'],
    'beef_carpaccio': ["Chef's knife", 'Cutting board', 'Serving platter', 'Mixing bowl', 'Whisk'],
    'london_broil': ['Grill pan', 'Meat thermometer', "Chef's knife", 'Tongs', 'Cutting board', 'Serving platter'],
    'beef_stuffed_peppers': ['Baking dish', 'Oven', "Chef's knife", 'Skillet', 'Mixing bowl', 'Aluminum foil'],
    'beef_sandwich': ["Chef's knife", 'Cutting board', 'Serving platter', 'Toaster', 'Spatula'],
    'beef_teppanyaki': ['Griddle', 'Spatula', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving platter'],
    'beef_cottage_pie': ['Skillet', 'Baking dish', 'Oven', 'Potato masher', "Chef's knife", 'Serving spoon'],
    'beef_sloppy_joe': ['Skillet', "Chef's knife", 'Wooden spoon', 'Mixing bowl', 'Serving platter', 'Ladle'],
    'flank_steak': ['Grill pan', 'Meat thermometer', "Chef's knife", 'Tongs', 'Mixing bowl', 'Serving platter'],
    'beef_brochettes': ['Grill', 'Metal skewers', "Chef's knife", 'Mixing bowl', 'Tongs', 'Basting brush'],
    'beef_paprikash': ['Dutch oven', 'Wooden spoon', "Chef's knife", 'Ladle', 'Serving bowl', 'Oven'],
    'beef_tamales': ['Steamer', 'Mixing bowl', "Chef's knife", 'Wooden spoon', 'Cutting board', 'Serving platter'],
    'beef_tostadas': ['Skillet', "Chef's knife", 'Spatula', 'Serving platter', 'Mixing bowl', 'Cheese grater'],
    
    # ==================== PORK DISHES (40 recipes) ====================
    'pork_chop': ['Skillet', 'Tongs', 'Meat thermometer', "Chef's knife", 'Oven', 'Serving platter'],
    'pulled_pork': ['Slow cooker', 'Tongs', "Chef's knife", 'Mixing bowl', 'Serving bowl', 'Fork'],
    'pork_ribs': ['Grill', 'Basting brush', 'Tongs', 'Meat thermometer', "Chef's knife", 'Serving platter'],
    'bacon': ['Skillet', 'Tongs', 'Paper towels', 'Baking sheet', 'Oven', 'Serving platter'],
    'ham': ['Roasting pan', 'Basting brush', 'Meat thermometer', 'Oven', "Chef's knife", 'Serving platter'],
    'pork_tenderloin': ['Baking sheet', 'Oven', 'Meat thermometer', "Chef's knife", 'Tongs', 'Serving platter'],
    'pork_belly': ['Roasting pan', 'Oven', "Chef's knife", 'Meat thermometer', 'Tongs', 'Serving platter'],
    'pork_stir_fry': ['Wok', "Chef's knife", 'Spatula', 'Mixing bowl', 'Rice cooker', 'Serving bowl'],
    'pork_schnitzel': ['Skillet', 'Meat tenderizer', 'Mixing bowl', 'Tongs', 'Spatula', 'Serving platter'],
    'pork_carnitas': ['Slow cooker', "Chef's knife", 'Tongs', 'Fork', 'Mixing bowl', 'Serving platter'],
    'pork_adobo': ['Pot', 'Wooden spoon', "Chef's knife", 'Ladle', 'Mixing bowl', 'Serving bowl'],
    'pork_satay': ['Grill', 'Bamboo skewers', "Chef's knife", 'Mixing bowl', 'Basting brush', 'Serving platter'],
    'pork_tonkatsu': ['Deep fryer', 'Meat tenderizer', 'Mixing bowl', 'Tongs', 'Paper towels', 'Serving platter'],
    'pork_vindaloo': ['Pot', 'Wooden spoon', "Chef's knife", 'Mixing bowl', 'Ladle', 'Serving bowl'],
    'pork_shoulder': ['Slow cooker', 'Meat thermometer', "Chef's knife", 'Tongs', 'Fork', 'Serving platter'],
    'pork_kebab': ['Grill', 'Metal skewers', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving platter'],
    'pork_curry': ['Pot', 'Wooden spoon', "Chef's knife", 'Mixing bowl', 'Ladle', 'Serving bowl'],
    'pork_ramen': ['Pot', 'Ladle', "Chef's knife", 'Strainer', 'Chopsticks', 'Ramen bowl'],
    'pork_tacos': ['Skillet', "Chef's knife", 'Spatula', 'Mixing bowl', 'Serving platter', 'Tongs'],
    'pork_dumplings': ['Steamer', 'Mixing bowl', "Chef's knife", 'Rolling pin', 'Serving platter', 'Dipping bowl'],
    'pork_buns': ['Steamer', 'Mixing bowl', "Chef's knife", 'Rolling pin', 'Bamboo steamer', 'Serving platter'],
    'pork_sausage': ['Skillet', 'Tongs', "Chef's knife", 'Serving platter', 'Mixing bowl', 'Meat grinder'],
    'pork_meatballs': ['Mixing bowl', 'Baking sheet', 'Oven', "Chef's knife", 'Cookie scoop', 'Serving bowl'],
    'bbq_pork': ['Grill', 'Basting brush', 'Tongs', "Chef's knife", 'Meat thermometer', 'Serving platter'],
    'pork_roast': ['Roasting pan', 'Oven', 'Meat thermometer', "Chef's knife", 'Basting brush', 'Serving platter'],
    'pork_loin': ['Roasting pan', 'Oven', 'Meat thermometer', "Chef's knife", 'Tongs', 'Serving platter'],
    'pork_chow_mein': ['Wok', "Chef's knife", 'Spatula', 'Mixing bowl', 'Tongs', 'Serving bowl'],
    'pork_fried_rice': ['Wok', "Chef's knife", 'Spatula', 'Rice cooker', 'Mixing bowl', 'Serving bowl'],
    'pork_gyoza': ['Skillet', 'Mixing bowl', "Chef's knife", 'Rolling pin', 'Spatula', 'Serving platter'],
    'pork_sisig': ['Skillet', "Chef's knife", 'Cutting board', 'Mixing bowl', 'Spatula', 'Serving bowl'],
    'pork_spring_rolls': ['Deep fryer', "Chef's knife", 'Mixing bowl', 'Tongs', 'Paper towels', 'Serving platter'],
    'pork_wonton': ['Steamer', 'Mixing bowl', "Chef's knife", 'Small spoon', 'Bamboo steamer', 'Dipping bowl'],
    'pork_egg_roll': ['Deep fryer', "Chef's knife", 'Mixing bowl', 'Tongs', 'Paper towels', 'Serving platter'],
    'glazed_ham': ['Roasting pan', 'Oven', 'Basting brush', 'Meat thermometer', "Chef's knife", 'Serving platter'],
    'pork_steak': ['Grill pan', 'Tongs', 'Meat thermometer', "Chef's knife", 'Mixing bowl', 'Serving platter'],
    'pork_burrito': ['Skillet', "Chef's knife", 'Spatula', 'Mixing bowl', 'Serving platter', 'Rice cooker'],
    'pork_quesadilla': ['Skillet', "Chef's knife", 'Spatula', 'Cheese grater', 'Pizza cutter', 'Serving platter'],
    'pork_enchiladas': ['Baking dish', 'Oven', 'Skillet', "Chef's knife", 'Spatula', 'Cheese grater'],
    'pork_pozole': ['Large pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Serving bowl', 'Strainer'],
    'pork_menudo': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Serving bowl'],
    
    # ==================== SEAFOOD DISHES (50 recipes) ====================
    'fish_curry': ['Skillet', 'Wooden spoon', "Chef's knife", 'Mixing bowl', 'Blender', 'Serving bowl'],
    'grilled_fish': ['Grill pan', 'Fish spatula', 'Tongs', "Chef's knife", 'Serving platter', 'Basting brush'],
    'fish_tacos': ['Skillet', 'Fish spatula', "Chef's knife", 'Mixing bowl', 'Serving platter', 'Lime press'],
    'salmon': ['Oven', 'Baking sheet', 'Fish spatula', "Chef's knife", 'Meat thermometer', 'Serving platter'],
    'shrimp_scampi': ['Skillet', 'Wooden spoon', 'Pasta pot', 'Colander', "Chef's knife", 'Tongs'],
    'tuna_steak': ['Grill pan', 'Tongs', 'Meat thermometer', "Chef's knife", 'Serving platter', 'Mixing bowl'],
    'seafood_paella': ['Paella pan', 'Wooden spoon', "Chef's knife", 'Ladle', 'Rice cooker', 'Serving spoon'],
    'lobster': ['Stockpot', 'Tongs', "Chef's knife", 'Butter dish', 'Serving platter', 'Nut cracker'],
    'fish_and_chips': ['Deep fryer', 'Tongs', "Chef's knife", 'Mixing bowl', 'Paper towels', 'Serving basket'],
    'crab_cakes': ['Skillet', 'Mixing bowl', "Chef's knife", 'Spatula', 'Serving platter', 'Fork'],
    'shrimp_tempura': ['Deep fryer', 'Mixing bowl', 'Chopsticks', 'Paper towels', "Chef's knife", 'Serving platter'],
    'sushi': ['Bamboo mat', 'Rice cooker', "Chef's knife", 'Cutting board', 'Mixing bowl', 'Serving platter'],
    'ceviche': ['Mixing bowl', "Chef's knife", 'Cutting board', 'Citrus press', 'Serving bowl', 'Spoon'],
    'fish_stew': ['Large pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'clam_chowder': ['Dutch oven', 'Ladle', "Chef's knife", 'Wooden spoon', 'Whisk', 'Soup bowl'],
    'lobster_bisque': ['Pot', 'Blender', 'Ladle', "Chef's knife", 'Strainer', 'Soup bowl'],
    'shrimp_cocktail': ['Pot', 'Mixing bowl', "Chef's knife", 'Ice bucket', 'Serving platter', 'Small bowls'],
    'grilled_shrimp': ['Grill', 'Metal skewers', 'Tongs', "Chef's knife", 'Basting brush', 'Serving platter'],
    'calamari': ['Deep fryer', 'Mixing bowl', 'Tongs', "Chef's knife", 'Paper towels', 'Serving platter'],
    'oysters': ['Oyster knife', 'Cutting board', 'Ice bucket', 'Serving platter', 'Small forks', 'Lemon'],
    'mussels': ['Large pot', 'Ladle', "Chef's knife", 'Tongs', 'Serving bowl', 'Soup bowl'],
    'scallops': ['Skillet', 'Tongs', "Chef's knife", 'Meat thermometer', 'Serving platter', 'Spatula'],
    'fish_pie': ['Pie dish', 'Oven', 'Pot', "Chef's knife", 'Mixing bowl', 'Spatula'],
    'baked_salmon': ['Baking dish', 'Oven', "Chef's knife", 'Aluminum foil', 'Fish spatula', 'Serving platter'],
    'teriyaki_salmon': ['Skillet', "Chef's knife", 'Whisk', 'Mixing bowl', 'Fish spatula', 'Serving platter'],
    'honey_glazed_salmon': ['Baking sheet', 'Oven', 'Whisk', 'Basting brush', "Chef's knife", 'Serving platter'],
    'blackened_fish': ['Cast iron skillet', "Chef's knife", 'Tongs', 'Mixing bowl', 'Fish spatula', 'Serving platter'],
    'poached_fish': ['Skillet', 'Slotted spoon', "Chef's knife", 'Fish spatula', 'Serving platter', 'Pot'],
    'steamed_fish': ['Steamer', "Chef's knife", 'Serving platter', 'Mixing bowl', 'Bamboo steamer', 'Chopsticks'],
    'fish_balls': ['Deep fryer', 'Mixing bowl', 'Slotted spoon', "Chef's knife", 'Food processor', 'Serving bowl'],
    'shrimp_alfredo': ['Pasta pot', 'Skillet', 'Whisk', "Chef's knife", 'Cheese grater', 'Serving bowl'],
    'shrimp_fried_rice': ['Wok', "Chef's knife", 'Spatula', 'Rice cooker', 'Mixing bowl', 'Serving bowl'],
    'shrimp_pasta': ['Pasta pot', 'Skillet', 'Colander', "Chef's knife", 'Tongs', 'Serving bowl'],
    'shrimp_gumbo': ['Dutch oven', 'Ladle', "Chef's knife", 'Wooden spoon', 'Rice cooker', 'Serving bowl'],
    'shrimp_stir_fry': ['Wok', "Chef's knife", 'Spatula', 'Mixing bowl', 'Rice cooker', 'Serving bowl'],
    'fish_tikka': ['Grill', 'Bamboo skewers', "Chef's knife", 'Mixing bowl', 'Basting brush', 'Serving platter'],
    'fish_masala': ['Skillet', 'Wooden spoon', "Chef's knife", 'Mixing bowl', 'Ladle', 'Serving bowl'],
    'crab_soup': ['Pot', 'Ladle', "Chef's knife", 'Strainer', 'Wooden spoon', 'Soup bowl'],
    'crab_legs': ['Steamer', 'Nut cracker', "Chef's knife", 'Tongs', 'Butter dish', 'Serving platter'],
    'stuffed_fish': ['Baking dish', 'Oven', "Chef's knife", 'Mixing bowl', 'Aluminum foil', 'Fish spatula'],
    'fish_sandwich': ['Skillet', "Chef's knife", 'Spatula', 'Toaster', 'Serving platter', 'Cutting board'],
    'tuna_salad': ['Mixing bowl', "Chef's knife", 'Fork', 'Can opener', 'Serving bowl', 'Spoon'],
    'salmon_sushi': ['Bamboo mat', 'Rice cooker', "Chef's knife", 'Cutting board', 'Mixing bowl', 'Serving platter'],
    'sashimi': ["Chef's knife", 'Cutting board', 'Serving platter', 'Small bowls', 'Chopsticks', 'Ice'],
    'fish_soup': ['Pot', 'Ladle', "Chef's knife", 'Strainer', 'Wooden spoon', 'Soup bowl'],
    'bouillabaisse': ['Large pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'cioppino': ['Dutch oven', 'Ladle', "Chef's knife", 'Wooden spoon', 'Serving bowl', 'Bread'],
    'lobster_roll': ["Chef's knife", 'Mixing bowl', 'Toaster', 'Serving platter', 'Spatula', 'Butter dish'],
    'shrimp_toast': ['Deep fryer', 'Food processor', "Chef's knife", 'Tongs', 'Paper towels', 'Serving platter'],
    'fish_cakes': ['Skillet', 'Mixing bowl', "Chef's knife", 'Spatula', 'Food processor', 'Serving platter'],
    
    # ==================== PASTA DISHES (50 recipes) ====================
    'pasta': ['Large pot', 'Colander', 'Wooden spoon', 'Tongs', 'Cheese grater', 'Serving bowl'],
    'spaghetti': ['Pasta pot', 'Colander', 'Pasta fork', 'Tongs', 'Cheese grater', 'Serving bowl'],
    'lasagna': ['Lasagna pan', 'Oven', 'Mixing bowl', 'Spatula', 'Cheese grater', 'Aluminum foil'],
    'fettuccine_alfredo': ['Pasta pot', 'Colander', 'Sauce pan', 'Whisk', 'Cheese grater', 'Serving bowl'],
    'mac_and_cheese': ['Pot', 'Colander', 'Cheese grater', 'Whisk', 'Baking dish', 'Oven'],
    'penne_arrabbiata': ['Pasta pot', 'Colander', 'Sauce pan', 'Wooden spoon', "Chef's knife", 'Serving bowl'],
    'carbonara': ['Pasta pot', 'Colander', 'Mixing bowl', 'Whisk', 'Cheese grater', 'Tongs'],
    'ravioli': ['Pasta pot', 'Colander', 'Slotted spoon', 'Sauce pan', 'Cheese grater', 'Serving bowl'],
    'pesto_pasta': ['Pasta pot', 'Colander', 'Food processor', "Chef's knife", 'Tongs', 'Serving bowl'],
    'tortellini': ['Pasta pot', 'Colander', 'Slotted spoon', 'Sauce pan', 'Cheese grater', 'Serving bowl'],
    'linguine': ['Pasta pot', 'Colander', 'Tongs', 'Sauce pan', 'Cheese grater', 'Serving bowl'],
    'macaroni': ['Pot', 'Colander', 'Wooden spoon', 'Cheese grater', 'Serving bowl', 'Measuring cups'],
    'rigatoni': ['Pasta pot', 'Colander', 'Wooden spoon', 'Sauce pan', 'Cheese grater', 'Serving bowl'],
    'fusilli': ['Pasta pot', 'Colander', 'Tongs', 'Sauce pan', 'Cheese grater', 'Serving bowl'],
    'angel_hair': ['Pasta pot', 'Colander', 'Tongs', 'Sauce pan', 'Cheese grater', 'Serving bowl'],
    'ziti': ['Pasta pot', 'Baking dish', 'Colander', 'Oven', 'Cheese grater', 'Serving bowl'],
    'orzo': ['Pot', 'Strainer', "Chef's knife", 'Wooden spoon', 'Mixing bowl', 'Serving bowl'],
    'gnocchi': ['Pot', 'Slotted spoon', 'Sauce pan', 'Cheese grater', 'Serving bowl', 'Spatula'],
    'pasta_primavera': ['Pasta pot', 'Colander', 'Skillet', "Chef's knife", 'Tongs', 'Serving bowl'],
    'pasta_bolognese': ['Pasta pot', 'Sauce pan', 'Colander', "Chef's knife", 'Ladle', 'Serving bowl'],
    'pasta_marinara': ['Pasta pot', 'Colander', 'Sauce pan', "Chef's knife", 'Wooden spoon', 'Serving bowl'],
    'pasta_aglio_olio': ['Pasta pot', 'Colander', 'Skillet', "Chef's knife", 'Tongs', 'Serving bowl'],
    'pasta_puttanesca': ['Pasta pot', 'Colander', 'Skillet', "Chef's knife", 'Tongs', 'Serving bowl'],
    'pasta_carbonara': ['Pasta pot', 'Colander', 'Mixing bowl', 'Whisk', 'Cheese grater', 'Tongs'],
    'pasta_cacio_pepe': ['Pasta pot', 'Colander', 'Tongs', 'Cheese grater', 'Mixing bowl', 'Serving bowl'],
    'pasta_amatriciana': ['Pasta pot', 'Colander', 'Skillet', "Chef's knife", 'Tongs', 'Serving bowl'],
    'baked_ziti': ['Baking dish', 'Oven', 'Pasta pot', 'Colander', 'Cheese grater', 'Spatula'],
    'stuffed_shells': ['Baking dish', 'Oven', 'Pasta pot', 'Mixing bowl', 'Cheese grater', 'Spatula'],
    'manicotti': ['Baking dish', 'Oven', 'Pasta pot', 'Mixing bowl', 'Cheese grater', 'Piping bag'],
    'cannelloni': ['Baking dish', 'Oven', 'Pasta pot', 'Mixing bowl', 'Cheese grater', 'Spatula'],
    'pasta_salad': ['Mixing bowl', 'Pasta pot', 'Colander', "Chef's knife", 'Whisk', 'Serving bowl'],
    'lo_mein': ['Wok', 'Pasta pot', 'Colander', "Chef's knife", 'Spatula', 'Serving bowl'],
    'pad_thai': ['Wok', 'Spatula', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving bowl'],
    'chow_mein': ['Wok', 'Spatula', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving bowl'],
    'ramen': ['Pot', 'Ladle', "Chef's knife", 'Strainer', 'Chopsticks', 'Ramen bowl'],
    'udon': ['Pot', 'Ladle', "Chef's knife", 'Strainer', 'Chopsticks', 'Soup bowl'],
    'soba': ['Pot', 'Strainer', "Chef's knife", 'Mixing bowl', 'Chopsticks', 'Serving bowl'],
    'rice_noodles': ['Pot', 'Strainer', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving bowl'],
    'pho': ['Stockpot', 'Ladle', "Chef's knife", 'Strainer', 'Chopsticks', 'Soup bowl'],
    'laksa': ['Pot', 'Ladle', "Chef's knife", 'Blender', 'Strainer', 'Soup bowl'],
    'vermicelli': ['Pot', 'Strainer', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving bowl'],
    'glass_noodles': ['Pot', 'Strainer', "Chef's knife", 'Mixing bowl', 'Chopsticks', 'Serving bowl'],
    'seafood_pasta': ['Pasta pot', 'Skillet', 'Colander', "Chef's knife", 'Tongs', 'Serving bowl'],
    'chicken_pasta': ['Pasta pot', 'Skillet', 'Colander', "Chef's knife", 'Tongs', 'Serving bowl'],
    'vegetable_pasta': ['Pasta pot', 'Skillet', 'Colander', "Chef's knife", 'Tongs', 'Serving bowl'],
    'mushroom_pasta': ['Pasta pot', 'Skillet', 'Colander', "Chef's knife", 'Tongs', 'Serving bowl'],
    'tomato_pasta': ['Pasta pot', 'Sauce pan', 'Colander', "Chef's knife", 'Wooden spoon', 'Serving bowl'],
    'creamy_pasta': ['Pasta pot', 'Sauce pan', 'Colander', 'Whisk', 'Tongs', 'Serving bowl'],
    'spicy_pasta': ['Pasta pot', 'Skillet', 'Colander', "Chef's knife", 'Tongs', 'Serving bowl'],
    'cold_pasta': ['Pasta pot', 'Colander', 'Mixing bowl', "Chef's knife", 'Whisk', 'Serving bowl'],
    
    # ==================== RICE DISHES (30 recipes) ====================
    'fried_rice': ['Wok', 'Spatula', 'Rice cooker', "Chef's knife", 'Mixing bowl', 'Serving bowl'],
    'biryani': ['Pressure cooker', "Chef's knife", 'Mixing bowl', 'Rice cooker', 'Ladle', 'Serving bowl'],
    'risotto': ['Sauce pan', 'Wooden spoon', 'Ladle', 'Cheese grater', "Chef's knife", 'Serving bowl'],
    'paella': ['Paella pan', 'Wooden spoon', "Chef's knife", 'Ladle', 'Rice cooker', 'Serving spoon'],
    'pilaf': ['Pot', 'Wooden spoon', "Chef's knife", 'Measuring cups', 'Lid', 'Serving bowl'],
    'jambalaya': ['Dutch oven', 'Wooden spoon', "Chef's knife", 'Measuring cups', 'Ladle', 'Serving bowl'],
    'spanish_rice': ['Pot', 'Wooden spoon', "Chef's knife", 'Mixing bowl', 'Ladle', 'Serving bowl'],
    'cilantro_lime_rice': ['Rice cooker', "Chef's knife", 'Mixing bowl', 'Fork', 'Citrus press', 'Serving bowl'],
    'coconut_rice': ['Rice cooker', 'Measuring cups', 'Fork', 'Serving bowl', 'Wooden spoon', 'Can opener'],
    'mexican_rice': ['Pot', 'Wooden spoon', "Chef's knife", 'Blender', 'Ladle', 'Serving bowl'],
    'sticky_rice': ['Steamer', 'Bamboo steamer', 'Mixing bowl', 'Wooden spoon', 'Serving bowl', 'Rice cooker'],
    'rice_pudding': ['Pot', 'Wooden spoon', 'Measuring cups', 'Whisk', 'Serving bowl', 'Ladle'],
    'rice_bowl': ['Rice cooker', "Chef's knife", 'Mixing bowl', 'Spatula', 'Serving bowl', 'Tongs'],
    'congee': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Rice cooker', 'Soup bowl'],
    'khichdi': ['Pressure cooker', "Chef's knife", 'Mixing bowl', 'Wooden spoon', 'Ladle', 'Serving bowl'],
    'plov': ['Dutch oven', 'Wooden spoon', "Chef's knife", 'Measuring cups', 'Ladle', 'Serving bowl'],
    'nasi_goreng': ['Wok', 'Spatula', 'Rice cooker', "Chef's knife", 'Mixing bowl', 'Serving bowl'],
    'arroz_con_pollo': ['Dutch oven', "Chef's knife", 'Wooden spoon', 'Rice cooker', 'Ladle', 'Serving bowl'],
    'stuffed_peppers': ['Baking dish', 'Oven', "Chef's knife", 'Rice cooker', 'Mixing bowl', 'Aluminum foil'],
    'cabbage_rolls': ['Baking dish', 'Oven', "Chef's knife", 'Rice cooker', 'Mixing bowl', 'Toothpicks'],
    'rice_casserole': ['Baking dish', 'Oven', 'Rice cooker', 'Mixing bowl', 'Cheese grater', 'Spatula'],
    'rice_balls': ['Mixing bowl', 'Rice cooker', "Chef's knife", 'Plastic wrap', 'Serving platter', 'Small bowls'],
    'arancini': ['Deep fryer', 'Rice cooker', 'Mixing bowl', 'Tongs', 'Paper towels', 'Serving platter'],
    'dolma': ['Pot', "Chef's knife", 'Rice cooker', 'Mixing bowl', 'Wooden spoon', 'Serving platter'],
    'rice_and_beans': ['Pot', 'Rice cooker', "Chef's knife", 'Wooden spoon', 'Ladle', 'Serving bowl'],
    'jollof_rice': ['Pot', "Chef's knife", 'Wooden spoon', 'Blender', 'Rice cooker', 'Serving bowl'],
    'bibimbap': ['Stone pot', 'Rice cooker', "Chef's knife", 'Skillet', 'Mixing bowl', 'Serving bowl'],
    'donburi': ['Rice cooker', 'Skillet', "Chef's knife", 'Mixing bowl', 'Ladle', 'Serving bowl'],
    'kimbap': ['Bamboo mat', 'Rice cooker', "Chef's knife", 'Cutting board', 'Mixing bowl', 'Serving platter'],
    'onigiri': ['Plastic wrap', 'Rice cooker', "Chef's knife", 'Mixing bowl', 'Small bowls', 'Serving platter'],
    
    # ==================== Continue with more categories... ====================
    
    # SOUP & STEWS (40 recipes)
    'soup': ['Large pot', 'Ladle', "Chef's knife", 'Strainer', 'Wooden spoon', 'Soup bowl'],
    'chicken_soup': ['Stockpot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'tomato_soup': ['Pot', 'Blender', 'Ladle', 'Wooden spoon', "Chef's knife", 'Soup bowl'],
    'minestrone': ['Large pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Cheese grater', 'Soup bowl'],
    'clam_chowder': ['Dutch oven', 'Ladle', "Chef's knife", 'Wooden spoon', 'Whisk', 'Soup bowl'],
    'french_onion_soup': ['Dutch oven', "Chef's knife", 'Ladle', 'Oven', 'Soup bowl', 'Cheese grater'],
    'butternut_squash_soup': ['Pot', 'Blender', "Chef's knife", 'Ladle', 'Wooden spoon', 'Soup bowl'],
    'potato_soup': ['Pot', 'Potato masher', 'Ladle', "Chef's knife", 'Whisk', 'Soup bowl'],
    'split_pea_soup': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'lentil_soup': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'mushroom_soup': ['Pot', 'Blender', 'Ladle', "Chef's knife", 'Whisk', 'Soup bowl'],
    'broccoli_soup': ['Pot', 'Blender', 'Ladle', "Chef's knife", 'Whisk', 'Soup bowl'],
    'cream_of_mushroom': ['Pot', 'Blender', 'Ladle', 'Whisk', "Chef's knife", 'Soup bowl'],
    'corn_chowder': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Whisk', 'Soup bowl'],
    'tortilla_soup': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Blender', 'Soup bowl'],
    'wonton_soup': ['Pot', 'Ladle', "Chef's knife", 'Chopsticks', 'Small spoon', 'Soup bowl'],
    'hot_and_sour_soup': ['Pot', 'Ladle', "Chef's knife", 'Whisk', 'Wooden spoon', 'Soup bowl'],
    'egg_drop_soup': ['Pot', 'Ladle', 'Whisk', "Chef's knife", 'Mixing bowl', 'Soup bowl'],
    'miso_soup': ['Pot', 'Ladle', "Chef's knife", 'Whisk', 'Strainer', 'Soup bowl'],
    'gazpacho': ['Blender', "Chef's knife", 'Mixing bowl', 'Serving bowl', 'Ladle', 'Cutting board'],
    'borscht': ['Pot', 'Ladle', "Chef's knife", 'Grater', 'Wooden spoon', 'Soup bowl'],
    'goulash': ['Dutch oven', 'Ladle', "Chef's knife", 'Wooden spoon', 'Oven', 'Soup bowl'],
    'tom_yum': ['Pot', 'Ladle', "Chef's knife", 'Mortar and pestle', 'Strainer', 'Soup bowl'],
    'tom_kha': ['Pot', 'Ladle', "Chef's knife", 'Blender', 'Can opener', 'Soup bowl'],
    'chicken_noodle': ['Stockpot', 'Ladle', "Chef's knife", 'Colander', 'Wooden spoon', 'Soup bowl'],
    'beef_noodle': ['Stockpot', 'Ladle', "Chef's knife", 'Strainer', 'Chopsticks', 'Soup bowl'],
    'vegetable_soup': ['Large pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'cabbage_soup': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'black_bean_soup': ['Pot', 'Blender', 'Ladle', "Chef's knife", 'Wooden spoon', 'Soup bowl'],
    'white_bean_soup': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'bean_soup': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'seafood_soup': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'fish_soup': ['Pot', 'Ladle', "Chef's knife", 'Strainer', 'Wooden spoon', 'Soup bowl'],
    'crab_bisque': ['Pot', 'Blender', 'Ladle', "Chef's knife", 'Strainer', 'Soup bowl'],
    'lobster_bisque': ['Pot', 'Blender', 'Ladle', "Chef's knife", 'Strainer', 'Soup bowl'],
    'shrimp_soup': ['Pot', 'Ladle', "Chef's knife", 'Wooden spoon', 'Strainer', 'Soup bowl'],
    'udon_soup': ['Pot', 'Ladle', "Chef's knife", 'Strainer', 'Chopsticks', 'Soup bowl'],
    'ramen_soup': ['Pot', 'Ladle', "Chef's knife", 'Strainer', 'Chopsticks', 'Ramen bowl'],
    'pumpkin_soup': ['Pot', 'Blender', 'Ladle', "Chef's knife", 'Wooden spoon', 'Soup bowl'],
    'carrot_soup': ['Pot', 'Blender', 'Ladle', "Chef's knife", 'Wooden spoon', 'Soup bowl'],

    # ==================== BREAKFAST DISHES (30 recipes) ====================
    'pancakes': ['Griddle', 'Mixing bowl', 'Whisk', 'Ladle', 'Spatula', 'Measuring cups'],
    'waffles': ['Waffle maker', 'Mixing bowl', 'Whisk', 'Ladle', 'Measuring cups', 'Serving platter'],
    'omelette': ['Skillet', 'Whisk', 'Spatula', 'Mixing bowl', "Chef's knife", 'Serving platter'],
    'scrambled_eggs': ['Skillet', 'Whisk', 'Spatula', 'Mixing bowl', 'Wooden spoon', 'Serving bowl'],
    'french_toast': ['Skillet', 'Mixing bowl', 'Whisk', 'Spatula', 'Serving platter', 'Measuring cups'],
    'eggs_benedict': ['Sauce pan', 'Whisk', 'Slotted spoon', 'Toaster', 'Mixing bowl', 'Serving platter'],
    'breakfast_burrito': ['Skillet', 'Spatula', "Chef's knife", 'Mixing bowl', 'Cheese grater', 'Serving platter'],
    'smoothie_bowl': ['Blender', 'Mixing bowl', "Chef's knife", 'Measuring cups', 'Serving bowl', 'Spoon'],
    'avocado_toast': ['Toaster', "Chef's knife", 'Cutting board', 'Fork', 'Serving platter', 'Mixing bowl'],
    'breakfast_sandwich': ['Skillet', 'Toaster', "Chef's knife", 'Spatula', 'Serving platter', 'Cheese grater'],
    'huevos_rancheros': ['Skillet', "Chef's knife", 'Spatula', 'Serving platter', 'Ladle', 'Mixing bowl'],
    'shakshuka': ['Skillet', "Chef's knife", 'Wooden spoon', 'Lid', 'Serving bowl', 'Ladle'],
    'quiche': ['Pie dish', 'Oven', 'Whisk', 'Mixing bowl', "Chef's knife", 'Cheese grater'],
    'frittata': ['Oven-safe skillet', 'Oven', 'Whisk', 'Mixing bowl', "Chef's knife", 'Spatula'],
    'breakfast_hash': ['Skillet', "Chef's knife", 'Spatula', 'Cutting board', 'Serving bowl', 'Wooden spoon'],
    'crepes': ['Crepe pan', 'Mixing bowl', 'Whisk', 'Ladle', 'Spatula', 'Serving platter'],
    'bagels': ['Toaster', "Chef's knife", 'Cutting board', 'Butter knife', 'Serving platter', 'Cream cheese'],
    'breakfast_pizza': ['Pizza stone', 'Oven', "Chef's knife", 'Cheese grater', 'Rolling pin', 'Pizza cutter'],
    'porridge': ['Pot', 'Wooden spoon', 'Measuring cups', 'Ladle', 'Serving bowl', 'Whisk'],
    'oatmeal': ['Pot', 'Wooden spoon', 'Measuring cups', 'Ladle', 'Serving bowl', 'Mixing bowl'],
    'granola': ['Baking sheet', 'Oven', 'Mixing bowl', 'Wooden spoon', 'Measuring cups', 'Storage container'],
    'breakfast_tacos': ['Skillet', "Chef's knife", 'Spatula', 'Mixing bowl', 'Cheese grater', 'Serving platter'],
    'english_breakfast': ['Skillet', 'Tongs', "Chef's knife", 'Serving platter', 'Spatula', 'Multiple pans'],
    'breakfast_bowl': ['Mixing bowl', "Chef's knife", 'Skillet', 'Spatula', 'Rice cooker', 'Serving bowl'],
    'eggs_florentine': ['Sauce pan', 'Whisk', 'Slotted spoon', 'Toaster', 'Mixing bowl', 'Serving platter'],
    'breakfast_quesadilla': ['Skillet', 'Spatula', "Chef's knife", 'Cheese grater', 'Pizza cutter', 'Serving platter'],
    'chilaquiles': ['Skillet', "Chef's knife", 'Spatula', 'Mixing bowl', 'Cheese grater', 'Serving platter'],
    'breakfast_casserole': ['Baking dish', 'Oven', 'Whisk', 'Mixing bowl', "Chef's knife", 'Cheese grater'],
    'egg_muffins': ['Muffin tin', 'Oven', 'Whisk', 'Mixing bowl', "Chef's knife", 'Ladle'],
    'breakfast_sausage': ['Skillet', 'Tongs', 'Spatula', 'Serving platter', 'Paper towels', 'Cutting board'],
    
    # ==================== DESSERTS (35 recipes) ====================
    'cake': ['Cake pan', 'Oven', 'Mixing bowl', 'Electric mixer', 'Measuring cups', 'Cooling rack'],
    'cookies': ['Baking sheet', 'Oven', 'Mixing bowl', 'Cookie scoop', 'Cooling rack', 'Spatula'],
    'brownies': ['Brownie pan', 'Oven', 'Mixing bowl', 'Whisk', 'Spatula', 'Cooling rack'],
    'cheesecake': ['Springform pan', 'Oven', 'Electric mixer', 'Mixing bowl', 'Spatula', 'Cooling rack'],
    'pie': ['Pie dish', 'Oven', 'Rolling pin', 'Mixing bowl', 'Pastry cutter', 'Pie server'],
    'cupcakes': ['Muffin tin', 'Oven', 'Electric mixer', 'Mixing bowl', 'Cookie scoop', 'Piping bag'],
    'ice_cream': ['Ice cream maker', 'Mixing bowl', 'Whisk', 'Measuring cups', 'Storage container', 'Ice cream scoop'],
    'tiramisu': ['Mixing bowl', 'Whisk', 'Baking dish', 'Spatula', 'Measuring cups', 'Serving spoon'],
    'creme_brulee': ['Ramekins', 'Oven', 'Whisk', 'Mixing bowl', 'Torch', 'Baking dish'],
    'macarons': ['Baking sheet', 'Oven', 'Piping bag', 'Mixing bowl', 'Electric mixer', 'Parchment paper'],
    'pudding': ['Pot', 'Whisk', 'Measuring cups', 'Mixing bowl', 'Serving bowl', 'Ladle'],
    'mousse': ['Mixing bowl', 'Whisk', 'Electric mixer', 'Serving glasses', 'Spatula', 'Piping bag'],
    'donuts': ['Deep fryer', 'Mixing bowl', 'Donut cutter', 'Tongs', 'Paper towels', 'Cooling rack'],
    'apple_pie': ['Pie dish', 'Oven', 'Rolling pin', "Chef's knife", 'Mixing bowl', 'Pastry cutter'],
    'pumpkin_pie': ['Pie dish', 'Oven', 'Mixing bowl', 'Whisk', 'Can opener', 'Pie server'],
    'pecan_pie': ['Pie dish', 'Oven', 'Mixing bowl', 'Whisk', 'Rolling pin', 'Pie server'],
    'lemon_bars': ['Baking dish', 'Oven', 'Mixing bowl', 'Whisk', 'Zester', 'Cooling rack'],
    'chocolate_cake': ['Cake pan', 'Oven', 'Electric mixer', 'Mixing bowl', 'Measuring cups', 'Cooling rack'],
    'carrot_cake': ['Cake pan', 'Oven', 'Grater', 'Mixing bowl', 'Electric mixer', 'Cooling rack'],
    'red_velvet_cake': ['Cake pan', 'Oven', 'Electric mixer', 'Mixing bowl', 'Measuring cups', 'Cooling rack'],
    'pound_cake': ['Loaf pan', 'Oven', 'Electric mixer', 'Mixing bowl', 'Measuring cups', 'Cooling rack'],
    'angel_food_cake': ['Tube pan', 'Oven', 'Electric mixer', 'Mixing bowl', 'Spatula', 'Cooling rack'],
    'bundt_cake': ['Bundt pan', 'Oven', 'Electric mixer', 'Mixing bowl', 'Measuring cups', 'Cooling rack'],
    'layer_cake': ['Round cake pan', 'Oven', 'Electric mixer', 'Mixing bowl', 'Cake leveler', 'Cooling rack'],
    'tres_leches': ['Baking dish', 'Oven', 'Mixing bowl', 'Whisk', 'Fork', 'Serving spoon'],
    'panna_cotta': ['Sauce pan', 'Whisk', 'Ramekins', 'Measuring cups', 'Ladle', 'Serving spoon'],
    'flan': ['Baking dish', 'Oven', 'Whisk', 'Sauce pan', 'Ramekins', 'Serving platter'],
    'baklava': ['Baking dish', 'Oven', 'Pastry brush', "Chef's knife", 'Sauce pan', 'Cooling rack'],
    'eclairs': ['Baking sheet', 'Oven', 'Piping bag', 'Sauce pan', 'Whisk', 'Cooling rack'],
    'profiteroles': ['Baking sheet', 'Oven', 'Piping bag', 'Sauce pan', 'Whisk', 'Serving platter'],
    'churros': ['Deep fryer', 'Piping bag', 'Tongs', 'Sauce pan', 'Paper towels', 'Serving platter'],
    'beignets': ['Deep fryer', 'Mixing bowl', 'Rolling pin', 'Tongs', 'Paper towels', 'Serving platter'],
    'cannoli': ['Deep fryer', 'Mixing bowl', 'Rolling pin', 'Cannoli tubes', 'Piping bag', 'Serving platter'],
    'sorbet': ['Ice cream maker', 'Blender', 'Mixing bowl', 'Storage container', 'Ice cream scoop', 'Serving bowl'],
    'pavlova': ['Baking sheet', 'Oven', 'Electric mixer', 'Mixing bowl', 'Piping bag', 'Serving platter'],
    
    # ==================== SALADS (25 recipes) ====================
    'salad': ['Salad bowl', "Chef's knife", 'Cutting board', 'Salad spinner', 'Tongs', 'Serving bowl'],
    'caesar_salad': ['Salad bowl', "Chef's knife", 'Whisk', 'Cheese grater', 'Tongs', 'Serving bowl'],
    'greek_salad': ['Salad bowl', "Chef's knife", 'Cutting board', 'Mixing bowl', 'Tongs', 'Serving bowl'],
    'cobb_salad': ['Salad bowl', "Chef's knife", 'Cutting board', 'Egg slicer', 'Tongs', 'Serving bowl'],
    'caprese_salad': ['Cutting board', "Chef's knife", 'Serving platter', 'Mixing bowl', 'Measuring spoons', 'Spoon'],
    'taco_salad': ['Salad bowl', "Chef's knife", 'Skillet', 'Spatula', 'Cheese grater', 'Serving bowl'],
    'pasta_salad': ['Mixing bowl', 'Pasta pot', 'Colander', "Chef's knife", 'Whisk', 'Serving bowl'],
    'potato_salad': ['Mixing bowl', 'Pot', "Chef's knife", 'Potato masher', 'Whisk', 'Serving bowl'],
    'coleslaw': ['Mixing bowl', "Chef's knife", 'Grater', 'Whisk', 'Tongs', 'Serving bowl'],
    'waldorf_salad': ['Mixing bowl', "Chef's knife", 'Apple corer', 'Whisk', 'Serving bowl', 'Cutting board'],
    'nicoise_salad': ['Salad bowl', "Chef's knife", 'Pot', 'Whisk', 'Can opener', 'Serving bowl'],
    'chef_salad': ['Salad bowl', "Chef's knife", 'Cutting board', 'Egg slicer', 'Cheese grater', 'Serving bowl'],
    'garden_salad': ['Salad bowl', "Chef's knife", 'Cutting board', 'Salad spinner', 'Tongs', 'Serving bowl'],
    'spinach_salad': ['Salad bowl', "Chef's knife", 'Salad spinner', 'Whisk', 'Tongs', 'Serving bowl'],
    'asian_salad': ['Salad bowl', "Chef's knife", 'Whisk', 'Grater', 'Tongs', 'Serving bowl'],
    'quinoa_salad': ['Mixing bowl', 'Pot', "Chef's knife", 'Strainer', 'Whisk', 'Serving bowl'],
    'fruit_salad': ['Mixing bowl', "Chef's knife", 'Cutting board', 'Melon baller', 'Serving bowl', 'Spoon'],
    'tabbouleh': ['Mixing bowl', "Chef's knife", 'Cutting board', 'Measuring cups', 'Wooden spoon', 'Serving bowl'],
    'fattoush': ['Salad bowl', "Chef's knife", 'Cutting board', 'Whisk', 'Tongs', 'Serving bowl'],
    'panzanella': ['Salad bowl', "Chef's knife", 'Cutting board', 'Toaster', 'Mixing bowl', 'Serving bowl'],
    'wedge_salad': ['Cutting board', "Chef's knife", 'Serving platter', 'Whisk', 'Mixing bowl', 'Spoon'],
    'kale_salad': ['Salad bowl', "Chef's knife", 'Salad spinner', 'Whisk', 'Tongs', 'Serving bowl'],
    'arugula_salad': ['Salad bowl', "Chef's knife", 'Whisk', 'Cheese grater', 'Tongs', 'Serving bowl'],
    'beet_salad': ['Salad bowl', "Chef's knife", 'Pot', 'Peeler', 'Whisk', 'Serving bowl'],
    'watermelon_salad': ['Mixing bowl', "Chef's knife", 'Cutting board', 'Whisk', 'Serving bowl', 'Spoon'],
    
    # ==================== SANDWICHES (20 recipes) ====================
    'sandwich': ["Chef's knife", 'Cutting board', 'Toaster', 'Serving platter', 'Spatula', 'Butter knife'],
    'grilled_cheese': ['Skillet', 'Spatula', 'Cheese grater', "Chef's knife", 'Serving platter', 'Cutting board'],
    'club_sandwich': ["Chef's knife", 'Cutting board', 'Toaster', 'Serving platter', 'Toothpicks', 'Spatula'],
    'blt_sandwich': ["Chef's knife", 'Cutting board', 'Toaster', 'Skillet', 'Serving platter', 'Paper towels'],
    'reuben_sandwich': ['Skillet', 'Spatula', "Chef's knife", 'Cheese grater', 'Serving platter', 'Tongs'],
    'panini': ['Panini press', "Chef's knife", 'Cutting board', 'Cheese grater', 'Serving platter', 'Spatula'],
    'sub_sandwich': ["Chef's knife", 'Cutting board', 'Bread knife', 'Serving platter', 'Mixing bowl', 'Spoon'],
    'wrap': ["Chef's knife", 'Cutting board', 'Mixing bowl', 'Serving platter', 'Spatula', 'Spoon'],
    'burger': ['Grill pan', 'Spatula', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving platter'],
    'pulled_pork_sandwich': ['Slow cooker', "Chef's knife", 'Tongs', 'Fork', 'Mixing bowl', 'Serving platter'],
    'chicken_sandwich': ['Skillet', 'Spatula', "Chef's knife", 'Toaster', 'Serving platter', 'Tongs'],
    'fish_sandwich': ['Skillet', 'Fish spatula', "Chef's knife", 'Toaster', 'Serving platter', 'Mixing bowl'],
    'veggie_sandwich': ["Chef's knife", 'Cutting board', 'Toaster', 'Serving platter', 'Mixing bowl', 'Spoon'],
    'meatball_sub': ['Sauce pan', "Chef's knife", 'Toaster', 'Cheese grater', 'Serving platter', 'Ladle'],
    'french_dip': ['Roasting pan', 'Oven', "Chef's knife", 'Ladle', 'Serving platter', 'Au jus container'],
    'sloppy_joe': ['Skillet', "Chef's knife", 'Wooden spoon', 'Mixing bowl', 'Ladle', 'Serving platter'],
    'turkey_sandwich': ["Chef's knife", 'Cutting board', 'Toaster', 'Serving platter', 'Butter knife', 'Spoon'],
    'tuna_melt': ['Skillet', 'Spatula', 'Can opener', 'Mixing bowl', 'Cheese grater', 'Serving platter'],
    'breakfast_sandwich': ['Skillet', 'Toaster', "Chef's knife", 'Spatula', 'Cheese grater', 'Serving platter'],
    'banh_mi': ["Chef's knife", 'Cutting board', 'Toaster', 'Mixing bowl', 'Serving platter', 'Peeler'],
    
    # ==================== APPETIZERS (30 recipes) ====================
    'mozzarella_sticks': ['Deep fryer', 'Mixing bowl', 'Tongs', 'Paper towels', 'Serving platter', 'Dipping bowl'],
    'chicken_wings': ['Baking sheet', 'Oven', 'Mixing bowl', 'Tongs', 'Wire rack', 'Serving platter'],
    'deviled_eggs': ['Pot', 'Mixing bowl', 'Egg slicer', 'Piping bag', "Chef's knife", 'Serving platter'],
    'bruschetta': ['Baking sheet', 'Oven', "Chef's knife", 'Cutting board', 'Mixing bowl', 'Serving platter'],
    'nachos': ['Baking sheet', 'Oven', "Chef's knife", 'Cheese grater', 'Serving platter', 'Mixing bowl'],
    'spring_rolls': ['Deep fryer', "Chef's knife", 'Mixing bowl', 'Tongs', 'Paper towels', 'Serving platter'],
    'samosas': ['Deep fryer', 'Rolling pin', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving platter'],
    'empanadas': ['Baking sheet', 'Oven', 'Rolling pin', "Chef's knife", 'Fork', 'Serving platter'],
    'quesadilla': ['Skillet', 'Spatula', "Chef's knife", 'Cheese grater', 'Pizza cutter', 'Serving platter'],
    'guacamole': ['Mixing bowl', "Chef's knife", 'Cutting board', 'Fork', 'Measuring spoons', 'Serving bowl'],
    'salsa': ['Food processor', "Chef's knife", 'Cutting board', 'Mixing bowl', 'Storage container', 'Serving bowl'],
    'hummus': ['Food processor', 'Mixing bowl', 'Measuring spoons', 'Spatula', 'Storage container', 'Serving bowl'],
    'spinach_dip': ['Mixing bowl', "Chef's knife", 'Oven', 'Baking dish', 'Wooden spoon', 'Serving bowl'],
    'cheese_board': ['Cheese board', "Chef's knife", 'Cheese slicer', 'Small bowls', 'Serving utensils', 'Crackers'],
    'stuffed_mushrooms': ['Baking sheet', 'Oven', "Chef's knife", 'Mixing bowl', 'Small spoon', 'Serving platter'],
    'jalapeño_poppers': ['Baking sheet', 'Oven', "Chef's knife", 'Mixing bowl', 'Piping bag', 'Serving platter'],
    'potato_skins': ['Baking sheet', 'Oven', "Chef's knife", 'Cheese grater', 'Small spoon', 'Serving platter'],
    'pigs_in_blanket': ['Baking sheet', 'Oven', 'Rolling pin', "Chef's knife", 'Pastry brush', 'Serving platter'],
    'shrimp_cocktail': ['Pot', 'Mixing bowl', "Chef's knife", 'Ice bucket', 'Serving platter', 'Small bowls'],
    'crab_cakes': ['Skillet', 'Mixing bowl', "Chef's knife", 'Spatula', 'Serving platter', 'Fork'],
    'chicken_satay': ['Grill', 'Bamboo skewers', "Chef's knife", 'Mixing bowl', 'Basting brush', 'Serving platter'],
    'beef_skewers': ['Grill', 'Metal skewers', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving platter'],
    'caprese_skewers': ['Bamboo skewers', "Chef's knife", 'Cutting board', 'Serving platter', 'Small bowls', 'Spoon'],
    'bacon_wrapped': ['Baking sheet', 'Oven', "Chef's knife", 'Toothpicks', 'Tongs', 'Serving platter'],
    'fried_pickles': ['Deep fryer', 'Mixing bowl', 'Tongs', 'Paper towels', 'Serving platter', 'Dipping bowl'],
    'onion_rings': ['Deep fryer', 'Mixing bowl', "Chef's knife", 'Tongs', 'Paper towels', 'Serving platter'],
    'pretzels': ['Baking sheet', 'Oven', 'Pot', 'Mixing bowl', 'Slotted spoon', 'Cooling rack'],
    'garlic_bread': ['Baking sheet', 'Oven', "Chef's knife", 'Mixing bowl', 'Pastry brush', 'Serving basket'],
    'cheese_fondue': ['Fondue pot', 'Cheese grater', 'Cutting board', "Chef's knife", 'Fondue forks', 'Serving platter'],
    'meat_and_cheese_platter': ['Serving platter', "Chef's knife", 'Cheese slicer', 'Small bowls', 'Serving utensils', 'Cutting board'],
    
    # ==================== SIDE DISHES (20 recipes) ====================
    'mashed_potatoes': ['Pot', 'Potato masher', "Chef's knife", 'Mixing bowl', 'Whisk', 'Serving bowl'],
    'french_fries': ['Deep fryer', "Chef's knife", 'Cutting board', 'Tongs', 'Paper towels', 'Serving basket'],
    'roasted_vegetables': ['Baking sheet', 'Oven', "Chef's knife", 'Mixing bowl', 'Spatula', 'Serving platter'],
    'steamed_vegetables': ['Steamer', "Chef's knife", 'Cutting board', 'Serving bowl', 'Tongs', 'Bamboo steamer'],
    'coleslaw': ['Mixing bowl', "Chef's knife", 'Grater', 'Whisk', 'Tongs', 'Serving bowl'],
    'corn_on_cob': ['Pot', 'Tongs', "Chef's knife", 'Butter dish', 'Serving platter', 'Corn holders'],
    'baked_beans': ['Pot', 'Wooden spoon', 'Can opener', 'Mixing bowl', 'Ladle', 'Serving bowl'],
    'mac_and_cheese': ['Pot', 'Cheese grater', 'Whisk', 'Baking dish', 'Oven', 'Serving bowl'],
    'green_beans': ['Pot', "Chef's knife", 'Colander', 'Skillet', 'Tongs', 'Serving bowl'],
    'asparagus': ['Baking sheet', 'Oven', "Chef's knife", 'Tongs', 'Mixing bowl', 'Serving platter'],
    'brussels_sprouts': ['Baking sheet', 'Oven', "Chef's knife", 'Mixing bowl', 'Spatula', 'Serving bowl'],
    'sweet_potato': ['Baking sheet', 'Oven', "Chef's knife", 'Fork', 'Butter knife', 'Serving platter'],
    'onion_rings': ['Deep fryer', "Chef's knife", 'Mixing bowl', 'Tongs', 'Paper towels', 'Serving basket'],
    'garlic_bread': ['Baking sheet', 'Oven', "Chef's knife", 'Mixing bowl', 'Pastry brush', 'Serving basket'],
    'dinner_rolls': ['Baking sheet', 'Oven', 'Mixing bowl', 'Pastry brush', 'Bread basket', 'Kitchen towel'],
    'cornbread': ['Baking dish', 'Oven', 'Mixing bowl', 'Whisk', 'Spatula', 'Serving basket'],
    'stuffing': ['Baking dish', 'Oven', 'Mixing bowl', "Chef's knife", 'Wooden spoon', 'Serving bowl'],
    'gravy': ['Sauce pan', 'Whisk', 'Ladle', 'Measuring cups', 'Strainer', 'Gravy boat'],
    'cranberry_sauce': ['Sauce pan', 'Wooden spoon', 'Measuring cups', 'Can opener', 'Serving bowl', 'Ladle'],
    'potato_wedges': ['Baking sheet', 'Oven', "Chef's knife", 'Mixing bowl', 'Spatula', 'Serving basket'],
    
    # ==================== SNACKS (15 recipes) ====================
    'popcorn': ['Popcorn maker', 'Large bowl', 'Measuring cups', 'Butter dish', 'Serving bowl', 'Spoon'],
    'trail_mix': ['Mixing bowl', 'Measuring cups', 'Storage container', 'Wooden spoon', 'Serving bowl', 'Small bowls'],
    'granola_bars': ['Baking dish', 'Oven', 'Mixing bowl', "Chef's knife", 'Parchment paper', 'Cooling rack'],
    'energy_balls': ['Food processor', 'Mixing bowl', 'Cookie scoop', 'Storage container', 'Measuring cups', 'Spoon'],
    'protein_bars': ['Baking dish', 'Blender', 'Mixing bowl', 'Spatula', "Chef's knife", 'Storage container'],
    'roasted_nuts': ['Baking sheet', 'Oven', 'Mixing bowl', 'Wooden spoon', 'Storage container', 'Cooling rack'],
    'kale_chips': ['Baking sheet', 'Oven', "Chef's knife", 'Mixing bowl', 'Tongs', 'Serving bowl'],
    'pita_chips': ['Baking sheet', 'Oven', "Chef's knife", 'Pastry brush', 'Serving bowl', 'Storage container'],
    'cheese_crackers': ['Baking sheet', 'Oven', 'Rolling pin', 'Cookie cutter', 'Cooling rack', 'Storage container'],
    'veggie_sticks': ['Cutting board', "Chef's knife", 'Peeler', 'Storage container', 'Serving platter', 'Dipping bowl'],
    'fruit_leather': ['Blender', 'Baking sheet', 'Oven', 'Parchment paper', "Chef's knife", 'Storage container'],
    'candied_nuts': ['Sauce pan', 'Baking sheet', 'Wooden spoon', 'Parchment paper', 'Cooling rack', 'Storage container'],
    'chocolate_bark': ['Baking sheet', 'Microwave', "Chef's knife", 'Spatula', 'Parchment paper', 'Storage container'],
    'rice_crispy_treats': ['Baking dish', 'Pot', 'Spatula', 'Measuring cups', "Chef's knife", 'Serving platter'],
    'puppy_chow': ['Large bowl', 'Microwave', 'Measuring cups', 'Wooden spoon', 'Storage container', 'Sifter'],
    
    'default': []  # Empty list triggers fallback message
}


# ==================== EQUIPMENT DATABASE (700+ Items) ====================
EQUIPMENT_PRICES = {
    # ==================== KNIVES & CUTTING TOOLS (50 items) ====================
    "chef's knife": 29.99, "knife": 29.99, "paring knife": 12.99, "bread knife": 24.99,
    "carving knife": 34.99, "utility knife": 15.99, "boning knife": 27.99, "cleaver": 39.99,
    "santoku knife": 32.99, "nakiri knife": 36.99, "fillet knife": 28.99, "steak knife": 49.99,
    "butter knife": 8.99, "dinner knife": 12.99, "cheese knife": 14.99, "oyster knife": 16.99,
    "palette knife": 11.99, "cake knife": 19.99, "serrated knife": 22.99, "ceramic knife": 24.99,
    "knife sharpener": 34.99, "electric knife sharpener": 79.99, "knife block": 44.99,
    "magnetic knife strip": 29.99, "knife guards": 12.99, "kitchen shears": 18.99,
    "poultry shears": 22.99, "herb scissors": 16.99, "pizza cutter": 8.99, "rotary cutter": 14.99,
    "mandoline slicer": 45.99, "vegetable slicer": 32.99, "julienne peeler": 9.99, "peeler": 6.99,
    "y-peeler": 8.99, "serrated peeler": 7.99, "apple peeler": 19.99, "potato peeler": 6.99,
    "citrus peeler": 5.99, "tomato knife": 13.99, "bagel slicer": 16.99, "egg slicer": 7.99,
    "strawberry huller": 5.99, "pineapple corer": 12.99, "avocado slicer": 9.99, "banana slicer": 6.99,
    "mushroom slicer": 8.99, "onion chopper": 19.99, "vegetable chopper": 24.99, "food chopper": 29.99,
    
    # ==================== CUTTING BOARDS (30 items) ====================
    "cutting board": 19.99, "chopping board": 19.99, "bamboo cutting board": 24.99,
    "plastic cutting board": 12.99, "wooden cutting board": 22.99, "glass cutting board": 16.99,
    "marble cutting board": 39.99, "acacia cutting board": 28.99, "teak cutting board": 34.99,
    "maple cutting board": 29.99, "walnut cutting board": 32.99, "oak cutting board": 26.99,
    "flexible cutting board": 9.99, "silicone cutting board": 14.99, "composite cutting board": 18.99,
    "end grain cutting board": 49.99, "edge grain cutting board": 36.99, "butcher block": 89.99,
    "carving board": 34.99, "serving board": 28.99, "charcuterie board": 42.99,
    "cheese cutting board": 32.99, "bread cutting board": 24.99, "fish cutting board": 26.99,
    "meat cutting board": 29.99, "vegetable cutting board": 19.99, "fruit cutting board": 17.99,
    "cutting board set": 54.99, "cutting board oil": 12.99, "cutting board cream": 9.99,
    
    # ==================== POTS & PANS (80 items) ====================
    "pot": 44.99, "large pot": 59.99, "stockpot": 69.99, "soup pot": 54.99,
    "pasta pot": 64.99, "lobster pot": 79.99, "canning pot": 74.99, "double boiler": 42.99,
    "milk pot": 29.99, "sauce pot": 39.99, "saucepan": 39.99, "small saucepan": 29.99,
    "medium saucepan": 44.99, "large saucepan": 54.99, "covered saucepan": 49.99,
    "pan": 39.99, "frying pan": 42.99, "skillet": 45.99, "non-stick pan": 49.99,
    "stainless steel pan": 54.99, "copper pan": 89.99, "aluminum pan": 34.99,
    "cast iron skillet": 54.99, "cast iron pan": 49.99, "enameled cast iron": 79.99,
    "carbon steel pan": 59.99, "ceramic pan": 44.99, "granite pan": 52.99,
    "wok": 49.99, "carbon steel wok": 59.99, "flat bottom wok": 54.99, "round bottom wok": 52.99,
    "electric wok": 89.99, "wok ring": 14.99, "wok spatula": 9.99, "wok ladle": 12.99,
    "grill pan": 52.99, "griddle": 44.99, "electric griddle": 79.99, "stovetop griddle": 39.99,
    "crepe pan": 34.99, "omelet pan": 29.99, "egg pan": 24.99, "frittata pan": 32.99,
    "fish pan": 42.99, "paella pan": 64.99, "tagine": 54.99, "braiser": 69.99,
    "saute pan": 49.99, "saucier": 54.99, "chef's pan": 59.99, "everyday pan": 64.99,
    "roasting pan": 45.99, "roaster": 52.99, "covered roaster": 64.99, "oval roaster": 56.99,
    "turkey roaster": 74.99, "roasting rack": 19.99, "v-rack": 24.99, "flat rack": 16.99,
    "dutch oven": 89.99, "french oven": 94.99, "enameled dutch oven": 119.99,
    "casserole dish": 34.99, "covered casserole": 44.99, "oval casserole": 39.99,
    "baking dish": 24.99, "glass baking dish": 29.99, "ceramic baking dish": 32.99,
    "lasagna pan": 28.99, "brownie pan": 22.99, "au gratin dish": 26.99,
    "pot set": 149.99, "pan set": 129.99, "cookware set": 199.99, "starter cookware set": 99.99,
    
    # ==================== MAJOR APPLIANCES (40 items) ====================
    "pressure cooker": 89.99, "electric pressure cooker": 119.99, "instant pot": 129.99,
    "slow cooker": 79.99, "programmable slow cooker": 99.99, "multi-cooker": 149.99,
    "rice cooker": 74.99, "fuzzy logic rice cooker": 129.99, "induction rice cooker": 189.99,
    "air fryer": 129.99, "digital air fryer": 149.99, "air fryer oven": 199.99,
    "deep fryer": 89.99, "electric deep fryer": 109.99, "turkey fryer": 179.99,
    "electric kettle": 34.99, "variable temp kettle": 79.99, "gooseneck kettle": 64.99,
    "tea kettle": 29.99, "stovetop kettle": 39.99, "whistling kettle": 34.99,
    "coffee maker": 79.99, "drip coffee maker": 89.99, "programmable coffee maker": 119.99,
    "espresso machine": 299.99, "super-automatic espresso": 899.99, "manual espresso": 199.99,
    "french press": 24.99, "pour over coffee": 34.99, "cold brew maker": 44.99,
    "toaster": 39.99, "2-slice toaster": 29.99, "4-slice toaster": 49.99,
    "toaster oven": 89.99, "convection toaster oven": 129.99, "countertop oven": 199.99,
    "microwave": 149.99, "microwave oven": 199.99, "over-range microwave": 299.99,
    
    # ==================== SMALL APPLIANCES (80 items) ====================
    "blender": 79.99, "high-speed blender": 299.99, "personal blender": 39.99,
    "immersion blender": 34.99, "hand blender": 29.99, "stick blender": 42.99,
    "food processor": 89.99, "mini food processor": 44.99, "full-size food processor": 149.99,
    "stand mixer": 279.99, "tilt-head mixer": 249.99, "bowl-lift mixer": 329.99,
    "hand mixer": 39.99, "electric mixer": 49.99, "handheld mixer": 34.99,
    "juicer": 99.99, "citrus juicer": 29.99, "masticating juicer": 199.99,
    "centrifugal juicer": 89.99, "cold press juicer": 299.99, "electric juicer": 79.99,
    "waffle maker": 44.99, "belgian waffle maker": 54.99, "flip waffle maker": 64.99,
    "sandwich maker": 34.99, "panini press": 79.99, "grill press": 24.99,
    "electric grill": 99.99, "indoor grill": 89.99, "smokeless grill": 129.99,
    "contact grill": 69.99, "open grill": 79.99, "reversible grill": 109.99,
    "griddle": 44.99, "electric griddle": 79.99, "pancake griddle": 39.99,
    "crepe maker": 49.99, "electric crepe maker": 59.99, "tortilla maker": 54.99,
    "pizza maker": 89.99, "pizza oven": 399.99, "outdoor pizza oven": 599.99,
    "bread maker": 149.99, "automatic bread maker": 179.99, "programmable bread maker": 199.99,
    "pasta maker": 129.99, "electric pasta maker": 199.99, "manual pasta machine": 79.99,
    "ice cream maker": 89.99, "compressor ice cream maker": 249.99, "frozen yogurt maker": 79.99,
    "popcorn maker": 29.99, "hot air popper": 34.99, "stovetop popcorn": 24.99,
    "cotton candy maker": 44.99, "sno-cone maker": 39.99, "donut maker": 49.99,
    "egg cooker": 29.99, "electric egg cooker": 34.99, "egg boiler": 24.99,
    "sous vide": 149.99, "immersion circulator": 179.99, "sous vide container": 34.99,
    "dehydrator": 89.99, "food dehydrator": 119.99, "jerky maker": 79.99,
    "yogurt maker": 44.99, "greek yogurt maker": 54.99, "fermentation crock": 64.99,
    "meat grinder": 89.99, "electric meat grinder": 149.99, "manual meat grinder": 54.99,
    "sausage stuffer": 79.99, "meat slicer": 129.99, "deli slicer": 179.99,
    "vacuum sealer": 89.99, "food vacuum sealer": 119.99, "chamber vacuum sealer": 399.99,
    "can opener": 12.99, "electric can opener": 29.99, "manual can opener": 8.99,
    "jar opener": 9.99, "bottle opener": 6.99, "wine opener": 14.99,
    "electric wine opener": 34.99, "corkscrew": 14.99, "lever corkscrew": 24.99,
    
    # ==================== MIXING & PREP TOOLS (100 items) ====================
    "mixing bowl": 14.99, "bowl": 8.99, "salad bowl": 16.99, "prep bowl": 12.99,
    "nesting bowls": 34.99, "stainless steel bowls": 29.99, "glass bowls": 24.99,
    "ceramic bowls": 32.99, "plastic bowls": 16.99, "melamine bowls": 22.99,
    "mixing bowl set": 39.99, "prep bowl set": 29.99, "serving bowl set": 44.99,
    "measuring cups": 11.99, "dry measuring cups": 9.99, "liquid measuring cup": 9.99,
    "adjustable measuring cup": 14.99, "stainless measuring cups": 16.99, "glass measuring cup": 12.99,
    "measuring spoons": 7.99, "magnetic measuring spoons": 12.99, "oval measuring spoons": 9.99,
    "kitchen scale": 24.99, "digital scale": 34.99, "food scale": 29.99,
    "baker's scale": 44.99, "mechanical scale": 19.99, "portion scale": 39.99,
    "timer": 12.99, "digital timer": 16.99, "magnetic timer": 14.99,
    "triple timer": 24.99, "hourglass timer": 9.99, "countdown timer": 19.99,
    "whisk": 8.99, "balloon whisk": 10.99, "flat whisk": 9.99,
    "french whisk": 12.99, "mini whisk": 6.99, "coil whisk": 11.99,
    "silicone whisk": 14.99, "stainless whisk": 9.99, "dough whisk": 13.99,
    "electric whisk": 29.99, "rotary whisk": 16.99, "milk frother": 19.99,
    "wooden spoon": 5.99, "spoon": 4.99, "slotted spoon": 6.99,
    "serving spoon": 7.99, "soup spoon": 8.99, "spaghetti spoon": 9.99,
    "risotto spoon": 12.99, "mixing spoon": 7.99, "tasting spoon": 5.99,
    "bamboo spoon": 8.99, "silicone spoon": 9.99, "nylon spoon": 6.99,
    "ladle": 7.99, "soup ladle": 9.99, "gravy ladle": 8.99,
    "sauce ladle": 10.99, "punch ladle": 14.99, "skimmer ladle": 11.99,
    "spatula": 6.99, "rubber spatula": 7.99, "silicone spatula": 8.99,
    "offset spatula": 8.99, "fish spatula": 9.99, "turner": 7.99,
    "slotted turner": 8.99, "flexible turner": 9.99, "nylon turner": 7.99,
    "metal spatula": 6.99, "heat-resistant spatula": 11.99, "jar spatula": 5.99,
    "frosting spatula": 9.99, "icing spatula": 8.99, "palette knife": 11.99,
    "tongs": 9.99, "kitchen tongs": 11.99, "silicone tongs": 12.99,
    "locking tongs": 10.99, "salad tongs": 8.99, "serving tongs": 9.99,
    "grilling tongs": 13.99, "pasta tongs": 10.99, "ice tongs": 7.99,
    "fork": 5.99, "pasta fork": 6.99, "carving fork": 12.99,
    "serving fork": 7.99, "salad fork": 6.99, "meat fork": 9.99,
    "basting brush": 5.99, "pastry brush": 6.99, "silicone brush": 8.99,
    "natural bristle brush": 7.99, "barbeque brush": 9.99, "marinade brush": 7.99,
    "potato masher": 14.99, "bean masher": 12.99, "avocado masher": 9.99,
    "ricer": 19.99, "potato ricer": 22.99, "food mill": 34.99,
    "mortar and pestle": 22.99, "marble mortar": 34.99, "granite mortar": 29.99,
    "wooden mortar": 19.99, "molcajete": 39.99, "spice grinder": 29.99,
    "pepper mill": 24.99, "salt grinder": 19.99, "pepper grinder": 22.99,
    "electric pepper mill": 34.99, "manual pepper mill": 16.99, "adjustable grinder": 26.99,
    
    # ==================== STRAINERS & COLANDERS (30 items) ====================
    "colander": 16.99, "mesh colander": 19.99, "stainless colander": 24.99,
    "silicone colander": 18.99, "collapsible colander": 22.99, "over-sink colander": 29.99,
    "strainer": 14.99, "fine mesh strainer": 17.99, "spider strainer": 19.99,
    "conical strainer": 24.99, "chinois": 34.99, "china cap": 29.99,
    "sieve": 13.99, "flour sifter": 16.99, "powdered sugar sifter": 14.99,
    "double mesh sieve": 22.99, "splash guard": 19.99, "grease strainer": 16.99,
    "pasta strainer": 15.99, "pot strainer": 18.99, "clip-on strainer": 12.99,
    "salad spinner": 24.99, "large salad spinner": 34.99, "mini salad spinner": 19.99,
    "vegetable spinner": 26.99, "lettuce spinner": 22.99, "herb spinner": 18.99,
    "splatter screen": 14.99, "grease splatter guard": 16.99, "mesh splatter": 12.99,
    
    # ==================== GRATERS & ZESTERS (25 items) ====================
    "cheese grater": 12.99, "grater": 11.99, "box grater": 14.99,
    "4-sided grater": 16.99, "6-sided grater": 19.99, "rotary grater": 22.99,
    "flat grater": 9.99, "handheld grater": 11.99, "coarse grater": 10.99,
    "fine grater": 12.99, "nutmeg grater": 8.99, "ginger grater": 9.99,
    "microplane": 13.99, "zester": 9.99, "citrus zester": 11.99,
    "lemon zester": 10.99, "orange zester": 10.99, "channel knife": 7.99,
    "rasp grater": 12.99, "parmesan grater": 14.99, "chocolate grater": 11.99,
    "coconut grater": 16.99, "garlic grater": 8.99, "truffle grater": 24.99,
    "garlic press": 11.99, "aluminum garlic press": 14.99, "stainless garlic press": 16.99,
    
    # ==================== BAKING EQUIPMENT (120 items) ====================
    "baking sheet": 16.99, "cookie sheet": 14.99, "half sheet pan": 18.99,
    "quarter sheet pan": 14.99, "jelly roll pan": 16.99, "rimmed baking sheet": 19.99,
    "insulated baking sheet": 24.99, "non-stick baking sheet": 22.99, "perforated pan": 19.99,
    "muffin tin": 18.99, "cupcake pan": 16.99, "12-cup muffin tin": 19.99,
    "24-cup mini muffin": 22.99, "6-cup jumbo muffin": 21.99, "silicone muffin pan": 24.99,
    "non-stick muffin tin": 20.99, "texas muffin pan": 23.99, "popover pan": 26.99,
    "cake pan": 19.99, "round cake pan": 16.99, "square cake pan": 17.99,
    "rectangular cake pan": 20.99, "heart cake pan": 18.99, "star cake pan": 19.99,
    "number cake pan": 22.99, "letter cake pan": 22.99, "character cake pan": 24.99,
    "springform pan": 22.99, "cheesecake pan": 24.99, "loose bottom pan": 21.99,
    "bundt pan": 24.99, "mini bundt pan": 19.99, "fluted bundt": 26.99,
    "nordic ware bundt": 34.99, "shaped bundt pan": 29.99, "silicone bundt": 22.99,
    "loaf pan": 14.99, "bread pan": 16.99, "pullman loaf pan": 34.99,
    "mini loaf pan": 19.99, "glass loaf pan": 18.99, "ceramic loaf pan": 21.99,
    "pie dish": 16.99, "pie pan": 15.99, "deep dish pie pan": 19.99,
    "glass pie dish": 18.99, "ceramic pie dish": 21.99, "disposable pie pan": 8.99,
    "tart pan": 19.99, "fluted tart pan": 22.99, "removable bottom tart": 24.99,
    "mini tart pans": 26.99, "tartlet pans": 29.99, "quiche pan": 21.99,
    "pizza pan": 16.99, "perforated pizza pan": 19.99, "deep dish pizza": 22.99,
    "pizza stone": 34.99, "cordierite pizza stone": 44.99, "steel pizza stone": 79.99,
    "pizza peel": 29.99, "wooden pizza peel": 34.99, "aluminum pizza peel": 39.99,
    "rolling pin": 14.99, "french rolling pin": 19.99, "marble rolling pin": 24.99,
    "tapered rolling pin": 16.99, "adjustable rolling pin": 22.99, "silicone rolling pin": 18.99,
    "pastry cutter": 8.99, "dough cutter": 9.99, "bench scraper": 9.99,
    "dough scraper": 6.99, "bowl scraper": 4.99, "flexible scraper": 5.99,
    "pastry blender": 11.99, "dough blender": 10.99, "pastry mixer": 12.99,
    "cookie cutter set": 12.99, "cookie cutters": 9.99, "shaped cookie cutters": 14.99,
    "christmas cookie cutters": 16.99, "holiday cookie cutters": 15.99, "alphabet cutters": 19.99,
    "cookie scoop": 8.99, "ice cream scoop": 9.99, "portion scoop": 7.99,
    "small cookie scoop": 6.99, "medium cookie scoop": 8.99, "large cookie scoop": 10.99,
    "cookie press": 24.99, "spritz cookie press": 29.99, "decorating press": 34.99,
    "piping bag": 7.99, "disposable piping bags": 9.99, "reusable piping bag": 11.99,
    "silicone piping bag": 14.99, "decorating bag": 8.99, "pastry bag": 9.99,
    "piping tips": 12.99, "decorating tips": 14.99, "russian piping tips": 19.99,
    "coupler set": 8.99, "piping nozzles": 16.99, "icing tips set": 24.99,
    "cake turntable": 29.99, "rotating cake stand": 34.99, "decorating turntable": 39.99,
    "cake leveler": 14.99, "cake slicer": 12.99, "layer cake slicer": 16.99,
    "cake tester": 4.99, "skewer": 2.99, "bamboo skewers": 3.99,
    "cooling rack": 14.99, "wire rack": 12.99, "stackable cooling rack": 24.99,
    "3-tier cooling rack": 29.99, "round cooling rack": 16.99, "rectangular rack": 15.99,
    "baking mat": 14.99, "silicone baking mat": 19.99, "non-stick mat": 16.99,
    "silpat": 24.99, "reusable baking mat": 18.99, "fiberglass mat": 22.99,
    "parchment paper": 8.99, "pre-cut parchment": 11.99, "parchment roll": 9.99,
    "wax paper": 5.99, "butcher paper": 7.99, "freezer paper": 6.99,
    
    # ==================== STORAGE CONTAINERS (60 items) ====================
    "storage container": 12.99, "airtight container": 15.99, "glass container": 16.99,
    "plastic container": 8.99, "food storage": 14.99, "tupperware": 11.99,
    "bpa-free container": 13.99, "microwave safe": 12.99, "freezer container": 14.99,
    "meal prep container": 19.99, "portion control container": 22.99, "bento box": 24.99,
    "lunch box": 18.99, "insulated lunch box": 29.99, "thermal lunch bag": 24.99,
    "mason jar": 9.99, "canning jar": 11.99, "ball jar": 10.99,
    "wide mouth jar": 12.99, "regular mouth jar": 9.99, "fermenting jar": 16.99,
    "spice jar": 6.99, "herb jar": 7.99, "seasoning jar": 5.99,
    "salt jar": 8.99, "sugar jar": 9.99, "coffee jar": 14.99,
    "tea jar": 12.99, "cookie jar": 24.99, "candy jar": 19.99,
    "bread box": 34.99, "bamboo bread box": 44.99, "metal bread box": 39.99,
    "roll-top bread box": 49.99, "countertop bread box": 36.99, "vintage bread box": 54.99,
    "cereal container": 14.99, "flour container": 16.99, "sugar container": 15.99,
    "rice container": 18.99, "pasta container": 13.99, "dry goods container": 12.99,
    "canister set": 49.99, "4-piece canister": 44.99, "glass canister": 54.99,
    "ceramic canister": 59.99, "stainless canister": 46.99, "acrylic canister": 39.99,
    "vacuum container": 29.99, "coffee canister": 34.99, "tea canister": 24.99,
    "snack container": 8.99, "sandwich container": 7.99, "salad container": 12.99,
    "soup container": 14.99, "sauce container": 6.99, "dressing container": 9.99,
    "oil dispenser": 16.99, "vinegar dispenser": 14.99, "olive oil bottle": 19.99,
    "soy sauce dispenser": 12.99, "honey dispenser": 14.99, "syrup dispenser": 16.99,
    
    # ==================== SPECIALTY TOOLS (100 items) ====================
    "meat thermometer": 19.99, "instant-read thermometer": 24.99, "digital thermometer": 29.99,
    "probe thermometer": 34.99, "wireless thermometer": 49.99, "bluetooth thermometer": 59.99,
    "candy thermometer": 16.99, "deep fry thermometer": 18.99, "oven thermometer": 12.99,
    "refrigerator thermometer": 9.99, "freezer thermometer": 8.99, "grill thermometer": 22.99,
    "smoking thermometer": 39.99, "infrared thermometer": 44.99, "laser thermometer": 49.99,
    "apple corer": 8.99, "pineapple corer": 12.99, "melon baller": 7.99,
    "cherry pitter": 14.99, "olive pitter": 12.99, "strawberry huller": 5.99,
    "corn stripper": 9.99, "herb stripper": 7.99, "stem remover": 6.99,
    "avocado tool": 11.99, "avocado slicer": 9.99, "3-in-1 avocado tool": 13.99,
    "banana slicer": 6.99, "egg slicer": 7.99, "tomato slicer": 11.99,
    "mushroom slicer": 8.99, "strawberry slicer": 7.99, "kiwi slicer": 6.99,
    "mango splitter": 9.99, "watermelon slicer": 16.99, "cantaloupe slicer": 12.99,
    "salad chopper": 19.99, "salad cutter": 14.99, "herb mincer": 16.99,
    "garlic mincer": 11.99, "onion mincer": 13.99, "vegetable mincer": 18.99,
    "food chopper": 24.99, "manual chopper": 19.99, "pull chopper": 22.99,
    "dicer": 29.99, "vegetable dicer": 34.99, "onion dicer": 26.99,
    "french fry cutter": 24.99, "potato cutter": 19.99, "vegetable spiralizer": 29.99,
    "spiralizer": 34.99, "handheld spiralizer": 14.99, "countertop spiralizer": 39.99,
    "mandoline": 44.99, "adjustable mandoline": 54.99, "safety mandoline": 49.99,
    "v-slicer": 39.99, "julienne slicer": 32.99, "ribbon slicer": 29.99,
    "cheese slicer": 12.99, "wire cheese slicer": 9.99, "adjustable cheese slicer": 16.99,
    "cheese plane": 11.99, "cheese knife set": 34.99, "soft cheese knife": 14.99,
    "hard cheese knife": 16.99, "parmesan knife": 18.99, "stilton scoop": 22.99,
    "butter curler": 8.99, "butter knife": 6.99, "butter spreader": 7.99,
    "corn holders": 6.99, "corn on cob holders": 7.99, "cob holders": 5.99,
    "skewers": 9.99, "bamboo skewers": 4.99, "metal skewers": 14.99,
    "kabob skewers": 12.99, "flat skewers": 11.99, "twisted skewers": 13.99,
    "baster": 11.99, "turkey baster": 14.99, "bulb baster": 9.99,
    "injector": 16.99, "meat injector": 19.99, "marinade injector": 22.99,
    "tenderizer": 14.99, "meat tenderizer": 16.99, "meat mallet": 12.99,
    "poultry shears": 19.99, "kitchen scissors": 16.99, "herb scissors": 14.99,
    "pizza scissors": 18.99, "food scissors": 15.99, "multi-blade scissors": 22.99,
    "dough docker": 9.99, "pastry docker": 11.99, "pizza docker": 12.99,
    "egg separator": 5.99, "egg white separator": 6.99, "yolk separator": 5.99,
    "egg piercer": 4.99, "egg topper": 7.99, "egg timer": 8.99,
    "citrus squeezer": 12.99, "lemon squeezer": 9.99, "lime press": 10.99,
    "orange juicer": 24.99, "manual juicer": 14.99, "handheld juicer": 11.99,
    "reamer": 6.99, "citrus reamer": 7.99, "wooden reamer": 5.99,
    
    # ==================== GRILLING & OUTDOOR (60 items) ====================
    "grill": 299.99, "gas grill": 399.99, "charcoal grill": 199.99,
    "pellet grill": 599.99, "electric grill": 149.99, "portable grill": 129.99,
    "tabletop grill": 99.99, "hibachi grill": 79.99, "kettle grill": 179.99,
    "kamado grill": 799.99, "barrel grill": 249.99, "offset smoker": 399.99,
    "smoker": 299.99, "electric smoker": 249.99, "propane smoker": 199.99,
    "vertical smoker": 179.99, "water smoker": 159.99, "bullet smoker": 169.99,
    "grill brush": 12.99, "wire brush": 9.99, "brass brush": 14.99,
    "steam brush": 24.99, "scraper tool": 11.99, "grill stone": 16.99,
    "bbq tools": 34.99, "grill tool set": 49.99, "3-piece bbq set": 29.99,
    "grill spatula": 14.99, "bbq spatula": 16.99, "wide spatula": 18.99,
    "grill fork": 12.99, "carving fork": 14.99, "bbq fork": 13.99,
    "grill tongs": 16.99, "locking tongs": 18.99, "long tongs": 19.99,
    "bbq tongs": 15.99, "heavy duty tongs": 21.99, "grilling tongs": 17.99,
    "basting brush": 9.99, "mop brush": 14.99, "silicone basting brush": 11.99,
    "grill basket": 22.99, "vegetable basket": 19.99, "fish basket": 24.99,
    "kabob basket": 21.99, "tumble basket": 29.99, "rolling basket": 26.99,
    "grill mat": 16.99, "bbq mat": 14.99, "non-stick grill mat": 19.99,
    "copper grill mat": 22.99, "fiberglass mat": 18.99, "grill topper": 24.99,
    "grill pan": 29.99, "cast iron grill pan": 39.99, "perforated pan": 26.99,
    "grill wok": 34.99, "stir fry pan": 32.99, "grilling skillet": 36.99,
    "smoking chips": 12.99, "wood chips": 14.99, "pellets": 19.99,
    "charcoal": 16.99, "lump charcoal": 24.99, "briquettes": 18.99,
    
    # ==================== BAR TOOLS (50 items) ====================
    "cocktail shaker": 24.99, "boston shaker": 29.99, "cobbler shaker": 22.99,
    "french shaker": 26.99, "professional shaker": 34.99, "weighted shaker": 39.99,
    "mixing glass": 29.99, "yarai mixing glass": 44.99, "seamless mixing glass": 39.99,
    "bar spoon": 12.99, "twisted bar spoon": 14.99, "long bar spoon": 16.99,
    "muddler": 11.99, "wooden muddler": 9.99, "stainless muddler": 14.99,
    "jigger": 9.99, "double jigger": 12.99, "japanese jigger": 16.99,
    "measuring jigger": 11.99, "adjustable jigger": 19.99, "stepped jigger": 14.99,
    "strainer": 14.99, "hawthorne strainer": 12.99, "julep strainer": 11.99,
    "fine strainer": 16.99, "mesh strainer": 13.99, "conical strainer": 18.99,
    "bottle opener": 6.99, "wall bottle opener": 14.99, "automatic opener": 24.99,
    "wine opener": 16.99, "corkscrew": 14.99, "waiter's corkscrew": 12.99,
    "wing corkscrew": 19.99, "electric wine opener": 34.99, "lever corkscrew": 49.99,
    "wine aerator": 24.99, "wine decanter": 39.99, "decanting pourer": 19.99,
    "wine pourer": 14.99, "drip stop": 8.99, "foil cutter": 9.99,
    "ice bucket": 34.99, "champagne bucket": 44.99, "double-wall ice bucket": 49.99,
    "ice scoop": 9.99, "bar ice scoop": 12.99, "stainless ice scoop": 14.99,
    "ice tongs": 11.99, "bar tongs": 13.99, "garnish tongs": 9.99,
    "citrus press": 29.99, "lime press": 24.99, "professional press": 39.99,
    "channel knife": 8.99, "bar knife": 16.99, "paring knife": 12.99,
    
    # ==================== CLEANING SUPPLIES (40 items) ====================
    "dish rack": 24.99, "dish drainer": 19.99, "drying rack": 29.99,
    "over-sink rack": 39.99, "roll-up rack": 22.99, "collapsible rack": 26.99,
    "dish mat": 14.99, "drying mat": 12.99, "microfiber mat": 16.99,
    "silicone mat": 18.99, "absorbent mat": 13.99, "quick-dry mat": 19.99,
    "dish brush": 5.99, "bottle brush": 7.99, "pot brush": 6.99,
    "scrub brush": 4.99, "vegetable brush": 5.99, "grill brush": 12.99,
    "sponge": 3.99, "scrub sponge": 4.99, "cellulose sponge": 3.49,
    "non-scratch sponge": 5.99, "heavy duty sponge": 6.99, "natural sponge": 7.99,
    "sponge holder": 8.99, "sink caddy": 14.99, "soap holder": 6.99,
    "soap dispenser": 14.99, "automatic dispenser": 29.99, "touchless dispenser": 34.99,
    "dish soap": 4.99, "eco-friendly soap": 6.99, "concentrated soap": 7.99,
    "dishwasher detergent": 12.99, "rinse aid": 8.99, "dishwasher cleaner": 9.99,
    "oven cleaner": 8.99, "degreaser": 9.99, "multi-surface cleaner": 6.99,
    "stainless cleaner": 11.99, "glass cleaner": 5.99, "granite cleaner": 9.99,
    
    # ==================== DINING & SERVING (80 items) ====================
    "dinner plate": 12.99, "salad plate": 9.99, "dessert plate": 8.99,
    "bread plate": 7.99, "charger plate": 16.99, "serving plate": 14.99,
    "plate set": 49.99, "dinnerware set": 99.99, "12-piece dinnerware": 89.99,
    "bowl": 8.99, "soup bowl": 9.99, "cereal bowl": 7.99,
    "pasta bowl": 11.99, "rice bowl": 6.99, "ramen bowl": 12.99,
    "serving bowl": 16.99, "mixing bowl": 14.99, "salad bowl": 18.99,
    "large serving bowl": 22.99, "fruit bowl": 19.99, "decorative bowl": 24.99,
    "mug": 9.99, "coffee mug": 11.99, "tea mug": 10.99,
    "travel mug": 19.99, "insulated mug": 24.99, "ceramic mug": 12.99,
    "glass": 6.99, "drinking glass": 7.99, "water glass": 8.99,
    "juice glass": 5.99, "tumbler": 9.99, "highball glass": 11.99,
    "wine glass": 14.99, "red wine glass": 16.99, "white wine glass": 15.99,
    "champagne flute": 18.99, "beer glass": 12.99, "pint glass": 9.99,
    "glassware set": 39.99, "stemware set": 54.99, "barware set": 49.99,
    "serving platter": 24.99, "rectangular platter": 29.99, "oval platter": 26.99,
    "round platter": 22.99, "tiered platter": 39.99, "cake platter": 34.99,
    "cheese platter": 32.99, "charcuterie board": 44.99, "serving board": 36.99,
    "gravy boat": 16.99, "sauce boat": 14.99, "creamer": 12.99,
    "sugar bowl": 13.99, "salt cellar": 9.99, "butter dish": 14.99,
    "napkin holder": 12.99, "napkin ring": 8.99, "napkin ring set": 24.99,
    "tablecloth": 29.99, "table runner": 19.99, "placemats": 24.99,
    "cloth napkins": 22.99, "dinner napkins": 18.99, "cocktail napkins": 12.99,
    "utensil holder": 16.99, "flatware caddy": 19.99, "silverware organizer": 24.99,
    "cake stand": 29.99, "tiered cake stand": 44.99, "rotating cake stand": 39.99,
    "cupcake stand": 34.99, "dessert stand": 32.99, "pie stand": 26.99,
    "salad servers": 14.99, "pasta server": 12.99, "cake server": 16.99,
    "pie server": 13.99, "lasagna server": 15.99, "fish server": 18.99,
    "tea pot": 34.99, "tea kettle": 29.99, "tea infuser": 12.99,
    "french press": 39.99, "coffee carafe": 29.99, "thermal carafe": 44.99,
}

equipment_icons = {
    # ==================== KNIVES & CUTTING TOOLS ====================
    "chef's knife": "🔪", "knife": "🔪", "paring knife": "🗡️", "bread knife": "🥖",
    "carving knife": "🍖", "utility knife": "🔪", "boning knife": "🦴", "cleaver": "🪓",
    "santoku knife": "🔪", "nakiri knife": "🔪", "fillet knife": "🐟", "steak knife": "🥩",
    "butter knife": "🧈", "dinner knife": "🍴", "cheese knife": "🧀", "oyster knife": "🦪",
    "palette knife": "🎨", "cake knife": "🎂", "serrated knife": "🔪", "ceramic knife": "⚪",
    "knife sharpener": "⚡", "electric knife sharpener": "⚡", "knife block": "🪵",
    "magnetic knife strip": "🧲", "knife guards": "🛡️", "kitchen shears": "✂️",
    "poultry shears": "🍗", "herb scissors": "🌿", "pizza cutter": "🍕", "rotary cutter": "⚙️",
    "mandoline slicer": "🥒", "vegetable slicer": "🥕", "julienne peeler": "🥕", "peeler": "🥔",
    "y-peeler": "🥒", "serrated peeler": "🍅", "apple peeler": "🍎", "potato peeler": "🥔",
    "citrus peeler": "🍊", "tomato knife": "🍅", "bagel slicer": "🥯", "egg slicer": "🥚",
    "strawberry huller": "🍓", "pineapple corer": "🍍", "avocado slicer": "🥑", "banana slicer": "🍌",
    "mushroom slicer": "🍄", "onion chopper": "🧅", "vegetable chopper": "🥕", "food chopper": "🔪",
    
    # ==================== CUTTING BOARDS ====================
    "cutting board": "🪵", "chopping board": "🪵", "bamboo cutting board": "🎋",
    "plastic cutting board": "🟦", "wooden cutting board": "🪵", "glass cutting board": "🔲",
    "marble cutting board": "⚪", "acacia cutting board": "🌳", "teak cutting board": "🌲",
    "maple cutting board": "🍁", "walnut cutting board": "🌰", "oak cutting board": "🌳",
    "flexible cutting board": "📋", "silicone cutting board": "🟦", "composite cutting board": "🟫",
    "end grain cutting board": "🪵", "edge grain cutting board": "🪵", "butcher block": "🔨",
    "carving board": "🍖", "serving board": "🍽️", "charcuterie board": "🧀",
    "cheese cutting board": "🧀", "bread cutting board": "🍞", "fish cutting board": "🐟",
    "meat cutting board": "🥩", "vegetable cutting board": "🥕", "fruit cutting board": "🍎",
    "cutting board set": "🪵", "cutting board oil": "🛢️", "cutting board cream": "🧴",
    
    # ==================== POTS & PANS ====================
    "pot": "🍲", "large pot": "🍲", "stockpot": "🍲", "soup pot": "🍜",
    "pasta pot": "🍝", "lobster pot": "🦞", "canning pot": "🥫", "double boiler": "♨️",
    "milk pot": "🥛", "sauce pot": "🍲", "saucepan": "🍳", "small saucepan": "🍳",
    "medium saucepan": "🍳", "large saucepan": "🍳", "covered saucepan": "🍳",
    "pan": "🥘", "frying pan": "🍳", "skillet": "🥘", "non-stick pan": "🍳",
    "stainless steel pan": "⚙️", "copper pan": "🟠", "aluminum pan": "⚪",
    "cast iron skillet": "⚫", "cast iron pan": "⚫", "enameled cast iron": "🔴",
    "carbon steel pan": "⚫", "ceramic pan": "⚪", "granite pan": "⚫",
    "wok": "🍜", "carbon steel wok": "🍜", "flat bottom wok": "🍜", "round bottom wok": "🍜",
    "electric wok": "⚡", "wok ring": "⭕", "wok spatula": "🥄", "wok ladle": "🥄",
    "grill pan": "🍖", "griddle": "🥞", "electric griddle": "⚡", "stovetop griddle": "🔥",
    "crepe pan": "🥞", "omelet pan": "🍳", "egg pan": "🥚", "frittata pan": "🍳",
    "fish pan": "🐟", "paella pan": "🥘", "tagine": "🏺", "braiser": "🍲",
    "saute pan": "🍳", "saucier": "🍲", "chef's pan": "🥘", "everyday pan": "🍳",
    "roasting pan": "🍗", "roaster": "🍗", "covered roaster": "🍗", "oval roaster": "🍗",
    "turkey roaster": "🦃", "roasting rack": "🔧", "v-rack": "⚙️", "flat rack": "▬",
    "dutch oven": "🍲", "french oven": "🍲", "enameled dutch oven": "🍲",
    "casserole dish": "🥘", "covered casserole": "🥘", "oval casserole": "🥘",
    "baking dish": "🥐", "glass baking dish": "🔲", "ceramic baking dish": "⚪",
    "lasagna pan": "🍝", "brownie pan": "🍫", "au gratin dish": "🧀",
    "pot set": "🍲", "pan set": "🍳", "cookware set": "🥘", "starter cookware set": "🍳",
    
    # ==================== MAJOR APPLIANCES ====================
    "pressure cooker": "💨", "electric pressure cooker": "⚡", "instant pot": "⚡",
    "slow cooker": "⏲️", "programmable slow cooker": "⏱️", "multi-cooker": "🍲",
    "rice cooker": "🍚", "fuzzy logic rice cooker": "🤖", "induction rice cooker": "⚡",
    "air fryer": "🌪️", "digital air fryer": "🌪️", "air fryer oven": "🔥",
    "deep fryer": "🍟", "electric deep fryer": "⚡", "turkey fryer": "🦃",
    "electric kettle": "☕", "variable temp kettle": "🌡️", "gooseneck kettle": "☕",
    "tea kettle": "🫖", "stovetop kettle": "🫖", "whistling kettle": "🎵",
    "coffee maker": "☕", "drip coffee maker": "☕", "programmable coffee maker": "⏱️",
    "espresso machine": "☕", "super-automatic espresso": "🤖", "manual espresso": "☕",
    "french press": "☕", "pour over coffee": "☕", "cold brew maker": "🧊",
    "toaster": "🍞", "2-slice toaster": "🍞", "4-slice toaster": "🍞",
    "toaster oven": "🔥", "convection toaster oven": "🌀", "countertop oven": "🔥",
    "microwave": "📟", "microwave oven": "📟", "over-range microwave": "📟",
    
    # ==================== SMALL APPLIANCES ====================
    "blender": "🌀", "high-speed blender": "⚡", "personal blender": "🥤",
    "immersion blender": "🌀", "hand blender": "🥄", "stick blender": "🥄",
    "food processor": "🥕", "mini food processor": "🥕", "full-size food processor": "⚙️",
    "stand mixer": "⚙️", "tilt-head mixer": "⚙️", "bowl-lift mixer": "⚙️",
    "hand mixer": "🌀", "electric mixer": "⚡", "handheld mixer": "🥄",
    "juicer": "🍊", "citrus juicer": "🍋", "masticating juicer": "🥤",
    "centrifugal juicer": "🌀", "cold press juicer": "🧊", "electric juicer": "⚡",
    "waffle maker": "🧇", "belgian waffle maker": "🧇", "flip waffle maker": "🧇",
    "sandwich maker": "🥪", "panini press": "🥪", "grill press": "🍖",
    "electric grill": "⚡", "indoor grill": "🍖", "smokeless grill": "🌬️",
    "contact grill": "🍖", "open grill": "🔥", "reversible grill": "🔄",
    "griddle": "🥞", "electric griddle": "⚡", "pancake griddle": "🥞",
    "crepe maker": "🥞", "electric crepe maker": "⚡", "tortilla maker": "🌮",
    "pizza maker": "🍕", "pizza oven": "🔥", "outdoor pizza oven": "🔥",
    "bread maker": "🍞", "automatic bread maker": "🤖", "programmable bread maker": "⏱️",
    "pasta maker": "🍝", "electric pasta maker": "⚡", "manual pasta machine": "🔧",
    "ice cream maker": "🍨", "compressor ice cream maker": "🧊", "frozen yogurt maker": "🍦",
    "popcorn maker": "🍿", "hot air popper": "🌀", "stovetop popcorn": "🍿",
    "cotton candy maker": "🍭", "sno-cone maker": "🍧", "donut maker": "🍩",
    "egg cooker": "🥚", "electric egg cooker": "⚡", "egg boiler": "♨️",
    "sous vide": "🌡️", "immersion circulator": "🌡️", "sous vide container": "🥫",
    "dehydrator": "🌬️", "food dehydrator": "🥦", "jerky maker": "🥓",
    "yogurt maker": "🍦", "greek yogurt maker": "🥛", "fermentation crock": "🏺",
    "meat grinder": "🥩", "electric meat grinder": "⚡", "manual meat grinder": "🔧",
    "sausage stuffer": "🌭", "meat slicer": "🔪", "deli slicer": "🥩",
    "vacuum sealer": "📦", "food vacuum sealer": "🔒", "chamber vacuum sealer": "🏭",
    "can opener": "🥫", "electric can opener": "⚡", "manual can opener": "🔧",
    "jar opener": "🏺", "bottle opener": "🍺", "wine opener": "🍷",
    "electric wine opener": "⚡", "corkscrew": "🍷", "lever corkscrew": "🔧",
    
    # ==================== MIXING & PREP TOOLS ====================
    "mixing bowl": "🥣", "bowl": "🥣", "salad bowl": "🥗", "prep bowl": "🥣",
    "nesting bowls": "🥣", "stainless steel bowls": "⚙️", "glass bowls": "🔲",
    "ceramic bowls": "⚪", "plastic bowls": "🟦", "melamine bowls": "🟧",
    "mixing bowl set": "🥣", "prep bowl set": "🥣", "serving bowl set": "🥣",
    "measuring cups": "📏", "dry measuring cups": "📏", "liquid measuring cup": "🥛",
    "adjustable measuring cup": "📏", "stainless measuring cups": "⚙️", "glass measuring cup": "🔲",
    "measuring spoons": "🥄", "magnetic measuring spoons": "🧲", "oval measuring spoons": "🥄",
    "kitchen scale": "⚖️", "digital scale": "🔢", "food scale": "⚖️",
    "baker's scale": "⚖️", "mechanical scale": "⚖️", "portion scale": "📊",
    "timer": "⏱️", "digital timer": "🔢", "magnetic timer": "🧲",
    "triple timer": "⏱️", "hourglass timer": "⏳", "countdown timer": "⏱️",
    "whisk": "🥄", "balloon whisk": "🎈", "flat whisk": "▬",
    "french whisk": "🇫🇷", "mini whisk": "🥄", "coil whisk": "🌀",
    "silicone whisk": "🟦", "stainless whisk": "⚙️", "dough whisk": "🍞",
    "electric whisk": "⚡", "rotary whisk": "🔄", "milk frother": "🥛",
    "wooden spoon": "🥄", "spoon": "🥄", "slotted spoon": "🕳️",
    "serving spoon": "🍽️", "soup spoon": "🍜", "spaghetti spoon": "🍝",
    "risotto spoon": "🍚", "mixing spoon": "🥄", "tasting spoon": "👅",
    "bamboo spoon": "🎋", "silicone spoon": "🟦", "nylon spoon": "🟨",
    "ladle": "🥄", "soup ladle": "🍜", "gravy ladle": "🍖",
    "sauce ladle": "🥄", "punch ladle": "🍹", "skimmer ladle": "🕳️",
    "spatula": "🥄", "rubber spatula": "🔴", "silicone spatula": "🟦",
    "offset spatula": "🥄", "fish spatula": "🐟", "turner": "🔄",
    "slotted turner": "🕳️", "flexible turner": "🥄", "nylon turner": "🟨",
    "metal spatula": "⚙️", "heat-resistant spatula": "🔥", "jar spatula": "🏺",
    "frosting spatula": "🎂", "icing spatula": "🧁", "palette knife": "🎨",
    "tongs": "🔧", "kitchen tongs": "🥄", "silicone tongs": "🟦",
    "locking tongs": "🔒", "salad tongs": "🥗", "serving tongs": "🍽️",
    "grilling tongs": "🍖", "pasta tongs": "🍝", "ice tongs": "🧊",
    "fork": "🍴", "pasta fork": "🍝", "carving fork": "🍖",
    "serving fork": "🍽️", "salad fork": "🥗", "meat fork": "🥩",
    "basting brush": "🖌️", "pastry brush": "🥐", "silicone brush": "🟦",
    "natural bristle brush": "🌾", "barbeque brush": "🍖", "marinade brush": "🖌️",
    "potato masher": "🥔", "bean masher": "🫘", "avocado masher": "🥑",
    "ricer": "🥔", "potato ricer": "🥔", "food mill": "⚙️",
    "mortar and pestle": "⚗️", "marble mortar": "⚪", "granite mortar": "⚫",
    "wooden mortar": "🪵", "molcajete": "🗿", "spice grinder": "🌶️",
    "pepper mill": "🌶️", "salt grinder": "🧂", "pepper grinder": "⚫",
    "electric pepper mill": "⚡", "manual pepper mill": "🔧", "adjustable grinder": "⚙️",
    
    # ==================== STRAINERS & COLANDERS ====================
    "colander": "🥣", "mesh colander": "🕸️", "stainless colander": "⚙️",
    "silicone colander": "🟦", "collapsible colander": "🔄", "over-sink colander": "🚰",
    "strainer": "🥣", "fine mesh strainer": "🕸️", "spider strainer": "🕷️",
    "conical strainer": "🔺", "chinois": "🇫🇷", "china cap": "🎩",
    "sieve": "🥣", "flour sifter": "🌾", "powdered sugar sifter": "🍬",
    "double mesh sieve": "🕸️", "splash guard": "🛡️", "grease strainer": "🛢️",
    "pasta strainer": "🍝", "pot strainer": "🍲", "clip-on strainer": "📎",
    "salad spinner": "🥗", "large salad spinner": "🥗", "mini salad spinner": "🥗",
    "vegetable spinner": "🥬", "lettuce spinner": "🥬", "herb spinner": "🌿",
    "splatter screen": "🛡️", "grease splatter guard": "🛡️", "mesh splatter": "🕸️",
    
    # ==================== GRATERS & ZESTERS ====================
    "cheese grater": "🧀", "grater": "🔧", "box grater": "📦",
    "4-sided grater": "🔲", "6-sided grater": "⬡", "rotary grater": "🔄",
    "flat grater": "▬", "handheld grater": "🤲", "coarse grater": "🔧",
    "fine grater": "✨", "nutmeg grater": "🌰", "ginger grater": "🫚",
    "microplane": "🧀", "zester": "🍋", "citrus zester": "🍊",
    "lemon zester": "🍋", "orange zester": "🍊", "channel knife": "🔪",
    "rasp grater": "🧀", "parmesan grater": "🧀", "chocolate grater": "🍫",
    "coconut grater": "🥥", "garlic grater": "🧄", "truffle grater": "🍄",
    "garlic press": "🧄", "aluminum garlic press": "⚪", "stainless garlic press": "⚙️",
    
    # ==================== BAKING EQUIPMENT ====================
    "baking sheet": "🍪", "cookie sheet": "🍪", "half sheet pan": "▬",
    "quarter sheet pan": "▪️", "jelly roll pan": "🍰", "rimmed baking sheet": "🍪",
    "insulated baking sheet": "🛡️", "non-stick baking sheet": "🍪", "perforated pan": "🕳️",
    "muffin tin": "🧁", "cupcake pan": "🧁", "12-cup muffin tin": "🧁",
    "24-cup mini muffin": "🧁", "6-cup jumbo muffin": "🧁", "silicone muffin pan": "🟦",
    "non-stick muffin tin": "🧁", "texas muffin pan": "🤠", "popover pan": "🎈",
    "cake pan": "🎂", "round cake pan": "⭕", "square cake pan": "🔲",
    "rectangular cake pan": "▬", "heart cake pan": "❤️", "star cake pan": "⭐",
    "number cake pan": "🔢", "letter cake pan": "🔤", "character cake pan": "👻",
    "springform pan": "🎂", "cheesecake pan": "🧀", "loose bottom pan": "🔓",
    "bundt pan": "🎂", "mini bundt pan": "🧁", "fluted bundt": "🎂",
    "nordic ware bundt": "🇳🇴", "shaped bundt pan": "🎨", "silicone bundt": "🟦",
    "loaf pan": "🍞", "bread pan": "🍞", "pullman loaf pan": "🚂",
    "mini loaf pan": "🍞", "glass loaf pan": "🔲", "ceramic loaf pan": "⚪",
    "pie dish": "🥧", "pie pan": "🥧", "deep dish pie pan": "🥧",
    "glass pie dish": "🔲", "ceramic pie dish": "⚪", "disposable pie pan": "♻️",
    "tart pan": "🥧", "fluted tart pan": "🌸", "removable bottom tart": "🔓",
    "mini tart pans": "🥧", "tartlet pans": "🥧", "quiche pan": "🥚",
    "pizza pan": "🍕", "perforated pizza pan": "🕳️", "deep dish pizza": "🍕",
    "pizza stone": "🪨", "cordierite pizza stone": "🪨", "steel pizza stone": "⚙️",
    "pizza peel": "🍕", "wooden pizza peel": "🪵", "aluminum pizza peel": "⚪",
    "rolling pin": "🥖", "french rolling pin": "🇫🇷", "marble rolling pin": "⚪",
    "tapered rolling pin": "🔻", "adjustable rolling pin": "⚙️", "silicone rolling pin": "🟦",
    "pastry cutter": "🥐", "dough cutter": "🍞", "bench scraper": "🧼",
    "dough scraper": "🍞", "bowl scraper": "🥣", "flexible scraper": "🔄",
    "pastry blender": "🥐", "dough blender": "🍞", "pastry mixer": "⚙️",
    "cookie cutter set": "🍪", "cookie cutters": "🍪", "shaped cookie cutters": "🎨",
    "christmas cookie cutters": "🎄", "holiday cookie cutters": "🎉", "alphabet cutters": "🔤",
    "cookie scoop": "🍪", "ice cream scoop": "🍨", "portion scoop": "🥄",
    "small cookie scoop": "🍪", "medium cookie scoop": "🍪", "large cookie scoop": "🍪",
    "cookie press": "🍪", "spritz cookie press": "🍪", "decorating press": "🎨",
    "piping bag": "🧁", "disposable piping bags": "♻️", "reusable piping bag": "🔄",
    "silicone piping bag": "🟦", "decorating bag": "🎨", "pastry bag": "🥐",
    "piping tips": "🧁", "decorating tips": "🎨", "russian piping tips": "🇷🇺",
    "coupler set": "🔗", "piping nozzles": "💧", "icing tips set": "🧁",
    "cake turntable": "🔄", "rotating cake stand": "🔄", "decorating turntable": "🎂",
    "cake leveler": "▬", "cake slicer": "🔪", "layer cake slicer": "🎂",
    "cake tester": "📍", "skewer": "🗡️", "bamboo skewers": "🎋",
    "cooling rack": "🧊", "wire rack": "🕸️", "stackable cooling rack": "📚",
    "3-tier cooling rack": "3️⃣", "round cooling rack": "⭕", "rectangular rack": "▬",
    "baking mat": "📋", "silicone baking mat": "🟦", "non-stick mat": "🍪",
    "silpat": "📋", "reusable baking mat": "🔄", "fiberglass mat": "🕸️",
    "parchment paper": "📄", "pre-cut parchment": "✂️", "parchment roll": "🧻",
    "wax paper": "📄", "butcher paper": "🥩", "freezer paper": "🧊",
    
    # ==================== STORAGE CONTAINERS ====================
    "storage container": "📦", "airtight container": "🔒", "glass container": "🔲",
    "plastic container": "🟦", "food storage": "🥫", "tupperware": "📦",
    "bpa-free container": "✅", "microwave safe": "📟", "freezer container": "🧊",
    "meal prep container": "🍱", "portion control container": "⚖️", "bento box": "🍱",
    "lunch box": "🎒", "insulated lunch box": "🧊", "thermal lunch bag": "🛍️",
    "mason jar": "🫙", "canning jar": "🥫", "ball jar": "⚾",
    "wide mouth jar": "🫙", "regular mouth jar": "🏺", "fermenting jar": "🧫",
    "spice jar": "🧂", "herb jar": "🌿", "seasoning jar": "🧂",
    "salt jar": "🧂", "sugar jar": "🍬", "coffee jar": "☕",
    "tea jar": "🍵", "cookie jar": "🍪", "candy jar": "🍬",
    "bread box": "🍞", "bamboo bread box": "🎋", "metal bread box": "⚙️",
    "roll-top bread box": "🔄", "countertop bread box": "🏪", "vintage bread box": "📻",
    "cereal container": "🥣", "flour container": "🌾", "sugar container": "🍬",
    "rice container": "🍚", "pasta container": "🍝", "dry goods container": "📦",
    "canister set": "🥫", "4-piece canister": "4️⃣", "glass canister": "🔲",
    "ceramic canister": "⚪", "stainless canister": "⚙️", "acrylic canister": "🔲",
    "vacuum container": "🔒", "coffee canister": "☕", "tea canister": "🍵",
    "snack container": "🥨", "sandwich container": "🥪", "salad container": "🥗",
    "soup container": "🍜", "sauce container": "🥫", "dressing container": "🥗",
    "oil dispenser": "🛢️", "vinegar dispenser": "🧴", "olive oil bottle": "🫒",
    "soy sauce dispenser": "🧴", "honey dispenser": "🍯", "syrup dispenser": "🍁",
    
    # ==================== SPECIALTY TOOLS ====================
    "meat thermometer": "🌡️", "instant-read thermometer": "⚡", "digital thermometer": "🔢",
    "probe thermometer": "📍", "wireless thermometer": "📡", "bluetooth thermometer": "📶",
    "candy thermometer": "🍬", "deep fry thermometer": "🍟", "oven thermometer": "🔥",
    "refrigerator thermometer": "🧊", "freezer thermometer": "❄️", "grill thermometer": "🍖",
    "smoking thermometer": "💨", "infrared thermometer": "🔴", "laser thermometer": "🔴",
    "apple corer": "🍎", "pineapple corer": "🍍", "melon baller": "🍈",
    "cherry pitter": "🍒", "olive pitter": "🫒", "strawberry huller": "🍓",
    "corn stripper": "🌽", "herb stripper": "🌿", "stem remover": "🌸",
    "avocado tool": "🥑", "avocado slicer": "🥑", "3-in-1 avocado tool": "🥑",
    "banana slicer": "🍌", "egg slicer": "🥚", "tomato slicer": "🍅",
    "mushroom slicer": "🍄", "strawberry slicer": "🍓", "kiwi slicer": "🥝",
    "mango splitter": "🥭", "watermelon slicer": "🍉", "cantaloupe slicer": "🍈",
    "salad chopper": "🥗", "salad cutter": "🔪", "herb mincer": "🌿",
    "garlic mincer": "🧄", "onion mincer": "🧅", "vegetable mincer": "🥕",
    "food chopper": "🔪", "manual chopper": "🔧", "pull chopper": "🔁",
    "dicer": "🎲", "vegetable dicer": "🥦", "onion dicer": "🧅",
    "french fry cutter": "🍟", "potato cutter": "🥔", "vegetable spiralizer": "🌀",
    "spiralizer": "🌀", "handheld spiralizer": "🤲", "countertop spiralizer": "🏪",
    "mandoline": "🔪", "adjustable mandoline": "⚙️", "safety mandoline": "🛡️",
    "v-slicer": "✌️", "julienne slicer": "🥕", "ribbon slicer": "🎀",
    "cheese slicer": "🧀", "wire cheese slicer": "🕸️", "adjustable cheese slicer": "⚙️",
    "cheese plane": "✈️", "cheese knife set": "🧀", "soft cheese knife": "🧀",
    "hard cheese knife": "🔪", "parmesan knife": "🧀", "stilton scoop": "🥄",
    "butter curler": "🧈", "butter knife": "🧈", "butter spreader": "🥪",
    "corn holders": "🌽", "corn on cob holders": "🌽", "cob holders": "🌽",
    "skewers": "🗡️", "bamboo skewers": "🎋", "metal skewers": "⚙️",
    "kabob skewers": "🍖", "flat skewers": "▬", "twisted skewers": "🌀",
    "baster": "💧", "turkey baster": "🦃", "bulb baster": "💡",
    "injector": "💉", "meat injector": "🥩", "marinade injector": "🧴",
    "tenderizer": "🔨", "meat tenderizer": "🥩", "meat mallet": "🔨",
    "poultry shears": "✂️", "kitchen scissors": "✂️", "herb scissors": "🌿",
    "pizza scissors": "🍕", "food scissors": "✂️", "multi-blade scissors": "✂️",
    "dough docker": "🍕", "pastry docker": "🥐", "pizza docker": "🍕",
    "egg separator": "🥚", "egg white separator": "⚪", "yolk separator": "🟡",
    "egg piercer": "📍", "egg topper": "🎩", "egg timer": "⏱️",
    "citrus squeezer": "🍋", "lemon squeezer": "🍋", "lime press": "🍈",
    "orange juicer": "🍊", "manual juicer": "🔧", "handheld juicer": "🤲",
    "reamer": "🍋", "citrus reamer": "🍊", "wooden reamer": "🪵",
    
    # ==================== GRILLING & OUTDOOR ====================
    "grill": "🔥", "gas grill": "🔥", "charcoal grill": "🔥",
    "pellet grill": "🌲", "electric grill": "⚡", "portable grill": "🎒",
    "tabletop grill": "🏪", "hibachi grill": "🇯🇵", "kettle grill": "🫖",
    "kamado grill": "🥚", "barrel grill": "🛢️", "offset smoker": "💨",
    "smoker": "💨", "electric smoker": "⚡", "propane smoker": "🔥",
    "vertical smoker": "↕️", "water smoker": "💧", "bullet smoker": "🔫",
    "grill brush": "🧹", "wire brush": "🕸️", "brass brush": "🟡",
    "steam brush": "♨️", "scraper tool": "🔧", "grill stone": "🪨",
    "bbq tools": "🍖", "grill tool set": "🧰", "3-piece bbq set": "3️⃣",
    "grill spatula": "🥄", "bbq spatula": "🍖", "wide spatula": "▬",
    "grill fork": "🍴", "carving fork": "🔪", "bbq fork": "🍖",
    "grill tongs": "🔧", "locking tongs": "🔒", "long tongs": "📏",
    "bbq tongs": "🍖", "heavy duty tongs": "💪", "grilling tongs": "🔥",
    "basting brush": "🖌️", "mop brush": "🧹", "silicone basting brush": "🟦",
    "grill basket": "🧺", "vegetable basket": "🥦", "fish basket": "🐟",
    "kabob basket": "🍖", "tumble basket": "🔄", "rolling basket": "🎲",
    "grill mat": "📋", "bbq mat": "🍖", "non-stick grill mat": "🍳",
    "copper grill mat": "🟠", "fiberglass mat": "🕸️", "grill topper": "⬆️",
    "grill pan": "🍖", "cast iron grill pan": "⚫", "perforated pan": "🕳️",
    "grill wok": "🍜", "stir fry pan": "🥘", "grilling skillet": "🍳",
    "smoking chips": "🪵", "wood chips": "🌲", "pellets": "⚫",
    "charcoal": "⚫", "lump charcoal": "🪨", "briquettes": "🔲",
    
    # ==================== BAR TOOLS ====================
    "cocktail shaker": "🍸", "boston shaker": "🥃", "cobbler shaker": "🍹",
    "french shaker": "🇫🇷", "professional shaker": "👔", "weighted shaker": "⚖️",
    "mixing glass": "🥃", "yarai mixing glass": "🇯🇵", "seamless mixing glass": "🔘",
    "bar spoon": "🥄", "twisted bar spoon": "🌀", "long bar spoon": "📏",
    "muddler": "🪵", "wooden muddler": "🌳", "stainless muddler": "⚙️",
    "jigger": "📏", "double jigger": "2️⃣", "japanese jigger": "🇯🇵",
    "measuring jigger": "⚖️", "adjustable jigger": "⚙️", "stepped jigger": "📊",
    "strainer": "🥅", "hawthorne strainer": "🕸️", "julep strainer": "🌿",
    "fine strainer": "✨", "mesh strainer": "🕸️", "conical strainer": "🔺",
    "bottle opener": "🍺", "wall bottle opener": "🧱", "automatic opener": "🤖",
    "wine opener": "🍷", "corkscrew": "🌀", "waiter's corkscrew": "🧑‍🍳",
    "wing corkscrew": "🦋", "electric wine opener": "⚡", "lever corkscrew": "🔧",
    "wine aerator": "🌬️", "wine decanter": "🍷", "decanting pourer": "💧",
    "wine pourer": "🍷", "drip stop": "🛑", "foil cutter": "✂️",
    "ice bucket": "🧊", "champagne bucket": "🍾", "double-wall ice bucket": "❄️",
    "ice scoop": "🥄", "bar ice scoop": "🧊", "stainless ice scoop": "⚙️",
    "ice tongs": "🧊", "bar tongs": "🍸", "garnish tongs": "🍋",
    "citrus press": "🍋", "lime press": "🍈", "professional press": "👔",
    "channel knife": "🔪", "bar knife": "🗡️", "paring knife": "🔪",
    
    # ==================== CLEANING SUPPLIES ====================
    "dish rack": "🧼", "dish drainer": "💧", "drying rack": "🌀",
    "over-sink rack": "🚰", "roll-up rack": "🔄", "collapsible rack": "📦",
    "dish mat": "📋", "drying mat": "💧", "microfiber mat": "🧽",
    "silicone mat": "🟦", "absorbent mat": "💧", "quick-dry mat": "⚡",
    "dish brush": "🧽", "bottle brush": "🍼", "pot brush": "🍲",
    "scrub brush": "🧹", "vegetable brush": "🥕", "grill brush": "🔥",
    "sponge": "🧽", "scrub sponge": "🧹", "cellulose sponge": "🟨",
    "non-scratch sponge": "✨", "heavy duty sponge": "💪", "natural sponge": "🌊",
    "sponge holder": "🏠", "sink caddy": "🧰", "soap holder": "🧼",
    "soap dispenser": "🧴", "automatic dispenser": "🤖", "touchless dispenser": "👋",
    "dish soap": "🧼", "eco-friendly soap": "♻️", "concentrated soap": "💧",
    "dishwasher detergent": "📦", "rinse aid": "✨", "dishwasher cleaner": "🧼",
    "oven cleaner": "🔥", "degreaser": "🛢️", "multi-surface cleaner": "🧹",
    "stainless cleaner": "⚙️", "glass cleaner": "🔲", "granite cleaner": "🪨",
    
    # ==================== DINING & SERVING ====================
    "dinner plate": "🍽️", "salad plate": "🥗", "dessert plate": "🍰",
    "bread plate": "🍞", "charger plate": "⭕", "serving plate": "🍽️",
    "plate set": "📚", "dinnerware set": "🍽️", "12-piece dinnerware": "🔢",
    "bowl": "🥣", "soup bowl": "🍜", "cereal bowl": "🥣",
    "pasta bowl": "🍝", "rice bowl": "🍚", "ramen bowl": "🍜",
    "serving bowl": "🥗", "mixing bowl": "🥣", "salad bowl": "🥗",
    "large serving bowl": "🥣", "fruit bowl": "🍎", "decorative bowl": "🎨",
    "mug": "☕", "coffee mug": "☕", "tea mug": "🍵",
    "travel mug": "🎒", "insulated mug": "🧊", "ceramic mug": "⚪",
    "glass": "🥛", "drinking glass": "🥤", "water glass": "💧",
    "juice glass": "🧃", "tumbler": "🥤", "highball glass": "🍹",
    "wine glass": "🍷", "red wine glass": "🔴", "white wine glass": "⚪",
    "champagne flute": "🥂", "beer glass": "🍺", "pint glass": "🍺",
    "glassware set": "🥛", "stemware set": "🍷", "barware set": "🍸",
    "serving platter": "🍽️", "rectangular platter": "▬", "oval platter": "🥚",
    "round platter": "⭕", "tiered platter": "📊", "cake platter": "🎂",
    "cheese platter": "🧀", "charcuterie board": "🥓", "serving board": "🪵",
    "gravy boat": "🚢", "sauce boat": "⛵", "creamer": "🥛",
    "sugar bowl": "🍬", "salt cellar": "🧂", "butter dish": "🧈",
    "napkin holder": "🧻", "napkin ring": "💍", "napkin ring set": "💍",
    "tablecloth": "📋", "table runner": "🏃", "placemats": "📄",
    "cloth napkins": "🧻", "dinner napkins": "🍽️", "cocktail napkins": "🍸",
    "utensil holder": "🥄", "flatware caddy": "🧰", "silverware organizer": "🗃️",
    "cake stand": "🎂", "tiered cake stand": "📊", "rotating cake stand": "🔄",
    "cupcake stand": "🧁", "dessert stand": "🍰", "pie stand": "🥧",
    "salad servers": "🥗", "pasta server": "🍝", "cake server": "🎂",
    "pie server": "🥧", "lasagna server": "🍝", "fish server": "🐟",
    "tea pot": "🫖", "tea kettle": "🫖", "tea infuser": "🍵",
    "french press": "☕", "coffee carafe": "☕", "thermal carafe": "🧊",
}



# ==================== MODEL CONFIGURATION ====================

AVAILABLE_MODELS = {
    "Llama 3.3 70B (Best)": {"type": "groq", "model": "llama-3.3-70b-versatile"},
    "Llama 3.1 8B (Fast)": {"type": "groq", "model": "llama-3.1-8b-instant"},
    "Mixtral 8x7B": {"type": "groq", "model": "mixtral-8x7b-32768"},
    "GPT-2": {"type": "huggingface", "model": "gpt2"},
    "FLAN-T5": {"type": "huggingface", "model": "google/flan-t5-base"},
    "DialoGPT": {"type": "huggingface", "model": "microsoft/DialoGPT-medium"}
}


CSV_PATH = r"C:\Users\Gouthum\Downloads\inlighn projects(practical)\recipe_dataset\RAW_recipes.csv"


# ==================== LOAD RECIPES CSV ====================

@st.cache_data
def load_recipes_csv():
    try:
        df = pd.read_csv(CSV_PATH)
        return df
    except Exception as e:
        st.error(f"Could not load CSV file: {e}")
        return None

recipes_df = load_recipes_csv()


# ========== ✅ CREATE CHROMADB KNOWLEDGE BASE (RAG Setup) ==========
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Check if recipes_df loaded properly
if recipes_df is not None:
    recipes_df = recipes_df.fillna("")

    # Combine relevant text columns (name + description + ingredients)
    if all(col in recipes_df.columns for col in ["name", "description", "ingredients"]):
        texts = (
            recipes_df["name"] + " " +
            recipes_df["description"] + " " +
            recipes_df["ingredients"].astype(str)
        ).tolist()
    else:
        texts = recipes_df.astype(str).apply(" ".join, axis=1).tolist()

    # Initialize embedding model

    from langchain_huggingface import HuggingFaceEmbeddings

    
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

    # Create or load Chroma vector store (persistent)
    db = Chroma.from_texts(texts, embedding_model, persist_directory="chroma_db_store")
    db.persist()

    # Create retriever for LangChain RAG
    retriever = db.as_retriever(search_kwargs={"k": 3})

    st.success("✅ RAG knowledge base ready using ChromaDB!")
else:
    st.warning("⚠️ Could not load recipe dataset — skipping RAG setup.")




# ==================== EXPORT Chat to text  FUNCTIONS ====================
def export_chat_to_text():
    """Export chat history to text format"""
    if not st.session_state.chat_history:
        return None, None  
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content = f"AI Recipe Assistant - Chat Export\nExported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += f"Total Messages: {len(st.session_state.chat_history)}\n" + "="*60 + "\n\n"
    for idx, chat in enumerate(st.session_state.chat_history, 1):
        content += f"Chat #{idx}\nYou: {chat['user']}\nAssistant: {chat['assistant']}\n" + "-"*60 + "\n\n"
    return content, f"chat_export_{timestamp}.txt"





# =================Export Chat Json Function=============================
def export_chat_to_json():
    """Export chat history to JSON format"""
    if not st.session_state.chat_history:
        return None, None  # ← FIXED: Return tuple instead of None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_data = {
        "export_date": datetime.now().isoformat(),
        "total_messages": len(st.session_state.chat_history),
        "user_name": st.session_state.preferences['user_name'],
        "conversations": st.session_state.chat_history
    }
    return json.dumps(export_data, indent=2), f"chat_export_{timestamp}.json"





#========================Create gmail share Function======================================
def create_gmail_body():
    """Create Gmail body with chat history"""
    if not st.session_state.chat_history:
        return ""
    body = "AI Recipe Assistant - Chat History%0D%0A%0D%0A"
    for idx, chat in enumerate(st.session_state.chat_history[:10], 1):
        # Clean special characters for URL encoding
        user_msg = chat['user'].replace('&', 'and').replace('#', '').replace('%', 'percent')
        asst_msg = chat['assistant'].replace('&', 'and').replace('#', '').replace('%', 'percent')
        
        # Truncate only if longer than 10000 characters
        if len(user_msg) > 10000:
            user_msg = user_msg[:10000] + "... (message truncated)"
        if len(asst_msg) > 10000:
            asst_msg = asst_msg[:10000] + "... (message truncated)"
        
        body += f"Chat {idx}:%0D%0AQ: {user_msg}%0D%0AA: {asst_msg}%0D%0A%0D%0A"
    
    if len(st.session_state.chat_history) > 10:
        body += f"...and {len(st.session_state.chat_history) - 10} more conversations. Download full history for all chats."
    return body




#==================Create whatsapp Text Function======================================
def create_whatsapp_text():
    """Create WhatsApp formatted text"""
    if not st.session_state.chat_history:
        return ""
    text = "🤖 *AI Recipe Assistant - Chat Export*\n\n"
    for idx, chat in enumerate(st.session_state.chat_history[:5], 1):
        # Escape special characters for URL encoding
        user_msg = chat['user'][:100].replace('&', 'and')
        asst_msg = chat['assistant'][:100].replace('&', 'and')
        text += f"*Chat {idx}:*\nQ: {user_msg}\nA: {asst_msg}\n\n"
    if len(st.session_state.chat_history) > 5:
        text += f"_...and {len(st.session_state.chat_history) - 5} more conversations_"
    return text




# ==================== HELPER FUNCTIONS ====================

# ====================Ingredient Information================
def get_ingredient_info(ingredient_lower):
    """Get price, quantity, and icon for an ingredient"""
    default_info = {'price': 5.0, 'quantity': '1 unit', 'icon': '🛒'}
    
    for key, data in ingredient_data.items():
        if key in ingredient_lower:
            return data
    return default_info



# ==================Item Information=======================(fix1)
def get_item_info(item_name):
    """Get info for any item (ingredient or equipment) with fallback message"""
    item_lower = item_name.lower().strip()
    
    # Check if it's equipment first
    if item_lower in EQUIPMENT_PRICES:
        return {
            'price': EQUIPMENT_PRICES[item_lower],
            'quantity': '1 unit',
            'icon': equipment_icons.get(item_lower, '❓'),
            'type': 'equipment',
            'available': True
        }
    
    # Check if it's an ingredient
    if item_lower in ingredient_data:
        return {
            **ingredient_data[item_lower],
            'type': 'ingredient',
            'available': True
        }
    
    # Item not found - return fallback message
    return {
        'price': 0.00,
        'quantity': 'Not available',
        'icon': '❌',
        'type': 'unavailable',
        'available': False,
        'message': f"'{item_name}' is currently not available in our inventory. Please check back later or contact support."
    }





# ========Checkout Function to save order History========================
def complete_purchase():                          #Function1
    """Complete the purchase and save to order history"""
    if st.session_state.cart:
        import datetime
        
        order = {
            'order_id': f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'items': st.session_state.cart.copy(),
            'total': st.session_state.total_price,
            'status': 'completed'
        }
        
        st.session_state.order_history.append(order)
        
        # Clear cart after purchase
        st.session_state.cart = []
        st.session_state.total_price = 0.0
        
        return order
    return None




# ==================Nutrition Calculation Function==============
def calculate_nutrition(ingredients_list):
    """Calculate total nutrition from ingredients"""
    total_nutrition = {
        'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0,
        'sodium': 0, 'calcium': 0, 'iron': 0, 'vitamin_a': 0, 'vitamin_c': 0
    }
    
    nutrition_details = []
    
    for ingredient in ingredients_list:
        ingredient_lower = ingredient.lower().strip()
        matched = False
        
        for food, nutrition in NUTRITION_DB.items():
            if food in ingredient_lower:
                for key in total_nutrition:
                    total_nutrition[key] += nutrition.get(key, 0)  # safe
                nutrition_details.append((ingredient, nutrition))
                matched = True
                break
        
        if not matched:
            for key in total_nutrition:
                total_nutrition[key] += 10  # fallback for unknown ingredients
    
    return total_nutrition, nutrition_details
    



# =================Calculate total Price with quantities======================
def calculate_price(ingredients_list, quantities=None):
    """Calculate total price with quantities"""
    total_price = 0
    item_prices = []
    
    if quantities is None:
        quantities = [1] * len(ingredients_list)
    
    for idx, ingredient in enumerate(ingredients_list):
        ingredient_lower = ingredient.lower().strip()
        info = get_ingredient_info(ingredient_lower)
        price = info['price'] * quantities[idx]
        quantity = info['quantity']
        icon = info['icon']
        item_prices.append((ingredient, price, quantity, icon, quantities[idx]))
        total_price += price
    
    return item_prices, total_price
    



#================Equipment for Recipies ======================
def get_equipment_for_recipe(recipe_name):
    """Get equipment needed for a recipe"""
    recipe_lower = recipe_name.lower()
    for keyword, equipment in COOKING_EQUIPMENT.items():
        if keyword in recipe_lower:
            return equipment
    return COOKING_EQUIPMENT['default']

def add_to_cart(ingredient, quantity=1):
    """Add item to shopping cart"""
    try:
        st.session_state.shopping_cart.append({
            'ingredient': ingredient,
            'quantity': quantity,
            'timestamp': datetime.now()
        })
        st.session_state.cart_items_count = len(st.session_state.shopping_cart)
        return True
    except:
        return False




#==================add item to cart with message=================
def add_to_cart_with_message(ingredient, quantity=1):
    """Add item to cart with success/failure message"""
    try:
        for _ in range(quantity):
            st.session_state.shopping_cart.append({
                'ingredient': ingredient,
                'quantity': 1,
                'timestamp': datetime.now()
            })
        st.session_state.cart_items_count = len(st.session_state.shopping_cart)
        return True, f"✅ {ingredient} (x{quantity}) added to cart! Happy shopping!"
    except Exception as e:
        return False, f"❌ We couldn't add {ingredient} due to technical issues. Please try again later."





# =================Update achivements Function =============================

def update_achievements():
    """Update user achievements based on activity"""
    achievements = st.session_state.achievements
    messages = st.session_state.total_messages
    favorites = len(st.session_state.favorites)
    cart_items = st.session_state.cart_items_count
    
    if messages >= 5 and '💬 Chatty Chef' not in achievements:
        achievements.append('💬 Chatty Chef')
        st.toast("🎉 Achievement Unlocked: Chatty Chef!")
    
    if messages >= 10 and '🔥 Cooking Enthusiast' not in achievements:
        achievements.append('🔥 Cooking Enthusiast')
        st.toast("🎉 Achievement Unlocked: Cooking Enthusiast!")
    
    if messages >= 50 and '👑 Master Chef' not in achievements:
        achievements.append('👑 Master Chef')
        st.toast("🎉 Achievement Unlocked: Master Chef!")
        st.balloons()
    
    if favorites >= 1 and '⭐ First Favorite' not in achievements:
        achievements.append('⭐ First Favorite')
        st.toast("🎉 Achievement Unlocked: First Favorite!")
    
    if cart_items >= 1 and '🛒 First Purchase' not in achievements:
        achievements.append('🛒 First Purchase')
        st.toast("🎉 Achievement Unlocked: First Purchase!")
    
    st.session_state.achievements = list(set(achievements))






#====================Locked Achivements Function============================
def get_locked_achievements():
    """Get list of locked achievements"""
    all_achievements = [
        ('🏆 First Chat', 1, 'messages'),
        ('💬 Chatty Chef', 5, 'messages'),
        ('🔥 Cooking Enthusiast', 10, 'messages'),
        ('👑 Master Chef', 50, 'messages'),
        ('⭐ First Favorite', 1, 'favorites'),
        ('🛒 First Purchase', 1, 'cart')
    ]
    
    locked = []
    unlocked = st.session_state.achievements
    messages = st.session_state.total_messages
    favorites = len(st.session_state.favorites)
    cart = st.session_state.cart_items_count
    
    for achievement, requirement, type_req in all_achievements:
        if achievement not in unlocked:
            if type_req == 'messages':
                locked.append(f"🔒 {achievement} (Send {requirement} messages) - Progress: {messages}/{requirement}")
            elif type_req == 'favorites':
                locked.append(f"🔒 {achievement} (Save {requirement} favorites) - Progress: {favorites}/{requirement}")
            elif type_req == 'cart':
                locked.append(f"🔒 {achievement} (Add {requirement} items to cart) - Progress: {cart}/{requirement}")
    
    return locked





# =================Search reipies Function =========================
def search_recipes(query, page=0, items_per_page=50):
    """Search recipes from CSV with pagination"""
    if not query or recipes_df is None:
        return pd.DataFrame(), 0
    
    mask = recipes_df['name'].str.contains(query, case=False, na=False)
    filtered_df = recipes_df[mask]
    
    total_results = len(filtered_df)
    start_idx = page * items_per_page
    end_idx = start_idx + items_per_page
    
    paginated_df = filtered_df.iloc[start_idx:end_idx]
    
    return paginated_df, total_results


# ==============CSV + ChromaDB (RAG Setup) ===========================
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = recipes_df['recipe'].astype(str).tolist()
chunks = text_splitter.split_text("\n".join(texts))

vector_db = Chroma.from_texts(chunks, embedding=embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 3})



# ================Chat with LLM (RAG Integrated, LangChain v1.x)========================
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

def chat_with_groq(user_message, model_name, chat_history=[]):
    """Chat with Groq LLM + RAG (Retrieval-Augmented Generation)"""
    try:
        model_config = AVAILABLE_MODELS[model_name]
        llm = ChatGroq(
            model=model_config["model"],
            temperature=0.7,
            max_tokens=1000
        )

        # ✅ Ensure retriever (ChromaDB) exists
        if 'retriever' not in globals():
            return "RAG not initialized yet. Please ensure ChromaDB setup runs before chat."

        # ✅ Define a simple prompt for contextual answering
        prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful AI cooking assistant. Use the following context to answer the user's question:
            {context}
            Question: {question}
            """
        )

        # ✅ Build RAG pipeline using the modern API
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        # ✅ Ask the model using retrieval + generation
        response = rag_chain.invoke({"input": user_message})
        return response["answer"] if "answer" in response else str(response)

    except Exception as e:
        return f"I'm here to help with cooking! What would you like to know? (Error: {str(e)})"




# ========== ✅ CREWAI MULTI-AGENT LAYER ==========
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

# Initialize Groq LLM Agent
llm_agent = ChatGroq(model="llama-3.3-70b-versatile")

# 🧩 Define all 5 specialized agents
recipe_chef = Agent(
    role="Recipe Chef",
    goal="Create, refine, and explain step-by-step recipes with clear cooking instructions.",
    backstory="A world-class chef passionate about flavor, creativity, and technique.",
    llm=llm_agent
)

equipment_expert = Agent(
    role="Equipment Expert",
    goal="Recommend the most suitable kitchen tools and appliances for each recipe, ensuring efficiency and safety.",
    backstory="A culinary engineer with expert knowledge of utensils, cookware, and modern gadgets.",
    llm=llm_agent
)

nutritionist = Agent(
    role="Nutritionist",
    goal="Analyze the nutritional content of recipes and suggest healthier ingredient substitutions.",
    backstory="A certified nutrition expert who specializes in balanced diet planning and healthy cooking.",
    llm=llm_agent
)

meal_planner = Agent(
    role="Meal Planner",
    goal="Design weekly or daily meal plans using recipe data and nutritional information to balance taste and health.",
    backstory="A creative planner who helps users maintain diet goals while enjoying diverse meals.",
    llm=llm_agent
)

shopping_assistant = Agent(
    role="Shopping Assistant",
    goal="Identify missing ingredients, recommend substitutes, and assist in adding items to the shopping cart.",
    backstory="A grocery expert familiar with local markets and online ingredient sourcing.",
    llm=llm_agent
)

# 🧠 Define collaborative tasks (can be dynamically replaced later)
task1 = Task(description="Generate a delicious and unique pasta recipe", agent=recipe_chef)
task2 = Task(description="Recommend essential tools and cooking equipment", agent=equipment_expert)
task3 = Task(description="Analyze and optimize recipe nutrition", agent=nutritionist)
task4 = Task(description="Plan a balanced meal schedule around this recipe", agent=meal_planner)
task5 = Task(description="Find and suggest missing ingredients for this dish", agent=shopping_assistant)

# ⚙️ Create multi-agent Crew in proper order
crew = Crew(
    agents=[recipe_chef, equipment_expert, nutritionist, meal_planner, shopping_assistant],
    tasks=[task1, task2, task3, task4, task5]
)

# ========== ✅ LANGGRAPH WORKFLOW INTEGRATION ==========
from agent_graph import build_agent_graph

# Build and run the agent coordination graph
graph = build_agent_graph()
result = graph.run()

# (Optional) Display LangGraph result in sidebar
st.sidebar.write("🧩 LangGraph Output:", result)


# ========== ✅ AUTOGEN MULTI-AGENT CHAT ==========
from autogen import AssistantAgent, UserProxyAgent

# Define AI agents (example roles)
chef = AssistantAgent(
    name="Chef",
    system_message="You are a creative chef who prepares and explains recipes clearly."
)
nutritionist = AssistantAgent(
    name="Nutritionist",
    system_message="You analyze nutritional values and suggest healthy alternatives."
)

# Start an autonomous chat between Chef and Nutritionist
chef.initiate_chat(
    nutritionist,
    message="How many calories does my pasta recipe have?"
)

# (Optional) Show AutoGen interaction result in sidebar for visibility
st.sidebar.write("🤖 AutoGen Agents are communicating...")




# ==================== SIDEBAR ==================== 
with st.sidebar:
    st.markdown(f"### Welcome, {st.session_state.preferences['user_name']}! 👋")
    col1, col2 = st.columns(2)             #updatee2
    with col1:
        if st.button(f"👛 Wallet\n${st.session_state.wallet_balance:.2f}", use_container_width=True):
            st.session_state.show_wallet_topup = True
            st.session_state.show_giftcard_topup = False
            st.rerun()
    with col2:
        if st.button(f"🎁 Gift Card\n${st.session_state.gift_card_balance:.2f}", use_container_width=True):
            st.session_state.show_giftcard_topup = True
            st.session_state.show_wallet_topup = False
            st.rerun() 

    # ========== ✅ AUTOGEN RUN BUTTON ==========
    st.markdown("---")  # Optional divider
    st.markdown("### 🤖 Agentic AI Discussion")
    
    if st.sidebar.button("🤝 Run AutoGen Discussion"):
        chef.initiate_chat(
            nutritionist,
            message="Let's analyze the calories for this pasta recipe."
        )
        st.sidebar.success("AutoGen discussion completed successfully!")


    
    # ==================== WALLET & GIFT CARD TOP-UP ==================== updatee3
    from datetime import datetime
    import random, time
    
    if st.session_state.show_wallet_topup or st.session_state.show_giftcard_topup:
        topup_type = "Wallet" if st.session_state.show_wallet_topup else "Gift Card"
        icon = "👛" if st.session_state.show_wallet_topup else "🎁"
        
        st.markdown(f"### {icon} Add Money to {topup_type}")
        
        if st.button("← Close"):
            st.session_state.show_wallet_topup = False
            st.session_state.show_giftcard_topup = False
            st.rerun()
        
        
        
        st.markdown("#### Select Payment Method:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💳 Credit Card", use_container_width=True):
                st.session_state.selected_topup_method = "credit_card"
            if st.button("🏦 Debit Card", use_container_width=True):
                st.session_state.selected_topup_method = "debit_card"
            if st.button("📱 UPI", use_container_width=True):
                st.session_state.selected_topup_method = "upi"
            if st.button("🌐 Net Banking", use_container_width=True):
                st.session_state.selected_topup_method = "netbanking"
        with col2:
            if st.button("💼 PayPal", use_container_width=True):
                st.session_state.selected_topup_method = "paypal"
            if st.button("📲 Google Pay", use_container_width=True):
                st.session_state.selected_topup_method = "gpay"
            if st.button("📳 PhonePe", use_container_width=True):
                st.session_state.selected_topup_method = "phonepe"
            if st.button("💰 Paytm", use_container_width=True):
                st.session_state.selected_topup_method = "paytm"
        

        # -------------------- Dynamic Payment Gateway Simulation --------------------
        import re
        import time, random
        from datetime import datetime
        import streamlit as st
        
        if 'selected_topup_method' in st.session_state and st.session_state.selected_topup_method:
            payment_method = st.session_state.selected_topup_method
        
            # ✅ Clean and simple: user can enter between 1 and 50000 (default 100, but editable)
            amount = st.number_input(
                "Enter Amount ($):",
                min_value=1,
                max_value=50000,
                value=100,
                step=10,
                help="Enter the amount you want to top-up (min $1, max $50,000)"
            )
            st.session_state.topup_amount = amount  # store chosen amount dynamically
        
            # Detect topup type
            topup_type = "Wallet" if st.session_state.get("show_wallet_topup", False) else "Gift Card"
        
            st.markdown(f"### 💳 {payment_method.replace('_', ' ').title()} Payment")
            st.info(f"You're adding **${float(amount):.2f}** to your **{topup_type}** using **{payment_method.replace('_', ' ').title()}**")
        
            with st.form(f"payment_form_{payment_method}"):
        
                # Credit/Debit Cards
                if payment_method in ["credit_card", "debit_card"]:
                    col1, col2 = st.columns(2)
                    with col1:
                        card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456", max_chars=16)
                    with col2:
                        expiry = st.text_input("Expiry (MM/YY or MM/YYYY)", placeholder="12/29", max_chars=7)
                    cvv = st.text_input("CVV", type="password", max_chars=3, placeholder="***")
                    name = st.text_input("Cardholder Name", placeholder="Goutham Kharvi")
                
                    # --- Phone number for OTP (required for card auth) ---
                    phone = st.text_input("Mobile Number for OTP", placeholder="+91 9XXXXXXXXX", key=f"card_phone_{payment_method}")
                
                    
                
                    # --------- Expiry validation (must be AFTER Nov 1, 2025) ----------
                    valid_expiry = True
                    expiry_error_shown = False
                    if expiry:
                        m = re.fullmatch(r"\s*(\d{1,2})\s*/\s*(\d{2}|\d{4})\s*$", expiry)
                        if not m:
                            valid_expiry = False
                            st.warning("⚠️ Enter expiry as MM/YY or MM/YYYY (e.g., 11/26 or 11/2026).")
                            expiry_error_shown = True
                        else:
                            mon = int(m.group(1))
                            yr = int(m.group(2))
                            if yr < 100:  # two-digit year -> convert to 20xx
                                yr += 2000
                            if mon < 1 or mon > 12:
                                valid_expiry = False
                                st.error("🚫 Invalid expiry month (must be 01-12).")
                                expiry_error_shown = True
                            else:
                                try:
                                    card_exp_date = datetime(yr, mon, 1)
                                    cutoff = datetime(2025, 11, 1)
                                    if card_exp_date <= cutoff:
                                        valid_expiry = False
                                        st.error("🚫 Card declined: card must expire after **Nov 2025**.")
                                        expiry_error_shown = True
                                except Exception:
                                    valid_expiry = False
                                    st.error("🚫 Invalid expiry date provided.")
                                    expiry_error_shown = True
                
                    # If user hasn't entered expiry yet, don't spam an error (only show if they typed invalid)
                    if not expiry and not expiry_error_shown:
                        valid_expiry = False  # mark as invalid until user provides a valid expiry
                

                    # ------------------ OTP send & validation inside the form ------------------
                    # Use form_submit_button for "Get OTP" (forms cannot contain st.button)
                    get_otp_clicked = st.form_submit_button("📩 Get OTP")
                    st.image("https://t4.ftcdn.net/jpg/04/16/93/07/360_F_416930739_UeumuMO5QhZOXIAc09s7gz6JSPT97duS.jpg", width=400)
                    
                    # If Get OTP clicked: require phone, generate (simulate) OTP and set session flag
                    if get_otp_clicked:
                        if not phone or not phone.strip():
                            st.error("🚫 Enter a mobile number to receive OTP.")
                        else:
                            # Generate and store OTP in session state for this payment_method
                            sent_otp = f"{random.randint(100000, 999999)}"
                            st.session_state[f"sent_otp_{payment_method}"] = sent_otp
                            st.session_state[f"otp_sent_flag_{payment_method}"] = True
                            st.success("✅ OTP sent to your registered mobile number.")
                    
                            # 🔹 Show popup OTP message for demo (just like Net Banking)
                            st.info(f"📩 **Your OTP is: {sent_otp}** (Do not share otp to anyone )")

                    
                    if st.session_state.get(f"otp_sent_flag_{payment_method}", False):
                        otp_value = st.text_input(
                            "Enter 6-digit OTP",
                            max_chars=6,
                            placeholder="Enter OTP here",
                            key=f"card_otp_input_{payment_method}"
                        )
                    
                        # 🔹 Live validation: digits only
                        if otp_value and not re.fullmatch(r"\d{0,6}", otp_value):
                            st.warning("⚠️ Only digits (0–9) are allowed. Non-numeric input will be ignored.")
                            otp_value = ''.join(filter(str.isdigit, otp_value))[:6]
                    
                        # 🔹 Too short? Show error & mark invalid
                        if otp_value and len(otp_value) < 6:
                            st.error("🚫 Please enter all 6 digits of your OTP before proceeding.")
                            valid_card_otp = False
                    
                        # 🔹 Exactly 6 digits → validate
                        elif re.fullmatch(r"\d{6}", otp_value):
                            sent = st.session_state.get(f"sent_otp_{payment_method}")
                            if sent and otp_value == sent:
                                st.success("✅ OTP verified successfully.")
                                valid_card_otp = True
                            else:
                                st.error("🚫 Invalid OTP! Please recheck and try again.")
                                valid_card_otp = False
                    else:
                        valid_card_otp = False


                        
                # ✅ UPI & Wallets
                elif payment_method in ["upi", "gpay", "phonepe", "paytm"]:
                    upi_id = st.text_input("Enter your UPI ID / Mobile Number", placeholder="example@upi or +91 XXXXX XXXXX")
                    st.image("https://indiashippingnews.com/wp-content/uploads/2024/08/UPI.jpg", width=400)
                    st.markdown("📱 **Scan QR or approve request in your UPI app**")
        
                    # --- Secure PIN field ---
                    pincode = st.text_input(
                        "Enter Secure PIN (Only 5 digits allowed)",
                        max_chars=5,
                        type="password",
                        placeholder="e.g., 12345"
                    )
        
                    # Validate PIN input live
                    if pincode and not re.fullmatch(r"\d{0,5}", pincode):
                        st.warning("⚠️ Only digits (0–9) are allowed. Non-numeric input will be ignored.")
                        pincode = ''.join(filter(str.isdigit, pincode))[:5]
        
                    valid_pin = bool(re.fullmatch(r"\d{5}", pincode))
        
                # ✅ PayPal
                elif payment_method == "paypal":
                    st.image(
                        "https://cdn.prod.website-files.com/659a9ef71c962485037fcc8f/66a067ab67d8703fc37fa481_AD_4nXepBT5ccXFloGAK7MKP6bnHmNR4_1A-cfFwKuF0NdbGFBviRzKalRjbXSa4x3tdZmlTCSTI0DQUJ4C0-AOjraTxENDhxk_4w7ei14KKLRO6RZ0oa_y8rP_gwIMSyJCq3LDTVcbpk3opw5bWvnCgJKJlW9AN.jpeg",
                        width=400
                    )
                    st.markdown("🌍 You’ll be redirected to PayPal secure gateway on submit.")
        
                    # --- Email & Password ---
                    email = st.text_input("PayPal Email", placeholder="your@email.com")
                    password = st.text_input(
                        "PayPal Password (10 characters with Uppercase, Number & Special Character)",
                        type="password",
                        max_chars=10,
                        placeholder="••••••••••"
                    )
        
                    # Password validation
                    valid_password = bool(re.fullmatch(
                        r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10}', password))
        
                    if password and not valid_password:
                        st.warning("⚠️ Password must be exactly 10 characters long and include uppercase, lowercase, number, and special character.")
        
                    # --- OTP Section ---
                    st.markdown("📱 **Enter your registered mobile number to receive OTP**")
                    mobile_number = st.text_input("Mobile Number", placeholder="+91 XXXXX XXXXX")
                    otp = st.text_input("Enter 6-digit OTP", max_chars=6, placeholder="Enter OTP here")

                    
        
                    # OTP validation
                    if otp and not re.fullmatch(r"\d{0,6}", otp):
                        st.warning("⚠️ Only digits (0–9) are allowed. Non-numeric input will be ignored.")
                        otp = ''.join(filter(str.isdigit, otp))[:6]
        
                    valid_otp = bool(re.fullmatch(r"\d{6}", otp))
        
                # ✅ Net Banking
                elif payment_method == "netbanking":
                    st.subheader("🏦 Net Banking Payment")
                
                    # ---- SELECT BANK ----
                    bank_name = st.selectbox(
                        "Select Bank",
                        [
                            "State Bank of India", "Canara Bank", "HDFC Bank", "ICICI Bank",
                            "Axis Bank", "IDBI Bank", "Kotak Mahindra Bank", "Bank of Baroda"
                        ]
                    )
                
                    # ---- USER ID (exactly 8 alphanumeric) ---- 
                    user_id = st.text_input(
                        "NetBanking User ID (exactly 8 alphanumeric characters)",
                        max_chars=8,
                        placeholder="Example: Abc12345",
                        key=f"netbank_user_{payment_method}"
                    )
                
                    valid_netbank_userid = False
                    if user_id:
                        if not re.fullmatch(r"[A-Za-z0-9]{8}", user_id):
                            st.error("🚫 User ID must be exactly 8 alphanumeric characters.")
                        else:
                            valid_netbank_userid = True
                    st.session_state["valid_netbank_userid"] = valid_netbank_userid
                
                    # ---- COUNTRY CODE & PHONE ----
                    country_code = st.text_input("Country Code (e.g. +91)", value="+91", max_chars=3, key=f"netbank_cc_{payment_method}")
                    phone_number = st.text_input("Phone Number (10 digits)", max_chars=10, key=f"netbank_phone_{payment_method}")
                
                    valid_netbank_phone = False
                    if phone_number:
                        if not re.fullmatch(r"\d{10}", phone_number):
                            st.error("🚫 Phone number must be exactly 10 digits.")
                        else:
                            valid_netbank_phone = True
                    st.session_state["valid_netbank_phone"] = valid_netbank_phone
                
                    # ---- OTP SECTION (ALWAYS VISIBLE) ----
                    st.markdown("### 🔐 OTP Verification")
                
                    # Get OTP Button - triggers popup alert
                    if st.form_submit_button("📩 Get OTP"):
                        if valid_netbank_userid and valid_netbank_phone:
                            generated_otp = f"{random.randint(100000, 999999)}"
                            st.session_state["netbank_otp"] = generated_otp
                            st.session_state["netbank_otp_sent"] = True
                            st.session_state["valid_netbank_otp"] = False
                
                            # ✅ Show popup alert with OTP
                            st.components.v1.html(
                                f"<script>alert('✅ Your 6-digit OTP is: {generated_otp}');</script>",
                                height=0,
                            )
                        else:
                            st.error("⚠️ Enter a valid User ID and 10-digit phone number before requesting OTP.")
                
                    # Enter OTP Field (always visible)
                    otp_input = st.text_input("Enter 6-digit OTP", max_chars=6, key=f"netbank_otp_input_{payment_method}")
                
                    netbank_otp_valid = False
                    if otp_input:
                        if not re.fullmatch(r"\d{6}", otp_input):
                            st.error("🚫 OTP must be exactly 6 digits.")
                        else:
                            sent_otp = st.session_state.get("netbank_otp")
                            if sent_otp and otp_input == sent_otp:
                                st.success("✅ OTP verified successfully.")
                                netbank_otp_valid = True
                            else:
                                st.error("🚫 Invalid OTP! Please check and try again.")
                    st.session_state["valid_netbank_otp"] = netbank_otp_valid
                
                    # ---- PASSWORD ----
                    st.markdown("### 🔑 NetBanking Password")
                    netbank_password = st.text_input(
                        "Enter NetBanking Password (min 12 chars, max 200, must have upper, lower, digit, special)",
                        type="password",
                        max_chars=200,
                        key=f"netbank_pwd_{payment_method}"
                    )
                
                    def validate_netbank_password(pwd):
                        if not pwd:
                            return None
                        if len(pwd) < 12:
                            return "⚠️ For security reasons, you need to enter your strong password (min 12 chars)."
                        if len(pwd) > 200:
                            return "🚫 Password too long — max 200 characters allowed."
                        if not re.search(r"[A-Z]", pwd):
                            return "Password must include at least one uppercase letter."
                        if not re.search(r"[a-z]", pwd):
                            return "Password must include at least one lowercase letter."
                        if not re.search(r"\d", pwd):
                            return "Password must include at least one digit."
                        if not re.search(r"[@$!%*?&\-\_\+\=<>#^(){}\[\]:;,.\/\\~`|]", pwd):
                            return "Password must include at least one special character."
                        return None
                
                    pwd_error = validate_netbank_password(netbank_password)
                    if pwd_error:
                        st.error(pwd_error)
                    st.session_state["valid_netbank_pwd"] = (pwd_error is None and bool(netbank_password))
                
                    # Keep for final payment validation
                    bank_name = bank_name
                    user_id = user_id
                    password = netbank_password




                        
                # ✅ Terms & Conditions
                st.markdown("### 🧾 Terms & Conditions")
                with st.expander("📜 View Terms and Conditions", expanded=False):
                    st.write("""
                    1. Payments are processed securely with encryption.  
                    2. Refunds (if any) will be credited within 3–5 business days.  
                    3. The user agrees not to share payment credentials.  
                    4. Transactions are final once confirmed.  
                    """)
        
                accept_terms = st.checkbox("✅ I accept the Terms and Conditions")
        
                # 🪙 Pay Button
                submitted = st.form_submit_button(f"💰 Pay ${float(amount):.2f}", type="primary", use_container_width=True)
        
                if submitted:
                    # Validation before payment
                    missing_fields = False
                    if payment_method in ["credit_card", "debit_card"] and (not card_number or not expiry or not cvv or not name):
                        missing_fields = True
                    elif payment_method in ["upi", "gpay", "phonepe", "paytm"] and not upi_id:
                        missing_fields = True
                    elif payment_method == "paypal":
                        if not email.strip() or not password.strip() or not mobile_number.strip() or not otp.strip():
                            missing_fields = True
                        elif not valid_password:
                            st.error("🚫 Invalid Password! Must be exactly 10 characters long and include uppercase, lowercase, number, and special character.")
                            missing_fields = True
                        elif not valid_otp:
                            st.error("🚫 Invalid OTP! Must be exactly 6 numeric digits.")
                            missing_fields = True
                            
                    # 🔹 UPDATED NETBANKING VALIDATION STARTS HERE
                   
                    elif payment_method == "netbanking":
                        # require all fields present
                        if not bank_name or not user_id or not password or not st.session_state.get("netbank_otp_sent", False):
                            missing_fields = True
                        elif not st.session_state.get("valid_netbank_userid", False):
                            st.error("🚫 Invalid User ID — must be exactly 8 alphanumeric characters.")
                            missing_fields = True
                        elif not st.session_state.get("valid_netbank_pwd", False):
                            st.error("🚫 Invalid NetBanking password. Must be at least 12 characters and include uppercase, lowercase, digit, and special symbol.")
                            missing_fields = True
                        elif not st.session_state.get("valid_netbank_otp", False):
                            st.error("🚫 OTP verification failed or missing. Please request OTP and enter the 6-digit code.")
                            missing_fields = True
        
                    if missing_fields:
                        st.warning("⚠️ Please fill in all the required fields before proceeding.")
                    elif not accept_terms:
                        st.error("❌ Please accept the Terms & Conditions to continue.")
                    elif payment_method in ["upi", "gpay", "phonepe", "paytm"] and not valid_pin:
                        st.error("🚫 Invalid PIN! Must be exactly 5 numeric digits.")
                    elif payment_method in ["credit_card", "debit_card"] and not valid_card_otp:
                        st.error("🚫 OTP verification failed. Please enter a valid 6-digit OTP.")
                    else:
                        # ✅ All conditions met → process payment
                        with st.spinner("🔄 Processing your payment securely..."):
                            time.sleep(2.5)
                            transaction_id = f"TXN-{random.randint(100000, 999999)}"
        
                        # ✅ Payment Success — update balances
                        if topup_type == "Wallet" or st.session_state.get("show_wallet_topup", False):
                            st.session_state.wallet_balance = float(st.session_state.get("wallet_balance", 0.0)) + float(amount)
                            st.session_state.wallet_transactions.append({
                                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'type': 'Top-up',
                                'method': payment_method,
                                'amount': float(amount),
                                'transaction_id': transaction_id,
                                'balance': st.session_state.wallet_balance
                            })
                        else:
                            st.session_state.gift_card_balance = float(st.session_state.get("gift_card_balance", 0.0)) + float(amount)
                            st.session_state.gift_card_transactions.append({
                                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'type': 'Top-up',
                                'method': payment_method,
                                'amount': float(amount),
                                'transaction_id': transaction_id,
                                'balance': st.session_state.gift_card_balance
                            })
        
                        st.success(f"✅ Payment Successful!\n\n💸 ${float(amount):.2f} added to your {topup_type}.")
                        st.markdown(f"**Transaction ID:** `{transaction_id}`")
                        st.balloons()
        
                        # Reset/cleanup
                        st.session_state.show_wallet_topup = False
                        st.session_state.show_giftcard_topup = False
                        if "selected_topup_method" in st.session_state:
                            del st.session_state.selected_topup_method
                        st.rerun()
        
            st.markdown("---")



            
    st.markdown("## 🧭 Navigation")
                
    page = st.radio("", [
                    "💬 Chat Assistant",
                    "🔧 Agent Tools",
                    "📊 Analytics",
                    "👤 Profile",
                    "🔄 Return & Replacement"
                ], key="navigation")
                
    st.markdown("---")
                
        
    st.markdown("## 🤖 AI Model")
    selected_model = st.selectbox(
        "Select Model:",
        list(AVAILABLE_MODELS.keys()),
        key="model_selector"
    )
    st.session_state.selected_model = selected_model
    
    st.markdown("---")
    
    st.markdown("## ⚙️ Quick Settings")
    temperature = st.slider("🌡️ Temperature", 0.0, 1.0, 0.7, 0.1)
    
    st.markdown("---")
    
    # Export Chats
    st.markdown("## 📤 Export Chats")
    
    if st.button("📤 Export Options", use_container_width=True, type="secondary"):
        st.session_state.show_export = not st.session_state.show_export
    
    if st.session_state.show_export:
        if not st.session_state.chat_history:
            st.warning("⚠️ No chat history to export!")
        else:
            st.success(f"✅ {len(st.session_state.chat_history)} conversations ready to export")
            
            # Download Section
            st.markdown("### 📥 Download")
            st.caption("Save your conversations locally")
            
            col1, col2 = st.columns(2)
            
            with col1:
                content_txt, filename_txt = export_chat_to_text()
                if content_txt:
                    st.download_button(
                        label="📄 Text File",
                        data=content_txt,
                        file_name=filename_txt,
                        mime="text/plain",
                        use_container_width=True,
                        help="Download as .txt file"
                    )
            
            with col2:
                content_json, filename_json = export_chat_to_json()
                if content_json:
                    st.download_button(
                        label="📋 JSON File",
                        data=content_json,
                        file_name=filename_json,
                        mime="application/json",
                        use_container_width=True,
                        help="Download as .json file"
                    )
            
            st.markdown("---")
            
            # Share Section
            st.markdown("### 📧 Share")
            st.caption("Share via email or messaging apps")
            
            # Gmail button 
            gmail_body = create_gmail_body()
            gmail_url = f"https://mail.google.com/mail/?view=cm&su=Recipe%20Chat%20Export&body={gmail_body}"
            st.link_button("📧 Share via Gmail", gmail_url, use_container_width=True)
            
            # WhatsApp button
            whatsapp_text = create_whatsapp_text()
            whatsapp_encoded = whatsapp_text.replace(' ', '%20').replace('\n', '%0A').replace('*', '%2A').replace('_', '%5F')
            whatsapp_url = f"https://wa.me/?text={whatsapp_encoded}"
            
            st.markdown(f"""
                <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                    <button style="
                        width: 100%;
                        padding: 0.6rem;
                        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 14px;
                        font-weight: bold;
                        margin-bottom: 0.5rem;
                        transition: transform 0.2s;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                    ">
                        💬 Share via WhatsApp
                    </button>
                </a>
            """, unsafe_allow_html=True)
            
            # Copy to Clipboard button
            chat_text = "\n\n".join([f"Q: {c['user']}\nA: {c['assistant']}" for c in st.session_state.chat_history[:100]])
            
            st.markdown("---")
            st.markdown("### 📋 Quick Copy")
            st.text_area(
                "Copy to clipboard:",
                value=chat_text,
                height=150,
                help="Select all and copy (Ctrl+A, Ctrl+C)",
                key="copy_text_area"
            )
            
            if len(st.session_state.chat_history) > 5:
                st.caption(f"_Showing 5 of {len(st.session_state.chat_history)} conversations. Download full history above._")
    
    st.markdown("---")
    
    st.markdown("## ⚡ Actions")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.success("Chat cleared!")
        st.rerun()
    
    if st.button(f"🛒 Shopping Cart ({st.session_state.cart_items_count})", use_container_width=True):
        st.session_state.current_page = 'cart'
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("## 📈 Stats")
    st.metric("💬 Messages", st.session_state.total_messages)
    st.metric("📚 Recipes", "231,637")
    st.metric("🤖 Agents", "5")
    st.metric("🛒 Cart Items", st.session_state.cart_items_count)
    




    
# ==================== MAIN CONTENT ====================

if page == "💬 Chat Assistant":
    st.markdown(
    """
    <h1 style="
        font-family: 'Times new roman', 'Noto Color Emoji', 'Apple Color Emoji';
        text-align: center;
        font-size: 4em;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 10px;
    ">
        🤖 <span style="color: #007BFF;">AI Culinary Assistant</span>
    </h1>
    """,
    unsafe_allow_html=True
)
    st.markdown(f"### 👨‍🍳 Welcome, Chef {st.session_state.preferences['user_name']} | Your AI-Powered Kitchen Advisor")
    
    st.markdown("### 💡 Try asking:")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🍝 How to make pasta?", use_container_width=True):
            query = "How to make pasta from scratch?"
            response = u"""
 Let's cook some delicious pasta together! 

 **Option 1: Making Pasta from Scratch**

 **Ingredients:**
- 2 cups (250g) all-purpose flour  
- 2 large eggs  
- ½ tsp salt  
- 1 tbsp olive oil (optional)  
- A little water (if needed)

 **Steps:**
1️ **Make the Dough**  
   On a clean surface, pour the flour and form a well in the center.  
   Crack eggs into the well. Add salt and olive oil.  
   Gently mix the eggs with a fork, slowly pulling in the flour from the sides.  
   Once it starts to come together, knead the dough with your hands.  

2️ **Knead the Dough**  
   Knead for 8–10 minutes until smooth and elastic.  
   If sticky, sprinkle a little flour.  
   If dry, add a few drops of water.  

3️ **Rest the Dough**  
   Wrap in plastic wrap and rest at room temperature for 30 minutes.  
   (This helps the gluten relax and makes it easier to roll.)  

4️ **Roll the Dough**  
   Cut dough into smaller pieces.  
   Using a rolling pin or pasta machine, flatten it until thin.  
   Dust lightly with flour to prevent sticking.  

5️ **Cut the Pasta**  
   Slice into desired shapes:  
   🍜 Fettuccine (wide ribbons)  
   🍝 Tagliatelle (medium)  
   🍲 Spaghetti (thin)  
   🧀 Lasagna sheets (flat)  

6️ **Boil the Pasta**  
   Bring a large pot of salted water to a rolling boil.  
   Add pasta and cook for 2–4 minutes (fresh pasta cooks quickly).  
   Drain and toss with sauce.  

---

 **Option 2: Using Store-Bought Dried Pasta**

 **Ingredients:**
- 200g pasta (penne, spaghetti, fusilli, etc.)  
- 2 liters water  
- 1 tsp salt  
- 1 tbsp olive oil (optional)

 **Steps:**
1️ **Boil Water**  
   Fill a pot with water and bring it to a boil.  
   Add salt (this flavors the pasta).  

2️ **Add Pasta**  
   Add the pasta and stir occasionally so it doesn’t stick.  

3️ **Cook**  
   Boil for 8–12 minutes (check the package for exact time).  
   Taste to check if it’s al dente (firm but cooked).  

4️ **Drain**  
   Drain the pasta but keep a little pasta water (for mixing with sauce).  

5️ **Add Sauce**  
   Toss with your favorite sauce like:  
    Tomato basil sauce  
    Alfredo cream sauce  
    Arrabbiata  
    Mushroom sauce  

---

 **AI Cooking Progress Simulation:**  
 Mixing ingredients... 
 Kneading and rolling dough... 
 Boiling water...  
 Tossing pasta with sauce... 
 Pasta ready! Buon appetito 🇮🇹
"""


            st.session_state.chat_history.append({'user': query, 'assistant': response})
            st.session_state.total_messages += 1
            update_achievements()
            st.rerun()
    
    with col2:
        if st.button("🍗 Chicken dinner", use_container_width=True):
            query = "Suggest a chicken dinner recipe"
            response =  """# Simple, tasty chicken dinner — step-by-step

Here’s an easy, all-in-one chicken dinner: **roast chicken thighs** with **roasted vegetables** and quick **mashed potatoes**. It’s beginner-friendly, flavorful, and everything finishes around the same time.

---

## Ingredients (serves 3–4)

* 6 bone-in, skin-on chicken thighs (or 4 large thighs)
* 1 lb (450 g) potatoes (Yukon gold or russet)
* 3–4 carrots
* 1 medium red onion
* 1 bell pepper (any color)
* 3 cloves garlic
* 2 tbsp olive oil (plus extra for potatoes)
* 1 tbsp butter (optional for mash)
* 1 tsp dried thyme (or rosemary or mixed herbs)
* 1 tsp paprika (smoked or sweet)
* Salt and black pepper (about 1½ tsp salt total)
* ½ cup (120 ml) chicken stock or water (optional, for pan)
* Optional: lemon (½, for squeezing), fresh parsley for garnish

---

## Equipment

* Oven (preheated to 425°F / 220°C)
* Roasting tray or large ovenproof skillet
* Saucepan for potatoes
* Potato masher or fork
* Knife and cutting board
* Meat thermometer (helpful)

---

## Prep (10–15 minutes)

1. Preheat oven to **425°F (220°C)**.
2. Pat chicken thighs dry with paper towel. Dry skin = crispier.
3. Peel potatoes and cut into even chunks (~1½ inch). Put in cold water to avoid browning.
4. Peel carrots and cut into sticks. Slice onion into wedges. Cut bell pepper into strips.
5. Mince 2 garlic cloves (reserve 1 for mash).
6. In a small bowl, mix 2 tbsp olive oil, 1 tsp paprika, 1 tsp dried thyme, 1 tsp salt, ½ tsp pepper and the minced garlic. Rub this under the skin and over the outside of each thigh.

---

## Step-by-step cooking

### 1) Start the potatoes (20–25 minutes)

1. Put potato chunks into a saucepan, cover with cold water and add a pinch of salt.
2. Bring to a boil, then reduce to a simmer. Cook until tender when pierced with a fork — **12–15 minutes**.
3. Drain, add butter (1 tbsp) and a splash of milk or water if you like, mash roughly with salt & pepper. Keep warm.

### 2) Roast chicken & vegetables (35–40 minutes total)

1. Spread the chopped carrots, onion, and bell pepper in a roasting tray. Toss with 1 tbsp olive oil, a pinch of salt and pepper.
2. Place the seasoned chicken thighs skin-side up on top of the vegetables. If you have ½ cup stock, pour it into the pan around (not over) the chicken — this keeps veg moist and makes a small pan sauce.
3. Roast in the preheated oven at **425°F / 220°C** for **35–40 minutes**, or until:

   * Chicken skin is golden and crisp.
   * Internal temperature = **165°F / 74°C** at the thickest part (use a meat thermometer).
     If you don’t have a thermometer, pierce — juices should run clear, not pink.
4. Optional last step for extra crisp: broil (grill) for 1–2 minutes, watching closely so it doesn’t burn.

### 3) Finish and plate

1. Remove chicken and vegetables from oven. Let chicken rest 5 minutes.
2. Spoon mashed potatoes on plates, place a chicken thigh on top, pile roasted vegetables beside it.
3. Spoon pan juices over chicken and veg. Squeeze a little lemon if using, and sprinkle chopped parsley.

---

## Quick timing overview

* Prep: 10–15 min
* Potatoes boiling & mashing: 20–25 min (overlaps with roasting)
* Roast: 35–40 min
* Total from start to table: about **45–55 minutes**.

---

## Tips & variations

* **Faster:** Use boneless thighs (cook ~20–25 min) or cut vegetables smaller.
* **One-pan weeknight:** Use chicken breasts cut into large pieces so timing lines up with veg (about 25–30 min).
* **Flavor swaps:** Use Italian seasoning, curry powder, or a BBQ rub instead of paprika/thyme.
* **Crispier skin:** Start chicken skin-side up in a cold pan on medium heat for 3–4 min to render fat, then transfer to oven.
* **Make it saucy:** After roasting, place the pan on the stove, simmer pan juices with a splash of wine or stock and 1 tsp mustard for a quick gravy.

---

If you want, I can give:

* A **spicy version** (chili + lime),
* A **low-carb** option (swap mashed potatoes for cauliflower mash), or
* A **weeknight shortcut** using boneless chicken and microwave potatoes.

Which of those sounds good?
"""
            st.session_state.chat_history.append({'user': query, 'assistant': response})
            st.session_state.total_messages += 1
            update_achievements()
            st.rerun()
    
    with col3:
        if st.button("🥗 Vegetarian recipes", use_container_width=True):
            query = "Can you show me a list of the top 20 vegetarian recipes along with their common ingredients and equipment required for cooking them?"
            response = """Here are 20 popular vegetarian recipes you can choose from:

1) Vegetable Stir-Fry with Tofu  
2) Lentil Curry with Rice  
3) Caprese Salad  
4) Pasta Primavera  
5) Stuffed Bell Peppers with Quinoa  
6) Paneer Butter Masala  
7) Chana Masala (Chickpea Curry)  
8) Veggie Biryani  
9) Spinach and Ricotta Lasagna  
10) Aloo Gobi (Potato & Cauliflower Curry)  
11) Vegetable Soup  
12) Mushroom Risotto  
13) Vegetable Pulao  
14) Palak Paneer  
15) Veggie Burger  
16) Mixed Vegetable Pakora  
17) Veggie Fried Rice  
18) Roasted Vegetable Sandwich  
19) Avocado Toast  
20) Vegetable Tacos  

Common ingredients used in vegetarian recipes include:
- Vegetables (carrots, bell peppers, onions, spinach, etc.)
- Legumes (lentils, chickpeas, beans)
- Paneer or tofu
- Rice, pasta, or quinoa
- Spices (turmeric, cumin, coriander, chili powder, etc.)
- Olive oil, butter, or ghee
- Garlic, ginger, and herbs

Common equipment required:
- Stove and pans
- Mixing bowls
- Knife and chopping board
- Blender or grinder (optional)
- Measuring spoons and cups
- Cooking pot or pressure cooker

Please tell me which vegetarian recipe you’d like to cook, and I’ll give you a complete step-by-step cooking guide with ingredients!"""
            st.session_state.chat_history.append({'user': query, 'assistant': response})
            st.session_state.total_messages += 1
            update_achievements()
            st.rerun()
    
    with col4:
        if st.button("📅 Meal plans", use_container_width=True):
            query = "Create a weekly meal plan"
            response = "I can create a personalized weekly meal plan for you! Would you like to redirect to the Meal Planner Agent for a detailed plan?"
            st.session_state.chat_history.append({'user': query, 'assistant': response})
            st.session_state.total_messages += 1
            update_achievements()
            st.rerun()
    
    st.markdown("---")
    
    for idx, chat in enumerate(st.session_state.chat_history):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"<div class='chat-user'>👤 You: {chat['user']}</div>", unsafe_allow_html=True)
        with col2:
            if st.button("⭐", key=f"fav_{idx}"):
                if chat not in st.session_state.favorites:
                    st.session_state.favorites.append(chat)
                    update_achievements()
                    st.success("Added to favorites!")
                    st.rerun()
        
        st.markdown(f"<div class='chat-bot'>🤖 Assistant: {chat['assistant']}</div>", unsafe_allow_html=True)
    
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        with st.spinner("🤔 Thinking..."):
            try:
                response = chat_with_groq(user_input, st.session_state.selected_model)
            except Exception as e:
                response = "I'm here to help with cooking! What would you like to know?"
        
        st.session_state.chat_history.append({'user': user_input, 'assistant': response})
        st.session_state.total_messages += 1
        update_achievements()
        st.rerun()


# ================Agent Tools=============================
elif page == "🔧 Agent Tools":
    st.markdown(
    """
    <h1 style="
        font-family: 'Times new roman', 'Noto Color Emoji', 'Apple Color Emoji';
        text-align: center;
        font-size: 4em;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 10px;
    ">
        🤖 <span style="color: #007BFF;">Specialized AI Agents</span>
    </h1>
    """,
    unsafe_allow_html=True
)

    
    agent_choice = st.selectbox(
        "Choose an agent:",
        ["👨‍🍳 Recipe Chef", "🔧 Equipment Expert", "🥗 Nutritionist", "📅 Meal Planner", "🛒 Shopping Assistant"]
    )
    
    if agent_choice == "👨‍🍳 Recipe Chef":
        st.markdown("### 👨‍🍳 Recipe Chef Agent")
        recipe_query = st.text_input("What recipe are you looking for?", key="recipe_search")
        
        # Initialize session state for recipe selection
        if 'recipe_results' not in st.session_state:
            st.session_state.recipe_results = []
        if 'recipe_query_name' not in st.session_state:
            st.session_state.recipe_query_name = ""
        
        if st.button("🔍 Search Recipes"):
            if recipe_query and recipes_df is not None:
                results_df, total_results = search_recipes(recipe_query, 0)
                
                if total_results > 0:
                    st.session_state.recipe_results = results_df
                    st.session_state.recipe_query_name = recipe_query
                else:
                    st.warning("No recipes found. Try a different search term.")
                    st.session_state.recipe_results = []
            else:
                st.warning("Please enter a recipe name")
        
        # Display recipe results (OUTSIDE the button block)
        if len(st.session_state.recipe_results) > 0:
            st.success(f"🎯 Found {len(st.session_state.recipe_results)} Recipes for '{st.session_state.recipe_query_name}'")
            
            for idx, row in st.session_state.recipe_results.iterrows():
                recipe_name = row['name']
                
                with st.expander(f"🍳 {recipe_name}"):
                    st.markdown("📝 **Ingredients:**")
                    
                    try:
                        ingredients = ast.literal_eval(row['ingredients'])
                    except:
                        ingredients = ['ingredient1', 'ingredient2', 'ingredient3']
                    
                    # Store selected items for this recipe
                    selected_items = []
                    selected_total = 0
                    
                    # Display ingredients with checkboxes and prices
                    st.markdown("---")
                    for ing_idx, ing in enumerate(ingredients[:10]):  # Limit to 10 items
                        ing_lower = ing.lower().strip()
                        ing_info = get_ingredient_info(ing_lower)
                        
                        col1, col2, col3, col4 = st.columns([1, 5, 2, 1])
                        with col1:
                            st.markdown(f"<div style='font-size: 30px; text-align: center;'>{ing_info['icon']}</div>", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"**{ing.capitalize()}**")
                            st.caption(f"{ing_info['quantity']}")
                        with col3:
                            st.markdown(f"**${ing_info['price']:.2f}**")
                        with col4:
                            if st.checkbox("Select", key=f"recipe_ing_{idx}_{ing_idx}"):
                                selected_items.append(ing)
                                selected_total += ing_info['price']
                    
                    st.markdown("---")
                    
                    # Show selected total
                    if selected_total > 0:
                        st.markdown(f"### 💰 Selected Total: ${selected_total:.2f}")
                        st.caption(f"_Selected {len(selected_items)} ingredients_")
                    else:
                        st.info("💡 Select ingredients to see total price")
                    
                    # Add to cart button
                    if st.button(f"➕ Add Selected to Cart", key=f"add_recipe_{idx}", type="primary", use_container_width=True):
                        if selected_items:
                            success_count = 0
                            for ing in selected_items:
                                success, msg = add_to_cart_with_message(ing, 1)
                                if success:
                                    success_count += 1
                            
                            if success_count > 0:
                                st.success(f"✅ {success_count} ingredients added to cart!")
                                update_achievements()
                                # Clear selections
                                st.session_state.recipe_results = []
                                st.session_state.recipe_query_name = ""
                                st.session_state.current_page = 'cart'
                                st.rerun()
                        else:
                            st.warning("⚠️ Please select at least one ingredient!")


    #==================Equipment Expert==========================================
    
    elif agent_choice == "🔧 Equipment Expert":
        st.session_state.redirect_to_shopping = False
        st.markdown("### 🍳 Equipment Expert Agent")
        equipment_query = st.text_input("What are you cooking?", placeholder="e.g., biryani, cake")
        
        if 'equipment_list' not in st.session_state:
            st.session_state.equipment_list = []
        if 'equipment_query_name' not in st.session_state:
            st.session_state.equipment_query_name = ""
        if 'equipment_quantities' not in st.session_state:
            st.session_state.equipment_quantities = {}
        
        if st.button("🔍 Find Equipment", type="primary"):
            if equipment_query:
                st.session_state.equipment_list = get_equipment_for_recipe(equipment_query)
                st.session_state.equipment_query_name = equipment_query
                # Initialize quantities
                st.session_state.equipment_quantities = {item: 1 for item in st.session_state.equipment_list}
        
        if st.session_state.equipment_list:
            st.markdown(f"### 🍽️ Equipment Needed for '{st.session_state.equipment_query_name.title()}':")
            st.markdown("---")
            
            selected_items = []
            selected_total = 0
            
            for idx, item in enumerate(st.session_state.equipment_list):
                # ✅ USE get_item_info() function instead of direct dictionary access
                item_info = get_item_info(item)
                
                # Check if item is available
                if not item_info['available']:
                    st.warning(item_info['message'])
                    continue  # Skip unavailable items
                
                price = item_info['price']
                icon = item_info['icon']
                
                col1, col2, col3, col4, col5 = st.columns([1, 4, 2, 2, 1])
                with col1:
                    st.markdown(f"<div style='font-size: 35px; text-align: center;'>{icon}</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**{item}**")
                with col3:
                    st.markdown(f"**${price:.2f}** each")
                with col4:
                    qty = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=100,
                        value=st.session_state.equipment_quantities.get(item, 1),
                        key=f"equip_qty_{idx}",
                        label_visibility="collapsed"
                    )
                    st.session_state.equipment_quantities[item] = qty
                with col5:
                    if st.checkbox("Select", key=f"equip_{idx}"):
                        selected_items.append((item, qty))
                        selected_total += price * qty
            
            st.markdown("---")
            
            if selected_total > 0:
                st.markdown(f"### 💰 Selected Total: ${selected_total:.2f}")
                st.caption(f"_Selected {len(selected_items)} items_")
            else:
                st.info("💡 Select equipment to see total price")
            
            if st.button("🛒 Buy Selected Equipment", type="primary", use_container_width=True):
                if selected_items:
                    added_count = 0
                    for item, qty in selected_items:
                        success = add_to_cart(item, qty)
                        if success:
                            added_count += 1
                    
                    if added_count > 0:
                        st.success(f"✅ {added_count} equipment items added to cart!")
                        update_achievements()
                        st.session_state.equipment_list = []
                        st.session_state.equipment_query_name = ""
                        st.session_state.equipment_quantities = {}
                        st.session_state.current_page = 'cart'
                        st.rerun()
                else:
                    st.warning("⚠️ Please select at least one equipment item!")





    #==================Nutriotionsit Agent=============================================
    elif agent_choice == "🥗 Nutritionist":
        st.markdown("### 🥗 Nutritionist Agent")
        nutrition_items = st.text_area("Enter ingredients (comma-separated):", key="nutrition_items", placeholder="chicken, rice, tomato")
        
        if st.button("💊 Analyze Nutrition"):
            if nutrition_items:
                items = [i.strip() for i in nutrition_items.split(',')]
                total_nutrition, nutrition_details = calculate_nutrition(items)
                
                st.markdown("### 💊 Nutritional Analysis:")
                
                # Show nutrition for each ingredient separately
                for ingredient, nutrition in nutrition_details:
                     with st.expander(f"📋 {ingredient.capitalize()} - Nutritional Breakdown"):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("🔥 Calories", f"{nutrition.get('calories', 0)} kcal")
                            st.metric("🥩 Protein", f"{nutrition.get('protein', 0)}g")
                            st.metric("🍞 Carbs", f"{nutrition.get('carbs', 0)}g")
                        
                        with col2:
                            st.metric("🧈 Fat", f"{nutrition.get('fat', 0)}g")
                            st.metric("🌾 Fiber", f"{nutrition.get('fiber', 0)}g")
                            st.metric("🧂 Sodium", f"{nutrition.get('sodium', 0)}mg")
                        
                        with col3:
                            st.metric("🦴 Calcium", f"{nutrition.get('calcium', 0)}mg")
                            st.metric("⚙️ Iron", f"{nutrition.get('iron', 0)}mg")
                            st.metric("🥕 Vitamin A", f"{nutrition.get('vitamin_a', 0)} IU")
                        
                        with col4:
                            st.metric("🍊 Vitamin C", f"{nutrition.get('vitamin_c', 0)} mg")



               
    #================Meal Planner agent==================================================
    elif agent_choice == "📅 Meal Planner":
        st.markdown("### 📅 Meal Planner Agent")
        
        col1, col2 = st.columns(2)
        with col1:
            num_days = st.slider("Number of days:", 1, 7, 5)
        with col2:
            dietary = st.selectbox("Dietary preferences:", 
                                   ["Vegetarian", "Vegan", "Gluten-Free", "Low-Carb", "High-Protein"])
        
        if st.button("📅 Generate Plan"):
            st.markdown("### 📅 Your Meal Plan:")



            
            # Complete meal plans for all 7 days with all dietary options
            meal_plans = {
    "Monday": {
        "cuisine": "🇮🇹 Italian Cuisine",
        "Vegetarian": {
            "breakfast": "Ricotta Toast with Honey & Berries 🍞🍯",
            "lunch": "Caprese Salad with Pesto Dressing 🥗",
            "snack": "Tomato Bruschetta 🍅",
            "dinner": "Mushroom Risotto 🍄"
        },
        "Vegan": {
            "breakfast": "Soy Latte with Almond Biscotti ☕🌰",
            "lunch": "Vegan Spaghetti Pomodoro 🍝",
            "snack": "Olive Tapenade with Whole-Grain Crackers 🫒🍘",
            "dinner": "Eggplant Parmigiana (no cheese) 🍆"
        },
        "Gluten-Free": {
            "breakfast": "Yogurt with Gluten-Free Granola 🍨",
            "lunch": "GF Penne Arrabbiata 🍅",
            "snack": "Roasted Chickpeas with Herbs 🌿",
            "dinner": "Polenta with Mushroom Sauce 🍄"
        },
        "Low-Carb": {
            "breakfast": "Scrambled Eggs with Spinach 🍳🥬",
            "lunch": "Zucchini Noodles with Marinara 🍝",
            "snack": "Caprese Skewers 🍅🧀",
            "dinner": "Grilled Eggplant with Tomato-Basil Topping 🍆🌿"
        },
        "High-Protein": {
            "breakfast": "Greek Yogurt with Nuts 🥣🥜",
            "lunch": "Lentil & Bean Salad 🥗",
            "snack": "Protein Smoothie (almond milk, banana) 🥤🍌",
            "dinner": "Tofu or Paneer Steak in Tomato Sauce 🍅🥩"
        }
    },
    "Tuesday": {
        "cuisine": "🇲🇽 Mexican Cuisine",
        "Vegetarian": {
            "breakfast": "Breakfast Burrito with Eggs & Veggies 🌯🥚",
            "lunch": "Veggie Quesadilla 🧀🌶️",
            "snack": "Nachos with Salsa 🧀🍅",
            "dinner": "Bean Enchiladas 🌮"
        },
        "Vegan": {
            "breakfast": "Chia Pudding with Coconut Milk 🥥",
            "lunch": "Vegan Burrito Bowl (beans, rice, avocado) 🥗🥑",
            "snack": "Guacamole with Veggie Sticks 🥑🥕",
            "dinner": "Vegan Tacos with Jackfruit Filling 🌮"
        },
        "Gluten-Free": {
            "breakfast": "Corn Tortilla Scramble 🌽",
            "lunch": "Veg Burrito Bowl (no wheat) 🥗",
            "snack": "GF Nachos with Guac 🧀🥑",
            "dinner": "Corn Tacos with Veggies & Salsa 🌮🍅"
        },
        "Low-Carb": {
            "breakfast": "Egg Scramble with Salsa 🍳🍅",
            "lunch": "Lettuce Wrap Tacos 🥬🌮",
            "snack": "Spiced Nuts 🌰",
            "dinner": "Grilled Veggie Fajitas (no tortilla) 🌶️🥦"
        },
        "High-Protein": {
            "breakfast": "Egg & Bean Burrito 🌯🥚",
            "lunch": "Quinoa and Black Bean Salad 🥗",
            "snack": "Greek Yogurt with Lime Zest 🍋",
            "dinner": "Grilled Tempeh Tacos 🌮"
        }
    },
    "Wednesday": {
        "cuisine": "🌏 Asian Cuisine",
        "Vegetarian": {
            "breakfast": "Vegetable Fried Rice 🍚🥕",
            "lunch": "Veg Hakka Noodles 🍜",
            "snack": "Veg Spring Rolls 🥟",
            "dinner": "Thai Green Curry with Rice 🍛"
        },
        "Vegan": {
            "breakfast": "Tofu Scramble with Rice 🍳🍚",
            "lunch": "Vegan Sushi Rolls 🍣",
            "snack": "Edamame 🫛",
            "dinner": "Thai Coconut Curry with Tofu 🥥🍛"
        },
        "Gluten-Free": {
            "breakfast": "Rice Congee 🍚",
            "lunch": "GF Soy Sauce Stir-Fry 🥦",
            "snack": "Rice Crackers 🍘",
            "dinner": "Stir-Fried Veggies with Jasmine Rice 🥬🍚"
        },
        "Low-Carb": {
            "breakfast": "Boiled Eggs with Veggies 🥚🥦",
            "lunch": "Cauliflower Fried Rice 🥦🍳",
            "snack": "Seaweed Chips 🍘",
            "dinner": "Steamed Tofu & Broccoli Bowl 🥦🍲"
        },
        "High-Protein": {
            "breakfast": "Protein Smoothie with Soy Milk 🥤",
            "lunch": "Teriyaki Tofu Bowl 🍱",
            "snack": "Edamame 🫛",
            "dinner": "Seared Paneer/Tofu Stir-Fry 🍲"
        }
    },
    "Thursday": {
        "cuisine": "🇺🇸 American Cuisine",
        "Vegetarian": {
            "breakfast": "Pancakes with Maple Syrup 🥞🍁",
            "lunch": "Mac & Cheese 🧀",
            "snack": "Granola Bar 🍫",
            "dinner": "Veggie Burger 🍔"
        },
        "Vegan": {
            "breakfast": "Oatmeal with Berries 🍓",
            "lunch": "Vegan Wrap with Avocado & Veggies 🌯🥑",
            "snack": "Peanut Butter & Banana Smoothie 🥤🍌",
            "dinner": "Beyond Burger with Salad 🍔🥗"
        },
        "Gluten-Free": {
            "breakfast": "Smoothie Bowl with GF Oats 🍓🥣",
            "lunch": "Grilled Salad (no croutons) 🥗",
            "snack": "Trail Mix 🌰",
            "dinner": "Baked Sweet Potato with Beans 🥔🫘"
        },
        "Low-Carb": {
            "breakfast": "Scrambled Eggs with Cheese 🍳🧀",
            "lunch": "Cobb Salad 🥗🥓",
            "snack": "Almonds 🌰",
            "dinner": "Grilled Veggies with Protein 🥦🍗"
        },
        "High-Protein": {
            "breakfast": "Greek Yogurt Parfait 🍓🥣",
            "lunch": "Quinoa & Lentil Bowl 🥗",
            "snack": "Protein Shake 🥤",
            "dinner": "Grilled Tofu/Paneer with Quinoa 🍱"
        }
    },
    "Friday": {
        "cuisine": "🇮🇳 Indian Cuisine",
        "Vegetarian": {
            "breakfast": "Masala Dosa 🥞🌶️",
            "lunch": "Paneer Butter Masala with Naan 🍛🥘",
            "snack": "Samosa 🥟",
            "dinner": "Dal Tadka with Rice 🍚"
        },
        "Vegan": {
            "breakfast": "Poha with Lemon 🍋",
            "lunch": "Chana Masala with Rice 🍛🫘",
            "snack": "Roasted Chana 🌰",
            "dinner": "Vegetable Curry with Roti 🌶️"
        },
        "Gluten-Free": {
            "breakfast": "Idli with Coconut Chutney 🥥",
            "lunch": "Vegetable Pulao 🍚",
            "snack": "Roasted Peanuts 🌰",
            "dinner": "Dal and Rice Combo 🍛"
        },
        "Low-Carb": {
            "breakfast": "Besan Chilla 🥞",
            "lunch": "Saag Paneer (no naan) 🧀🥬",
            "snack": "Cucumber Slices with Chaat Masala 🥒",
            "dinner": "Mixed Veg Curry 🌶️"
        },
        "High-Protein": {
            "breakfast": "Moong Dal Chilla 🥞",
            "lunch": "Rajma with Brown Rice 🍚🫘",
            "snack": "Greek Yogurt with Fruits 🍓🥣",
            "dinner": "Tofu Curry with Quinoa 🍛"
        }
    },
    "Saturday": {
        "cuisine": "🇫🇷 French Cuisine",
        "Vegetarian": {
            "breakfast": "Crepes with Berries 🥞🍓",
            "lunch": "Quiche with Salad 🥧🥗",
            "snack": "Madeleines 🍪",
            "dinner": "Ratatouille with Rice 🍆🍚"
        },
        "Vegan": {
            "breakfast": "Vegan Crepes with Maple Syrup 🥞🍁",
            "lunch": "Ratatouille Bowl 🍆🥣",
            "snack": "Baguette with Olive Tapenade 🫒🥖",
            "dinner": "Grilled Veggies with Couscous 🥦🍚"
        },
        "Gluten-Free": {
            "breakfast": "GF Crepes 🥞",
            "lunch": "Nicoise Salad 🥗🐟",
            "snack": "Fruit & Nut Mix 🍎🌰",
            "dinner": "Mushroom Risotto 🍄"
        },
        "Low-Carb": {
            "breakfast": "Eggs with Avocado 🍳🥑",
            "lunch": "Cauliflower Quiche 🥧🥦",
            "snack": "Olives & Cheese 🧀🫒",
            "dinner": "Baked Zucchini Gratin 🥒"
        },
        "High-Protein": {
            "breakfast": "Greek Yogurt with Almonds 🥣🌰",
            "lunch": "Lentil Salad 🥗",
            "snack": "Protein Bar 🍫",
            "dinner": "Grilled Tofu or Tempeh Steak 🍱"
        }
    },
    "Sunday": {
        "cuisine": "🌊 Mediterranean Cuisine",
        "Vegetarian": {
            "breakfast": "Greek Yogurt with Honey & Nuts 🍯🥣",
            "lunch": "Falafel Wrap 🌯",
            "snack": "Hummus with Veggies 🥕",
            "dinner": "Grilled Halloumi with Rice 🍚🧀"
        },
        "Vegan": {
            "breakfast": "Oat Bowl with Fruits 🍓🥣",
            "lunch": "Falafel Bowl with Tzatziki 🥗",
            "snack": "Hummus & Pita 🥙",
            "dinner": "Stuffed Bell Peppers with Couscous 🌶️"
        },
        "Gluten-Free": {
            "breakfast": "Chia Yogurt Parfait 🍓",
            "lunch": "Lentil Salad with Feta 🧀🥗",
            "snack": "Roasted Chickpeas 🫛",
            "dinner": "Quinoa Tabbouleh 🥣"
        },
        "Low-Carb": {
            "breakfast": "Boiled Eggs with Spinach 🥚🥬",
            "lunch": "Grilled Veg Salad 🥗",
            "snack": "Nuts & Olives 🌰🫒",
            "dinner": "Baked Eggplant with Tomato Sauce 🍆🍅"
        },
        "High-Protein": {
            "breakfast": "Protein Smoothie 🥤",
            "lunch": "Chickpea & Feta Salad 🧀🥗",
            "snack": "Greek Yogurt 🍨",
            "dinner": "Grilled Paneer/Tofu with Quinoa 🍛"
        }
    }
}

            
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            
            for i in range(num_days):
                day_name = days[i]
                day_plan = meal_plans[day_name]
                
                with st.expander(f"{day_plan['cuisine']} {day_name} – {dietary}"):
                    st.markdown(f"### 🥦 {dietary}")
                    meals = day_plan[dietary]
                    st.markdown(f"* 🌅 **Breakfast:** {meals['breakfast']}")
                    st.markdown(f"* 🌞 **Lunch:** {meals['lunch']}")
                    st.markdown(f"* 🍪 **Snack:** {meals['snack']}")
                    st.markdown(f"* 🌙 **Dinner:** {meals['dinner']}")


           
    #========================Shopping assistant agent======================================= 
    elif agent_choice == "🛒 Shopping Assistant":
        st.markdown("### 🛒 Shopping Assistant Agent")
        
        if st.session_state.redirect_to_shopping and len(st.session_state.shopping_cart) > 0:
            st.success("✅ Recipe ingredients loaded into cart!")
            st.session_state.redirect_to_shopping = False
        
        st.markdown(f"**🛒 Cart: {st.session_state.cart_items_count} items**")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            shop_items = st.text_area("Enter ingredients or equipment:", placeholder="pasta, tomatoes, cheese, knife, pot")
        with col2:
            if st.button("Clear Cart"):
                st.session_state.shopping_cart = []
                st.session_state.cart_items_count = 0
                st.success("Cart cleared!")
                st.rerun()
        
        qty = st.number_input("Quantity per item:", min_value=1, value=1, max_value=500000, key="shop_qty")

        
        
        # Initialize session state for shopping list
        if 'shopping_list_items' not in st.session_state:
            st.session_state.shopping_list_items = []
        if 'shopping_list_data' not in st.session_state:
            st.session_state.shopping_list_data = []
        if 'shopping_list_total' not in st.session_state:
            st.session_state.shopping_list_total = 0
        if 'shopping_list_qty' not in st.session_state:
            st.session_state.shopping_list_qty = 1






        #===============Generate Shopping List Function(button)========================================
        if st.button("🛒 Generate Shopping List", type="primary"):
            if shop_items:
                items = [i.strip() for i in shop_items.split(',')]
                quantities = [qty] * len(items)
                item_prices, total = calculate_price(items, quantities)
                
                # Store in session state
                st.session_state.shopping_list_items = items
                st.session_state.shopping_list_data = item_prices
                st.session_state.shopping_list_total = total
                st.session_state.shopping_list_qty = qty



        
        
        # =======================Display shopping list (OUTSIDE the button block)=========================
        if st.session_state.shopping_list_data:
            st.markdown("### 🛒 Your Shopping List:")
            st.markdown("---")
            
            selected_items = []
            selected_total = 0  # Track selected items total
            
            for idx, (item, price, quantity, icon, qty_val) in enumerate(st.session_state.shopping_list_data):
                col1, col2, col3, col4 = st.columns([1, 5, 2, 1])
                with col1:
                    st.markdown(f"<div style='font-size: 40px; text-align: center;'>{icon}</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div style='font-size: 18px; font-weight: bold;'>{item.capitalize()}</div><div style='font-size: 14px; color: gray;'>{quantity} x{qty_val}</div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div style='font-size: 20px; font-weight: bold; color: green;'>${price:.2f}</div>", unsafe_allow_html=True)
                with col4:
                    # Add checkbox for selection
                    if st.checkbox("Select", key=f"shop_item_{idx}"):
                        selected_items.append((item, st.session_state.shopping_list_qty))
                        selected_total += price  # Add to selected total
            
            st.markdown("---")




            
            # ==========================Display dynamic total based on selected items==============================================
            if selected_total > 0:
                st.markdown(f"### 💰 Selected Total: ${selected_total:.2f}")
                st.caption(f"_Original Total: ${st.session_state.shopping_list_total:.2f}_")
                
                if selected_total > 50:
                    st.warning("💡 Tip: Consider buying in bulk to save money!")
                else:
                    st.success("✅ Budget-friendly shopping list!")
            else:
                st.markdown(f"### 💰 Total: ${st.session_state.shopping_list_total:.2f}")
                st.info("💡 Select items to see updated total")




            
            
            # ====================================Buy Selected Items button=========================================================
            if st.button("🛍️ Buy Selected Items", type="primary", use_container_width=True):
                if selected_items:
                    success_count = 0
                    for item, quantity in selected_items:
                        success = add_to_cart(item, quantity)
                        if success:
                            success_count += 1
                    
                    if success_count > 0:
                        st.success(f"✅ {success_count} items added to cart! Happy shopping!")
                        update_achievements()
                        # Clear the shopping list
                        st.session_state.shopping_list_items = []
                        st.session_state.shopping_list_data = []
                        st.session_state.shopping_list_total = 0
                        # Redirect to shopping cart
                        st.session_state.current_page = 'cart'
                        st.rerun()
                    else:
                        st.error("❌ Failed to add items to cart. Please try again.")
                else:
                    st.warning("⚠️ Please select at least one item to purchase!")  






#========================Analaytics =======================================================
elif page == "📊 Analytics":
    st.markdown(
    """
    <h1 style="
        font-family: 'Times new roman', 'Noto Color Emoji', 'Apple Color Emoji';
        text-align: center;
        font-size: 4em;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 10px;
    ">
        📊 <span style="color: #007BFF;">Analytics Dashboard</span>
    </h1>
    """,
    unsafe_allow_html=True
)

    
    st.markdown("### 🧑‍🍳 Your Cooking Journey")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("💬\nTotal Chats\n" + str(st.session_state.total_messages)):
            st.session_state.show_all_chats = True
    with col2:
        st.metric("📖 Recipes DB", "231K+")
    with col3:
        st.metric("🤖 AI Agents", "5")
    with col4:
        if st.button("⭐\nFavorites\n" + str(len(st.session_state.favorites))):
            st.session_state.show_favorites = True
    
    st.markdown("---")




    
    #============= Show all chats if clicked==================================
    if 'show_all_chats' in st.session_state and st.session_state.show_all_chats:
        st.markdown("### 📜 All Conversations")
        if st.button("← Back to Overview"):
            st.session_state.show_all_chats = False
            st.rerun()
        
        if st.session_state.chat_history:
            for idx, chat in enumerate(st.session_state.chat_history):
                with st.expander(f"💬 Chat {idx + 1} - {chat['user'][:50]}..."):
                    st.markdown(f"**You:** {chat['user']}")
                    st.markdown(f"**Assistant:** {chat['assistant']}")
                    
                    col1, col2 = st.columns([5, 1])
                    with col2:
                        if st.button("⭐", key=f"fav_analytics_{idx}"):
                            if chat not in st.session_state.favorites:
                                st.session_state.favorites.append(chat)
                                update_achievements()
                                st.success("Added to favorites!")
                                st.rerun()
        else:
            st.info("No conversations yet. Start chatting!")



    
    
    # =========================Show favorites if clicked===================================
    elif 'show_favorites' in st.session_state and st.session_state.show_favorites:
        st.markdown("### ⭐ Your Favorite Conversations")
        if st.button("← Back to Overview"):
            st.session_state.show_favorites = False
            st.rerun()
        
        if st.session_state.favorites:
            for idx, fav in enumerate(st.session_state.favorites):
                with st.expander(f"⭐ Favorite {idx + 1} - {fav['user'][:50]}..."):
                    st.markdown(f"**Question:** {fav['user']}")
                    st.markdown(f"**Answer:** {fav['assistant']}")
                    
                    if st.button("🗑️ Remove", key=f"remove_fav_{idx}"):
                        st.session_state.favorites.pop(idx)
                        update_achievements()
                        st.success("Removed from favorites!")
                        st.rerun()
        else:
            st.info("No favorites yet. Click the ⭐ button on chat messages to save them!")
    
    else:
        # ====================Recent conversations preview================================
        st.markdown("### 💬 Recent Conversations")
        if st.session_state.chat_history:
            for idx, chat in enumerate(st.session_state.chat_history[-5:]):
                with st.expander(f"💬 Chat {idx + 1} - {chat['user'][:50]}..."):
                    st.markdown(f"**You:** {chat['user']}")
                    st.markdown(f"**Assistant:** {chat['assistant']}")
        else:
            st.info("No conversations yet. Start chatting!")
        
        st.markdown("---")
        
        st.markdown("### 📈 Usage Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔥 Most Active")
            st.markdown(f"* Total Messages: {st.session_state.total_messages}")
            st.markdown(f"* Current Model: {selected_model}")
            st.markdown(f"* Cooking Level: {st.session_state.preferences['skill_level']}")
            st.markdown(f"* Favorites Saved: {len(st.session_state.favorites)}")
            st.markdown(f"* Cart Items: {st.session_state.cart_items_count}")
        
        with col2:
            st.markdown("#### 🎯 Unlocked Achievements")
            for achievement in st.session_state.achievements:
                st.markdown(f"✅ {achievement}")
            
            st.markdown("#### 🔒 Progress Tracking")
            locked = get_locked_achievements()
            for lock in locked[:5]:  # Show first 5 locked
                st.markdown(f"* {lock}")
    
    st.markdown("---")



# ==============Profile CSS ==============================
elif page == "👤 Profile":
    # Advanced CSS for Profile Page
    st.markdown("""
    <style>
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    .profile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        animation: fadeInUp 0.6s ease-out;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
    }
    
    .profile-avatar {
        font-size: 5rem;
        animation: float 3s ease-in-out infinite;
        display: inline-block;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.3));
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
        border-left: 5px solid #667eea;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        border-left-color: #764ba2;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .stat-card:hover::before {
        left: 100%;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 1rem 1.5rem;
        border-radius: 50px;
        display: inline-block;
        margin: 0.5rem;
        color: white;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
        animation: fadeInUp 1s ease-out;
        transition: all 0.3s ease;
    }
    
    .achievement-badge:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.5);
    }
    
    .locked-badge {
        background: linear-gradient(135deg, #ccc 0%, #999 100%);
        padding: 1rem 1.5rem;
        border-radius: 50px;
        display: inline-block;
        margin: 0.5rem;
        color: white;
        font-weight: bold;
        opacity: 0.6;
        animation: fadeInUp 1s ease-out;
    }
    
    .progress-ring {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        animation: fadeInUp 1.2s ease-out;
        margin: 1rem 0;
    }
    
    .level-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        animation: shimmer 3s infinite;
        background-size: 1000px 100%;
    }
    </style>
    """, unsafe_allow_html=True)


   
    # ==========Profile Header Card====================
    st.markdown(f"""
    <div class='profile-card'>
        <div class='profile-avatar'>👨‍🍳</div>
        <h1 style='margin: 1rem 0 0.5rem 0;'>{st.session_state.preferences['user_name']}</h1>
        <p style='opacity: 0.9; font-size: 1.1rem;'>Master Chef in Training</p>
        <div style='margin-top: 1rem;'>
            <span class='level-badge'>Level {min(st.session_state.total_messages // 10, 50)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Progress Tracker")



        
    # ==================Add CSS for colored stat cards========================
    st.markdown("""
    <style>
    .stat-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(17, 153, 142, 0.3);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(17, 153, 142, 0.5);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .stat-label {
        color: #ffffff;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)


   
    # ===============Statistics Cards=============================
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("🗣️", st.session_state.total_messages, "Total Chats"),
        ("⭐", len(st.session_state.favorites), "Favorites"),
        ("🏆", len(st.session_state.achievements), "Achievements"),
        ("🍳", "231K+", "Recipes")
    ]
    
    for col, (icon, value, label) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class='stat-card'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{icon}</div>
                <div class='stat-number'>{value}</div>
                <div class='stat-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🏆 Your Achievements")





    
    # =================Display achievements with badges============================
    achievements_html = "<div style='text-align: center; padding: 1rem;'>"
    for achievement in st.session_state.achievements:
        achievements_html += f"<div class='achievement-badge'>{achievement}</div>"
    achievements_html += "</div>"
    st.markdown(achievements_html, unsafe_allow_html=True)    
    
    st.markdown("---")
    
    st.markdown("### 🔒 Locked Achievements & Progress")
    
    locked = get_locked_achievements()
    
    if locked:
        for lock in locked:
            st.info(lock)
    else:
        st.balloons()
        st.success("🎉 Congratulations! You've unlocked ALL achievements!")
    
    st.markdown("---")
    
    st.markdown("### 🕒 Recent Activity")





    
    # ======================Calculate actual activity metrics==================================
    last_chat_time = "Just now" if st.session_state.total_messages > 0 else "No activity yet"
    member_since = datetime.now().strftime("%B %Y")

    activity_data = {
        "Metric": ["⏰ Last Active", "🗣️ Total Conversations", "⭐ Favorite Recipes", "🛒 Shopping Cart Items", "🤖 Current AI Model", "📅 Member Since"],
        "Value": [
            last_chat_time,
            str(st.session_state.total_messages),
            str(len(st.session_state.favorites)),
            str(st.session_state.cart_items_count),
            selected_model,
            member_since
        ]
    }



    # ==========================Add custom styling for the table==========================================
    st.markdown("""
    <style>
    /* Style the table container */
    div[data-testid="stTable"] {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Style table headers */
    div[data-testid="stTable"] table thead tr th {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #1e3c72 !important;
        font-weight: bold !important;
        padding: 1.2rem !important;
        text-align: left !important;
        font-size: 1.1rem !important;
        letter-spacing: 1px !important;
        border: none !important;
        text-transform: uppercase;
    }
    
    /* Style table rows */
    div[data-testid="stTable"] table tbody tr {
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.1) !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    div[data-testid="stTable"] table tbody tr:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(10px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Style table cells */
    div[data-testid="stTable"] table tbody tr td {
        padding: 1.2rem !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        border: none !important;
        font-weight: 500 !important;
    }
    
    /* First column (Metric) styling */
    div[data-testid="stTable"] table tbody tr td:first-child {
        font-weight: 700 !important;
        color: #FFD700 !important;
        font-size: 1.05rem !important;
    }
    
    /* Second column (Value) styling */
    div[data-testid="stTable"] table tbody tr td:last-child {
        font-weight: 600 !important;
        color: #ffffff !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Remove default table borders */
    div[data-testid="stTable"] table {
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    activity_df = pd.DataFrame(activity_data)
    st.table(activity_df)
    
    st.markdown("---")    

    


    # =================Achievement progress bars=============================
    st.markdown("### ⚜️ Achievement Progress")
    
    messages = st.session_state.total_messages
    favorites = len(st.session_state.favorites)
    cart = st.session_state.cart_items_count



    # ================Calculate progress percentages=========================
    message_progress = min(messages / 50, 1.0)
    favorite_progress = min(favorites / 10, 1.0)
    cart_progress = min(cart / 20, 1.0)



    
    # ===============Simple CSS for native Streamlit components===============
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }
    
    div[data-testid="stProgress"] > div > div {
        background: rgba(255, 255, 255, 0.2);
        height: 15px;
        border-radius: 10px;
    }
    
    div[data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%) !important;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(255, 215, 0, 0.6);
    }
    
    .stMarkdown h4 {
        color: white !important;
        text-align: center;
        font-size: 1.8rem !important;
    }
    
    .stMarkdown p {
        color: white !important;
        text-align: center;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)




    
    # =======Create 3 columns=====================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 💬")
        st.markdown(f"**Message Milestones**")
        st.progress(message_progress)
        st.markdown(f"**{int(message_progress * 100)}%**")
        st.markdown(f"{messages}/50 messages")
        st.caption("Master Chef achievement")
    
    with col2:
        st.markdown("#### ⭐")
        st.markdown(f"**Favorite Milestones**")
        st.progress(favorite_progress)
        st.markdown(f"**{int(favorite_progress * 100)}%**")
        st.markdown(f"{favorites}/10 favorites")
        st.caption("Favorite Master achievement")
    
    with col3:
        st.markdown("#### 🛒")
        st.markdown(f"**Shopping Milestones**")
        st.progress(cart_progress)
        st.markdown(f"**{int(cart_progress * 100)}%**")
        st.markdown(f"{cart}/20 cart items")
        st.caption("Shopping Expert achievement")

        

    # ================Profile settings============================
    st.markdown("### ⚙️ Profile Settings")



    
    # ==================Add stunning CSS with colored background==========
    st.markdown("""
    <style>
    /* Remove the blue bar by hiding empty container */
    div[data-testid="stVerticalBlock"] > div:empty {
        display: none;
    }
    
    /* Input field styling - YELLOW BACKGROUND WITH BLACK TEXT */
    div[data-testid="stTextInput"] > div > div > input {
        background: #FFD700 !important;
        border: 1px solid #FFA500;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        color: #000000 !important;
        font-weight: 600;
    }
    
    div[data-testid="stTextInput"] > div > div > input::placeholder {
        color: #666666 !important;
    }
    
    div[data-testid="stTextInput"] > div > div > input:focus {
        box-shadow: 0 0 0 3px rgba(255, 165, 0, 0.5);
        border-color: #FFA500;
    }
    
    /* Selectbox styling - YELLOW BACKGROUND WITH BLACK TEXT */
    div[data-testid="stSelectbox"] > div > div {
        background: #FFD700 !important;
        border: 1px solid #FFA500;
        border-radius: 10px;
        color: #000000 !important;
    }
    
    div[data-testid="stSelectbox"] select {
        color: #000000 !important;
        font-weight: 600;
    }
    
    /* MultiSelect styling - YELLOW BACKGROUND */
    div[data-testid="stMultiSelect"] > div > div {
        background: #FFD700 !important;
        border: 1px solid #FFA500;
        border-radius: 10px;
    }
    
    div[data-testid="stMultiSelect"] input {
        color: #000000 !important;
        font-weight: 600;
    }
    
    /* Labels styling */
    .stTextInput > label, .stSelectbox > label, .stMultiSelect > label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Save button styling */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #2c3e50;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 1.2rem;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1.5rem;
    }
    
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.6);
    }
    
    /* Section divider */
    .section-divider {
        border-top: 2px solid rgba(255, 255, 255, 0.3);
        margin: 1.5rem 0;
    }
    
    .section-title {
        color: #FFD700;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>👤 Personal Information</div>", unsafe_allow_html=True)




    
    # ==================Name input (ORIGINAL - NOT CHANGED)=========================================
    new_name = st.text_input("Name:", value=st.session_state.preferences['user_name'])



    
    # ==================Additional useful fields===================================================
    col1, col2 = st.columns(2)
    with col1:
        user_email = st.text_input("📧 Email:", placeholder="your@email.com")
    with col2:
        user_location = st.text_input("📍 Location:", placeholder="City, Country")
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>🍽️ Cooking Preferences</div>", unsafe_allow_html=True)




    
    # ===================Dietary preference (EXPANDED TO 10 OPTIONS)===================================
    new_dietary = st.selectbox("Dietary Preference:", [
        "None", 
        "Vegetarian", 
        "Vegan", 
        "Gluten-Free", 
        "Keto", 
        "Paleo", 
        "Dairy-Free", 
        "Nut-Free", 
        "Low-Carb", 
        "Halal"
    ])




    
    # =====================Cooking level (ORIGINAL - NOT CHANGED)=================================
    new_skill = st.selectbox("Cooking Level:", ["Beginner", "Intermediate", "Advanced", "Expert"])



    
    # =====================Additional preferences================================================
    col1, col2 = st.columns(2)
    with col1:
        cuisine_preference = st.multiselect(
            "🌍 Favorite Cuisines:",
            ["Italian", "Chinese", "Indian", "Mexican", "Japanese", "French", "Thai", "Mediterranean"]
        )
    with col2:
        cooking_time = st.selectbox(
            "⏱️ Preferred Cooking Time:",
            ["Quick (< 30 min)", "Medium (30-60 min)", "Long (> 60 min)", "Any"]
        )



    
    # ==================Save button (ORIGINAL - NOT CHANGED)=======================================
    if st.button("💾 Save Profile"):
        st.session_state.preferences['user_name'] = new_name
        st.session_state.preferences['dietary'] = new_dietary
        st.session_state.preferences['skill_level'] = new_skill
        st.success("✅ Profile updated!")
        st.rerun()





# ==================== NEW: RETURN & REPLACEMENT PAGE ====================(new added)
elif page == "🔄 Return & Replacement":
    st.markdown(
    """
    <h1 style="
        font-family: 'Times new roman', 'Noto Color Emoji', 'Apple Color Emoji';
        text-align: center;
        font-size: 4em;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 10px;
    ">
        🔄 Returns & Replacements
    </h1>
    """,
    unsafe_allow_html=True
)




    # ==================== CSS for Return & Replacement Page ====================(new added)
    st.markdown("""
    <style>
    .return-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4);
    }
    
    h1.main-header {
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Segoe UI Emoji', 'Noto Color Emoji', 'Apple Color Emoji', sans-serif !important;
    }

    h1.main-header::first-letter {
        font-family: 'Segoe UI Emoji', 'Noto Color Emoji', 'Apple Color Emoji', sans-serif !important;
    }

    .emoji {
        font-family: 'Segoe UI Emoji', 'Noto Color Emoji', 'Apple Color Emoji', sans-serif !important;
    }

    

    
    .eligible-order {
        background: linear-gradient(135deg, #ffffff 0%, #e8f5e9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #4caf50;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .eligible-order:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 20px rgba(76, 175, 80, 0.3);
    }
    
    .ineligible-order {
        background: linear-gradient(135deg, #ffffff 0%, #ffebee 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #f44336;
        margin: 1rem 0;
        opacity: 0.6;
    }
    
    .return-reason-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .return-reason-card:hover {
        border-color: #f093fb;
        background: #fff3f9;
        transform: scale(1.02);
    }
    
    .status-pending {
        background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .status-approved {
        background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .status-rejected {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .status-completed {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ==================== Tab Selection ====================
    tab1, tab2, tab3 = st.tabs(["📦 Request Return/Replace", "📋 My Requests", "ℹ️ Policy"])
    
    # ==================== TAB 1: REQUEST RETURN/REPLACEMENT ====================
    with tab1:
        st.markdown("### 📦 Select Order for Return/Replacement")
        
        # Filter delivered orders only (eligible for return/replacement)
        eligible_orders = [
        order for order in st.session_state.orders 
        if order['status'] == 'Delivered' 
        or (order['status'] == 'Cancelled' and order.get('was_delivered', False))
    ]
        
        if not eligible_orders:
            st.info("📦 No delivered orders available for return or replacement.")
            st.info("💡 Only delivered orders can be returned or replaced within 7 days of delivery.")
        else:
            st.success(f"✅ You have {len(eligible_orders)} order(s) eligible for return/replacement")
            
            for order in eligible_orders:
                with st.expander(f"🛍️ Order #{order['order_id']} - ${order['total']:.2f} - Delivered on {order['date']}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("### 📋 Order Details")
                        st.markdown(f"**Order ID:** {order['order_id']}")
                        st.markdown(f"**Order Date:** {order['date']}")
                        st.markdown(f"**Total Amount:** ${order['total']:.2f}")
                        st.markdown(f"**Status:** {order['status']}")
                        
                        st.markdown("---")
                        
                        st.markdown("### 🛒 Items in this Order")
                        for item in order['items']:
                            item_info = get_item_info(item['ingredient'])
                            st.markdown(f"* {item_info['icon']} **{item['ingredient'].capitalize()}** - Qty: {item['quantity']}")
                    
                    with col2:
                        st.markdown("### 🔄 Action")
                        
                        # Check eligibility (within 7 days)
                        order_date = datetime.strptime(order['date'], "%Y-%m-%d %H:%M:%S")
                        days_since_delivery = (datetime.now() - order_date).days
                        
                        if days_since_delivery <= 7:
                            st.success(f"✅ Eligible for return/replacement")
                            st.caption(f"({7 - days_since_delivery} days remaining)")
                            
                            col_return, col_replace = st.columns(2)
                            
                            with col_return:
                                if st.button("🔙 Return", key=f"return_{order['order_id']}", use_container_width=True):
                                    st.session_state[f"show_return_form_{order['order_id']}"] = True
                                    st.session_state[f"return_type_{order['order_id']}"] = "Return"
                            
                            with col_replace:
                                if st.button("🔄 Replace", key=f"replace_{order['order_id']}", use_container_width=True):
                                    st.session_state[f"show_return_form_{order['order_id']}"] = True
                                    st.session_state[f"return_type_{order['order_id']}"] = "Replacement"
                        else:
                            st.error(f"❌ Return period expired")
                            st.caption(f"(Delivered {days_since_delivery} days ago)")
                            st.caption("Returns accepted within 7 days only")
                    
                    # ==================== RETURN/REPLACEMENT FORM ====================
                    if st.session_state.get(f"show_return_form_{order['order_id']}", False):
                        action_type = st.session_state.get(f"return_type_{order['order_id']}", "Return")
                        
                        st.markdown("---")
                        st.markdown(f"### 📝 {action_type} Request Form")
                        
                        with st.form(f"return_form_{order['order_id']}"):
                            # Reason selection
                            if action_type == "Return":
                                reasons = [
                                    "🔴 Defective/Damaged Product",
                                    "📦 Wrong Item Received",
                                    "💔 Not as Described",
                                    "🚚 Missing Items",
                                    "😞 Quality Issues",
                                    "🤔 Changed Mind",
                                    "📏 Size/Fit Issues",
                                    "🎨 Color/Appearance Mismatch",
                                    "⏰ Received Too Late",
                                    "❓ Other"
                                ]
                            else:
                                reasons = [
                                    "🔴 Defective/Damaged Product",
                                    "📦 Wrong Item Received",
                                    "💔 Not as Described",
                                    "🚚 Missing Parts/Components",
                                    "😞 Quality Issues",
                                    "❓ Other"
                                ]
                            
                            selected_reason = st.selectbox(f"Reason for {action_type}:", reasons)
                            
                            # Additional details
                            details = st.text_area(
                                "Please provide additional details:",
                                placeholder="Describe the issue in detail...",
                                height=100
                            )
                            
                            # Photo upload option
                            st.markdown("📸 **Upload Photos (Optional but recommended)**")
                            uploaded_photos = st.file_uploader(
                                "Upload product photos showing the issue:",
                                type=['jpg', 'jpeg', 'png'],
                                accept_multiple_files=True,
                                key=f"photos_{order['order_id']}"
                            )
                            
                            # Item selection for return/replacement
                            st.markdown("---")
                            st.markdown("### 🛒 Select Items to Return/Replace")
                            
                            selected_items = []
                            for idx, item in enumerate(order['items']):
                                item_info = get_item_info(item['ingredient'])
                                if st.checkbox(
                                    f"{item_info['icon']} {item['ingredient'].capitalize()} (Qty: {item['quantity']})",
                                    key=f"item_{order['order_id']}_{idx}"
                                ):
                                    selected_items.append(item)
                            
                            # Bank details for refund (only for returns)
                            if action_type == "Return":
                                st.markdown("---")
                                st.markdown("### 💰 Refund Details")
                                refund_method = st.radio(
                                    "Preferred Refund Method:",
                                    ["👛 Wallet (Instant)", "🎁 Gift Card (Instant)", "🏦 Bank Account (3-5 days)", "💳 Original Payment Method"]
                                )
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                submit = st.form_submit_button(f"✅ Submit {action_type} Request", type="primary", use_container_width=True)
                            
                            with col2:
                                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                            
                            if submit:
                                if selected_items and details:
                                    # Create return/replacement request
                                    request_id = f"{'RET' if action_type == 'Return' else 'REP'}-{st.session_state.return_counter if action_type == 'Return' else st.session_state.replacement_counter}"
                                    
                                    request = {
                                        'request_id': request_id,
                                        'order_id': order['order_id'],
                                        'action_type': action_type,
                                        'reason': selected_reason,
                                        'details': details,
                                        'items': selected_items,
                                        'photos': len(uploaded_photos) if uploaded_photos else 0,
                                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        'status': 'Pending Approval',
                                        'refund_method': refund_method if action_type == 'Return' else None,
                                        'timeline': [
                                            {'step': f'{action_type} Requested', 'completed': True, 'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                                            {'step': 'Under Review', 'completed': False, 'time': None},
                                            {'step': 'Pickup Scheduled', 'completed': False, 'time': None},
                                            {'step': 'Quality Check', 'completed': False, 'time': None},
                                            {'step': 'Approved' if action_type == 'Return' else 'Replacement Shipped', 'completed': False, 'time': None}
                                        ]
                                    }
                                    
                                    # Add to appropriate list
                                    if action_type == "Return":
                                        st.session_state.return_requests.append(request)
                                        st.session_state.return_counter += 1
                                    else:
                                        st.session_state.replacement_requests.append(request)
                                        st.session_state.replacement_counter += 1
                                    
                                    st.balloons()
                                    st.success(f"✅ {action_type} request #{request_id} submitted successfully!")
                                    st.info(f"📧 Confirmation email sent to {order['customer']['email']}")
                                    st.info(f"📞 Support will contact you within 24 hours")
                                    
                                    # Clear form state
                                    st.session_state[f"show_return_form_{order['order_id']}"] = False
                                    st.rerun()
                                else:
                                    st.error("❌ Please select items and provide details!")
                            
                            if cancel:
                                st.session_state[f"show_return_form_{order['order_id']}"] = False
                                st.rerun()
    
    # ==================== TAB 2: MY REQUESTS ====================
    with tab2:
        st.markdown("### 📋 Your Return & Replacement Requests")
        
        all_requests = st.session_state.return_requests + st.session_state.replacement_requests
        
        if not all_requests:
            st.info("📋 No return or replacement requests yet.")
        else:
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                filter_type = st.selectbox("Filter by Type:", ["All", "Returns", "Replacements"])
            with col2:
                filter_status = st.selectbox("Filter by Status:", ["All", "Pending Approval", "Approved", "Rejected", "Completed"])
            
            # Filter requests
            filtered_requests = all_requests
            if filter_type != "All":
                filtered_requests = [r for r in filtered_requests if r['action_type'] == filter_type[:-1]]  # Remove 's'
            if filter_status != "All":
                filtered_requests = [r for r in filtered_requests if r['status'] == filter_status]
            
            st.markdown(f"**Showing {len(filtered_requests)} request(s)**")
            
            # Display requests
            for request in filtered_requests:
                with st.expander(f"{'🔙' if request['action_type'] == 'Return' else '🔄'} {request['action_type']} Request #{request['request_id']} - {request['status']}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("### 📋 Request Details")
                        st.markdown(f"**Request ID:** {request['request_id']}")
                        st.markdown(f"**Order ID:** {request['order_id']}")
                        st.markdown(f"**Type:** {request['action_type']}")
                        st.markdown(f"**Reason:** {request['reason']}")
                        st.markdown(f"**Details:** {request['details']}")
                        st.markdown(f"**Request Date:** {request['date']}")
                        
                        # Status badge
                        status_class = f"status-{request['status'].lower().replace(' ', '-')}"
                        if request['status'] == 'Pending Approval':
                            status_class = "status-pending"
                        elif request['status'] == 'Approved':
                            status_class = "status-approved"
                        elif request['status'] == 'Rejected':
                            status_class = "status-rejected"
                        elif request['status'] == 'Completed':
                            status_class = "status-completed"
                        
                        st.markdown(f"**Status:** <span class='{status_class}'>{request['status']}</span>", unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        st.markdown("### 🛒 Items")
                        for item in request['items']:
                            item_info = get_item_info(item['ingredient'])
                            st.markdown(f"* {item_info['icon']} **{item['ingredient'].capitalize()}** - Qty: {item['quantity']}")
                    
                    with col2:
                        st.markdown("### 📍 Tracking")
                        
                        for step in request['timeline']:
                            status_icon = "✅" if step['completed'] else "⏳"
                            st.markdown(f"{status_icon} **{step['step']}**")
                            if step['time']:
                                st.caption(step['time'])



    # ==================== TAB 3: POLICY ====================(new added)
    with tab3:
        st.markdown("### ℹ️ Return & Replacement Policy")
        
        st.markdown("""
        #### 📦 Return Policy
        
        **Eligibility:**
        * Returns accepted within **7 days** of delivery
        * Product must be unused and in original packaging
        * All accessories and tags must be included
        
        **Return Process:**
        1. Submit return request through this page
        2. Our team reviews your request (24-48 hours)
        3. Once approved, schedule pickup or ship item back
        4. Quality check (2-3 business days)
        5. Refund processed to your chosen method
        
        **Refund Timeline:**
        * Wallet/Gift Card: Instant
        * Bank Account: 3-5 business days
        * Original Payment Method: 5-7 business days
        
        ---
        
        #### 🔄 Replacement Policy
        
        **Eligibility:**
        * Replacement available within **7 days** of delivery
        * Only for defective, damaged, or wrong items
        
        **Replacement Process:**
        1. Submit replacement request with photos
        2. Our team reviews your request (24-48 hours)
        3. Once approved, new item ships immediately
        4. Original item picked up after delivery
        
        **Replacement Timeline:**
        * New item ships within 1-2 business days
        * Delivery in 3-5 business days
        
        ---
        
        #### ❌ Non-Returnable Items
        
        * Perishable goods
        * Customized/Personalized items
        * Digital products
        * Gift cards
        * Items on sale (final sale)
        
        ---
        
        #### 📞 Need Help?
        
        **Customer Support:**
        * 📧 Email: returns@recipeai.com
        * 📞 Phone: 1-800-RECIPE-AI
        * 💬 Live Chat: Available 24/7
        * ⏰ Response Time: Within 24 hours
        
        ---
        
        #### 💡 Tips for Successful Returns
        
        * Take clear photos of defective/damaged items
        * Include all original packaging and accessories
        * Provide detailed description of issue
        * Keep order confirmation email handy
        * Track your return shipment
        
        ---
        
        **Last Updated:** October 30, 2025
        """)

# ✅ ADD THESE NEW FUNCTIONS - MOVE BEFORE CART SECTION
def generate_invoice_text(order):
    """Generate invoice as text for download"""
    invoice = f"""
    ==========================================
           AI RECIPE ASSISTANT - INVOICE
    ==========================================
    
    Order ID: {order['order_id']}
    Order Date: {order['date']}
    Status: {order['status']}
    
    ==========================================
                CUSTOMER DETAILS
    ==========================================
    Name: {order['customer']['name']}
    Email: {order['customer']['email']}
    Phone: {order['customer']['phone']}
    
    Delivery Address:
    {order['customer']['address']}
    {order['customer']['city']}, {order['customer']['state']} {order['customer']['zip']}
    
    ==========================================
                 ORDER ITEMS
    ==========================================
    """
    
    for item in order['items']:
        info = get_ingredient_info(item['ingredient'].lower())
        item_total = info['price'] * item['quantity']
        invoice += f"\n{item['ingredient'].capitalize()}\n"
        invoice += f"  Quantity: {item['quantity']} x ${info['price']:.2f}\n"
        invoice += f"  Subtotal: ${item_total:.2f}\n"
    
    invoice += f"""
    ==========================================
                PAYMENT SUMMARY
    ==========================================
    Subtotal:          ${order['total']:.2f}
    Delivery:          FREE
    Tax (5%):          ${order['total'] * 0.05:.2f}
    ==========================================
    TOTAL PAID:        ${order['total'] * 1.05:.2f}
    ==========================================
    
    Payment Method: {order['payment_method'].replace('_', ' ').title()}
    
    Thank you for shopping with AI Recipe Assistant!
    For support: 1-800-RECIPE-AI
    Email: support@recipeai.com
    
    ==========================================
    """
    return invoice





# ========== Send Email Confirmation ==================================================
def send_email_confirmation(order):
    """Simulate sending email confirmation"""
    email_content = f"""
    Dear {order['customer']['name']},
    
    Thank you for your order!
    
    Order ID: {order['order_id']}
    Total: ${order['total'] * 1.05:.2f}
    
    Your order has been confirmed and will be delivered to:
    {order['customer']['address']}, {order['customer']['city']}, {order['customer']['state']}
    
    Expected Delivery: 3-5 business days
    
    Track your order: https://recipeai.com/track/{order['order_id']}
    
    Thank you for shopping with us!
    
    Best regards,
    AI Recipe Assistant Team
    """
    return True






# ==================== CART & ORDERS PAGE ====================
if st.session_state.current_page == 'cart':
    # Initialize payment page state
    if 'payment_page' not in st.session_state:
        st.session_state.payment_page = False
    if 'selected_payment_method' not in st.session_state:
        st.session_state.selected_payment_method = None
    if 'view_orders' not in st.session_state:
        st.session_state.view_orders = False
    if 'order_confirmation' not in st.session_state:
        st.session_state.order_confirmation = False
    if 'latest_order' not in st.session_state:
        st.session_state.latest_order = None
        



    
    # =================Payment Page CSS=============================
    st.markdown("""
    <style>
    .payment-header {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(17, 153, 142, 0.4);
    }
    
    .payment-method-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #11998e;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .payment-method-card:hover {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(17, 153, 142, 0.4);
    }
    
    .payment-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .form-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .success-animation {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        box-shadow: 0 10px 30px rgba(17, 153, 142, 0.5);
        animation: celebration 1s ease-in-out;
    }
    
    @keyframes celebration {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.05) rotate(2deg); }
        75% { transform: scale(1.05) rotate(-2deg); }
    }
    
    .order-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #11998e;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .order-card:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 20px rgba(17, 153, 142, 0.3);
    }
    
    .order-status {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .status-processing {
        background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%);
        color: white;
    }
    
    .status-shipped {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        color: white;
    }
    
    .status-delivered {
        background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
        color: white;
    }

    .status-cancelled {                         
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        color: white;
    }
    
    .order-item {
        background: #f5f5f5;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .tracking-timeline {
        position: relative;
        padding-left: 2rem;
        margin: 1rem 0;
    }
    
    .tracking-step {
        position: relative;
        padding: 1rem 0;
        border-left: 3px solid #e0e0e0;
    }
    
    .tracking-step.completed {
        border-left-color: #4caf50;
    }
    
    .tracking-step.cancelled {
        border-left-color: #f44336;
    }
    
    .tracking-step.replacement {
        border-left-color: #ffa500;
    }
    
    .tracking-step::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 1.5rem;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #e0e0e0;
    }
    
    .tracking-step.completed::before {
        background: #4caf50;
    }
    
    .tracking-step.cancelled::before {
        background: #f44336;
    }
    
    .tracking-step.replacement::before {
        background: #ffa500;
    }
    
    .confirmation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .summary-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)





    
    # ==================Function to save order===================================================================
    def save_order(customer_details, payment_method, items, total):
        order = {
            'order_id': f"ORD-{st.session_state.order_counter}",
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'customer': customer_details,
            'payment_method': payment_method,
            'items': items.copy(),
            'total': total,
            'status': 'Processing',
            'tracking': [
                {'step': 'Order Placed', 'completed': True, 'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                {'step': 'Payment Confirmed', 'completed': True, 'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                {'step': 'Preparing Order', 'completed': False, 'time': None},
                {'step': 'Out for Delivery', 'completed': False, 'time': None},
                {'step': 'Delivered', 'completed': False, 'time': None}
            ]
        }
        st.session_state.orders.append(order)
        st.session_state.latest_order = order
        st.session_state.order_counter += 1




    
    
    # =======================ORDER CONFIRMATION PAGE =======================================================
    if st.session_state.order_confirmation and st.session_state.latest_order:
        order = st.session_state.latest_order
        
        st.markdown("<div class='confirmation-box'><div style='font-size: 5rem;'>🎉</div><h1>Order Placed Successfully!</h1><p style='font-size: 1.2rem;'>Thank you for your order!</p></div>", unsafe_allow_html=True)
        
        st.balloons()




        
        # ===============Order Summary==============================
        st.markdown("## 📋 Order Summary")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### Order #{order['order_id']}")
            st.markdown(f"**Order Date:** {order['date']}")
            st.markdown(f"**Payment Method:** {order['payment_method'].replace('_', ' ').title()}")
            st.markdown(f"**Status:** <span class='order-status status-processing'>Processing</span>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("### 👤 Delivery Information")
            st.markdown(f"**Name:** {order['customer']['name']}")
            st.markdown(f"**Email:** {order['customer']['email']}")
            st.markdown(f"**Phone:** {order['customer']['phone']}")
            st.markdown(f"**Address:** {order['customer']['address']}, {order['customer']['city']}, {order['customer']['state']} {order['customer']['zip']}")
        
        with col2:
            st.markdown("### 📍 Order Tracking")
            for track in order['tracking']:
                status_icon = "✅" if track['completed'] else "⏳"
                st.markdown(f"{status_icon} **{track['step']}**")
                if track['time']:
                    st.caption(track['time'])
        
        st.markdown("---")






        
        # ==========================Items Ordered=============================================
       
        st.markdown("### 🛒 Items Ordered")
        
        for item in order['items']:
            item_info = get_item_info(item['ingredient'])
            item_total = item_info['price'] * item['quantity']
            
            col1, col2, col3, col4 = st.columns([1, 4, 2, 2])
            with col1:
                st.markdown(f"<div style='font-size: 2rem; text-align: center;'>{item_info['icon']}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{item['ingredient'].capitalize()}**")
                if item_info['type'] == 'equipment':
                    st.caption("⚙️ Equipment")
            with col3:
                st.markdown(f"Qty: {item['quantity']}")
            with col4:
                st.markdown(f"**${item_total:.2f}**")
        
        st.markdown("---")






        
        # ===========================Price Breakdown==============================================
        st.markdown("### 💰 Payment Details")
        
        col1, col2, col3 = st.columns([3, 1, 1])
        with col2:
            st.markdown("**Subtotal:**")
            st.markdown("**Delivery:**")
            st.markdown("**Tax (5%):**")
            st.markdown("---")
            st.markdown("### **Total Paid:**")
        with col3:
            st.markdown(f"${order['total']:.2f}")
            st.markdown("Free 🎉")
            st.markdown(f"${order['total'] * 0.05:.2f}")
            st.markdown("---")
            st.markdown(f"### **${order['total'] * 1.05:.2f}**")
        
        st.markdown("---")






        
        # ===========================Action Buttons=======================================
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🏠 Continue Shopping", type="primary", use_container_width=True):
                st.session_state.order_confirmation = False
                st.session_state.current_page = 'main'
                st.rerun()
        with col2:
            if st.button("📦 View All Orders", type="secondary", use_container_width=True):
                st.session_state.order_confirmation = False
                st.session_state.view_orders = True
                st.rerun()
        with col3:


            
            # ✅ FIXED DOWNLOAD INVOICE
            invoice_text = generate_invoice_text(order)
            st.download_button(
                label="📄 Download Invoice",
                data=invoice_text,
                file_name=f"Invoice_{order['order_id']}.txt",
                mime="text/plain",
                key=f"invoice_orders_{order['order_id']}_{uuid.uuid4()}",
                use_container_width=True
            )


        
        # ✅ EMAIL CONFIRMATION MESSAGE
        st.success(f"✅ Order confirmation will be sent to {order['customer']['email']}")
        st.info(f"📧 Please check your inbox and spam folder")
        st.info(f"📦 Expected delivery: 3-5 business days")





    
    # ========== YOUR ORDERS PAGE ==========
    elif st.session_state.view_orders:
        st.markdown("<div class='payment-header'>📦 Your Orders</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("← Back"):
                st.session_state.view_orders = False
                st.rerun()
        with col3:
            if st.button("🔄 Returns", use_container_width=True):
                st.session_state.view_returns = True
                st.session_state.view_orders = False
                st.rerun()
        
        if st.session_state.orders:
            st.markdown(f"### 📊 Total Orders: {len(st.session_state.orders)}")






            
            # =================Filter options========================================
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_status = st.selectbox("Filter by Status:", ["All", "Processing", "Shipped", "Delivered", "Cancelled"])
            with col2:
                sort_by = st.selectbox("Sort by:", ["Newest First", "Oldest First", "Highest Amount", "Lowest Amount"])




            
            # ==================Sort and filter orders==============================
            filtered_orders = st.session_state.orders.copy()
            
            if filter_status != "All":
                filtered_orders = [o for o in filtered_orders if o['status'] == filter_status]
            
            if sort_by == "Newest First":
                filtered_orders = sorted(filtered_orders, key=lambda x: x['date'], reverse=True)
            elif sort_by == "Oldest First":
                filtered_orders = sorted(filtered_orders, key=lambda x: x['date'])
            elif sort_by == "Highest Amount":
                filtered_orders = sorted(filtered_orders, key=lambda x: x['total'], reverse=True)
            elif sort_by == "Lowest Amount":
                filtered_orders = sorted(filtered_orders, key=lambda x: x['total'])
            
            st.markdown("---")






        
            # =============================Display orders=========================================
            for idx, order in enumerate(filtered_orders):
                with st.expander(f"🛍️ Order #{order['order_id']} - ${order['total']:.2f} - {order['date']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"### Order Details")
                        st.markdown(f"**Order ID:** {order['order_id']}")
                        st.markdown(f"**Date:** {order['date']}")
                        st.markdown(f"**Payment Method:** {order['payment_method'].replace('_', ' ').title()}")




                        
                        # ========================Order status===================================
                        status_class = f"status-{order['status'].lower()}"
                        if order['status'] == 'Cancelled':
                            status_class = "status-cancelled"
                            st.markdown(f"**Status:** <span class='order-status {status_class}'>{order['status']}</span>", unsafe_allow_html=True)
                            st.error(f"**Cancelled on:** {order.get('cancellation_date', 'N/A')}")
                            st.warning(f"**Reason:** {order.get('cancellation_reason', 'N/A')}")




                            
                            # ==================Show refund status===============================
                            if 'refund_status' in order:
                                st.markdown("---")
                                st.markdown("### 💰 Refund Status")
                                
                                if order['refund_status'] == 'Completed':
                                    st.success(f"✅ **Refund Completed**")
                                    st.info(f"💵 Amount: ${order['refund_amount']:.2f}")
                                    st.info(f"📍 Method: {order['refund_method']}")
                                    st.info(f"📅 Date: {order['refund_date']}")
                                    
                                    if order['refund_method'] == 'Wallet':
                                        st.success(f"👛 Credited to your wallet instantly!")
                                
                                elif order['refund_status'] == 'Processing':
                                    st.warning(f"⏳ **Refund Processing**")
                                    st.info(f"💵 Amount: ${order['refund_amount']:.2f}")
                                    st.info(f"📍 Method: {order['refund_method']}")
                                    st.info(f"🏦 Bank: {order.get('refund_bank_details', {}).get('bank', 'N/A')}")
                                    st.info(f"💳 Account: ***{order.get('refund_bank_details', {}).get('account', 'N/A')}")
                                    expected_date = order.get('refund_expected', (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"))
                                    st.info(f"📅 Expected: {expected_date}")
                                    st.caption("⏰ Refund will be credited in 3-5 business days")
                        else:
                            st.markdown(f"**Status:** <span class='order-status {status_class}'>{order['status']}</span>", unsafe_allow_html=True)                        
                        st.markdown("---")




                        
                        # ======================Customer details===================================
                        st.markdown("### 👤 Delivery Information")
                        st.markdown(f"**Name:** {order['customer']['name']}")
                        st.markdown(f"**Email:** {order['customer']['email']}")
                        st.markdown(f"**Phone:** {order['customer']['phone']}")
                        st.markdown(f"**Address:** {order['customer']['address']}, {order['customer']['city']}, {order['customer']['state']} {order['customer']['zip']}")
                    
                    with col2:


                        
                        # ======================= Tracking Timeline===================================
                        st.markdown("### 📍 Order Tracking")
                        st.markdown("<div class='tracking-timeline'>", unsafe_allow_html=True)



                        
                        
                        # =======================Show different tracking for cancelled orders=================
                        if order['status'] == 'Cancelled':
                            # Show completed steps
                            for track in order['tracking'][:2]:  # Only Order Placed and Payment Confirmed
                                st.markdown(f"""
                                <div class='tracking-step completed'>
                                    <strong>✅ {track['step']}</strong><br>
                                    <small style='color: #666;'>{track['time']}</small>
                                </div>
                                """, unsafe_allow_html=True)



                            
                            #==================================== Show cancellation============================
                            st.markdown(f"""
                            <div class='tracking-step cancelled'>
                                <strong>❌ Order Cancelled</strong><br>
                                <small style='color: #666;'>{order.get('cancellation_date', 'N/A')}</small>
                            </div>
                            """, unsafe_allow_html=True)



                            
                            # ====================================Show refund steps============================
                            if 'refund_status' in order:
                                if order['refund_status'] == 'Processing':
                                    st.markdown("""
                                    <div class='tracking-step cancelled'>
                                        <strong>⏳ Refund Processing</strong><br>
                                        <small style='color: #666;'>In Progress</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.markdown(f"""
                                    <div class='tracking-step'>
                                        <strong>💰 Refund Completed</strong><br>
                                        <small style='color: #666;'>Expected: {order.get('refund_expected', 'N/A')}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                                elif order['refund_status'] == 'Completed':
                                    st.markdown(f"""
                                    <div class='tracking-step cancelled'>
                                        <strong>✅ Refund Completed</strong><br>
                                        <small style='color: #666;'>{order.get('refund_date', 'N/A')}</small>
                                    </div>
                                    """, unsafe_allow_html=True)




                        
                        # =================Show different tracking for replacement==============================
                        elif 'return_request_id' in order:
                            return_req = None
                            for req in st.session_state.return_requests:
                                if req['request_id'] == order['return_request_id']:
                                    return_req = req
                                    break
                            
                            if return_req and return_req['action_type'] == 'Replace':
                                for track in order['tracking'][:2]:
                                    st.markdown(f"""
                                    <div class='tracking-step completed'>
                                        <strong>✅ {track['step']}</strong><br>
                                        <small style='color: #666;'>{track['time']}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                st.markdown(f"""
                                <div class='tracking-step replacement'>
                                    <strong>🔄 Replacement Requested</strong><br>
                                    <small style='color: #666;'>{return_req['request_date']}</small>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                for step in return_req['timeline'][2:]:
                                    completed_class = "replacement" if step['completed'] else ""
                                    status_icon = "✅" if step['completed'] else "⏳"
                                    time_text = step['time'] if step['time'] else "Pending"
                                    
                                    st.markdown(f"""
                                    <div class='tracking-step {completed_class}'>
                                        <strong>{status_icon} {step['step']}</strong><br>
                                        <small style='color: #666;'>{time_text}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                # Normal tracking for returns
                                for track in order['tracking']:
                                    completed_class = "completed" if track['completed'] else ""
                                    status_icon = "✅" if track['completed'] else "⏳"
                                    time_text = track['time'] if track['time'] else "Pending"
                                    
                                    st.markdown(f"""
                                    <div class='tracking-step {completed_class}'>
                                        <strong>{status_icon} {track['step']}</strong><br>
                                        <small style='color: #666;'>{time_text}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            # Normal tracking
                            for track in order['tracking']:
                                completed_class = "completed" if track['completed'] else ""
                                status_icon = "✅" if track['completed'] else "⏳"
                                time_text = track['time'] if track['time'] else "Pending"
                                
                                st.markdown(f"""
                                <div class='tracking-step {completed_class}'>
                                    <strong>{status_icon} {track['step']}</strong><br>
                                    <small style='color: #666;'>{time_text}</small>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("---")




                    
                    # ====================Order items==========================================
                    
                    st.markdown("### 🛒 Items Ordered")
                    
                    for item in order['items']:
                        item_info = get_item_info(item['ingredient'])
                        item_total = item_info['price'] * item['quantity']
                        
                        col1, col2, col3, col4 = st.columns([1, 4, 2, 2])
                        with col1:
                            st.markdown(f"<div style='font-size: 2rem; text-align: center;'>{item_info['icon']}</div>", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"**{item['ingredient'].capitalize()}**")
                            if item_info['type'] == 'equipment':
                                st.caption("⚙️ Equipment")
                        with col3:
                            st.markdown(f"Qty: {item['quantity']}")
                        with col4:
                            st.markdown(f"**${item_total:.2f}**")
                    
                    st.markdown("---")




                    
                    # ==============================Order summary=========================================
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col2:
                        st.markdown("**Subtotal:**")
                        st.markdown("**Delivery:**")
                        st.markdown("**Tax (5%):**")
                        st.markdown("### **Total:**")
                    with col3:
                        st.markdown(f"${order['total']:.2f}")
                        st.markdown("Free 🎉")
                        st.markdown(f"${order['total'] * 0.05:.2f}")
                        st.markdown(f"### **${order['total'] * 1.05:.2f}**")



                    
                    # ===========================Action buttons=======================================
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        # ✅ IMPROVED DOWNLOAD INVOICE
                        invoice_text = generate_invoice_text(order)
                        st.download_button(
                            label="📄 Download Invoice",
                            data=invoice_text,
                            file_name=f"Invoice_{order['order_id']}.txt",
                            mime="text/plain",
                            key=f"invoice_orders_{order['order_id']}_{idx}",
                            use_container_width=True
                        )
                    with col2:
                        # ✅ Unique toggle state per order
                        toggle_key = f"show_support_{order['order_id']}_orderspage_{idx}"
                    
                        if toggle_key not in st.session_state:
                            st.session_state[toggle_key] = False
                    
                        # ✅ Button logic
                        if not st.session_state[toggle_key]:
                            if st.button("📞 Contact Support", key=f"contact_{order['order_id']}_orderspage_{idx}", use_container_width=True):
                                st.session_state[toggle_key] = True
                                st.rerun()
                        else:
                            if st.button("❌ Close Support", key=f"close_{order['order_id']}_orderspage_{idx}", use_container_width=True):
                                st.session_state[toggle_key] = False
                                st.rerun()
                    
                    # ✅ Animated Support Panel (only when toggled on)
                    if st.session_state[toggle_key]:
                        st.markdown(
                            f"""
                            <style>
                            @keyframes slideIn {{
                                0% {{opacity: 0; transform: translateY(-15px);}}
                                100% {{opacity: 1; transform: translateY(0);}}
                            }}
                            .support-box {{
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                border: 2px solid #22c55e;
                                padding: 18px 20px;
                                border-radius: 12px;
                                background: linear-gradient(135deg, #f0fff4 0%, #dcfce7 100%);
                                color: #064e3b;
                                font-family: 'Segoe UI', sans-serif;
                                animation: slideIn 0.5s ease forwards;
                                box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                                margin-top: 10px;
                                width: 100%;
                            }}
                            .support-text {{
                                flex: 1;
                                margin-right: 20px;
                            }}
                            .support-box h4 {{
                                color: #15803d;
                                margin-bottom: 10px;
                            }}
                            .support-box ul {{
                                margin-left: 15px;
                                line-height: 1.6;
                            }}
                            .support-box a {{
                                color: #065f46;
                                text-decoration: none;
                            }}
                            .support-box a:hover {{
                                text-decoration: underline;
                            }}
                            .support-img {{
                                width: 300px;
                                height: auto;
                                border-radius: 10px;
                                box-shadow: 0px 2px 8px rgba(0,0,0,0.2);
                                animation: float 2.5s ease-in-out infinite;
                            }}
                            @keyframes float {{
                                0% {{ transform: translateY(0px); }}
                                50% {{ transform: translateY(-6px); }}
                                100% {{ transform: translateY(0px); }}
                            }}
                            </style>
                        
                            <div class='support-box'>
                                <div class='support-text'>
                                    <h4>📞 Customer Support — Order #{order['order_id']}</h4>
                                    <ul>
                                        <li><b>Phone:</b> 1-800-RECIPE-AI (24/7)</li>
                                        <li><b>Email:</b> <a href='mailto:support@recipeai.com'>support@recipeai.com</a></li>
                                        <li><b>Live Chat:</b> Available on our official website</li>
                                        <li><b>Response Time:</b> Within 24 hours</li>
                                    </ul>
                                </div>
                                <div style='flex-shrink:0;'>
                                    <img class='support-img' src='https://cdn.vectorstock.com/i/preview-1x/69/46/customer-service-logo-template-vector-33316946.jpg' alt='Customer Support'/>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )



                    
                    with col3:
                        if order['status'] == 'Processing':
                            # ✅ CANCEL ORDER BUTTON
                            if st.button("❌ Cancel Order", key=f"cancel_{order['order_id']}_orders_{idx}", use_container_width=True):
                                st.session_state[f"show_cancel_form_{order['order_id']}"] = True
                        elif order['status'] == 'Delivered':
                            # ✅ RETURN/REPLACE BUTTON
                            if st.button("🔄 Return/Replace", key=f"return_{order['order_id']}_orders_{idx}", use_container_width=True):
                                st.session_state[f"show_return_form_{order['order_id']}"] = True



                    
                    # ✅ CANCEL ORDER FORM
                    # ✅ CANCEL ORDER FORM
                    if st.session_state.get(f"show_cancel_form_{order['order_id']}", False):
                        with st.form(f"cancel_form_{order['order_id']}"):
                            st.markdown("### ⚠️ Cancel Order Confirmation")
                            st.warning(f"Are you sure you want to cancel Order #{order['order_id']}?")
                            
                            cancel_reason = st.selectbox(
                                "Reason for cancellation:",
                                [
                                    "Changed my mind",
                                    "Found a better price elsewhere",
                                    "Ordered by mistake",
                                    "Delivery time too long",
                                    "Wrong items ordered",
                                    "Other"
                                ]
                            )
                            
                            cancel_details = st.text_area("Additional details (optional):", placeholder="Please provide more information...")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("✅ Confirm Cancellation", type="primary", use_container_width=True):
                                    # Cancel the order
                                    for ord in st.session_state.orders:
                                        if ord['order_id'] == order['order_id']:
                                            # ✅ FIXED: Mark that this was delivered before cancellation
                                            if ord['status'] == 'Delivered':
                                                ord['was_delivered'] = True
                                            ord['status'] = 'Cancelled'
                                            ord['cancellation_reason'] = cancel_reason
                                            ord['cancellation_details'] = cancel_details
                                            ord['cancellation_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    
                                    st.success(f"✅ Order #{order['order_id']} has been cancelled successfully!")
                                    st.info(f"📧 Cancellation confirmation will be sent to {order['customer']['email']}")
                                    
                                    # Show refund options
                                    st.session_state[f"show_cancel_form_{order['order_id']}"] = False
                                    st.session_state[f"show_refund_options_{order['order_id']}"] = True
                                    st.rerun()
                            
                            with col2:
                                if st.form_submit_button("❌ Keep Order", use_container_width=True):
                                    st.session_state[f"show_cancel_form_{order['order_id']}"] = False
                                    st.rerun()




                    
                    # ✅ REFUND OPTIONS (FIXED - PREVENT DOUBLE REFUNDS)

                    if (
                        st.session_state.get(f"show_refund_options_{order['order_id']}", False)
                        and order['status'] == 'Cancelled'
                    ):
                        # Check if refund already processed
                        if order.get('refund_status') in ['Processing', 'Completed']:
                            st.warning("⚠️ Refund has already been processed for this order!")
                            if st.button("← Back", key=f"back_refund_{order['order_id']}"):
                                st.session_state[f"show_refund_options_{order['order_id']}"] = False
                                st.rerun()
                        else:
                            st.markdown("---")
                            st.markdown("### 💰 Select Refund Method")
                            
                            refund_amount = order['total'] * 1.05  # Including tax
                            original_payment = order['payment_method']
                            
                            st.info(f"**Refund Amount:** ${refund_amount:.2f}")
                            st.info(f"**Original Payment:** {original_payment.replace('_', ' ').title()}")






                            
                            # ==============SMART REFUND ROUTING based on original payment method====================
                            if original_payment in ['wallet', 'gift_card']:


                                
                                # ===========If paid with wallet/gift card, refund ONLY to same method========================
                                st.success(f"✅ Refund will be credited to your {original_payment.replace('_', ' ').title()} instantly!")
                                
                                if st.button(f"💰 Refund to {original_payment.replace('_', ' ').title()}", type="primary", use_container_width=True, key=f"instant_refund_{order['order_id']}"):
                                    if original_payment == 'wallet':
                                        st.session_state.wallet_balance += refund_amount
                                        st.session_state.wallet_transactions.append({
                                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            'type': 'Refund',
                                            'order_id': order['order_id'],
                                            'amount': refund_amount,
                                            'balance': st.session_state.wallet_balance
                                        })
                                    else:
                                        st.session_state.gift_card_balance += refund_amount
                                        st.session_state.gift_card_transactions.append({
                                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            'type': 'Refund',
                                            'order_id': order['order_id'],
                                            'amount': refund_amount,
                                            'balance': st.session_state.gift_card_balance
                                        })



                                    
                                    # ===========Update order=========================
                                    for ord in st.session_state.orders:
                                        if ord['order_id'] == order['order_id']:
                                            ord['refund_status'] = 'Completed'
                                            ord['refund_method'] = original_payment.replace('_', ' ').title()
                                            ord['refund_amount'] = refund_amount
                                            ord['refund_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    
                                    st.balloons()
                                    st.success(f"🎉 ${refund_amount:.2f} credited instantly!")
                                    st.session_state[f"show_refund_options_{order['order_id']}"] = False
                                    st.rerun()
                            
                            else:
                                # For other payment methods, offer multiple refund options
                                st.markdown("#### Choose Refund Destination:")
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    if st.button("🏦 Bank Account (3-5 days)", key=f"bank_refund_{order['order_id']}", use_container_width=True):
                                        st.session_state[f"refund_method_{order['order_id']}"] = "bank"
                                        st.rerun()
                                    
                                    if st.button("📱 UPI (1-2 days)", key=f"upi_refund_{order['order_id']}", use_container_width=True):
                                        st.session_state[f"refund_method_{order['order_id']}"] = "upi"
                                        st.rerun()
                                
                                with col2:
                                    if st.button("👛 Wallet (Instant)", key=f"wallet_refund_{order['order_id']}", use_container_width=True):
                                        st.session_state[f"refund_method_{order['order_id']}"] = "wallet"
                                        st.rerun()
                                    
                                    if st.button("🎁 Gift Card (Instant)", key=f"giftcard_refund_{order['order_id']}", use_container_width=True):
                                        st.session_state[f"refund_method_{order['order_id']}"] = "giftcard"
                                        st.rerun()




                                
                                # =================Bank Account Refund Form===================================
                                if st.session_state.get(f"refund_method_{order['order_id']}", "") == "bank":
                                    with st.form(f"bank_refund_form_{order['order_id']}"):
                                        st.markdown("#### 🏦 Bank Account Details")
                                        
                                        account_holder = st.text_input("Account Holder Name *", placeholder="John Doe")
                                        bank_name = st.text_input("Bank Name *", placeholder="State Bank")
                                        account_number = st.text_input("Account Number *", placeholder="1234567890")
                                        confirm_account = st.text_input("Confirm Account Number *", placeholder="1234567890")
                                        ifsc_code = st.text_input("IFSC Code *", placeholder="SBIN0001234")
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            if st.form_submit_button("✅ Process Refund", type="primary", use_container_width=True):
                                                if account_holder and bank_name and account_number and ifsc_code and account_number == confirm_account:
                                                    for ord in st.session_state.orders:
                                                        if ord['order_id'] == order['order_id']:
                                                            ord['refund_status'] = 'Processing'
                                                            ord['refund_method'] = 'Bank Account'
                                                            ord['refund_amount'] = refund_amount
                                                            ord['refund_bank_details'] = {
                                                                'holder': account_holder,
                                                                'bank': bank_name,
                                                                'account': account_number[-4:],
                                                                'ifsc': ifsc_code
                                                            }
                                                            ord['refund_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                            ord['refund_expected'] = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
                                                    
                                                    st.balloons()
                                                    st.success(f"✅ Refund of ${refund_amount:.2f} initiated!")
                                                    st.session_state[f"show_refund_options_{order['order_id']}"] = False
                                                    st.session_state[f"refund_method_{order['order_id']}"] = None
                                                    st.rerun()
                                                else:
                                                    st.error("❌ Please fill all fields correctly!")
                                        
                                        with col2:
                                            if st.form_submit_button("← Back", use_container_width=True):
                                                st.session_state[f"refund_method_{order['order_id']}"] = None
                                                st.rerun()





                                
                                # ======================UPI Refund Form============================
                                elif st.session_state.get(f"refund_method_{order['order_id']}", "") == "upi":
                                    with st.form(f"upi_refund_form_{order['order_id']}"):
                                        st.markdown("#### 📱 UPI Details")
                                        
                                        upi_id = st.text_input("UPI ID *", placeholder="yourname@okaxis")
                                        confirm_upi = st.text_input("Confirm UPI ID *", placeholder="yourname@okaxis")
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            if st.form_submit_button("✅ Process Refund", type="primary", use_container_width=True):
                                                if upi_id and upi_id == confirm_upi:
                                                    for ord in st.session_state.orders:
                                                        if ord['order_id'] == order['order_id']:
                                                            ord['refund_status'] = 'Processing'
                                                            ord['refund_method'] = 'UPI'
                                                            ord['refund_amount'] = refund_amount
                                                            ord['refund_upi_id'] = upi_id
                                                            ord['refund_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                            ord['refund_expected'] = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
                                                    
                                                    st.balloons()
                                                    st.success(f"✅ Refund of ${refund_amount:.2f} initiated to UPI!")
                                                    st.session_state[f"show_refund_options_{order['order_id']}"] = False
                                                    st.session_state[f"refund_method_{order['order_id']}"] = None
                                                    st.rerun()
                                                else:
                                                    st.error("❌ UPI IDs don't match!")
                                        
                                        with col2:
                                            if st.form_submit_button("← Back", use_container_width=True):
                                                st.session_state[f"refund_method_{order['order_id']}"] = None
                                                st.rerun()





                                
                                # =====================Wallet Refund==============================
                                elif st.session_state.get(f"refund_method_{order['order_id']}", "") == "wallet":
                                    st.markdown("#### 👛 Wallet Refund")
                                    st.info(f"💰 ${refund_amount:.2f} will be credited to your wallet instantly!")
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if st.button("✅ Confirm", type="primary", use_container_width=True, key=f"confirm_wallet_{order['order_id']}"):
                                            st.session_state.wallet_balance += refund_amount
                                            st.session_state.wallet_transactions.append({
                                                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                'type': 'Refund',
                                                'order_id': order['order_id'],
                                                'amount': refund_amount,
                                                'balance': st.session_state.wallet_balance
                                            })
                                            
                                            for ord in st.session_state.orders:
                                                if ord['order_id'] == order['order_id']:
                                                    ord['refund_status'] = 'Completed'
                                                    ord['refund_method'] = 'Wallet'
                                                    ord['refund_amount'] = refund_amount
                                                    ord['refund_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                            
                                            st.balloons()
                                            st.success(f"🎉 ${refund_amount:.2f} credited to wallet!")
                                            st.session_state[f"show_refund_options_{order['order_id']}"] = False
                                            st.session_state[f"refund_method_{order['order_id']}"] = None
                                            st.rerun()
                                    
                                    with col2:
                                        if st.button("← Back", use_container_width=True, key=f"back_wallet_{order['order_id']}"):
                                            st.session_state[f"refund_method_{order['order_id']}"] = None
                                            st.rerun()





                                
                                #==================== Gift Card Refund===========================================
                                elif st.session_state.get(f"refund_method_{order['order_id']}", "") == "giftcard":
                                    st.markdown("#### 🎁 Gift Card Refund")
                                    st.info(f"💰 ${refund_amount:.2f} will be credited to your gift card instantly!")
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if st.button("✅ Confirm", type="primary", use_container_width=True, key=f"confirm_giftcard_{order['order_id']}"):
                                            st.session_state.gift_card_balance += refund_amount
                                            st.session_state.gift_card_transactions.append({
                                                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                'type': 'Refund',
                                                'order_id': order['order_id'],
                                                'amount': refund_amount,
                                                'balance': st.session_state.gift_card_balance
                                            })
                                            
                                            for ord in st.session_state.orders:
                                                if ord['order_id'] == order['order_id']:
                                                    ord['refund_status'] = 'Completed'
                                                    ord['refund_method'] = 'Gift Card'
                                                    ord['refund_amount'] = refund_amount
                                                    ord['refund_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                            
                                            st.balloons()
                                            st.success(f"🎉 ${refund_amount:.2f} credited to gift card!")
                                            st.session_state[f"show_refund_options_{order['order_id']}"] = False
                                            st.session_state[f"refund_method_{order['order_id']}"] = None
                                            st.rerun()
                                    
                                    with col2:
                                        if st.button("← Back", use_container_width=True, key=f"back_giftcard_{order['order_id']}"):
                                            st.session_state[f"refund_method_{order['order_id']}"] = None
                                            st.rerun()





                                        
                                        #============== ✅ RETURN/REPLACEMENT SYSTEM (MUST BE INSIDE ORDER LOOP)==================
                                        if st.session_state.get(f"show_return_form_{order['order_id']}", False):
                                            with st.form(f"return_form_{order['order_id']}"):
                                                st.markdown("### 🔄 Return or Replace Order")
                                                st.info(f"**Order ID:** {order['order_id']} | **Total:** ${order['total'] * 1.05:.2f}")



                                                
                                                # ================Return or Replace choice===========================
                                                action_type = st.radio(
                                                    "What would you like to do?",
                                                    ["Return (Get Refund)", "Replace (Get New Product)"],
                                                    horizontal=True
                                                )
                                                
                                                st.markdown("---")



                                                
                                                # =====================Reason for return/replacement==================
                                                if "Return" in action_type:
                                                    st.markdown("#### 📋 Reason for Return")
                                                    return_reason = st.selectbox(
                                                        "Select Reason:",
                                                        [
                                                            "Product damaged/defective",
                                                            "Wrong item delivered",
                                                            "Product not as described",
                                                            "Quality issues",
                                                            "Size/fit issues",
                                                            "Changed my mind",
                                                            "Better price available elsewhere",
                                                            "Received incomplete product",
                                                            "Other"
                                                        ]
                                                    )
                                                else:
                                                    st.markdown("#### 📋 Reason for Replacement")
                                                    return_reason = st.selectbox(
                                                        "Select Reason:",
                                                        [
                                                            "Product damaged/defective",
                                                            "Wrong item delivered",
                                                            "Product not as described",
                                                            "Quality issues",
                                                            "Size/fit issues",
                                                            "Missing parts/accessories",
                                                            "Color/style different from order",
                                                            "Other"
                                                        ]
                                                    )
                                                
                                                return_details = st.text_area(
                                                    "Additional Details (Optional):",
                                                    placeholder="Please describe the issue in detail..."
                                                )




                                                
                                                # =============Photo upload simulation=======================
                                                st.markdown("📸 Upload Photos (Optional)")
                                                uploaded_photos = st.file_uploader(
                                                    "Upload photos of the product/issue",
                                                    type=['jpg', 'jpeg', 'png'],
                                                    accept_multiple_files=True,
                                                    key=f"photos_{order['order_id']}"
                                                )
                                                
                                                st.markdown("---")




                                                
                                                # ====================Pickup details==============================
                                                st.markdown("#### 📍 Pickup Details")
                                                st.info("Our delivery partner will pick up the product from your address")
                                                
                                                pickup_address = st.text_area(
                                                    "Pickup Address:",
                                                    value=f"{order['customer']['address']}, {order['customer']['city']}, {order['customer']['state']} {order['customer']['zip']}",
                                                    height=100
                                                )
                                                
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    pickup_date = st.date_input(
                                                        "Preferred Pickup Date:",
                                                        min_value=datetime.now().date(),
                                                        max_value=(datetime.now() + timedelta(days=7)).date()
                                                    )
                                                with col2:
                                                    pickup_time = st.selectbox(
                                                        "Preferred Time Slot:",
                                                        ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"]
                                                    )
                                                
                                                st.markdown("---")
                                                
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    if st.form_submit_button("✅ Submit Request", type="primary", use_container_width=True):
                                                        # Create return request
                                                        return_request = {
                                                            'request_id': f"RET-{len(st.session_state.return_requests) + 1001}",
                                                            'order_id': order['order_id'],
                                                            'action_type': 'Return' if 'Return' in action_type else 'Replace',
                                                            'reason': return_reason,
                                                            'details': return_details,
                                                            'pickup_address': pickup_address,
                                                            'pickup_date': pickup_date.strftime("%Y-%m-%d"),
                                                            'pickup_time': pickup_time,
                                                            'request_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                            'status': 'Pickup Scheduled',
                                                            'customer': order['customer'],
                                                            'order_total': order['total'] * 1.05,
                                                            'payment_method': order['payment_method'],
                                                            'photos_uploaded': len(uploaded_photos) if uploaded_photos else 0,
                                                            'timeline': [
                                                                {'step': 'Request Submitted', 'completed': True, 'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                                                                {'step': 'Pickup Scheduled', 'completed': True, 'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                                                                {'step': 'Product Picked Up', 'completed': False, 'time': None},
                                                                {'step': 'Quality Check', 'completed': False, 'time': None},
                                                                {'step': 'Refund Processed' if 'Return' in action_type else 'Replacement Shipped', 'completed': False, 'time': None}
                                                            ]
                                                        }
                                                        
                                                        st.session_state.return_requests.append(return_request)
                                                        
                                                        # Update order status
                                                        for ord in st.session_state.orders:
                                                            if ord['order_id'] == order['order_id']:
                                                                ord['return_request_id'] = return_request['request_id']
                                                                ord['return_status'] = 'Pickup Scheduled'
                                                        
                                                        st.success(f"✅ {'Return' if 'Return' in action_type else 'Replacement'} request submitted successfully!")
                                                        st.info(f"📋 Request ID: {return_request['request_id']}")
                                                        st.info(f"📅 Pickup scheduled for: {pickup_date.strftime('%B %d, %Y')} ({pickup_time})")
                                                        st.info(f"📧 Confirmation sent to {order['customer']['email']}")
                                                        
                                                        st.session_state[f"show_return_form_{order['order_id']}"] = False
                                                        st.session_state[f"show_return_tracking_{return_request['request_id']}"] = True
                                                        st.rerun()
                                                
                                                with col2:
                                                    if st.form_submit_button("← Cancel", use_container_width=True):
                                                        st.session_state[f"show_return_form_{order['order_id']}"] = False
                                                        st.rerun()




                    
                    # ============✅ SHOW RETURN/REPLACEMENT TRACKING (MUST BE INSIDE ORDER LOOP)=================================
                    if 'return_request_id' in order:
                        # ============================Find the return request=============================
                        return_req = None
                        for req in st.session_state.return_requests:
                            if req['request_id'] == order['return_request_id']:
                                return_req = req
                                break
                        
                        if return_req:
                            st.markdown("---")
                            st.markdown(f"### 🔄 {return_req['action_type']} Request Status")


                            
                            # ==================Status badge================
                            status_colors = {
                                'Pickup Scheduled': '🟡',
                                'Product Picked Up': '🟠',
                                'Quality Check': '🔵',
                                'Approved': '🟢',
                                'Refund Processing': '🟢',
                                'Refund Completed': '✅',
                                'Replacement Shipped': '🟢',
                                'Replacement Delivered': '✅',
                                'Rejected': '🔴'
                            }
                            
                            status_icon = status_colors.get(return_req['status'], '⚪')
                            st.info(f"{status_icon} **Status:** {return_req['status']}")
                            st.caption(f"Request ID: {return_req['request_id']}")





                            
                            # ================Timeline================================
                            st.markdown("#### 📍 Tracking Timeline")
                            for step in return_req['timeline']:
                                status_icon = "✅" if step['completed'] else "⏳"
                                st.markdown(f"{status_icon} **{step['step']}**")
                                if step['time']:
                                    st.caption(step['time'])




                            
                            # =======================Process refund button (simulate quality check approval)======================
                            if return_req['status'] == 'Pickup Scheduled' or return_req['status'] == 'Product Picked Up':
                                st.markdown("---")
                                if st.button("🔍 Simulate Quality Check (Admin)", key=f"quality_check_{return_req['request_id']}", type="secondary"):
                                    # Approve and move to refund
                                    return_req['status'] = 'Approved'
                                    return_req['timeline'][3]['completed'] = True
                                    return_req['timeline'][3]['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    
                                    if return_req['action_type'] == 'Return':
                                        st.session_state[f"show_refund_options_{order['order_id']}"] = True
                                    else:
                                        return_req['status'] = 'Replacement Shipped'
                                        return_req['timeline'][4]['completed'] = True
                                        return_req['timeline'][4]['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    
                                    st.success("✅ Quality check completed! Request approved.")
                                    st.rerun()
        
        else:
            st.info("📦 No orders yet. Start shopping to place your first order!")



    
    # ========== RETURN REQUESTS PAGE ==========
    elif st.session_state.get('view_returns', False):
        st.markdown("<div class='payment-header'>🔄 Return & Replacement Requests</div>", unsafe_allow_html=True)
        
        if st.button("← Back to Orders"):
            st.session_state.view_returns = False
            st.session_state.view_orders = True
            st.rerun()
        
        if st.session_state.return_requests:
            st.markdown(f"### 📊 Total Requests: {len(st.session_state.return_requests)}")
            
            for req in st.session_state.return_requests:
                with st.expander(f"🔄 {req['action_type']} Request - {req['request_id']} - ${req['order_total']:.2f}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"### Request Details")
                        st.markdown(f"**Request ID:** {req['request_id']}")
                        st.markdown(f"**Order ID:** {req['order_id']}")
                        st.markdown(f"**Type:** {req['action_type']}")
                        st.markdown(f"**Reason:** {req['reason']}")
                        st.markdown(f"**Request Date:** {req['request_date']}")
                        st.markdown(f"**Status:** {req['status']}")
                        
                        if req['details']:
                            st.markdown(f"**Details:** {req['details']}")
                        
                        st.markdown("---")
                        
                        st.markdown("### 📍 Pickup Information")
                        st.markdown(f"**Date:** {req['pickup_date']}")
                        st.markdown(f"**Time:** {req['pickup_time']}")
                        st.markdown(f"**Address:** {req['pickup_address']}")
                    
                    with col2:
                        st.markdown("### 📍 Tracking")
                        for step in req['timeline']:
                            icon = "✅" if step['completed'] else "⏳"
                            st.markdown(f"{icon} **{step['step']}**")
                            if step['time']:
                                st.caption(step['time'])
        else:
            st.info("🔄 No return/replacement requests yet.")





    
    # ========== CART VIEW (Before Payment) ==========
    elif not st.session_state.payment_page:
        st.markdown("<h1 class='main-header'>🛒 Shopping Cart</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← Back to Main"):
                st.session_state.current_page = 'main'
                st.rerun()
        with col2:
            # ✅ ONLY SHOW "Your Orders" BUTTON IF ORDERS EXIST
            if len(st.session_state.orders) > 0:
                if st.button("📦 Your Orders", type="secondary", use_container_width=True):
                    st.session_state.view_orders = True
                    st.rerun()
        
        if st.session_state.shopping_cart:
            st.markdown(f"### 🛒 Your Cart ({st.session_state.cart_items_count} items)")
            
            total_cart_price = 0
            items_to_remove = []
            
            for idx, item in enumerate(st.session_state.shopping_cart):
                item_info = get_item_info(item['ingredient'])
                item_price = item_info['price'] * item['quantity']
                total_cart_price += item_price
                
                col1, col2, col3, col4, col5 = st.columns([1, 4, 2, 2, 1])
                with col1:
                    st.markdown(f"<div style='font-size: 35px; text-align: center;'>{item_info['icon']}</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**{item['ingredient'].capitalize()}**")
                    if item_info['type'] == 'equipment':
                        st.caption("⚙️ Equipment")
                    else:
                        st.caption(f"📦 {item_info['quantity']}")
                with col3:
                    st.markdown(f"**${item_info['price']:.2f}** each")
                with col4:
                    # Quantity editor
                    new_qty = st.number_input(
                        "Qty",
                        min_value=1,
                        max_value=100,
                        value=item['quantity'],
                        key=f"cart_qty_{idx}",
                        label_visibility="collapsed"
                    )
                    # Update quantity if changed
                    if new_qty != item['quantity']:
                        st.session_state.shopping_cart[idx]['quantity'] = new_qty
                        st.rerun()
                    
                    st.caption(f"Total: ${item_price:.2f}")
                with col5:
                    if st.button("🗑️", key=f"remove_{idx}"):
                        items_to_remove.append(idx)
            
            # Remove items marked for deletion
            if items_to_remove:
                for idx in sorted(items_to_remove, reverse=True):
                    st.session_state.shopping_cart.pop(idx)
                st.session_state.cart_items_count = len(st.session_state.shopping_cart)
                st.rerun()
            
            st.markdown("---")
            st.markdown(f"## 💰 Total: ${total_cart_price:.2f}")
            
            # Store total in session state for payment page
            st.session_state.cart_total = total_cart_price
            
            if st.button("🛍️ Proceed to Checkout", type="primary", use_container_width=True):
                st.session_state.payment_page = True
                st.rerun()
        else:
            st.info("🛒 Your cart is empty. Start shopping!")






    
    # ========== PAYMENT PAGE ==========
    else:
        st.markdown("<div class='payment-header'>💳 Payment & Checkout</div>", unsafe_allow_html=True)
        
        if st.button("← Back to Cart"):
            st.session_state.payment_page = False
            st.rerun()




        
        # ===============Customer Details Section========================
        import re
        
        # ==================== Customer Details Section ====================
        st.markdown("## 👤 Customer Details")
        
        with st.container():
            col1, col2 = st.columns(2)
        
            with col1:
                # Full Name
                customer_name = st.text_input("Full Name *", placeholder="Gouthum Kharvi")
                if not customer_name.strip():
                    st.warning("⚠️ Please enter your full name with surname.")
                elif len(customer_name.split()) < 2:
                    st.warning("⚠️ Please include both first and last names.")
        
                # Email Address (restricted to specific domains)
                customer_email = st.text_input("Email Address *", placeholder="example@gmail.com")
                allowed_domains = ["gmail.com", "outlook.com", "proton.me"]
                if not customer_email.strip():
                    st.warning("⚠️ Please enter your email address.")
                elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", customer_email):
                    st.warning("⚠️ Please enter a valid email address.")
                else:
                    domain = customer_email.split("@")[-1]
                    if domain not in allowed_domains and not domain.endswith(".com"):
                        st.warning("⚠️ Please use a valid email (gmail, outlook, proton, or company domain).")
        
                # Phone number (must be exactly 10 digits)
                customer_phone = st.text_input("Phone Number *", placeholder="+91 | Enter 10-digit number")
                phone = re.sub(r'\D', '', customer_phone)  # remove non-digits
                if not phone:
                    st.warning("⚠️ Please enter your phone number.")
                elif len(phone) != 10:
                    st.warning("⚠️ Phone number must be exactly 10 digits (excluding country code).")
        
            with col2:
                # Address
                customer_address = st.text_area("Delivery Address *", placeholder="Main Street, Apt 4B, near Jaydeva Hospital")
                if not customer_address.strip():
                    st.warning("⚠️ Please enter your delivery address.")
        
                # City (custom input)
                customer_city = st.text_input("City *", placeholder="Enter your city")
                if not customer_city.strip():
                    st.warning("⚠️ Please enter your city name.")
        
                # State (searchable dropdown with all Indian states and UTs)
                indian_states = [
                    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
                    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
                    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
                    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
                    "Uttar Pradesh", "Uttarakhand", "West Bengal",
                    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
                    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
                ]
                customer_state = st.selectbox("State *", ["Select your state"] + indian_states, index=0)
                if customer_state == "Select your state":
                    st.warning("⚠️ Please select your state from the list.")
        
                # ZIP Code (exactly 6 digits)
                customer_zip = st.text_input("ZIP Code *", placeholder="574630", max_chars=6)
                zip_digits = re.sub(r'\D', '', customer_zip)
                if not zip_digits:
                    st.warning("⚠️ Please enter your ZIP code.")
                elif len(zip_digits) < 6:
                    st.warning("⚠️ ZIP code must be 6 digits.")
                elif len(zip_digits) > 6:
                    st.warning("⚠️ ZIP code cannot exceed 6 digits.")
        
        st.markdown("---")





        
        
        # ==================Payment Method Selection=================================
        st.markdown("## 💳 Select Payment Method")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💳\nCredit Card", key="credit_card", use_container_width=True):
                st.session_state.selected_payment_method = "credit_card"
            if st.button("💵\nCash on Delivery", key="cod", use_container_width=True):
                st.session_state.selected_payment_method = "cod"
        
        with col2:
            if st.button("🏦\nDebit Card", key="debit_card", use_container_width=True):
                st.session_state.selected_payment_method = "debit_card"
            if st.button("📱\nGoogle Pay", key="gpay", use_container_width=True):
                st.session_state.selected_payment_method = "gpay"
        
        with col3:
            if st.button("💼\nPayPal", key="paypal", use_container_width=True):
                st.session_state.selected_payment_method = "paypal"
            if st.button("📲\nPhonePe", key="phonepe", use_container_width=True):
                st.session_state.selected_payment_method = "phonepe"
        
        st.markdown("---")



        
        # =================✅ ADD WALLET & GIFT CARD PAYMENT BUTTONS updatee5b===================
        col4, col5 = st.columns(2)
        
        with col4:
            wallet_balance = st.session_state.wallet_balance
            wallet_disabled = wallet_balance < st.session_state.cart_total
            button_text = f"👛 Wallet (${wallet_balance:.2f})"
            if wallet_disabled:
                button_text += " - Insufficient"
            
            if st.button(button_text, key="wallet_pay", use_container_width=True, disabled=wallet_disabled):
                st.session_state.selected_payment_method = "wallet"
        
        with col5:
            gift_balance = st.session_state.gift_card_balance
            gift_disabled = gift_balance < st.session_state.cart_total
            button_text = f"🎁 Gift Card (${gift_balance:.2f})"
            if gift_disabled:
                button_text += " - Insufficient"
            
            if st.button(button_text, key="giftcard_pay", use_container_width=True, disabled=gift_disabled):
                st.session_state.selected_payment_method = "gift_card"
        
        st.markdown("---")


        
        # Payment Forms Based on Selection(updatee5b)
        # ==================== PAYMENT FORMS BASED ON SELECTION ====================

        # ==============✅ WALLET PAYMENT==========================
        if st.session_state.selected_payment_method == "wallet":
            st.markdown("### 👛 Wallet Payment")

            # 💳 Add wallet image (fit width, black background)
            st.markdown(
                """
                <div style='background-color:black; padding:10px; border-radius:10px; text-align:center;'>
                    <img src='https://i.pinimg.com/564x/cd/0b/81/cd0b818d8493d4d7368c07f49f4d65f8.jpg' 
                         style='width:10%; height:auto; border-radius:10px;'/>
                </div>
                """, unsafe_allow_html=True
            )
            
            with st.form("wallet_payment_form"):
                st.success(f"✅ Available Balance: ${st.session_state.wallet_balance:.2f}")
                st.info(f"💰 Order Total: ${st.session_state.cart_total:.2f}")
                
                remaining = st.session_state.wallet_balance - st.session_state.cart_total
                st.info(f"💵 Remaining Balance: ${remaining:.2f}")
                
                submit = st.form_submit_button(f"💰 Pay ${st.session_state.cart_total:.2f}", type="primary", use_container_width=True)
                
                if submit:
                    if customer_name and customer_email and customer_phone and customer_address:
                        
                        
                        
                        
                        #=================== Deduct from wallet=========================
                        st.session_state.wallet_balance -= st.session_state.cart_total
                        st.session_state.wallet_transactions.append({
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'type': 'Purchase',
                            'order_id': f"ORD-{st.session_state.order_counter}",
                            'amount': -st.session_state.cart_total,
                            'balance': st.session_state.wallet_balance
                        })
                        
                        customer_details = {
                            'name': customer_name,
                            'email': customer_email,
                            'phone': customer_phone,
                            'address': customer_address,
                            'city': customer_city,
                            'state': customer_state,
                            'zip': customer_zip
                        }
                        save_order(customer_details, 'wallet', st.session_state.shopping_cart, st.session_state.cart_total)
                        
                        st.session_state.shopping_cart = []
                        st.session_state.cart_items_count = 0
                        st.session_state.payment_page = False
                        st.session_state.order_confirmation = True
                        st.rerun()
                    else:
                        st.error("❌ Please fill all required fields!")



        
        
        # =====================✅ GIFT CARD PAYMENT===========================================
        elif st.session_state.selected_payment_method == "gift_card":
            st.markdown("### 🎁 Gift Card Payment")

            # 🎁 Add giftcard image (fit width, black background)
            st.markdown(
                """
                <div style='background-color:black; padding:10px; border-radius:10px; text-align:center;'>
                    <img src='https://media.istockphoto.com/id/2225574507/photo/golden-credit-or-gift-card-with-golden-ribbon.jpg?s=612x612&w=0&k=20&c=dIgcOElMBapEFlNR-7rHmgTXjjFLI0zHBVDYhWErgQo='
                         style='width:40%; height:auto; border-radius:10px;'/>
                </div>
                """, unsafe_allow_html=True
            )

            with st.form("giftcard_payment_form"):
                st.success(f"✅ Available Balance: ${st.session_state.gift_card_balance:.2f}")
                st.info(f"💰 Order Total: ${st.session_state.cart_total:.2f}")
                
                remaining = st.session_state.gift_card_balance - st.session_state.cart_total
                st.info(f"💵 Remaining Balance: ${remaining:.2f}")
                
                submit = st.form_submit_button(f"💰 Pay ${st.session_state.cart_total:.2f}", type="primary", use_container_width=True)
                
                if submit:
                    if customer_name and customer_email and customer_phone and customer_address:




                        
                        #================== Deduct from gift card=========================
                        st.session_state.gift_card_balance -= st.session_state.cart_total
                        st.session_state.gift_card_transactions.append({
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'type': 'Purchase',
                            'order_id': f"ORD-{st.session_state.order_counter}",
                            'amount': -st.session_state.cart_total,
                            'balance': st.session_state.gift_card_balance
                        })
                        
                        customer_details = {
                            'name': customer_name,
                            'email': customer_email,
                            'phone': customer_phone,
                            'address': customer_address,
                            'city': customer_city,
                            'state': customer_state,
                            'zip': customer_zip
                        }
                        save_order(customer_details, 'gift_card', st.session_state.shopping_cart, st.session_state.cart_total)
                        
                        st.session_state.shopping_cart = []
                        st.session_state.cart_items_count = 0
                        st.session_state.payment_page = False
                        st.session_state.order_confirmation = True
                        st.rerun()
                    else:
                        st.error("❌ Please fill all required fields!")




        
        # ==============================✅ CREDIT/DEBIT CARD PAYMENT===============================================
      # ==============================✅ CREDIT/DEBIT CARD PAYMENT===============================================
        elif st.session_state.selected_payment_method == "credit_card" or st.session_state.selected_payment_method == "debit_card":
            import random
            from datetime import datetime
        
            card_type = "Credit" if st.session_state.selected_payment_method == "credit_card" else "Debit"
            st.markdown(f"### 💳 {card_type} Card Payment")
            st.markdown(
                """
                <div style='background-color:white; padding:10px; border-radius:30px; text-align:center;'>
                    <img src='https://t3.ftcdn.net/jpg/05/63/00/96/360_F_563009614_0Pfnd5c4fWwWgAUfhXoQkfOX4XSi78Ba.jpg'/>
                </div>
                """, unsafe_allow_html=True
            )
        
            # ------------------ OTP Session Variables ------------------
            if "otp_sent" not in st.session_state:
                st.session_state.otp_sent = False
            if "otp_verified" not in st.session_state:
                st.session_state.otp_verified = False
            if "generated_otp" not in st.session_state:
                st.session_state.generated_otp = None
        
            with st.form("card_payment_form"):
                card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456", max_chars=19)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    expiry_month = st.text_input("Expiry Month", placeholder="MM", max_chars=2)
                    valid_month = True
                    if expiry_month.strip():
                        if not expiry_month.isdigit():
                            st.warning("⚠️ Please enter a numeric month (01–12).")
                            valid_month = False
                        else:
                            m = int(expiry_month)
                            if m < 1 or m > 12:
                                st.warning("⚠️ Please enter a valid month (1–12).")
                                valid_month = False
        
                with col2:
                    expiry_year = st.text_input("Expiry Year", placeholder="YY", max_chars=2)
                with col3:
                    cvv = st.text_input("CVV", placeholder="123", max_chars=3, type="password")
                
                cardholder_name = st.text_input("Cardholder Name", placeholder="Gouthum Kharvi")
        
                # ------------------ Phone Number & OTP ------------------
                phone_number = st.text_input("Registered Phone Number", placeholder="+91 9876543210")
                otp_button = st.form_submit_button("📲 Get OTP", use_container_width=True)
        
                if otp_button:
                    if phone_number.strip():
                        st.session_state.generated_otp = str(random.randint(100000, 999999))
                        st.session_state.otp_sent = True
                        st.session_state.otp_verified = False
                        st.info(f"✅ OTP sent to {phone_number}")
                        st.caption(f"(For demo, your OTP is **{st.session_state.generated_otp}**)")  # Show OTP for testing
                    else:
                        st.warning("⚠️ Please enter your registered phone number to receive OTP.")
        
                if st.session_state.otp_sent and not st.session_state.otp_verified:
                    otp_input = st.text_input("Enter OTP", placeholder="6-digit OTP", max_chars=6)
                    if otp_input:
                        if not otp_input.isdigit():
                            st.warning("⚠️ OTP must contain only numbers.")
                        elif len(otp_input) < 6:
                            st.warning("⚠️ OTP must be 6 digits.")
                        elif len(otp_input) > 6:
                            st.warning("⚠️ OTP cannot exceed 6 digits.")
        
                    verify_button = st.form_submit_button("🔒 Verify OTP", use_container_width=True)
                    if verify_button:
                        if otp_input == st.session_state.generated_otp:
                            st.session_state.otp_verified = True
                            st.success("✅ OTP verified successfully!")
                        else:
                            st.error("❌ Invalid OTP. Please try again.")
        
                # ------------------ Terms and Conditions ------------------
                agree_terms = st.checkbox("I agree to the Terms & Conditions")
        
                submit = st.form_submit_button(f"💰 Pay ${st.session_state.cart_total:.2f}", type="primary", use_container_width=True)
        
                if submit:
                    if not (customer_name and customer_email and customer_phone and customer_address and card_number and cvv and cardholder_name):
                        st.error("❌ Please fill all required fields!")
                    elif not valid_month:
                        st.error("🚫 Invalid expiry month! Please enter between 1–12.")
                    else:
                        try:
                            exp_month = int(expiry_month)
                            exp_year = int(expiry_year) + 2000  # Convert YY to YYYY
                            current_year = datetime.now().year
                            current_month = datetime.now().month
        
                            # Expiry date validation
                            if exp_month < 1 or exp_month > 12:
                                st.error("🚫 Invalid month! Please enter between 1–12.")
                            elif exp_year < 2025 or (exp_year == 2025 and exp_month < 11):
                                st.error("🚫 Card Declined! Card expired or not valid before November 2025.")
                            elif not st.session_state.otp_verified:
                                st.warning("⚠️ Please verify OTP before proceeding with payment.")
                            elif not agree_terms:
                                st.warning("⚠️ Please accept the Terms & Conditions to continue.")
                            else:
                                # ==============Save order====================
                                customer_details = {
                                    'name': customer_name,
                                    'email': customer_email,
                                    'phone': customer_phone,
                                    'address': customer_address,
                                    'city': customer_city,
                                    'state': customer_state,
                                    'zip': customer_zip
                                }
                                save_order(customer_details, st.session_state.selected_payment_method, st.session_state.shopping_cart, st.session_state.cart_total)
        
                                # ============Clear cart and redirect to confirmation=======================
                                st.session_state.shopping_cart = []
                                st.session_state.cart_items_count = 0
                                st.session_state.payment_page = False
                                st.session_state.order_confirmation = True
                                st.session_state.otp_sent = False
                                st.session_state.otp_verified = False
                                st.session_state.generated_otp = None
                                st.rerun()
                        except ValueError:
                            st.error("⚠️ Please enter valid expiry month and year (MM/YY format).")



        
                
        
        
        
        
        
        # ====================✅ PAYPAL PAYMENT==============================
        # ====================✅ PAYPAL PAYMENT==============================
        elif st.session_state.selected_payment_method == "paypal":
            st.markdown("### 💼 PayPal Payment")
        
            import re
            import random
            from datetime import datetime
        
            # ---------------------- TEMP EMAIL CHECK -------------------------
            temp_email_domains = [
                "mailinator.com", "tempmail.com", "10minutemail.com",
                "throwawaymail.com", "guerrillamail.com", "yopmail.com"
            ]
        
            def is_valid_password(password):
                """Password must be 8–250 chars, with uppercase, lowercase, number, and special character"""
                return (
                    8 < len(password) <= 250
                    and re.search(r"[A-Z]", password)
                    and re.search(r"[a-z]", password)
                    and re.search(r"[0-9]", password)
                    and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
                )
        
            def is_temporary_email(email):
                """Reject temporary email domains"""
                return any(domain in email for domain in temp_email_domains)
        
            # ---------------------- PAYPAL UI -------------------------
            st.markdown(
                f"""
                <div style='
                    text-align: center; 
                    padding: 2rem; 
                    background: black;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(255,255,255,0.2);
                '>
                    <img src="https://static.vecteezy.com/ti/vettori-gratis/t1/20336281-paypal-logo-vettore-paypal-logo-gratuito-vettore-gratuito-vettoriale.jpg"
                         alt="PayPal"
                         style="width: 100%; max-width: 600px; border-radius: 10px; margin-bottom: 1rem;">
                    <h3 style='color: #ffffff;'>PayPal Checkout</h3>
                    <p style='color: #81d4fa;'>Secure Payment Gateway</p>
                    <h2 style='color: #81d4fa;'>${st.session_state.cart_total:.2f}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
        
            # ---------------------- PHONE NUMBER + OTP -------------------------
            if "paypal_otp" not in st.session_state:
                st.session_state.paypal_otp = None
            if "paypal_verified" not in st.session_state:
                st.session_state.paypal_verified = False
        
            paypal_phone = st.text_input("📱 Enter your phone number", placeholder="Enter your registered PayPal phone number")
        
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("📨 Get OTP"):
                    if paypal_phone and paypal_phone.isdigit() and len(paypal_phone) == 10:
                        st.session_state.paypal_otp = random.randint(100000, 999999)
                        st.session_state.paypal_verified = False
                        st.success(f"✅ OTP has been sent successfully to your mobile number ending with {paypal_phone[-2:]}")
                        st.info(f"(For testing only) Your OTP is: {st.session_state.paypal_otp}")
                    else:
                        st.error("❌ Please enter a valid 10-digit phone number")
        
            if st.session_state.paypal_otp:
                entered_otp = st.text_input("🔑 Enter 6-digit OTP", placeholder="Enter the OTP")
        
                if st.button("✅ Verify OTP"):
                    if not entered_otp.isdigit() or len(entered_otp) != 6:
                        st.error("⚠️ OTP must be exactly 6 digits.")
                    elif int(entered_otp) != st.session_state.paypal_otp:
                        st.error("❌ Invalid OTP. Please try again.")
                    else:
                        st.session_state.paypal_verified = True
                        st.success("🎉 OTP verified successfully!")
        
            # ---------------------- AFTER OTP VERIFIED -------------------------
            if st.session_state.paypal_verified:
                with st.form("paypal_form"):
                    paypal_email = st.text_input("📧 PayPal Email", placeholder="your@email.com")
                    paypal_password = st.text_input("🔒 PayPal Password", type="password", placeholder="Enter your PayPal password")
        
                    submit = st.form_submit_button("💰 Pay with PayPal", type="primary", use_container_width=True)
        
                    if submit:
                        if not (customer_name and customer_email and paypal_email and paypal_password):
                            st.error("❌ Please fill all required fields!")
                        elif is_temporary_email(paypal_email):
                            st.warning("⚠️ Temporary email addresses are not allowed. Please use a valid PayPal email.")
                        elif not is_valid_password(paypal_password):
                            st.error(
                                "⚠️ Password must be more than 8 and less than 250 characters, "
                                "and include at least one uppercase, one lowercase, one number, and one special character."
                            )
                        else:
                            customer_details = {
                                'name': customer_name,
                                'email': customer_email,
                                'phone': customer_phone,
                                'address': customer_address,
                                'city': customer_city,
                                'state': customer_state,
                                'zip': customer_zip
                            }
        
                            save_order(
                                customer_details,
                                st.session_state.selected_payment_method,
                                st.session_state.shopping_cart,
                                st.session_state.cart_total
                            )
        
                            st.session_state.shopping_cart = []
                            st.session_state.cart_items_count = 0
                            st.session_state.payment_page = False
                            st.session_state.order_confirmation = True
                            st.success("✅ Payment successful! Redirecting to PayPal confirmation...")
                            st.rerun()


        
        
        
        
        
        # ========================✅ GOOGLE PAY PAYMENT================================
       
        elif st.session_state.selected_payment_method == "gpay":
            st.markdown("### 📱 Google Pay")
        
            with st.form("gpay_form"):
                st.markdown(
                    f"""
                    <div style='
                        text-align: center; 
                        padding: 2rem; 
                        background: black;
                        border-radius: 15px;
                        box-shadow: 0 4px 15px rgba(255,255,255,0.2);
                    '>
                        <img src="https://static0.anpoimages.com/wordpress/wp-content/uploads/2021/02/26/google-pay-logo-2020-hero.png?w=1200&h=628&fit=crop"
                             alt="Google Pay"
                             style="width: 100%; max-width: 800px; border-radius: 30px; margin-bottom: 1rem;">
                        <h3 style='color: #ffffff;'>Google Pay Secure Payment</h3>
                        <p style='color: #90caf9;'>Use UPI ID or mobile number to pay</p>
                        <h2 style='color: #90caf9;'>${st.session_state.cart_total:.2f}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
                # --- UPI ID or Phone ---
                upi_id = st.text_input("Enter Google Pay UPI ID or Phone Number", placeholder="example@okaxis or 9876543210")
        
                # --- Password (6 digits only) ---
                gpay_password = st.text_input("Enter your Google Pay password (6 digits)", type="password", max_chars=6)
        
                if gpay_password and (not gpay_password.isdigit() or len(gpay_password) != 6):
                    st.error("❌ Password must be exactly 6 digits (numbers only).")
        
                # --- Mobile Number ---
                gpay_number = st.text_input("Enter your registered phone number", placeholder="+91", max_chars=13)
        
                # Validate phone number
                phone_clean = gpay_number.replace("+91", "").strip()
                if phone_clean:
                    if not phone_clean.isdigit():
                        st.error("❌ Phone number must contain digits only.")
                    elif len(phone_clean) != 10:
                        st.error("❌ Phone number must be exactly 10 digits.")
        
                # --- OTP Section ---
                if "gpay_otp" not in st.session_state:
                    st.session_state.gpay_otp = None
        
                get_otp = st.form_submit_button("📩 Get OTP")
        
                if get_otp:
                    import random
                    st.session_state.gpay_otp = str(random.randint(100000, 999999))
                    st.success(f"✅ OTP Sent Successfully to your registered phone number (Your OTP is: {st.session_state.gpay_otp})")
        
                entered_otp = st.text_input("Enter OTP (6 digits)", type="password", max_chars=6)
        
                submit_payment = st.form_submit_button("💰 Confirm Payment", type="primary", use_container_width=True)
        
                if submit_payment:
                    if not upi_id:
                        st.error("❌ Please enter UPI ID or Phone number.")
                    elif not gpay_password or not gpay_password.isdigit() or len(gpay_password) != 6:
                        st.error("❌ Invalid password! Must be 6 digits.")
                    elif not phone_clean.isdigit() or len(phone_clean) != 10:
                        st.error("❌ Invalid phone number! Must be 10 digits.")
                    elif not entered_otp or not entered_otp.isdigit() or len(entered_otp) != 6:
                        st.error("❌ Invalid OTP! Must be 6 digits.")
                    elif st.session_state.gpay_otp is None:
                        st.error("❌ Please click 'Get OTP' first.")
                    elif entered_otp != st.session_state.gpay_otp:
                        st.error("❌ Incorrect OTP. Please try again.")
                    else:
                        if customer_name and customer_email:
                            customer_details = {
                                'name': customer_name,
                                'email': customer_email,
                                'phone': customer_phone,
                                'address': customer_address,
                                'city': customer_city,
                                'state': customer_state,
                                'zip': customer_zip
                            }
        
                            save_order(
                                customer_details,
                                st.session_state.selected_payment_method,
                                st.session_state.shopping_cart,
                                st.session_state.cart_total
                            )
        
                            st.session_state.shopping_cart = []
                            st.session_state.cart_items_count = 0
                            st.session_state.payment_page = False
                            st.session_state.order_confirmation = True
                            st.rerun()
                        else:
                            st.error("❌ Please fill all required fields before confirming payment.")


        
        
        
        
        
        # =======================✅ PHONEPE PAYMENT===================================
        elif st.session_state.selected_payment_method == "phonepe":
            st.markdown("### 📲 PhonePe Secure Payment")
        
            with st.form("phonepe_form"):
                st.markdown(
                    f"""
                    <div style='
                        text-align: center; 
                        padding: 2rem; 
                        background: black;
                        border-radius: 15px;
                        box-shadow: 0 4px 15px rgba(255,255,255,0.2);
                    '>
                        <img src="https://mir-s3-cdn-cf.behance.net/projects/808/ecbe29236861555.Y3JvcCwyNzYxLDIxNjAsMzc1LDA.png"
                             alt="PhonePe"
                             style="width: 100%; max-width: 600px; border-radius: 30px; margin-bottom: 1rem;">
                        <h3 style='color: #ffffff;'>PhonePe Secure Payment</h3>
                        <p style='color: #ffcc80;'>Use UPI ID or mobile number to pay</p>
                        <h2 style='color: #ffcc80;'>${st.session_state.cart_total:.2f}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
                # --- UPI ID or Phone ---
                phonepe_upi = st.text_input("Enter PhonePe UPI ID or Phone Number", placeholder="example@ybl or 9876543210")
        
                # --- Password (6 digits only) ---
                phonepe_password = st.text_input("Enter your PhonePe password (6 digits)", type="password", max_chars=6)
                if phonepe_password and (not phonepe_password.isdigit() or len(phonepe_password) != 6):
                    st.error("❌ Password must be exactly 6 digits (numbers only).")
        
                # --- Mobile Number ---
                phonepe_number = st.text_input("Enter your registered phone number", placeholder="+91", max_chars=13)
        
                # Validate phone number
                phone_clean = phonepe_number.replace("+91", "").strip()
                if phone_clean:
                    if not phone_clean.isdigit():
                        st.error("❌ Phone number must contain digits only.")
                    elif len(phone_clean) != 10:
                        st.error("❌ Phone number must be exactly 10 digits.")
        
                # --- OTP Section ---
                if "phonepe_otp" not in st.session_state:
                    st.session_state.phonepe_otp = None
        
                get_otp = st.form_submit_button("📩 Get OTP")
        
                if get_otp:
                    import random
                    st.session_state.phonepe_otp = str(random.randint(100000, 999999))
                    st.success(f"✅ OTP Sent Successfully to your registered phone number (Your OTP is: {st.session_state.phonepe_otp})")
        
                entered_otp = st.text_input("Enter OTP (6 digits)", type="password", max_chars=6)
        
                submit_payment = st.form_submit_button("💰 Confirm Payment", type="primary", use_container_width=True)
        
                if submit_payment:
                    if not phonepe_upi:
                        st.error("❌ Please enter UPI ID or Phone number.")
                    elif not phonepe_password or not phonepe_password.isdigit() or len(phonepe_password) != 6:
                        st.error("❌ Invalid password! Must be 6 digits.")
                    elif not phone_clean.isdigit() or len(phone_clean) != 10:
                        st.error("❌ Invalid phone number! Must be 10 digits.")
                    elif not entered_otp or not entered_otp.isdigit() or len(entered_otp) != 6:
                        st.error("❌ Invalid OTP! Must be 6 digits.")
                    elif st.session_state.phonepe_otp is None:
                        st.error("❌ Please click 'Get OTP' first.")
                    elif entered_otp != st.session_state.phonepe_otp:
                        st.error("❌ Incorrect OTP. Please try again.")
                    else:
                        if customer_name and customer_email:
                            customer_details = {
                                'name': customer_name,
                                'email': customer_email,
                                'phone': customer_phone,
                                'address': customer_address,
                                'city': customer_city,
                                'state': customer_state,
                                'zip': customer_zip
                            }
        
                            save_order(
                                customer_details,
                                st.session_state.selected_payment_method,
                                st.session_state.shopping_cart,
                                st.session_state.cart_total
                            )
        
                            st.session_state.shopping_cart = []
                            st.session_state.cart_items_count = 0
                            st.session_state.payment_page = False
                            st.session_state.order_confirmation = True
                            st.rerun()
                        else:
                            st.error("❌ Please fill all required fields before confirming payment.")


        

        
        
        
        # =====================✅ CASH ON DELIVERY================================
        elif st.session_state.selected_payment_method == "cod":
            st.markdown("### 💵 Cash on Delivery")
        
            with st.form("cod_form"):
                st.markdown(
                    f"""
                    <div style='
                        text-align: center; 
                        padding: 2rem; 
                        background: black;
                        border-radius: 30px;
                        box-shadow: 0 4px 15px rgba(255,255,255,0.2);
                    '>
                        <img src="https://img.freepik.com/premium-photo/delivery-man-holding-cardboard-boxes-isolated-blue-background-courier-service-delivery-banner_926199-1831029.jpg"
                             alt="Cash on Delivery"
                             style="width: 100%; max-width: 500px; border-radius: 30px; margin-bottom: 1rem;">
                        <h3 style='color: #ffffff;'>Pay when you receive</h3>
                        <p style='color: #ffcc80; font-size: 1.4rem;'>
                            Amount to pay: <strong>${st.session_state.cart_total:.2f}</strong>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
                st.info("💡 No advance payment required. Pay cash to delivery partner.")
        
                submit = st.form_submit_button("✅ Confirm Order (COD)", type="primary", use_container_width=True)
        
                if submit:
                    if customer_name and customer_email and customer_address:
                        customer_details = {
                            'name': customer_name,
                            'email': customer_email,
                            'phone': customer_phone,
                            'address': customer_address,
                            'city': customer_city,
                            'state': customer_state,
                            'zip': customer_zip
                        }
                        save_order(
                            customer_details,
                            st.session_state.selected_payment_method,
                            st.session_state.shopping_cart,
                            st.session_state.cart_total
                        )
        
                        st.session_state.shopping_cart = []
                        st.session_state.cart_items_count = 0
                        st.session_state.payment_page = False
                        st.session_state.order_confirmation = True
                        st.rerun()
                    else:
                        st.error("❌ Please fill all delivery details!")

        
                
        
        
        
        
        
        # ====================✅ NO PAYMENT METHOD SELECTED=================================
        else:
            st.info("👆 Please select a payment method above")






# ================Update achievements on every interaction===========================
update_achievements()





# ======================Footer (Black Futuristic + Robot Thinking Animation) — safe from f-string brace errors=============================
st.markdown("---")

html = """
<style>
@keyframes pulseGlow {
    0% { box-shadow: 0 0 10px rgba(102,126,234,0.4), 0 0 20px rgba(102,126,234,0.2); }
    50% { box-shadow: 0 0 25px rgba(102,126,234,0.8), 0 0 50px rgba(102,126,234,0.4); }
    100% { box-shadow: 0 0 10px rgba(102,126,234,0.4), 0 0 20px rgba(102,126,234,0.2); }
}

@keyframes neuralFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes floatBot {
    0% { transform: translateY(0px) rotateY(0deg); }
    50% { transform: translateY(-6px) rotateY(3deg); }
    100% { transform: translateY(0px) rotateY(0deg); }
}

.footer-futuristic {
    text-align: center;
    color: #e0e0e0;
    padding: 2rem;
    border-radius: 25px;
    background: linear-gradient(-45deg, #000000, #0a0a0a, #141414, #1a1a1a);
    background-size: 400% 400%;
    animation: neuralFlow 12s ease infinite, floatBot 6s ease-in-out infinite;
    backdrop-filter: blur(14px);
    perspective: 1000px;
    box-shadow: 0 0 30px rgba(102,126,234,0.2), inset 0 0 20px rgba(255,255,255,0.05);
    transform-style: preserve-3d;
    transition: all 0.5s ease;
    border: 1px solid rgba(102,126,234,0.3);
    position: relative;
    overflow: hidden;
}

/* Glowing circuit pulse (AI brain waves) */
.footer-futuristic::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(102,126,234,0.15), transparent 70%);
    animation: pulseGlow 5s infinite;
    z-index: 0;
    pointer-events: none;
}

.footer-futuristic h3 {
    color: #8ab4f8;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 2;
}

.footer-futuristic p {
    margin: 0.3rem 0;
    position: relative;
    z-index: 2;
}

.footer-futuristic hr {
    width: 60%;
    margin: 1rem auto;
    border: 0;
    border-top: 1px solid rgba(255,255,255,0.2);
    position: relative;
    z-index: 2;
}

.highlight {
    color: #ffda79;
    font-weight: bold;
    text-shadow: 0 0 8px rgba(255,218,121,0.6);
}

.footer-bot {
    font-size: 2rem;
    animation: floatBot 4s ease-in-out infinite;
    display: inline-block;
    transform-origin: center;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 2;
}
</style>

<div class="footer-futuristic">
    <div class="footer-bot">🤖</div>
    <h3>Powered by Advanced AI Technology</h3>
    <p><strong>👨‍💻 Developer: Gouthum Kharvi</strong> </p>
    <p><strong>🔗 Stack:</strong> LangChain, RAG + CrewAI Multi-Agent System</p>
    <p><strong> Database:</strong> 231,637 Recipes | ChromaDB Vector Store</p>
    <p><strong>🤖 Current Model:</strong> {SELECTED_MODEL}</p>
    <hr>
    <p style='font-size:0.9rem;'>© 2025 AI Recipe Assistant | Version 3.0 Enhanced</p>
</div>
"""

# ======= Safely inject the model name without using f-strings or .format (which would interpret braces)====================

html = html.replace("{SELECTED_MODEL}", str(selected_model))

st.markdown(html, unsafe_allow_html=True)