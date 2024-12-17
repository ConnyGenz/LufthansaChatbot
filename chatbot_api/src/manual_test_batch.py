import dotenv
dotenv.load_dotenv()
from chatbot_api.src.agents.lufthansa_rag_agent import lufthansa_qa_agent_executor

list_of_questions = []
list_of_answers = []

# Document with questions to be asked. To be provided by user.
file_path = "neue_Fragen_Dez_2024.txt"

# Read question file and create list of strings
with open(file_path, 'r', encoding="utf-8") as file:
    lines = file.readlines()

# Remove linebreak at the end of question strings and write to question list
for line in lines:
    line_wo_linebreak = line.strip()
    list_of_questions.append(line_wo_linebreak)

print("These are the questions:")
print(list_of_questions)

# Call agent to answer the questions
for question in list_of_questions:
    result = lufthansa_qa_agent_executor.invoke({"input": question})
    response = result["output"]
    list_of_answers.append(response)

# Write answers to a file
counter = 1
with open('answers.txt', 'w', encoding="utf-8") as f:
    for answer in list_of_answers:
        f.write("Antwort" + str(counter) + "\n")
        f.write(f"{answer}\n\n")
        counter += 1

print("These are the answers:")
print(list_of_answers)
print("The answers will also be printed to 'answers.txt'.")

