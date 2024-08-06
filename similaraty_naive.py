import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

sample_amount = 20

class num_one:
  # 建構式(Constructor)
  def __init__(self, num=0, value=0.0):
    self.num = num  # 圖片號碼(Attribute)
    self.value = value  # 相似度(Attribute)
  # 方法(Method)
  def info(self):
    print(f"#1 number = \"{self.num}\" ,  sim_value = \"{self.value}\" ")

target = num_one()

def image_to_vector(image):
    # 将图片展平成一维向量
    return image.flatten().reshape(1, -1)

# 读取图片
img_input = cv2.imread('/app/sum_project/archive/training/Bread/0.jpg')

for eva_num in range(sample_amount):
    img_eva = cv2.imread(f'/app/sum_project/archive/training/Bread/{eva_num}.jpg')

    # 确保图片大小相同
    if img_input.shape != img_eva.shape:
        img_input = cv2.resize(img_input, (img_eva.shape[1], img_eva.shape[0]))

    # 转换为灰度图像（如果需要，可以省略这一步）
    img_input_gray = cv2.cvtColor(img_input, cv2.COLOR_BGR2GRAY)
    img_eva_gray = cv2.cvtColor(img_eva, cv2.COLOR_BGR2GRAY)

    # 将图片转换为向量
    vector1 = image_to_vector(img_input_gray)
    vector2 = image_to_vector(img_eva_gray)

    # 计算余弦相似度
    cos_sim = cosine_similarity(vector1, vector2)

    if(cos_sim[0][0] >= target.value):
        target.value = cos_sim[0][0]
        target.num = eva_num

    print(f'pic_num = /app/sum_project/archive/training/Bread/{eva_num}.jpg')
    print(f"Cosine Similarity: {cos_sim[0][0]}")

target.info()