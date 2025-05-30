import requests
import re
import time
import streamlit as st
from duckduckgo_search import ddg
from googlesearch import search

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Email Spider GPT", layout="wide")
st.title("📬 Email Spider GPT Enhanced")
st.markdown("Estrai email pubbliche da siti trovati via DuckDuckGo, Google o Bing (se disponibile).")

# ---------------------- SIDEBAR INPUT ----------------------
with st.sidebar:
    st.header("⚙️ Impostazioni")
    browser_type = st.selectbox("🌐 Motore di ricerca", ["DuckDuckGo", "Google", "Bing (non attivo)"], index=0)
    keyword = st.text_input("🔍 Parole chiave", placeholder="es. sport Piemonte")
    max_results = st.slider("🔢 Numero siti da analizzare", min_value=10, max_value=100, value=30, step=10)
    delay = st.slider("⏱️ Ritardo tra le richieste (sec)", min_value=0, max_value=10, value=1)
    start_button = st.button("🚀 Avvia la ricerca email")

# ---------------------- FUNZIONI ----------------------
def get_urls_ddg(query, num_results):
    results = ddg(query, max_results=num_results)
    return [r['href'] for r in results if 'href' in r]

def get_urls_google(query, num_results):
    return list(search(query, num_results=num_results))

def extract_emails_from_url(url):
    emails = set()
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code == 200:
            found = re.findall(r"[\\w\\.-]+@[\\w\\.-]+", response.text)
            for email in found:
                if len(email) < 100 and not email.lower().endswith(('.jpg', '.png', '.svg')):
                    emails.add(email)
    except:
        pass
    return emails

# ---------------------- LOGICA DI ESECUZIONE ----------------------
if start_button and keyword:
    st.info(f"🔎 Cerco email con la keyword: **{keyword}** usando **{browser_type}**")
    
    # Selezione motore
    if browser_type == "DuckDuckGo":
        urls = get_urls_ddg(keyword, max_results)
    elif browser_type == "Google":
        urls = get_urls_google(keyword, max_results)
    else:
        st.warning("⚠️ Motore Bing non ancora attivo. Usa DuckDuckGo o Google.")
        urls = []

    all_emails = set()

    if urls:
        with st.spinner("📡 Estrazione email in corso..."):
            for i, url in enumerate(urls):
                st.write(f"[{i+1}/{len(urls)}] 🌍 {url}")
                found = extract_emails_from_url(url)
                all_emails.update(found)
                time.sleep(delay)

        if all_emails:
            st.success(f"✅ Trovate {len(all_emails)} email.")
            filename = f"email_{keyword.replace(' ', '_')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for email in sorted(all_emails):
                    f.write(email + "\\n")
            with open(filename, "rb") as f:
                st.download_button("📥 Scarica il file .txt", f, file_name=filename)
        else:
            st.warning("⚠️ Nessuna email trovata.")
    else:
        st.warning("❌ Nessun sito trovato. Prova con un'altra keyword.")


