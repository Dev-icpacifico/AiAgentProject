from general_conf.imports import *

# Configuración de la API Key
# Se extrae de un fichero de configuraciones

# Configuración de directorio de persistencia para Chroma
chroma_directory = "hr-assistant/data"
persist_directory = os.path.join(chroma_directory, "chroma")

# Título de la aplicación
st.title("📄 Búsqueda Inteligente en Documentos PDF")

# Subir el archivo PDF
uploaded_file = st.file_uploader("Sube un archivo PDF para procesarlo", type=["pdf"])

# Campo para ingresar preguntas
question = st.text_input("Haz una pregunta sobre el documento:")

# Configurar el procesamiento por lotes
batch_size = 20

if uploaded_file and question:
    # Guardar archivo subido en una ubicación temporal
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    try:
        # Limpiar directorio de persistencia
        if os.path.exists(persist_directory) and os.listdir(persist_directory):
            shutil.rmtree(persist_directory)
        os.makedirs(persist_directory, exist_ok=True)

        # Cargar el archivo PDF
        st.write("📥 Cargando documento...")
        loader = PyPDFLoader(temp_file_path)
        paginas = loader.load()
        st.write(f"🔢 Total de páginas: {len(paginas)}")

        # Configurar el splitter de texto
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        # Inicializar embeddings y base vectorial
        embedding = OpenAIEmbeddings()
        vectordb = None

        # Procesar el documento por lotes
        st.write("⏳ Procesando el documento...")
        for i in range(0, len(paginas), batch_size):
            batch = paginas[i:i + batch_size]
            docs = text_splitter.split_documents(batch)

            if vectordb is None:
                vectordb = Chroma.from_documents(
                    documents=docs,
                    embedding=embedding,
                    persist_directory=persist_directory
                )
            else:
                vectordb.add_documents(docs)

        vectordb.persist()
        st.write("✅ Base vectorial creada con éxito.")

        # Realizar búsqueda de similitud
        st.write("🔍 Buscando respuesta...")
        resultados = vectordb.similarity_search(question, k=2)

        if resultados:
            st.subheader("📌 Resultados:")
            for idx, resultado in enumerate(resultados, start=1):
                st.markdown(f"### Resultado {idx}:")
                st.write(resultado.page_content)
        else:
            st.write("⚠️ No se encontraron resultados para la pregunta.")
    finally:
        # Eliminar el archivo temporal después del procesamiento
        os.remove(temp_file_path)
