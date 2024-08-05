from diffusers import DiffusionPipeline
from PIL import Image
import torch

pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cuda")
pipe.load_lora_weights("beaf-model", weight_name="pytorch_lora_weights.safetensors", adapter_name="beaf")
# pipe.load_lora_weights("rice-model", weight_name="pytorch_lora_weights.safetensors", adapter_name="rice")
# pipe.load_lora_weights("salad-model", weight_name="pytorch_lora_weights.safetensors", adapter_name="salad")

# pipe.set_adapters(["noodle", "rice", "salad"], adapter_weights=[0.7, 0.8, 0.9])

# generator = torch.manual_seed(0)
# prompt = "A bowl of rice with salad"
# image = pipe(prompt, generator=generator, cross_attention_kwargs={"scale": 1.0}).images[0]

image = pipe("steak is a better choice for meal", num_inference_steps=25).images[0]
#print(type(image))
image.save("beaf.jpg")
#plt.show()