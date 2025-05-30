import requests
from bs4 import BeautifulSoup
import re
import time
import os
import streamlit as st
from duckduckgo_search import ddg

st.set_page_config(page_title="Email Spider GPT Ready", layout="wide")
st.title("📬 Email Spider GPT Ready")
st.markdown("Strumento automatizzato per l'estrazione di email pubbliche in base a keyword.")

with st.sidebar:
    st.header("⚙️ Configurazione GPT")
    
    browser_type = st.selectbox("🌐 Seleziona un browser (simulato)", ["DuckDuckGo", "Google (prossimamente)", "Bing (prossimamente)"], index=0)
    keyword = st.text_input("🔍 Parole chiave per la ricerca", placeholder="es. sport Piemonte")
    max_results = st.slider("🔢 Numero di siti da analizzare", min_value=10, max_value=500, value=100, step=10)
    delay = st.slider("⏱️ Ritardo tra richieste (in secondi)", min_value=0, max_value=10, value=1)
    start_button = st.button("🚀 Avvia la ricerca email")

def get_urls(keyword, num_results):
    results = ddg(keyword, max_results=num_results)
    urls = [r['href'] for r in results if 'href' in r]
    return urls

def extract_emails_from_url(url):
    emails = set()
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code == 200:
            found = re.findall(r'[\\w\\.-]+@[\\w\\.-]+', response.text)
            for email in found:
                if len(email) < 100 and not email.endswith(".jpg"):
                    emails.add(email)
    except:
        pass
    return emails

if start_button and keyword:
    st.info(f"🔎 Inizio ricerca email con keyword: **{keyword}** usando browser: **{browser_type}**")
    urls = get_urls(keyword, max_results)
    all_emails = set()

    with st.spinner("📡 Estrazione email in corso..."):
        for i, url in enumerate(urls):
            st.write(f"[{i+1}/{len(urls)}] Analizzo: {url}")
            emails = extract_emails_from_url(url)
            all_emails.update(emails)
            time.sleep(delay)

    if all_emails:
        st.success(f"✅ Trovate {len(all_emails)} email pubbliche.")
        filename = f"email_{keyword.replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for email in sorted(all_emails):
                f.write(email + "\\n")

        with open(filename, "rb") as f:
            st.download_button("📥 Scarica il file .txt", f, f_
