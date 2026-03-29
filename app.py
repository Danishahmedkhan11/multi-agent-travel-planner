import streamlit as st
import os
import sys
import importlib.util
from dotenv import load_dotenv

# Set page config
st.set_page_config(
    page_title="VoyageAI: Smart Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Function to dynamically load Multi-agents.py without its side effects
@st.cache_resource
def load_travel_module():
    module_name = "multi_agents_logic"
    file_path = "Multi-agents.py"
    
    if not os.path.exists(file_path):
        st.error(f"Error: {file_path} not found.")
        return None

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    
    # Read the file and execute only the definitions
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
        # We find the line where the hardcoded execution starts
        # and only execute everything before that.
        cutoff = len(lines)
        for i, line in enumerate(lines):
            # Look for the start of the sample execution
            if 'questions = "' in line or 'print("Final Travel Plan:")' in line:
                cutoff = i
                break
        
        relevant_code = "".join(lines[:cutoff])
        
        # Add the directory of the file to sys.path so it can find Tool_agents.py
        sys.path.insert(0, os.getcwd())
        
        try:
            exec(relevant_code, module.__dict__)
        except Exception as e:
            st.error(f"Error loading logic: {e}")
            return None
            
    return module

# Load the logic module
logic = load_travel_module()

# App Header
st.title("🌍 VoyageAI: Smart Travel Planner")
st.markdown("""
Welcome to the **AI Travel Planning Assistant**! 
This app uses a team of specialized agents to plan your perfect trip:
- 🛠️ **Logistics Specialist**: Handles distances, times, and costs.
- 🎨 **Recommendation Specialist**: Suggests attractions, dining, and activities.
""")

# Check for API Keys
if not os.getenv("OPENROUTER_API_KEY"):
    st.warning("⚠️ OPENROUTER_API_KEY not found in .env. Please configure it to proceed.")

# Main Form
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        destination = st.text_input("📍 Where are you going?", placeholder="e.g. Paris, Tokyo, Bali")
        origin = st.text_input("🛫 Departing from?", placeholder="e.g. London, New York")
        duration = st.number_input("📅 Duration (Days)", min_value=1, max_value=30, value=3)
        
    with col2:
        budget = st.text_input("💰 Total Budget ($)", placeholder="e.g. 1500")
        travelers = st.selectbox("👥 Travelers", ["Solo", "Couple", "Family", "Friends"])
        interests = st.multiselect(
            "🎨 Interests",
            ["Art", "Food", "History", "Nature", "Adventure", "Shopping", "Relaxation", "Nightlife"],
            default=["Art", "Food"]
        )

    additional_info = st.text_area("✍️ Any other preferences?", placeholder="e.g. Vegetarian food only, flying only, luxury hotels...")

    if st.button("🚀 Generate My Travel Plan", type="primary"):
        if not destination:
            st.error("Please provide a destination!")
        elif not logic:
            st.error("Could not load the travel planning logic.")
        else:
            # Construct the prompt
            interest_str = ", ".join(interests) if interests else "various activities"
            prompt = f"Plan a {duration}-day trip to {destination} for a {travelers.lower()} with a budget of ${budget}, departing from {origin}. They are interested in {interest_str}. {additional_info}"
            
            # Show progress
            with st.status("🤖 Agents are working on your plan...", expanded=True) as status:
                st.write("Initializing session...")
                session_id = logic.generate_session_id()
                st.write(f"Session ID: `{session_id}`")
                
                st.write("Coordinating specialists...")
                try:
                    # Access logic.model and logic.run_llm_call
                    response = logic.run_llm_call(session_id, logic.model, prompt)
                    
                    status.update(label="✅ Travel Plan Complete!", state="complete", expanded=False)
                    
                    st.divider()
                    st.subheader(f"✨ Your {duration}-Day Trip to {destination}")
                    st.markdown(response)
                    
                    # Flush Langfuse if it exists in the module
                    if hasattr(logic, "langfuse_client"):
                        logic.langfuse_client.flush()
                        st.info("📊 Interaction logged to Langfuse.")
                        
                except Exception as e:
                    status.update(label="❌ Error generating plan", state="error")
                    st.error(f"An error occurred: {e}")

# Footer
st.divider()
st.caption("Powered by Multi-Agent Orchestration | LangChain | OpenRouter")
