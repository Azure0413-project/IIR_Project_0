import random
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd

# 加載模型和tokenizer
model_name = "EleutherAI/gpt-neo-2.7B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 加載CSV數據，使用合適的編碼
dataset_path = '/home/peicichen112/老公/RAG/project/document/dataset.csv'
menu_path = '/home/peicichen112/老公/RAG/project/document/menu.csv'

for encoding in ['utf-8', 'latin1', 'ISO-8859-1']:
    try:
        df = pd.read_csv(dataset_path, encoding=encoding)
        menu_df = pd.read_csv(menu_path, encoding=encoding)
        break
    except UnicodeDecodeError:
        continue

# 將數據轉換為字典
symptom_data = df.set_index('Name')[['description', 'reason']].to_dict('index')
menu_data = menu_df.set_index('kind')['food'].to_dict()

def generate_response(prompt, symptom_data, menu_data):
    # 檢查prompt是否包含症狀
    for symptom, data in symptom_data.items():
        if symptom.lower() in prompt.lower():
            food_options = data['description'].split(', ')
            chosen_food = random.choice(food_options)
            
            # 在菜單數據中查找匹配的種類
            for kind, foods in menu_data.items():
                if kind in chosen_food.lower():
                    food_list = foods.split(', ')
                    chosen_food = random.choice(food_list)
                    break
            
            # 使用模型生成解釋
            explanation_prompt = f"Explain why it is beneficial to eat foods that help manage {symptom.lower()} like {chosen_food}. {data['reason']}"
            inputs = tokenizer(explanation_prompt, return_tensors="pt")
            outputs = model.generate(**inputs, max_length=100)
            explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "food": f"Today, you might want to eat some {chosen_food}.",
                "explanation": f"{explanation}"
            }
    
    # 如果未檢測到症狀，將其視為一般查詢
    for kind, foods in menu_data.items():
        if kind in prompt.lower():
            food_list = foods.split(', ')
            chosen_food = random.choice(food_list)
            return f"Today I want to eat {chosen_food}."
    
    # 如果找不到匹配的種類，使用模型生成食物名稱
    generate_food_prompt = f"Suggest a food item for {prompt}."
    inputs = tokenizer(generate_food_prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=50)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return f"Today I want to eat {response}."

# 測試生成回應
prompt = "Today someone with diabetes wants to eat some food. Do you have any recommendations?"
response = generate_response(prompt, symptom_data, menu_data)
print(response["food"])
print(response["explanation"])

prompt = "Today I want to eat some noodles"
response = generate_response(prompt, symptom_data, menu_data)
print(response)

prompt = "Today I want to eat fried food"
response = generate_response(prompt, symptom_data, menu_data)
print(response)
