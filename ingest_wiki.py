from playwright.sync_api import sync_playwright
import os
import time

if not os.path.exists("data"):
    os.makedirs("data")

def extraire_fandom_ultime(nom):
    with sync_playwright() as p:
        # Lancement du navigateur avec affichage (headless=False) pour voir ce qui bloque si besoin
        # Change en True une fois que ça fonctionne
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # URL vers le wiki ANGLAIS (souvent plus stable pour les tests) ou FR
        url = f"https://jujutsu-kaisen.fandom.com/fr/wiki/{nom.replace(' ', '_')}"
        print(f"🌐 Navigation vers : {url}")
        
        try:
            # Augmentation du timeout à 60s
            page.goto(url, wait_until="load", timeout=60000)
            
            # 1. On attend un peu que les pubs/popups se chargent
            time.sleep(5) 
            
            # 2. Tenter de cliquer sur "Accepter" si un bouton de cookies apparaît
            # (Optionnel, mais aide souvent)
            try:
                page.click("text=Accepter", timeout=5000)
            except:
                pass

            # 3. Extraction du texte via le sélecteur le plus stable
            # On cherche d'abord le contenu, sinon tout le texte du body
            if page.locator(".mw-parser-output").count() > 0:
                content = page.locator(".mw-parser-output").inner_text()
            else:
                print("⚠️ .mw-parser-output non trouvé, extraction du texte global...")
                content = page.locator("body").inner_text()
            
            if content and len(content) > 200:
                nom_fichier = f"data/{nom.replace(' ', '_')}.txt"
                with open(nom_fichier, "w", encoding="utf-8") as f:
                    f.write(f"SOURCE: {url}\n\n")
                    f.write(content)
                print(f"✅ Sauvegardé : {nom_fichier} ({len(content)} caractères)")
            else:
                print(f"❌ Contenu trop court ou vide pour {nom}")

        except Exception as e:
            print(f"❌ Erreur critique pour {nom} : {e}")
        
        browser.close()

# --- Exécution ---
personnages = ["Satoru Gojo", "Yuji Itadori"]
for p in personnages:
    extraire_fandom_ultime(p)