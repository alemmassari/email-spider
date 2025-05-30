# -----------------------------------------
# 📦 Requisiti per Streamlit Cloud (requirements.txt):
# streamlit
# requests
# beautifulsoup4
# googlesearch-python
# -----------------------------------------

import requests
import re
import time
import streamlit as st
from googlesearch import search

st.set_page_config(page_title="Email Spider GPT - Google", layout="wide")
st.title("📬 Email Spider (solo Google)")
st.markdown("Estrai email pubbliche dai siti trovati con Google Search.")

with st.sidebar:
    st.header("⚙️ Impostazioni")
    keyword = st.text_input("🔍 Parole chiave", placeholder="es. sport Piemonte")
    max_results = st.slider("🔢 Numero siti da analizzare", min_value=10, max_value=100, value=30, step=10)
    delay = st.slider("⏱️ Ritardo tra richieste (sec)", min_value=0, max_value=10, value=1)
    start_button = st.button("🚀 Avvia la ricerca email")

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

if start_button and keyword:
    st.info(f"🔎 Cerco email con la keyword: **{keyword}** usando Google")
    urls = get_urls_google(keyword, max_results)
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
