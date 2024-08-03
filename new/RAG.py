import random
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd

# Load model and tokenizer
model_name = "EleutherAI/gpt-neo-2.7B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load data from CSV with appropriate encoding
dataset_path = '/home/peicichen112/老公/RAG/project/document/dataset.csv'
menu_path = '/home/peicichen112/老公/RAG/project/document/menu.csv'

for encoding in ['utf-8', 'latin1', 'ISO-8859-1']:
    try:
        df = pd.read_csv(dataset_path, encoding=encoding)
        menu_df = pd.read_csv(menu_path, encoding=encoding)
        break
    except UnicodeDecodeError:
        continue

# Convert data to dictionary
symptom_data = df.set_index('Name')[['description', 'reason']].to_dict('index')
menu_data = menu_df.set_index('kind')['food'].to_dict()

def generate_response(prompt, symptom_data, menu_data):
    # Check if prompt contains a symptom from the dataset
    for symptom, data in symptom_data.items():
        if symptom.lower() in prompt.lower():
            food_options = data['description'].split(', ')
            chosen_food = random.choice(food_options)
            
            # Check for matching kind in menu data
            for kind, foods in menu_data.items():
                if kind in chosen_food.lower():
                    food_list = foods.split(', ')
                    chosen_food = random.choice(food_list)
                    break
            
            explanation = data['reason']
            return {
                "food": f"Today, you might want to eat some {chosen_food}.",
                "explanation": f"{explanation}"
            }
    
    # If no symptom is detected, treat it as a general query
    for kind, foods in menu_data.items():
        if kind in prompt.lower():
            food_list = foods.split(', ')
            chosen_food = random.choice(food_list)
            return f"Today I want to eat {chosen_food}."
    
    # If no matching kind is found, choose a random food from all options
    all_foods = [food for foods in menu_data.values() for food in foods.split(', ')]
    chosen_food = random.choice(all_foods)
    return f"Today I want to eat {chosen_food}."

# Test the function with different prompts
prompt = "Today someone with diabetes wants to eat some food. Do you have any recommendations?"
response = generate_response(prompt, symptom_data, menu_data)
print(response["food"])
print(response["explanation"])

prompt = "Today I want to eat some beans"
response = generate_response(prompt, symptom_data, menu_data)
print(response)
