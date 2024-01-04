

def verify_professor_identity(equation, correct_answer):
    # Prompt the professor to solve the equation
    answer = int(input(f"Please solve the following equation to verify your identity:\n{equation}\nAnswer: "))
    # Check the answer
    return answer == correct_answer