#%% pakete
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
 
 
#%% RAG function 
def my_rag(query: str, k: int=3, llm_model: str="gemma3:4b") -> str:
    
    # retriever
    embedding_model = OllamaEmbeddings(model="embeddinggemma")
    vectordb = FAISS.load_local(folder_path="Weltliteratur", embeddings=embedding_model, allow_dangerous_deserialization=True)
    
    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    res = retriever.invoke(input=query)
    
    
    
    # augmentation
    # gegeben: [Document, ...], gesucht [str, str, ...] -> str "context: ...; context: ..."
    res_list_str = [doc.page_content for doc in res]
    context_infos = "; context: ".join(res_list_str)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Du bist ein freundlicher Assistent, der Fragen beantwortet.
        Dir werden Kontextinformationen bereitgestellt und du beantwortest die Frage des Nutzers ausschließlich auf Basis der Kontextinfos.
        Antworte kurz und bündig und in der Sprache in der die Frage gestellt wurde.
        """),
        ("user", "Frage: {question}; Kontextinformationen: {context_infos}")
    ])
    
    # generation
    model = ChatOllama(model=llm_model)
    
    # chain
    chain = prompt_template | model | StrOutputParser()
    rag_out = chain.invoke({"question": query, "context_infos": context_infos})
    return rag_out

#%% test RAG function
query = "Welcher Kapitän jagt den Wal?"
my_rag(query=query, k=2, llm_model="gemma3:4b")