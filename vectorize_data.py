import os
import chromadb
import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. On initialise la base de données (ChromaDB)
# Un dossier 'base_jjk' sera créé automatiquement pour stocker les données
client = chromadb.PersistentClient(path="./base_jjk")
collection = client.get_or_create_collection(name="jjk_collection")

# 2. On configure le découpeur de texte (Chunking)
# On coupe par morceaux de 800 caractères avec un petit chevauchement
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,    # On augmente pour garder l'intégralité d'une technique (ex: Poing Divergent)
    chunk_overlap=250,  # Plus de chevauchement pour que le contexte se répète entre les blocs
    separators=["\n\n", "\n", ".", "!", "?", " "] # Priorité aux paragraphes puis aux phrases
)

def preparer_ma_base():
    # Parcourir les fichiers dans le dossier data
    for nom_fichier in os.listdir("data"):
        if nom_fichier.endswith(".txt"):
            print(f"📖 Analyse de : {nom_fichier}")
            
            with open(f"data/{nom_fichier}", "r", encoding="utf-8") as f:
                contenu = f.read()
                
                # Découper le texte en morceaux
                chunks = text_splitter.split_text(contenu)
                print(f"   -> {len(chunks)} morceaux créés.")

                for i, chunk in enumerate(chunks):
                    # ÉTAPE CLÉ : Transformer le texte en vecteur (nombres) avec Ollama
                    # On utilise le modèle llama3 que tu as déjà
                    print(f"   ⚡ Vectorisation du morceau {i}...")
                    
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
                        print(f"❌ Erreur avec Ollama : {e}")

    print("\n✅ Félicitations ! Ta base de données JJK est prête.")

if __name__ == "__main__":
    preparer_ma_base()