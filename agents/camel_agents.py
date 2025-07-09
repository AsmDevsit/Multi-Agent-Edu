from camel.models import ModelFactory
from camel.types import ModelType, ModelPlatformType
from camel.configs import MistralConfig
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from agents.prompts import student_prompt, teacher_prompt, validator_prompt

# Initialize Mistral model
mistral_model = ModelFactory.create(
    model_platform=ModelPlatformType.MISTRAL,
    model_type=ModelType.MISTRAL_LARGE,
    model_config_dict=MistralConfig(temperature=0.7).as_dict(),
)

def create_agent(system_prompt):
    return ChatAgent(
        system_message=BaseMessage(
            role_name="system",
            role_type="system",
            content=system_prompt,
            meta_dict={},
        ),
        model=mistral_model,
    )

def run_student_agent(topic):
    student = create_agent(student_prompt.format(topic=topic))
    msg = BaseMessage(
        role_name="user",
        role_type="user",
        content=f"What is {topic}?",
        meta_dict={},
    )
    return student.step(msg).msg.content

def run_teacher_agent(question):
    teacher = create_agent(teacher_prompt)
    msg = BaseMessage(
        role_name="user",
        role_type="user",
        content=question,
        meta_dict={},
    )
    return teacher.step(msg).msg.content

def run_validator_agent(explanation):
    validator = create_agent(validator_prompt)
    msg = BaseMessage(
        role_name="user",
        role_type="user",
        content=explanation,
        meta_dict={},
    )
    return validator.step(msg).msg.content
