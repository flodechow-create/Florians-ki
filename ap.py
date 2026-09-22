import streamlit as st
from google import genai
from google.genai import types

# 1. Seiteneinstellungen
st.set_page_config(page_title="Florians KI-Assistent", page_icon="🤖", layout="wide")
st.title("🤖 Florians KI-Assistent")

# 2. Sidebar für Konfiguration
with st.sidebar:
 st.header("⚙️ Einstellungen")
 api_key = st.text_input("Google Gemini API-Key", type="password")

# Client initialisieren
if api_key:
 client = genai.Client(api_key=api_key)

# 3. Chat-Verlauf initialisieren
if "messages" not in st.session_state:
 st.session_state.messages = []

# 4. Bisherigen Verlauf in der UI anzeigen
for msg in st.session_state.messages:
 with st.chat_message(msg["role"]):
 st.markdown(msg["content"])

# 5. Nutzereingabe & Verarbeitung
if prompt := st.chat_input("Schreibe oder frage etwas..."):
 if not api_key:
 st.warning("⚠️ Bitte gib zuerst deinen API-Key in der Seitenleiste ein!")
 st.stop()

 # Nutzernachricht im UI und Verlauf speichern
 st.session_state.messages.append({"role": "user", "content": prompt})
 with st.chat_message("user"):
 st.markdown(prompt)

 # Inhalt für die API formatieren
 contents = []
 for msg in st.session_state.messages:
 role = "user" if msg["role"] == "user" else "model"
 contents.append(
 types.Content(
 role=role, parts=[types.Part.from_text(text=msg["content"])]
 )
 )

 # Antwort generieren
 with st.chat_message("model"):
 with st.spinner("Überlege..."):
 try:
 response = client.models.generate_content(
 model="gemini-2.5-flash",
 contents=contents,
 )
 answer_text = response.text
 st.markdown(answer_text)

 # Antwort im Verlauf speichern
 st.session_state.messages.append(
 {"role": "model", "content": answer_text}
 )

 except Exception as e:
 st.error(f"Fehler bei der Anfrage: {e}")





