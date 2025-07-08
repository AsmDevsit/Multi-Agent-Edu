from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from agents.camel_agents import run_student_agent, run_teacher_agent, run_validator_agent

# State schema
state = {
    "input": str,
    "steps": int,
    "turn": int,
    "result": list,
}

# Step: Student Agent asks a question
def student_step(state):
    topic = state["input"]
    question = run_student_agent(topic)
    return {
        "input": topic,
        "turn": state["turn"],
        "steps": state["steps"],
        "student_question": question,
        "result": state["result"],
    }

# Step: Teacher Agent responds
def teacher_step(state):
    answer = run_teacher_agent(state["student_question"])
    return {
        **state,
        "teacher_response": answer,
    }

# Step: Validator Agent checks the answer
def validator_step(state):
    feedback = run_validator_agent(state["teacher_response"])
    updated_result = state.get("result", [])
    updated_result.append({
        "student_question": state["student_question"],
        "teacher_response": state["teacher_response"],
        "student_follow_up": state["student_question"],  # Placeholder follow-up
        "validator_feedback": feedback,
    })
    return {
        "input": state["input"],
        "turn": state["turn"] + 1,
        "steps": state["steps"],
        "result": updated_result,
    }

# Condition to stop after 3 steps
def should_continue(state):
    return state["turn"] < state["steps"]

# Build LangGraph
builder = StateGraph(state)

builder.add_node("student", student_step)
builder.add_node("teacher", teacher_step)
builder.add_node("validator", validator_step)

builder.set_entry_point("student")
builder.add_edge("student", "teacher")
builder.add_edge("teacher", "validator")
builder.add_conditional_edges("validator", should_continue, {
    True: "student",
    False: END,
})

graph = builder.compile()

def run_learning_session(topic):
    inputs = {
        "input": topic,
        "steps": 3,
        "turn": 0,
        "result": [],
    }
    final_state = graph.invoke(inputs)
    return final_state["result"]

