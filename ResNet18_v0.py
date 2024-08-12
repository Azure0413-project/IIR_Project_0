import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os
import random
import matplotlib.pyplot as plt
import numpy as np
import cv2
from sklearn.metrics.pairwise import cosine_similarity
import heapq
import pandas as pd
import numpy as np
import json

# 加載預訓練的ResNet18模型，不包括頂層的全連接層
base_model = models.resnet18(pretrained=True)
base_model = nn.Sequential(*list(base_model.children())[:-1])  # 移除頂層的全連接層
base_model.eval()  # 設置模型為評估模式

# 定義圖片的預處理變換
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_and_preprocess_image(img_path):
    # 加載圖片
    img = Image.open(img_path).convert('RGB')
    # 預處理圖片
    img_tensor = preprocess(img)
    # 添加批量維度
    img_tensor = img_tensor.unsqueeze(0)
    return img_tensor

def encode_image(img_path):
    img_tensor = load_and_preprocess_image(img_path)

    # print(img_tensor)
    with torch.no_grad():
        latent_vector = base_model(img_tensor)
    return latent_vector

# 編碼圖片
select_num = 3
sample_amount = 4913
z_vec = []
data_path = '/app/sum_project/data/data/'
gen_path = '/app/sum_project/food_gen_dataset/meat'
# 1942, 2512-2999, 3171, 3202-3999, file noneexist
for pic_num in range(sample_amount):
    img_path = os.path.join(data_path, f'{pic_num}.jpeg')
    if os.path.isfile(img_path):
        latent_vector = encode_image(img_path)

        z_vec.append(latent_vector)

        print(img_path)
        print("Latent vector shape:", latent_vector.shape,  type(latent_vector))

data_set_amount = len(z_vec)

# gen_pic to be compare, rand a label
img_path_valid = []
latent_vector_valid = []
rand_num = random.sample(range(1, 4), select_num)

for i in range (select_num):
    img_path_valid.append(os.path.join(gen_path, f'LINE_ALBUM_food_test_gen_240806_{rand_num[i]}.jpg'))
    latent_vector_valid.append(encode_image(img_path_valid[i]))
print(img_path_valid)

def image_to_vector(image):
    # pic to 1 dimension
    return image.flatten().reshape(1, -1)

def find_k_largest_with_indices(data_list, amount_largest):
    # list with value adn index
    data_list_with_indices = [(val, i) for i, val in enumerate(data_list)]
    # heapq.nlargest find top k largest value
    largest_with_indices = heapq.nlargest(amount_largest, data_list_with_indices)
    labels = [i for val, i in largest_with_indices]
    values = [val for val, i in largest_with_indices]
    return labels, values

df = pd.read_csv("/app/sum_project/data/data/restaurant.csv")
df

df['used'] = 0
type(df['used'][0])
df

amount_largest = 3
# 找一個test
for i in range(select_num):
  vector1 = image_to_vector(latent_vector_valid[i]) #gen picture
  sim_store = []
  
  for eva_num in range(data_set_amount):
      
      # 将图片转换为向量
      vector2 = image_to_vector(z_vec[eva_num]) #dataset compare

      # 计算余弦相似度
      cos_sim = cosine_similarity(vector1, vector2)

      # cos_sim[0][0] : similarity values
      # print('pic_label = ' + data_path + f'/{eva_num}.jpeg')
      # print(f"Cosine Similarity: {cos_sim[0][0]}")
      sim_store.append(float(cos_sim[0][0]))

  # top[0] : picture label , top[1] : similarity values
  top = find_k_largest_with_indices(sim_store, amount_largest)
  filtered_df = df[df['id'] == top[0][0]]

  if(filtered_df['used'][filtered_df.index[0]] == 1):
    filtered_df = df[df['id'] == top[0][1]]
  if(filtered_df['used'][filtered_df.index[0]] == 1):
    filtered_df = df[df['id'] == top[0][1]]
  filtered_df

  json_str = filtered_df.to_json(orient='split')
  print(json_str)
  df.loc[filtered_df.index[0], 'used'] = 1
  # plotfig(label, values)

  # compare_picture
  fin_gen_path = os.path.join(gen_path, f'LINE_ALBUM_food_test_gen_240806_{rand_num[i]}.jpg')
  fin_data_path = os.path.join(data_path, f'{top[0][0]}.jpeg')
  pic_gen = Image.open(fin_gen_path)
  pic_data = Image.open(fin_data_path)
  # subploi for gen_pic and data_pic
  fig, axs = plt.subplots(1, 2, figsize=(10, 5))
  axs[0].imshow(pic_gen)
  axs[0].axis('off')
  axs[0].set_title('gen')
  axs[1].imshow(pic_data)
  axs[1].axis('off')
  axs[1].set_title('data' + f'{top[0][0]}.jpeg')
  plt.show()
  
