import requests
import re
import time
import streamlit as st
from duckduckgo_search import ddg

# ---------------------- CONFIGURAZIONE STREAMLIT ----------------------
st.set_page_config(page_title="Email Spider GPT Ready", layout="wide")
st.title("📬 Email Spider GPT Ready")
st.markdown("Strumento etico per l'estrazione di email pubbliche a partire da parole chiave.")

# ---------------------- SIDEBAR: INPUT UTENTE ----------------------
with st.sidebar:
    st.header("⚙️ Impostazioni Ricerca")
    browser_type = st.selectbox("🌐 Browser simulato", ["DuckDuckGo"], index=0)
    keyword = st.text_input("🔍 Parole chiave", placeholder="es. sport Piemonte")
    max_results = st.slider("🔢 Numero di siti da analizzare", min_value=10, max_value=500, value=100, step=10)
    delay = st.slider("⏱️ Ritardo tra le richieste (sec)", min_value=0, max_value=10, value=1)
    start_button = st.button("🚀 Avvia ricerca email")

# ---------------------- FUNZIONI ----------------------
def get_urls(keyword, num_results):
    results = ddg(keyword, max_results=num_results)
    return [r['href'] for r in results if 'href' in r]

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

# ---------------------- AVVIO RICERCA ----------------------
if start_button and keyword:
    st.info(f"🔎 Ricerca avviata con keyword: **{keyword}** su {max_results} siti...")
    urls = get_urls(keyword, max_results)
    all_emails = set()

    with st.spinner("📡 Estrazione email in corso..."):
        for i, url in enumerate(urls):
            st.write(f"[{i+1}/{len(urls)}] 🌍 {url}")
            found = extract_emails_from_url(url)
            all_emails.update(found)
            time.sleep(delay)

    # ---------------------- RISULTATI ----------------------
    if all_emails:
        st.success(f"✅ Trovate {len(all_emails)} email.")
        filename = f"email_{keyword.replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for email in sorted(all_emails):
                f.write(email + "\\n")

        with open(filename, "rb") as f:
            st.download_button("📥 Scarica il file .txt", f, file_name=filename)
    else:
        st.warning("⚠️ Nessuna email trovata. Prova a cambiare keyword o aumentare i risultati.")

