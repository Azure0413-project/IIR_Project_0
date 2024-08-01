from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from langchain.chains import RetrievalQA
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import os

import warnings
warnings.filterwarnings('ignore')

def db_update(db_destination, document_dir, device_choice, chunk_size, chunk_overlap):

    # count the total pdf in this dir
    document = os.listdir(document_dir)

    # path to the pre-trained model
    modelPath = "sentence-transformers/all-MiniLM-l6-v2"
    model_kwargs = {'device': device_choice}
    encode_kwargs = {'normalize_embeddings': False}

    # Initialize an instance of HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,     
        model_kwargs=model_kwargs, 
        encode_kwargs=encode_kwargs 
    )

    if os.path.exists(db_destination) == True:
        print(os.path.split(db_destination)[1])
        db = FAISS.load_local(os.path.split(db_destination)[1], embeddings,allow_dangerous_deserialization=True)
    else:
        for i in range(len(document)):

            #  Create a loader instance ansd load the PDF in
            loader = CSVLoader(os.path.join(document_dir,document[i]))
            data = loader.load()

            # It splits text into chunks of 1000 characters each with a 150-character overlap.
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

            # split the text into documents using the text splitter.
            docs = text_splitter.split_documents(data)

            # create the db
            db = FAISS.from_documents(docs, embeddings)
            
            # save the db
            db.save_local(os.path.split(db_destination)[1])
    
    return db


def RAG(query:str, db_destination=None, document_dir=None,chunk_size=1000, chunk_overlap=150, device_choice='cpu'):

    # get the db
    db = db_update(db_destination=db_destination, document_dir=document_dir, device_choice=device_choice, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    retriever = db.as_retriever(search_kwargs={"k": 1})

    model_name = 'google/flan-t5-base'
    tokenizer = AutoTokenizer.from_pretrained(model_name, padding=True, truncation=True, max_length=200)
    text2text = pipeline(
        task = 'text2text-generation',
        model = model_name,
        tokenizer = tokenizer,
        max_new_tokens = 200,
    )


    # Create an instance of the HuggingFacePipeline, which wraps the question-answering pipeline
    # with additional model-specific arguments (temperature and max_length)
    # llm = HuggingFacePipeline(
    #     pipeline=text2text,
    #     model_kwargs={'temperature': 0.7, 'max_new_tokens': 200},
    # )


    # Create a retriever object from the 'db' with a search configuration where it retrieves up to 4 relevant splits/documents.
    


    system_prompt = (
        "Use the given context to answer the question. "
        "If you don't know the answer, say you don't know. "
        "Use three sentence maximum and keep the answer concise. "
        "Context: {context}"
    )
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
    )
    question_answer_chain = create_stuff_documents_chain(text2text, prompt)
    retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    retrieval_chain.invoke({'input':query})

    # print(docs[0].page_content)
    print('done')
    


RAG('please suggest for me a dish. I want to have chicken, eggs. I am a diabete patient', '/home/project/faiss_index', '/home/project/document')