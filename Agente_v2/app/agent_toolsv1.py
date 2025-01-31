# Generar Embeddings
print("Generar Embeddings")
embeddings = OpenAIEmbeddings()

# 1. Cargar la base de datos Chroma previamente guardada
print("1. Cargar la base de datos Chroma previamente guardada")
vectorstore = Chroma(persist_directory="./data/chroma", embedding_function=embeddings)

# Obtener el número de documentos almacenados
print("# Obtener el número de documentos almacenados")
num_documents = vectorstore._collection.count()
print(f"Documentos cargados en la base de datos: {num_documents}")

# Obtener todos los documentos con sus metadatos
docs_with_metadata = vectorstore._collection.get()

# Mostrar los metadatos de cada documento
for doc_id, metadata in zip(docs_with_metadata["ids"], docs_with_metadata["metadatas"]):
    print(f"ID: {doc_id}, Metadata: {metadata}")

# 2. Crear el retriever
print("2. Crear el retriever")
retriever = vectorstore.as_retriever()


# Creación de las herramientas
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# HERRAMIENTA PARA LA BUSQUEDA EN ARCHIVOS PDF
pdf_qa_tool = Tool(
    name="QA Tool",
    func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever).run,
    description="Utiliza esta herramientas cuando se te pregunte por las politicas y procedimientos de la empresa Contructora del Mar ."
)

# HERRAMIENTA PARA LA ASISTENCIA DE RRHH EN LA LEGISLACIÓN CHILENA
api_wrapper = WikipediaAPIWrapper(lang='es', top_k_results=1, doc_content_chars_max=500)
wikipedia = WikipediaQueryRun(api_wrapper=api_wrapper)
wikipedia_tool = Tool(
    name="Wikipedia Tool",
    func=wikipedia.run,
    description="Utiliza esta herramienta cuando debas buscuar algo respecto a la legislación chilena de RRHH"
)

tools = [pdf_qa_tool, wikipedia_tool]

promt = """Eres un asistente consultor que entrega información acerca de las politicas y procedimientos de la empresa Contructora del Mar .,
que ayuda a resolver problemas y dudas respecto a estos documentos. 
Además Eres un consultor de Recursos Humanos, especificamente en la legislación Chile.
Debes responder solo en estos dos contextos que te he entregado, por lo que debes omitir cualquier otra pregunta fuera de los contextos respondiendo que no puedes responder a lo que se te ha preguntado
Reponde a las siguientes preguntas: {q}
"""
promt_template = PromptTemplate.from_template(promt)
prompt = hub.pull('hwchase17/react')

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

for i in range(0, 5):
    # 4. Realizar una consulta
    print("4. Realizar una consulta")
    print("Realizando la pregunta")
    query = input("")
    print(query)
    response = agent_executor.invoke({
        'input': promt_template.format(q=query)})
    print("Respondiendo a la pregunta")
    print("Respuesta:", response)