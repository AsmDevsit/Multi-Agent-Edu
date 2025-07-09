from agents.camel_agents import run_student_agent, run_teacher_agent, run_validator_agent

def run_learning_session(topic, steps=3):
    result = []
    for turn in range(steps):
        student_question = run_student_agent(topic)
        teacher_response = run_teacher_agent(student_question)
        student_follow_up = run_student_agent(teacher_response)
        validator_feedback = run_validator_agent(teacher_response)

        result.append({
            "student_question": student_question,
            "teacher_response": teacher_response,
            "student_follow_up": student_follow_up,
            "validator_feedback": validator_feedback,
        })

    return result
