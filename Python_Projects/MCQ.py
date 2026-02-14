quiz = {
    "What is the output of print(2 ** 3)?": "8",
    "Which keyword is used to define a function in Python?": "def",
    "Which data type is used to store True/False?": "bool",
    "What does len() do?": "length"
}

score = 0

print("\n🧠 Python Quiz Started!\n")

for question, answer in quiz.items():
    user_answer = input(question + " ").strip().lower()
    if user_answer == answer:
        print("✅ Correct!\n")
        score += 1
    else:
        print(f"❌ Wrong! Correct answer is: {answer}\n")

print(f"🏁 Quiz Finished! Your Score: {score}/{len(quiz)}")
