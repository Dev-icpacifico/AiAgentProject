from general_conf.imports import *

# Configurar variables de entorno
load_dotenv(find_dotenv())
print("Ingresando la APIKEY")

# Verificar existencia del archivo PDF
pdf_path = "Documentos/R.I.O.H.S CONST. Ene. 2025.pdf"
if not exists(pdf_path):
    raise FileNotFoundError(f"El archivo {pdf_path} no fue encontrado.")

# Cargar y procesar el documento
loader = PyPDFLoader(pdf_path)
paginas = loader.load()
print(f"El documento tiene {len(paginas)} páginas.")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=650, chunk_overlap=80)
docs = text_splitter.split_documents(paginas)
print(f"El documento fue dividido en {len(docs)} partes.")

# Configurar embeddings y base vectorial
embedding = OpenAIEmbeddings()
persist_directory = os.path.join("hr-assistant/data", "chroma")

if os.path.exists(persist_directory):
    shutil.rmtree(persist_directory)
os.makedirs(persist_directory, exist_ok=True)

# Crear la base de datos vectorial
try:
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=persist_directory
    )
    print("Base de datos vectorial creada con éxito.")
    print(f"Documentos indexados: {vectordb._collection.count()}")
except Exception as e:
    print(f"Ocurrió un error al crear la base de datos: {e}")
    exit()

# Realizar búsqueda de similitud
question = "¿Qué debe hacer una persona interesada en trabajar en la Empresa Constructora del Mar II SpA.?"
resultados = vectordb.similarity_search(question, k=2)
if resultados:
    for idx, resultado in enumerate(resultados):
        print(f"Resultado {idx + 1}: {resultado.page_content}")
else:
    print("No se encontraron resultados.")
