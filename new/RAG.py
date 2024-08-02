import random
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd

# Load model and tokenizer
model_name = "EleutherAI/gpt-neo-2.7B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load data from CSV with appropriate encoding
file_path = '/home/peicichen112/老公/RAG/project/document/dataset.csv'
for encoding in ['utf-8', 'latin1', 'ISO-8859-1']:
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        break
    except UnicodeDecodeError:
        continue

# Convert data to dictionary
symptom_data = df.set_index('Name')['description'].to_dict()

def generate_response(prompt, symptom_data):
    # Check if prompt contains a symptom from the dataset
    for symptom, description in symptom_data.items():
        if symptom.lower() in prompt.lower():
            food_options = description.split(', ')
            chosen_food = random.choice(food_options)
            
            # Generate an explanation using the model
            explanation_prompt = f"Explain why it is beneficial to eat foods that help manage {symptom.lower()}."
            inputs = tokenizer(explanation_prompt, return_tensors="pt")
            outputs = model.generate(**inputs, max_length=100)
            explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "food":f"Today, you might want to eat some {chosen_food}.",
                "explanation":f"{explanation}"
            }
    
    # If no symptom is detected, treat it as a general query
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=500)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return response

# Test the function with different prompts
prompt = "Today someone with obesity wants to eat some food. Do you have any recommendations?"
response = generate_response(prompt, symptom_data)
print(response["food"])  
print(response["explanation"])

prompt = "Do you have any recommended food?"
response = generate_response(prompt, symptom_data)
print(response["food"])  
print(response["explanation"])
