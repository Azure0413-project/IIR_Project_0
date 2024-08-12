from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import os

# import warnings
# warnings.filterwarnings('ignore')

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
    retriever = db.as_retriever()


    # get the llm
    # model_name = 'meta-llama/Meta-Llama-3-8B'
    model_name = 'google/flan-t5-base'
    tokenizer = AutoTokenizer.from_pretrained(model_name, padding=True, truncation=True, max_length=2000)
    text2text = pipeline(
        task = 'text2text-generation',
        model = model_name,
        tokenizer = tokenizer,
        max_new_tokens = 2000,
        device = 'cpu'
    )

    # prompt
    from langchain.prompts import PromptTemplate
    location_extractor_prompt = PromptTemplate(
        input_variables=['dish', 'query'],
        template=
        """
        The system recommand {dish}.
        """
    )
    

    # retrive form the db
    col = retriever.get_relevant_documents(query)[0].page_content.split('\n')
    ingredient = col[3].split(':')[1]
    dish = col[1].split(':')[1]

    # combine with the prompt
    prompt_text = location_extractor_prompt.format(dish=dish, query=query)

    # put the prompt into llm
    llmresult = text2text(prompt_text)
    # print(llmresult)
    
    return llmresult[0]['generated_text']
    
    

RAG('i have diabetes,  please recommand one diet for me', '/home/project/faiss_index', '/home/project/document')
