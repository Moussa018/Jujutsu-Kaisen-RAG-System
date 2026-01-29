from fastapi import FastAPI
import ollama
import chromadb

app = FastAPI()

# 1. Connexion à la base de données que tu viens de créer
client = chromadb.PersistentClient(path="./base_jjk")
collection = client.get_collection(name="jjk_collection")

@app.get("/chat")
def chat_with_jjk(question: str):
    # A. Transformer ta question en vecteur pour chercher dans la base
    response_emb = ollama.embeddings(model="llama3.2:1b", prompt=question)
    question_vector = response_emb["embedding"]

    # B. Chercher les 2 morceaux de texte les plus proches de ta question
    results = collection.query(
        query_embeddings=[question_vector],
        n_results=2
    )
    
    # On récupère le texte trouvé
    contexte = "\n".join(results["documents"][0])

    # C. Créer le message pour Ollama avec le contexte du Wiki
    prompt_final = f"""
    Tu es un assistant expert en Jujutsu Kaisen. 
    Utilise uniquement les informations suivantes pour répondre à la question. 
    Si tu ne sais pas, dis-le.

    CONTEXTE :
    {contexte}

    QUESTION :
    {question}
    """

    # D. Générer la réponse avec Llama 3
    output = ollama.generate(model="llama3.2:1b", prompt=prompt_final)

    return {
        "reponse": output["response"],
        "sources": results["metadatas"][0]
    }