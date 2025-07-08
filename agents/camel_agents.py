from camel.models import ModelFactory
from camel.types import ModelType, ModelPlatformType
from camel.configs import MistralConfig
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.toolkits.search_toolkit import SearchToolkit
from agents.prompts import student_prompt, teacher_prompt, validator_prompt

# Initialize Mistral model
mistral_model = ModelFactory.create(
    model_platform=ModelPlatformType.MISTRAL,
    model_type=ModelType.MISTRAL_LARGE,
    model_config_dict=MistralConfig(temperature=0.7).as_dict(),
)

# Get all tools and filter to safe ones
all_tools = SearchToolkit().get_tools()
safe_tool_names = ["search_khan_academy", "search_youtube", "search_google"]

# Safe filtering based on .name attribute
safe_tools = [tool for tool in all_tools if hasattr(tool, "name") and tool.name in safe_tool_names]

def create_agent(system_prompt):
    return ChatAgent(
        system_message=system_prompt,
        message_window_size=10,
        model=mistral_model,
        tools=safe_tools
    )

def run_student_agent(topic):
    student = create_agent(student_prompt.format(topic=topic))
    msg = BaseMessage.make_user_message("Student", f"What is {topic}?")
    return student.step(msg).msg.content

def run_teacher_agent(question):
    teacher = create_agent(teacher_prompt)
    msg = BaseMessage.make_user_message("Student", question)
    return teacher.step(msg).msg.content

def run_validator_agent(explanation):
    validator = create_agent(validator_prompt)
    msg = BaseMessage.make_user_message("Teacher", explanation)
    return validator.step(msg).msg.content

