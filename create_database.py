from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.vectorstores import Chroma
import os
import shutil

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():
    documents = load_documents()    
    save_to_chroma()
    return

# Load in data for tokenizer
def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    return documents

def save_to_chroma():
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    # Load the pre-trained tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")
    
    #Read text file into string
    with open('data/test.txt', 'r') as file:
        text = file.read()

     # Tokenize the text data
    tokenized_text = tokenizer.encode(text)

    # Generate embeddings using the pre-trained model
    embeddings = model(input_ids=tokenized_text['input_ids'], attention_mask=tokenized_text['attention_mask'])


    # Create a new DB from the documents.
    db = Chroma.from_documents(
        tokenized_text, embeddings, persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(tokenized_text)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
