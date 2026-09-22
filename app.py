import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader

# 1. Seiteneinstellungen
st.set_page_config(
 page_title="Florians KI-Assistent",
 page_icon="🤖",
 layout="wide"
)

st.title("🤖 Florians KI-Assistent")
st.caption("Ein eigener KI-Chat mit PDF-Analysefunktion (RAG-Light)")

# 2. Sidebar für Konfiguration & Dokumenten-Upload
with st.sidebar:
 st.header("⚙️ Einstellungen")
 api_key = st.text_input("Google Gemini API-Key", type="password", help="Hole deinen Key auf aistudio.google.com")
 
 st.divider()
 st.header("📄 Zusatzfunktion: PDF-Analyse")
 uploaded_file = st.file_uploader("Lade ein PDF hoch", type=["pdf"])
 
 pdf_text = ""
 if uploaded_file is not None:
 try:
 reader = PdfReader(uploaded_file)
 for page in reader.pages:
 text = page.extract_text()
 if text:
 pdf_text += text + "\n"
 st.success(f"✅ PDF geladen ({len(reader.pages)} Seiten)")
 except Exception as e:
 st.error(f"Fehler beim Lesen der PDF: {e}")

# 3. Chat-Verlauf initialisieren
if "messages" not in st.session_state:
 st.session_state.messages = []

# 4. Bisherigen Verlauf in der UI anzeigen
for message in st.session_state.messages:
 with st.chat_message(message["role"]):
 st.markdown(message["content"])

# 5. Nutzereingabe & Verarbeitung
if prompt := st.chat_input("Schreibe eine Nachricht..."):
 if not api_key:
 st.warning("⚠️ Bitte gib zuerst deinen Gemini API-Key in der linken Seitenleiste ein.")
 st.stop()

 # Nutzernachricht im UI und Verlauf speichern
 st.session_state.messages.append({"role": "user", "content": prompt})
 with st.chat_message("user"):
 st.markdown(prompt)

 # Gemini Client initialisieren
 client = genai.Client(api_key=api_key)

 # System-Instruktion & Dokumenten-Kontext aufbauen
 system_instruction = "Du bist ein hilfreicher, freundlicher KI-Assistent namens Florians KI."
 if pdf_text:
 system_instruction += (
 f"\n\nDer Nutzer hat ein Dokument hochgeladen. "
 f"Nutze den folgenden Inhalt bevorzugt, um Fragen zu beantworten:\n\n--- DOKUMENT START ---\n{pdf_text}\n--- DOKUMENT ENDE ---"
 )

 # Verlauf für die API vorbereiten
 contents = []
 for msg in st.session_state.messages:
 role = "user" if msg["role"] == "user" else "model"
 contents.append(
 types.Content(
 role=role,
 parts=[types.Part.from_text(text=msg["content"])]
 )
 )

 # Antwort generieren
 with st.chat_message("assistant"):
 with st.spinner("Überlege..."):
 try:
 response = client.models.generate_content(
 model="gemini-2.5-flash",
 contents=contents,
 config=types.GenerateContentConfig(
 system_instruction=system_instruction,
 temperature=0.7,
 )
 )
 
 answer_text = response.text
 st.markdown(answer_text)
 
 # Antwort im Verlauf speichern
 st.session_state.messages.append({"role": "assistant", "content": answer_text})
 
 except Exception as e:
 st.error(f"Fehler bei der Anfrage: {e}")


