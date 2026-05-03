def generate_quiz(topic: str):

    topic = topic.lower()

    quiz_db = {

        "percentages": [
            {
                "question": "What is 20% of 150?",
                "answer": "30"
            },
            {
                "question": "45 is what percent of 90?",
                "answer": "50"
            },
            {
                "question": "Price increases from 200 to 250. What is percentage increase?",
                "answer": "25"
            }
        ],

        "probability": [
            {
                "question": "Probability of getting heads when tossing a coin?",
                "answer": "0.5"
            },
            {
                "question": "Probability of rolling a 3 on a die?",
                "answer": "1/6"
            }
        ]

    }

    if topic not in quiz_db:
        return f"No quiz available for {topic}"

    questions = quiz_db[topic]

    quiz_text = ""

    for i, q in enumerate(questions):

        quiz_text += f"\nQuestion {i+1}\n{q['question']}\n"

    return quiz_text