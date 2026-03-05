import os
import chromadb
import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter

# On initialise la base de données 
# dossier 'base_jjk' sera créé automatiquement pour stocker les données
client = chromadb.PersistentClient(path="./base_jjk")
collection = client.get_or_create_collection(name="jjk_collection")

# 2. On configure le découpeur de texte (Chunking)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,    
    chunk_overlap=250, 
    separators=["\n\n", "\n", ".", "!", "?", " "]
)

def preparer_ma_base():
    for nom_fichier in os.listdir("data"):
        if nom_fichier.endswith(".txt"):
            print(f" Analyse de : {nom_fichier}")
            
            with open(f"data/{nom_fichier}", "r", encoding="utf-8") as f:
                contenu = f.read()
                
                # Découper le texte en morceaux
                chunks = text_splitter.split_text(contenu)
                print(f"{len(chunks)} morceaux créés.")

                for i, chunk in enumerate(chunks):
                    # Transformer le texte en vecteur (nombres)
                    print(f" Vectorisation du morceau {i}...")
                    
                    try:
                        response = ollama.embeddings(model="llama3.2:1b", prompt=chunk)
                        vecteur = response["embedding"]

                        # Ajouter le morceau, son vecteur et son texte dans ChromaDB
                        collection.add(
                            ids=[f"{nom_fichier}_{i}"],
                            embeddings=[vecteur],
                            documents=[chunk],
                            metadatas=[{"source": nom_fichier}]
                        )
                    except Exception as e:
                        print(f"Erreur avec Ollama : {e}")

    print("\n Félicitations ! Ta base de données JJK est prête.")

if __name__ == "__main__":
    preparer_ma_base()
