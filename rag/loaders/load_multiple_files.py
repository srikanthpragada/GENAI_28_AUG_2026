# Load document from Text File
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_community.document_loaders.text import TextLoader

# Load the text file from the given directory
pdf_loader = DirectoryLoader("./docs", glob=["*.pdf"],
                         loader_cls=PyPDFLoader,
                         loader_kwargs= {"mode" : "single"})

# Load the text file from the given directory
text_loader = DirectoryLoader("./docs", glob=["*.txt"],
                         loader_cls=TextLoader,
                       )

# Loading docs from both 
docs = pdf_loader.load() + text_loader.load() 
print("Loaded Documents :", len(docs))

