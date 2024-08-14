from test_call import call_diffusion
from RAG import RAG
from PIL import Image

prompt = RAG('i have diabetes,  please recommand one diet for me, i want chicken', '/workspace/faiss_index', '/workspace/document')
call_diffusion(prompt)
#for i, item in enumerate(image):
    #print(item)
    #item.save(f"{i}.png")
