from final import RDS
import os
from PIL import Image

prompt = "please give me a chicken salad"
new_prompt, restaurant_name, food_name, food_price,image_1,image_2,image_3, response_image_url_1, response_image_url_2, response_image_url_3, google_map = RDS(prompt)

# print(new_prompt)
# print(restaurant_name)
# print(food_name)
# print(food_price)
# print(response_image_url_1)
# print(response_image_url_2)
# print(response_image_url_3)
# print(google_map)
print(image_1)

# print(os.getcwd())
# new_prompt, restaurant_name, food_name, food_price, response_image_url_1, response_image_url_2, response_image_url_3, google_map = RDS(prompt)


# print(new_prompt)
# print(restaurant_name)
# print(food_name)
# print(food_price)
# print(response_image_url_1)
# print(response_image_url_2)
# print(response_image_url_3)
# print(google_map)