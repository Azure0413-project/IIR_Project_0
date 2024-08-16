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

from test_call import call_diffusion
from RAG import RAG
from PIL import Image
from tqdm import tqdm

def RDS(str):
    prompt = RAG(str, '/workspace/faiss_index', '/workspace/document')
    images = call_diffusion(prompt)
    # 加載預訓練的ResNet18模型，不包括頂層的全連接層
    base_model = models.vgg19(pretrained=True)
    # base_model = nn.Sequential(*list(base_model.children())[:-1])  # 移除頂層的全連接層
    base_model.eval()  # 設置模型為評估模式
    model_name = 'vgg19'

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
    sample_amount = 4000
    z_vec = []
    z_vec_label = []
    data_path = '/workspace/data/'
    gen_path = '/workspace/test_img'
    # 1942, 2512-2999, 3171, 3202-3999, file noneexist
    
    z_vec = torch.load(f"/workspace/z_vec_{model_name}.pth")
    z_vec_label = np.load(f'/workspace/z_vec_label_{model_name}.npy')
    z_vec_label = z_vec_label.tolist()

    data_set_amount = len(z_vec)

    # gen_pic to be compare, rand a label
    img_path_valid = []
    latent_vector_valid = []
    rand_num = random.sample(range(0, 3), select_num)
    for i in range (select_num):
        img_path_valid.append(os.path.join(gen_path, f'{rand_num[i]}.jpg'))
        latent_vector_valid.append(encode_image(img_path_valid[i]))
    # print(img_path_valid)

    def image_to_vector(image):
        # pic to 1 dimension
        return image.flatten().reshape(1, -1)

    def find_k_largest_with_indices(data_label_list, data_list, amount_largest):
        new_list = list(zip(data_label_list, data_list))
        # list with value adn index
        data_list_with_indices = [(val, i) for i, val in new_list]
        # heapq.nlargest find top k largest value
        largest_with_indices = heapq.nlargest(amount_largest, data_list_with_indices)
        labels = [i for val, i in largest_with_indices]
        values = [val for val, i in largest_with_indices]
        return labels, values

    df = pd.read_csv("/workspace/data/restaurant.csv")

    def show_fig(gen_path, data_path, f_df_label) :
        pic_gen = Image.open(gen_path)
        pic_data = Image.open(data_path)
        # subplot for gen_pic and data_pic
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].imshow(pic_gen)
        axs[0].axis('off')
        axs[0].set_title('gen')
        axs[1].imshow(pic_data)
        axs[1].axis('off')
        axs[1].set_title('data' + f_df_label)
        plt.show()

    df['used'] = 0
    amount_largest = 3
    json_id = []
    json_rest_name = []
    json_food_name = []
    json_food_price = []
    json_food_img = []
    json_rest_map = []
    top_k_label = []
    top_k_value = []

    big = torch.tensor([])
    for eva_num in range(data_set_amount):
        # picture to vector
        vector2 = image_to_vector(z_vec[eva_num]) #dataset compare
        big = torch.cat((big, vector2), 0)

    # calculate gen pic[i] with database picture
    for i in range(select_num):
        vector1 = image_to_vector(latent_vector_valid[i]) #gen picture
        #sim_store = []
        sim_store = cosine_similarity(big, vector1)
        #print(sim_store.shape)
        sim_store = sim_store.squeeze()
        sim_store = sim_store.tolist()
        #print(sim_store)

        # top[0] : picture label , top[1] : similarity values
        top_k = find_k_largest_with_indices(z_vec_label, sim_store, amount_largest)
        max_0 = top_k[0][0]
        f_df = df[df['id'] == max_0]
        f_df_idx = f_df.index[0]

        if(df['used'][f_df_idx] == 1):
            f_df = df[df['id'] == top_k[0][1]]
            f_df_idx = f_df.index[0]
        if(df['used'][f_df_idx] == 1):
            f_df = df[df['id'] == top_k[0][2]]
            f_df_idx = f_df.index[0]

        df.loc[f_df_idx, 'used'] = 1
        
        f_df_label = f_df['id'][f_df_idx]

        # convert python file into JSON file and return value 
        json_str = f_df.to_json(orient='split')
        json_dict = json.loads(json_str)
        json_value = json_dict['data'][0]
        print(json_value)

        json_id.append(json_value[0])
        json_rest_name.append(json_value[1])
        json_food_name.append(json_value[2])
        json_food_price.append(json_value[3])
        json_food_img.append(json_value[4])
        json_rest_map.append(json_value[5])

        # def : plotfig(label, values)
        fin_gen_path = os.path.join(gen_path, f'{rand_num[i]}.jpg')
        fin_data_path = os.path.join(data_path, f'{f_df_label}.jpeg')
        show_fig(fin_gen_path, fin_data_path, f'{f_df_label}')

        top_k_label.append(top_k[0])
        top_k_value.append(top_k[1])

        for i in range(amount_largest):
        print(top_k_label[i])
        print(top_k_value[i])
        plt.scatter(top_k_label[i], top_k_value[i])
        plt.xlabel("pic label")
        plt.ylabel("similarity")
        plt.title("top 3 similarity for each gen")
        plt.savefig(f'{model_name}_sim_{i}.jpg', format='jpg')
        plt.show()
    return prompt, json_rest_name, json_food_name, json_food_price, images[0], images[1], images[2], json_food_img[0], json_food_img[1], json_food_img[2],json_rest_map
