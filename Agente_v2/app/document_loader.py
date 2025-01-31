# Selección de documentos
file_path_1 = "C:/Users/Luis Pizarro/PycharmProjects/DHAgent/Agente_v2/data/raw/POL-ICP-CDM-TI-001 Política Integral de Control de Equipos y Accesos (1).pdf"
file_path_2 = "C:/Users/Luis Pizarro/PycharmProjects/DHAgent/Agente_v2/data/raw/PRC-ICP-CDM-CDG-001 Elaboración de documentos.pdf"
file_path_3 = "C:/Users/Luis Pizarro/PycharmProjects/DHAgent/Agente_v2/data/raw/PRC-ICP-CDM-CDG-002 Control de documentos.pdf"

# Lista con los archivos que se quieren cargar
print("Lista con los archivos que se quieren cargar")
# pdf_files = [file_path_1]
pdf_files = [file_path_1, file_path_2, file_path_3]

# Cargar los documentos PDF
print("Cargando documentos PDF")
loader1 = PyPDFLoader(file_path_1)
loader2 = PyPDFLoader(file_path_2)
loader3 = PyPDFLoader(file_path_3)

documents1 = loader1.load()
documents2 = loader2.load()
documents3 = loader3.load()

# Combinar todos los documentos
all_documents = documents1 + documents2 + documents3

# Dividir los documentos en fragmentos
print("Dividir los documentos en fragmentos")
text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True)

split_documents = text_splitter.split_documents(all_documents)

# Generar Embeddings
print("Generar Embeddings")
embeddings = OpenAIEmbeddings()

# Creación o conexión con la base de datos Chroma
print("Creación o conexión con la base de datos Chroma")
vectorstore = Chroma(persist_directory="./data/chroma", embedding_function=embeddings)

# Agregar los documentos fragmentados a chroma
print("Agregar los documentos fragmentados a chroma")
vectorstore.add_documents(split_documents)

# Guardar la base de datos en el disco
print("Guardar la base de datos en el disco")
vectorstore.persist()

print("Todos los documentos han sido cargados")

# Consultar información de los múltiples archivos
print("Consultar información de los múltiples archivos")