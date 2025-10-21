from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


class AgentState(BaseModel):
    """State of the soil agent."""
    messages: list = [] 
    response: str = ""
    category: str = ""   
    soil_data: dict = {} 


class Category(BaseModel):
    """Category used for routing."""
    category: str


def create_llm_msg(system_prompt, history):
    """Convert chat history into structured LLM messages."""
    resp = [SystemMessage(content=system_prompt)]
    for m in history:
        if m["role"] == "user":
            resp.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            resp.append(AIMessage(content=m["content"]))
    return resp


class ChatbotAgent:
    """Soil analysis chatbot agent."""

    def __init__(self, api_key: str):
        self.model = ChatOpenAI(model_name="gpt-5-nano", openai_api_key=api_key)

        workflow = StateGraph(AgentState)
        workflow.add_node("classifier", self.classifier)
        workflow.add_node("soil_agent", self.soil_agent)
        workflow.add_node("general_agent", self.general_agent)

        workflow.add_edge(START, "classifier")
        workflow.add_conditional_edges("classifier", self.main_router)
        workflow.add_edge("soil_agent", END)
        workflow.add_edge("general_agent", END)

        self.graph = workflow.compile()

    def classifier(self, state: AgentState):
        """Classify query as soil-related or general."""
        CLASSIFIER_PROMPT = """
        You are a classifier that decides whether the user's message is about SOIL or GENERAL topics.
        If the user mentions soil, crops, nutrients, moisture, or fertilizers — classify as "soil_agent".
        Otherwise classify as "general_agent".
        """
        llm_messages = create_llm_msg(CLASSIFIER_PROMPT, state.messages)
        llm_response = self.model.with_structured_output(Category).invoke(llm_messages)
        category = llm_response.category.strip().lower()
        print(f"Classified category: {category}")
        return {"category": category}

    def main_router(self, state: AgentState):
        """Route to the correct agent."""
        if state.category == "soil_agent":
            return "soil_agent"
        return "general_agent"

    def soil_agent(self, state: AgentState):
        SOIL_PROMPT = """
        You are a smart soil compatibility assistant.

        Given soil data (N, P, K, pH, humidity, temperature, region) and a crop name,
        determine:
        1. Soil suitability for that crop (0–100%).
        2. Which nutrients are deficient or excessive.
        3. How to improve soil health and crop yield.
        4. If possible, suggest alternative crops better suited to that soil.

        Be concise but specific, and use an expert yet friendly tone.
        """
        llm_messages = create_llm_msg(SOIL_PROMPT, state.messages)
        return {"response": self.model.stream(llm_messages), "category": "soil_agent"}

    def general_agent(self, state: AgentState):
        """Fallback for non-soil conversations."""
        GENERAL_PROMPT = """
        You are a helpful assistant for general agricultural questions.
        Respond clearly and supportively to the user’s query.
        """
        llm_messages = create_llm_msg(GENERAL_PROMPT, state.messages)
        return {"response": self.model.stream(llm_messages), "category": "general_agent"}
