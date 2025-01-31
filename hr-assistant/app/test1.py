from general_conf.imports import *

docs = ["Hola mundo", "Prueba embeddings"]
embedding_func = OpenAIEmbeddings()

try:
    vectordb = Chroma.from_texts(texts=docs, embedding=embedding_func)
    print("Chroma creado con éxito.")
except Exception as e:
    print("Error en Chroma:", e)
