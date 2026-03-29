# ✈️ VoyageAI: Smart Multi-Agent Travel Planner

VoyageAI is an advanced travel planning system powered by **LangChain** and **OpenRouter (GPT-4o-mini)**. It uses a multi-agent orchestration strategy to provide comprehensive, personalized travel itineraries.

## 🤖 How It Works
The system employs a "Coordinator" agent that delegates tasks to two specialized AI experts:
1.  **🛠️ Logistics Specialist**: Calculates distances, travel times, estimated costs (transport/accommodation), and optimizes routes.
2.  **🎨 Recommendation Specialist**: Suggests top attractions, local hidden gems, dining experiences, and cultural insights.

The final output is a seamless blend of practical logistics and exciting activities tailored to your specific budget and interests.

---

## 🚀 Getting Started

### 1. Prerequisites
*   Python 3.9+
*   An [OpenRouter API Key](https://openrouter.ai/)
*   (Optional) [Langfuse](https://langfuse.com/) credentials for tracing and monitoring.

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone <your-github-repo-url>
cd Multi-agents
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and add your keys:
```env
OPENROUTER_API_KEY=your_key_here
TEAM_NAME=your_team_name
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 4. Running the App
Launch the interactive Web UI:
```bash
streamlit run app.py
```

---

## 📂 Project Structure

### 🧠 `Multi-agents.py` (The Brain)
This is the core logic of the application. It handles:
*   **Orchestration**: Creates the high-level "Travel Coordinator" agent that understands user requests and decides when to call specific specialists.
*   **LLM Configuration**: Sets up the OpenRouter integration (GPT-4o-mini) with custom temperature and token limits.
*   **Session Management**: Generates unique ULID-based session IDs to group all agent interactions for a single trip.
*   **Observability**: Integrated with **Langfuse** using the `@observe()` decorator and `CallbackHandler` to provide deep traces of every decision the AI makes, including cost and latency tracking.

### 🛠️ `Tool_agents.py` (The Specialists)
Contains the specific definitions and system prompts for the **Logistics** and **Recommendations** agents. These are exposed as "Tools" that the main coordinator can call upon.

### 🎨 `app.py` (The Interface)
A Streamlit-based Web UI (VoyageAI) that provides a user-friendly way to interact with the agents. It dynamically loads the logic from `Multi-agents.py` without triggering its hardcoded test scripts.

### 📋 `requirements.txt`
Lists all necessary Python libraries for both local development and cloud deployment.

---

## 📊 Monitoring
This project is integrated with **Langfuse**. Every travel plan generated is logged with a unique ULID session ID, allowing you to track token usage, costs, and agent reasoning steps in real-time.

---
*Built with ❤️ using LangChain, Streamlit, and OpenRouter.*
