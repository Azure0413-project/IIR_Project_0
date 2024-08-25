from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import os
from openai import OpenAI
import random

import warnings
warnings.filterwarnings('ignore')

def db_update(db_destination, document_dir, device_choice, chunk_size, chunk_overlap):

    # count the total pdf in this dir
    document = os.listdir(document_dir)

    # path to the pre-trained model
    modelPath = "sentence-transformers/all-MiniLM-l6-v2"
    model_kwargs = {'device': device_choice}


    # Initialize an instance of HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,     
        model_kwargs=model_kwargs, 
    )

    if os.path.exists(db_destination) == True:
        db = FAISS.load_local(os.path.split(db_destination)[1], embeddings,allow_dangerous_deserialization=True)
    else:
        for i in range(len(document)):
            
            # according to different file, use different method
            if document[i].split('.')[1] == 'csv':
                loader = CSVLoader(os.path.join(document_dir,document[i]))
            elif document[i].split('.')[1] == 'pdf':
                loader = PyMuPDFLoader(os.path.join(document_dir,document[i]))
            
            # load the data
            data = loader.load()

            # It splits text into chunks of 1000 characters each with a 150-character overlap.
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            docs = text_splitter.split_documents(data)

            # create the db
            if i != 0:
                db.merge_from(FAISS.from_documents(docs, embeddings))
            else:
                db = FAISS.from_documents(docs, embeddings)
        
        # save the db
        db.save_local(os.path.split(db_destination)[1])
    
    return db


def RAG(query:str, db_destination=None, document_dir=None,chunk_size=1000, chunk_overlap=150, device_choice='cpu'):

    # get the db
    db = db_update(db_destination=db_destination, document_dir=document_dir, device_choice=device_choice, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    retriever = db.as_retriever(search_kwargs={"k": 10})
    
    # retrive form the db and random pick one document
    choose = random.randint(0, 9)
    col = retriever.get_relevant_documents(query)[choose].page_content.split('\n')
    ingredient = col[3].split(':')[1]
    dish = col[1].split(':')[1]

    # print(col)

    # prompt
    from langchain.prompts import PromptTemplate

    # combine with the prompt
    openAIprompt = PromptTemplate(
        input_variables=['dish'],
        template=
        """
        You are a friendly doctor and the system find the user should eat{dish}, please answer in 100 words.
        """
    )
    prompt = openAIprompt.format(dish=dish)
    # print(prompt)
    
    # answer using openai api
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # tell gpt which role should it play
            {   
                "role": "system", 
                "content": prompt
            },
            # user input
            {
                "role": "user",
                "content": query
            }
        ]
    )
    
    print(f'Dish recomman: {dish}')
    print(f'Anser: {completion.choices[0].message.content}')

    return dish, completion.choices[0].message.content
    
    

RAG('i have pregnancy, please recommand one diet for me', '/home/project/faiss_index', '/home/project/document')
RAG('i have pregnancy, please recommand one diet for me', '/home/project/faiss_index', '/home/project/document')
