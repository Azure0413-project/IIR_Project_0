from diffusers import DiffusionPipeline
from PIL import Image
import torch
import os

def call_diffusion(prompt):
    #print(os.getcwd())
    os.chdir("/workspace/diffusers")
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cuda")
    pipe.load_lora_weights("examples/dreambooth/chicken-model", weight_name="pytorch_lora_weights.safetensors", adapter_name="beaf")
    pipe.load_lora_weights("examples/dreambooth/rice-model", weight_name="pytorch_lora_weights.safetensors", adapter_name="rice")
    pipe.load_lora_weights("examples/dreambooth/salad-model", weight_name="pytorch_lora_weights.safetensors", adapter_name="salad")
    pipe.load_lora_weights("examples/dreambooth/egg-model", weight_name="pytorch_lora_weights.safetensors", adapter_name="egg")
    pipe.load_lora_weights("examples/dreambooth/bread-model", weight_name="pytorch_lora_weights.safetensors", adapter_name="bread")
    pipe.load_lora_weights("examples/dreambooth/noodle-model", weight_name="pytorch_lora_weights.safetensors", adapter_name="noodle")

    pipe.set_adapters(["beaf", "rice", "salad", "egg", "bread", "noodle"], 
                        adapter_weights=[0.7, 0.8, 0.65, 0.5, 0.4, 0.3])

    generator = torch.manual_seed(0)
    #   prompt = "A bowl of rice with salad"
    #   image = pipe(prompt, generator=generator, cross_attention_kwargs={"scale": 1.0}).images[0]
    os.makedirs("/workspace/test_img", exist_ok = True)
    
    images = []

    for i in range(3):
        image = pipe(prompt, generator=generator, cross_attention_kwargs={"scale": 1.0}).images[0]
        #image = pipe(prompt, num_inference_steps=25).images[0]
        #print(type(image))
        image.save(f"/workspace/test_img/{i}.jpg")
        #plt.show()
        images.append(image)

    return images