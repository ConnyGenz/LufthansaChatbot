import dotenv
from get_text_from_word import from_word_to_txt
from split_txt_material import chunk_as_documents
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()
filepath = "../../data/"
filenames = ["Aktionaersinfos-2017", "Aktionaersinfos-2018", "Aktionaersinfos-2020", "Aktionaersinfos-2021"]

input_file_path = "../../Output/"
output_file_path = "../../Output/"

# Specify word document with textual material, read content and write txt file
from_word_to_txt(filepath, filenames, output_file_path)

# Chunk content of txt files into LangChain Documents
my_document_chunks = chunk_as_documents(filenames, input_file_path, 700, 50)

# Choose location to store vectors
CHROMA_PATH = "../../chroma_aktionaersinfos"

# Choosing a model for embeddings
embeddings = OpenAIEmbeddings() # You can also specify a specific model in brackets here

# Embed chunks and store in vectorstore
aktionaersinfos_vector_db = Chroma.from_documents(my_document_chunks,
                                                  embeddings,
                                                  persist_directory=CHROMA_PATH)

# Create retriever from vectorstore
retriever = aktionaersinfos_vector_db.as_retriever()
