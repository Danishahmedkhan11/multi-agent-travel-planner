import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from Tool_agents import plan_logistics_agent, get_recommendations_agent
import ulid
from langfuse import Langfuse, observe, propagate_attributes
from langfuse.langchain import CallbackHandler


# Load environment variables from .env file
load_dotenv()

# Configure OpenRouter model
model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=1000,
)

# print(f"✓ Model configured: {model}")



# Initialize Langfuse client
langfuse_client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

print("✓ Langfuse initialized successfully")
if langfuse_client:
    print(f"✓ Langfuse client info: {langfuse_client}")
else:
    print("✗ Warning: Langfuse client initialization may have failed")


def generate_session_id():
    """Generate a unique session ID using TEAM_NAME and ULID."""
    return f"{os.getenv('TEAM_NAME', 'tutorial')}-{ulid.new().str}"



@observe()
def run_llm_call(session_id, model, prompt):
    """Run a single LangChain invocation and track it in Langfuse."""
    # Propagate session_id to all spans in this context
    with propagate_attributes(session_id=session_id):
        # Create Langfuse callback handler for automatic generation tracking
        # The handler will attach to the current trace created by @observe()
        langfuse_handler = CallbackHandler()


        orchestrator = create_agent(
            model=model,
            system_prompt="""You are a travel planning coordinator. 
            When planning trips, use both specialists:
            1. Use plan_logistics_agent to calculate practical details: distances, times, costs, and routes
            2. Use get_recommendations_agent to suggest attractions, restaurants, and activities
            Always combine both the practical logistics and exciting recommendations in your final response.""",
            tools=[plan_logistics_agent, get_recommendations_agent]
        )
        

        # Invoke LangChain with Langfuse handler to track tokens and costs
        request = {"messages": [HumanMessage(content=prompt)]}

        # Get combined logistics and recommendations
        final_plan = orchestrator.invoke(request, config={"callbacks": [langfuse_handler]})

        if isinstance(final_plan, dict):
            if "messages" in final_plan and isinstance(final_plan["messages"], list):
                return final_plan["messages"][-1].content
            return str(final_plan)

        # Fallback for non-dict responses
        return getattr(final_plan, "content", str(final_plan))


print("✓ Langfuse initialized successfully")
print(f"✓ Public key: {os.getenv('LANGFUSE_PUBLIC_KEY', 'Not set')[:20]}...")
print("✓ Helper functions ready: generate_session_id(), invoke_langchain(), run_llm_call()")

# questions = "Plan a 3-day trip to Paris for a couple with a budget of $1500, departing from London. They are interested in art and food."
session_id = generate_session_id()
print(f"Session ID: {session_id}")

print("Final Travel Plan:")


response = run_llm_call(session_id, model, questions)
print(response)

langfuse_client.flush()

print("=" * 50)
print(f"✓ All {len(questions)} traces sent to Langfuse!")
print(f"✓ All grouped under session: {session_id}")
print("✓ You can inspect this session using get_trace_info(session_id) and print_results(info) below.")


