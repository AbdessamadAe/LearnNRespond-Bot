from ast import List, main
import json
from difflib import get_close_matches
from pickle import NONE

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question, questions: list[str]) -> str | None:
    matches: List = get_close_matches(user_question, questions,n=1, cutoff=0.7)
    return matches[0] if matches else None

def get_answer(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        
def chat_bot():
    knowledge_base: dict  = load_knowledge_base("knowledge_base.json")
    try:
        while True:
            user_input: str = input("You:").lower()
            if user_input =='quit':
                break
            best_match: str | None = find_best_match(user_input, [q['question'] for q in knowledge_base['questions']])
            if best_match:
                answer: str = get_answer(best_match, knowledge_base)
                print(f'Bot: {answer}')
            else:
                print('Bot: I don\'t know the answer. Can you teach me?')
                new_answer: str = input('Type the answer or "skip" to skip: ')
                if new_answer!='skip':
                    knowledge_base['questions'].append({'question': user_input, 'answer': new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print('Bot: Thank you!')
    except KeyboardInterrupt:
        print("\nChatbot session ended.")

if __name__ == '__main__':
    chat_bot()