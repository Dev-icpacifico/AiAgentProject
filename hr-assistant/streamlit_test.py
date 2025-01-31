from general_conf.imports import *


def save_history(question, answer):
    with open("history.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {question} -> {answer}\n")

def load_history():
    if os.path.exists("history.txt"):
        with open("history.txt", "r") as f:
            return f.readlines()
    return []

def clear_history():
    if os.path.exists("history.txt"):
        open("history.txt", "w").close()

def main():
    st.set_page_config(page_title="Agente Willson 🤖🏐", layout="wide", page_icon="🤖")
    st.title("Agente Willson 🤖🏐")

    instrucciones = """
    -Eres un agente de ia que ayuda a las personas a resolver preguntas de archivos pdf.
    """
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instrucciones=instrucciones)
    st.write("Promt Cargado...")

    sys.setrecursionlimit(10000)  # Aumenta el límite de recursión si es necesario

    # Configuración de la API Key
    # Se extrae de un fichero de configuraciones

    # from document_loader import reglamento_interno
    load_dotenv(find_dotenv())

    # Asignar la apikey de openai
    # openai.api_key = os.getenv("OPENAI_API_KEY")

    # Cargar el archivo PDF
    # loader = PyPDFLoader("Documentos/2024_11-04_Contrato_de_trabajo_Rocio_Flores_Munoz.pdf")
    # loader = PyPDFLoader("Documentos/R.I.O.H.S CONST. Ene. 2025.pdf")
    loader = PyPDFLoader("Documentos/POL-ICP-CDM-TI-001 Política Integral de Control de Equipos y Accesos (1).pdf")
    paginas = loader.load()

    print(len(paginas))

    # Dividir el documento cargado
    """text_splitter = CharacterTextSplitter(
        separator= "\n",
        chunk_size= 1000, #Cantidad de caracteres de los textos separados
        chunk_overlap= 200, # Caracteres tomados de textos anteriores como si fuera una desviación
        length_function=len
    )"""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Reducir el tamaño de los fragmentos
        chunk_overlap=200,  # Menor superposición entre fragmentos
        length_function=len
    )

    docs = text_splitter.split_documents(
        paginas)  # Para ejecutar el méthodo texsplitter del texto que cargamos en la variable paginas
    print(len(docs))

    # Usar Embeddings
    # Transformamos el documento en vectores
    embedding = OpenAIEmbeddings()  # creamos la variable para llamar al metodo embeddings

    # Ahora debemos vectorizar los archivos en una base de datos local
    chroma_directory = "hr-assistant/data"
    persist_directory = os.path.join(chroma_directory, "chroma")

    # Verificar si el directorio existe y contiene archivos
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        # SI el directorio existe y no está vacio, bórralo
        shutil.rmtree(persist_directory)
        print("El directorio existe")

    # Vuelve a crear el archivo
    os.makedirs(persist_directory, exist_ok=True)

    print("Directorio de persistencia preparado")

    # Guardar la base de datos de forma local
    print("Guardar la base de datos de forma local")
    print(len(docs))
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=persist_directory
    )
    # vectordb.persist()
    print("Base de datos vectorial creada con éxito.")

    print("Cantidad de colecciones: ", vectordb._collection.count())


    llm_name = "gpt-3.5-turbo"
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model_name=llm_name, temperature=0)
    from langchain.chains import RetrievalQA

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever()
    )
    #agente = create_react_agent(llm =llm, prompt=prompt, tools=)
    # agente_executor = AgentExecutor(agente=agente, verbose=True)

    # Solicitar al usuario la pregunta para el agente
    user_input = st.text_input("Introduce una pregunta para Willson: ", key="input_text")
    col1, col2 = st.columns(2)
    with col1:
        ejecutar = st.button("Ejecutar", key="execute_button")
    with col2:
        limpiar = st.button("Limpiar historial", key="clear_button")

    if ejecutar:
        if user_input:
            respuesta = qa_chain.invoke(input={"input": user_input})
            st.markdown("#### Respuesta de Willson")
            save_history(user_input, respuesta["output"])
        else:
            st.warning("Por favor, introduce una pregunta para Willson")


if __name__ == '__main__':
    main()