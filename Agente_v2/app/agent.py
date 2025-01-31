# Create Embeddings


print("Generar Embeddings")
embeddings = OpenAIEmbeddings()

# 1. Load la base de datos Chroma previamente guardada
print("1. Cargar la base de datos Chroma previamente guardada")
vectorstore = Chroma(persist_directory="./data/chroma", embedding_function=embeddings)

# Get el número de documentos almacenados
print("# Obtener el número de documentos almacenados")
num_documents = vectorstore._collection.count()
print(f"Documentos cargados en la base de datos: {num_documents}")

# Get todos los documentos con sus metadatos
docs_with_metadata = vectorstore._collection.get()

# Show los metadatos de cada documento
for doc_id, metadata in zip(docs_with_metadata["ids"], docs_with_metadata["metadatas"]):
    print(f"ID: {doc_id}, Metadata: {metadata}")

# 2. Create el retriever
print("2. Crear el retriever")
retriever = vectorstore.as_retriever()

# 3. Setting una cadena de preguntas y respuestas
print("3. Configurar una cadena de preguntas y respuestas")
llm_name = "gpt-3.5-turbo"
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name=llm_name, temperature=0),
    retriever=retriever,
)

for i in range(0, 5):
    # 4. Make a query
    print("4. Realizar una consulta")
    print("Realizando la pregunta")
    query = input("")
    print(query)
    response = qa_chain.invoke(query)
    print("Respondiendo a la pregunta")
    print("Respuesta:", response)