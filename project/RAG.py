from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from langchain.chains import RetrievalQA
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
        db = FAISS.load_local(os.path.split(db_destination)[1], embeddings,allow_dangerous_deserialization=True)
    else:
        for i in range(len(document)):

            #  Create a loader instance ansd load the PDF in
            loader = CSVLoader(os.path.join(document_dir,document[i]), source_column="Disease")
            data = loader.load()

            # It splits text into chunks of 1000 characters each with a 150-character overlap.
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

            # split the text into documents using the text splitter.
            docs = text_splitter.split_documents(data)

            # create the db
            db = FAISS.from_documents(docs, embeddings)
            
            # save the db
            db.save_local(os.path.split(db_destination)[0])
    
    return db


def RAG(query:str, db_destination=None, document_dir=None,chunk_size=1000, chunk_overlap=150, device_choice='cpu'):

    # get the db
    db = db_update(db_destination=db_destination, document_dir=document_dir, device_choice=device_choice, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    retriever = db.as_retriever()
    print(retriever.get_)


    # get the llm
    # model_name = 'meta-llama/Meta-Llama-3-8B'
    model_name = 'google/flan-t5-base'
    tokenizer = AutoTokenizer.from_pretrained(model_name, padding=True, truncation=True, max_length=512)
    text2text = pipeline(
        task = 'text2text-generation',
        model = model_name,
        tokenizer = tokenizer,
        max_new_tokens = 512,
        device = 'cpu'
    )


    # Create an instance of the HuggingFacePipeline, which wraps the question-answering pipeline
    # with additional model-specific arguments (temperature and max_length)
    llm = HuggingFacePipeline(
        pipeline=text2text,
        model_kwargs={'temperature': 0.7, 'max_new_tokens': 512},
    )
    

    # It's configured with a language model (llm), a chain type "refine," the retriever we created, and an option to not return source documents.
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="refine", retriever=retriever, return_source_documents=False)
    a = qa.invoke(query)

    print(a['result'])
    

RAG('please suggest for me a dish.I am a diabete patient', '/home/project/faiss_index', '/home/project/document')