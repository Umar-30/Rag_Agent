import streamlit as st
import requests
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="RAG Insight Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE OFFICIAL UNIFIED UI (CSS) ---
st.markdown("""
    <style>
    /* Global Reset & Pure Black Background */
    .stApp, .stMain, .stBottom, [data-testid="stMainBlockContainer"], [data-testid="stBottomBlockContainer"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* Remove all default borders and shadows */
    .st-emotion-cache-4rsbii, .st-emotion-cache-liupih, .st-emotion-cache-1p2n2i4, .st-emotion-cache-128upt6 {
        background-color: #000000 !important;
        border: none !important;
        box-shadow: none !important;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
    }

    .block-container {
        max-width: 1000px !important;
        padding-top: 2rem !important;
        margin: auto;
    }

    /* THE UNIFIED AI CARD - STITCHING LOGIC */
    .hero-unit {
        background-color: #050505;
        border: 2px solid #58A6FF; /* Unified Glow Border */
        border-bottom: none; /* Open bottom to merge */
        border-radius: 24px 24px 0 0;
        padding: 5rem 2rem 1.5rem 2rem;
        text-align: center;
        margin: 2rem auto 0 auto;
        max-width: 850px !important;
        box-shadow: 0 -10px 40px rgba(59, 130, 246, 0.1);
    }

    /* Target the Chat Input to physically merge with the div above */
    [data-testid="stChatInput"] {
        position: relative !important;
        background-color: #050505 !important;
        border: 2px solid #58A6FF !important;
        border-top: none !important; /* Open top to merge */
        border-radius: 0 0 24px 24px !important;
        padding: 0 3rem 4rem 3rem !important;
        margin: 0 auto !important; /* Center match */
        max-width: 850px !important; /* Width match */
        bottom: auto !important;
        z-index: 10;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.9);
    }

    /* Target all internal wrappers from your HTML snippet */
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] div[class*="st-emotion-cache"] {
        background-color: transparent !important;
        border: none !important;
    }

    /* Remove the 'invisible gap' between Streamlit elements */
    [data-testid="stVerticalBlock"] > div:has(div.hero-unit) + div {
        margin-top: -1px !important;
    }

    /* THE TEXTAREA - ABSOLUTE BLACK */
    [data-testid="stChatInputTextArea"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        caret-color: #FFFFFF !important;
        border: 1px solid #374151 !important;
        border-radius: 12px !important;
    }

    /* THE SUBMIT BUTTON */
    [data-testid="stChatInputSubmitButton"] {
        background-color: #58A6FF !important;
        border-radius: 50% !important;
    }
    
    [data-testid="stChatInputSubmitButton"] svg {
        color: #000000 !important;
    }

    /* TYPOGRAPHY */
    .main-header {
        font-size: 3.5rem;
        font-weight: 900;
        color: #58A6FF;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #8B949E;
        margin-bottom: 0;
    }

    /* CHAT MESSAGES */
    [data-testid="stChatMessage"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        margin-top: 1rem;
    }
    
    [data-testid="stChatMessage"] * {
        color: #FFFFFF !important;
    }

    /* SIDEBAR - PURE BLACK */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #30363D;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebarCollapse"] svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* BUTTONS */
    .stButton>button {
        background-color: #21262D;
        color: #FFFFFF;
        border: 1px solid #30363D;
        border-radius: 8px;
        font-weight: 600;
        height: 3em;
    }
    
    .stButton>button:hover {
        border-color: #58A6FF;
    }

    .stChatInputContainer {
        position: static !important;
        background-color: transparent !important;
        padding: 0 !important;
    }

    /* MOBILE RESPONSIVE */
    @media (max-width: 768px) {
        .main-header { font-size: 2rem; }
        .sub-header { font-size: 1rem; }
        .hero-unit, [data-testid="stChatInput"] { max-width: 95% !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MAIN UI STRUCTURE ---
st.markdown("""
    <div class="hero-unit">
        <h1 class="main-header">🧠 RAG Insight</h1>
        <p class="sub-header">Professional Enterprise AI Document Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar for Controls and Knowledge Base
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("Knowledge Hub")
    
    st.markdown("""
    <div class="info-card">
        <strong>Engine:</strong> Cohere Command-R<br>
        <strong>Vector DB:</strong> Qdrant<br>
        <strong>RAG Protocol:</strong> Enabled
    </div>
    """, unsafe_allow_html=True)

    # Document Topic Section
    st.subheader("📄 Current Context")
    st.markdown("""
    <div style="background-color: #21262D; padding: 10px; border-radius: 8px; border-left: 4px solid #58A6FF; margin-bottom: 15px;">
        <span style="font-size: 0.9rem; color: #E0E0E0;">
            <strong>Topic:</strong> General Knowledge / Document Analysis<br>
            <strong>Source:</strong> sample.pdf
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📁 Document Management")
    
    # Pre-requisite Note
    st.warning("⚠️ **Note:** Please 'Initialize' before asking questions to process the document embeddings.")

    if st.button("Initialize Knowledge Base"):
        with st.spinner("Processing document embeddings..."):
            try:
                # Adding a small delay for UI feel
                time.sleep(1) 
                response = requests.post("http://localhost:8000/ingest")
                if response.status_code == 200:
                    st.success("✅ System ready! Document indexed.")
                else:
                    st.error(f"❌ Initialization failed: {response.text}")
            except Exception as e:
                st.error(f"⚠️ Connection error: {e}")

    st.divider()
    
    with st.expander("🔍 How it works"):
        st.write("""
        1. **Context Ingestion:** Documents are parsed and converted into high-dimensional vectors.
        2. **Neural Search:** Your questions are compared against the document database to find relevant matches.
        3. **Guided Synthesis:** The AI generates an answer restricted solely to the retrieved context for maximum accuracy.
        """)

# Chat Interface Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history with custom styling
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Interaction
if prompt := st.chat_input("Ask a question about your documents..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Analyzing knowledge base..."):
            try:
                response = requests.post(
                    "http://localhost:8000/query",
                    json={"question": prompt}
                )
                if response.status_code == 200:
                    answer = response.json().get("answer", "I couldn't find a relevant answer in the provided documents.")
                    
                    # Simulate typing effect for a better feel
                    full_response = ""
                    for chunk in answer.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error("The backend service is currently unreachable.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# Footer
st.markdown("---")
st.caption("Powered by Cohere and Qdrant • Developed for RAG Insights")
