
from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langchain_core.messages import HumanMessage



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


# Create specialized logistics planning agent
logistics_agent = create_agent(
    model=model,
    system_prompt="""You are a travel logistics expert. You handle practical travel planning:
    - Calculate distances between locations and travel times
    - Estimate costs for transportation, accommodation, and activities
    - Optimize routes and suggest efficient itineraries
    - Consider time zones, weather, and practical constraints
    Always provide short, clear, practical logistics information."""
)

# Create specialized recommendations agent
recommendations_agent = create_agent(
    model=model,
    system_prompt="""You are a travel recommendations specialist. You suggest experiences and activities:
    - Recommend top attractions, landmarks, and must-see places
    - Suggest restaurants, local cuisine, and dining experiences
    - Recommend cultural activities, events, and local experiences
    - Provide insights about local customs, best times to visit, and hidden gems
    Always provide brief, engaging, personalized recommendations."""
)





@tool
def plan_logistics_agent(trip_request: str) -> str:
    """
    Plan travel logistics including distances, times, costs, and routes.
    Use this to calculate practical travel information and optimize itineraries.
    
    Args:
        trip_request: Trip details (e.g., "3 days in Paris, budget $1500, from London")
    
    Returns:
        Logistics information: distances, travel times, costs, and route suggestions
    """
    response = logistics_agent.invoke({"messages": [HumanMessage(f"Plan logistics for this trip: {trip_request}")]})
    return response["messages"][-1].content

@tool
def get_recommendations_agent(trip_details: str) -> str:
    """
    Get travel recommendations for attractions, restaurants, and activities.
    Use this to suggest what to see, do, and eat at the destination.
    
    Args:
        trip_details: Destination and trip information (e.g., "3 days in Paris, interested in art and food")
    
    Returns:
        Recommendations for attractions, restaurants, activities, and cultural insights
    """
    response = recommendations_agent.invoke({"messages": [HumanMessage(f"Provide recommendations for: {trip_details}")]})
    return response["messages"][-1].content

