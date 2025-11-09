# SmartHack Django — Booking + RAG SQL Chat

Un proiect Django care combină un planner de rezervări (hărți interactive + programări) cu un chatbot RAG Text‑to‑SQL (Gemini) care răspunde în limbaj natural, interogând direct baza de date.

## Demo Rapid
- Loghează‑te, deschide harta, apasă pe balonul de chat din colțul dreapta‑jos și întreabă: „Câte rezervări sunt azi?”
- Chatul folosește un agent LangChain care citește schema DB și generează interogări SQL către baza ta de date.

## Funcționalități
- Planner de birouri cu rezervări, vizualizare pe hartă, și cont utilizator.
- Chat RAG Text‑to‑SQL alimentat de Google Gemini (`gemini-2.5-flash`).
- Auto‑fallback de model și mesaje de eroare clare (inclusiv 429 rate‑limit cu timp de retry).
- Listare automată a modelelor disponibile la startup în consolă.

## Cerințe
- Python 3.10+
- Pachete Python:
  - `django`, `dj-database-url`
  - `langchain`, `langchain-community`, `langchain-google-genai`, `google-generativeai`
  - `sqlalchemy`, `psycopg2-binary` (dacă folosești Postgres)

Instalare rapidă:
- `pip install django dj-database-url langchain langchain-community langchain-google-genai google-generativeai sqlalchemy psycopg2-binary`

## Configurare Chei și DB
- Cheie Gemini (recomandat prin env):
  - Windows PowerShell: `setx GOOGLE_API_KEY "AI...your_key..."`
  - Sau hardcode în `smart_hack/settings.py` → `HARDCODED_GOOGLE_API_KEY = "AI..."`
- Modelul folosit:
  - `smart_hack/settings.py` → `GOOGLE_MODEL = "gemini-2.5-flash"`
  - Fallback: `GOOGLE_MODEL_FALLBACK = "gemini-2.5-flash"`
- Baza de date:
  - Env `CHAT_DATABASE_URL` sau `DATABASE_URL` (ex. Postgres):
    - `postgresql+psycopg2://USER:PASS@HOST:PORT/DB?sslmode=require`
  - Pentru dezvoltare locală poți folosi SQLite:
    - `setx CHAT_DATABASE_URL "sqlite:///C:/SmartHack_Django/db.sqlite3"`

Notă: Backend‑ul normalizează automat URL‑ul Postgres (elimină `channel_binding` și adaugă driverul psycopg2 dacă lipsește).

## Rulare
- `python manage.py migrate`
- `python manage.py runserver`
- Deschide `http://127.0.0.1:8000/` și autentifică‑te.

La pornire, consola va afișa modelele disponibile:
- `[Gemini] Available models: gemini-2.5-flash, ...`

## Arhitectură & Fisiere Cheie
- Chat UI (inclus automat în pagini pentru utilizatori autentificați):
  - `backend/templates/backend/_rag_chat.html`
  - Stiluri: `backend/static/backend/style.css`
- Pagini principale:
  - `backend/templates/backend/index.html` (hartă + rezervări)
  - `backend/templates/backend/login.html`, `backend/templates/backend/profile.html`
- Endpointuri backend:
  - RAG Chat API: `POST /api/chat/sql/` în `backend/views.py`
  - Disponibilitate/rezervare: `backend/urls.py` → `/api/availability/<css_id>/`, `/api/book/`
- Modele DB: `backend/models.py` (`User`, `Obiect`, `Rezervare`)
- Config aplicație (lista modele la startup): `backend/apps.py`
- Setări proiect: `smart_hack/settings.py`

## API Chat (RAG SQL)
- Endpoint: `POST /api/chat/sql/`
- Body JSON: `{ "question": "..." }`
- Răspuns:
  - Succes: `{ "answer": "...", "model_used": "gemini-..."? }`
  - Eroare input: `400 { "error": "Invalid JSON body" }`
  - Neautentificat: `401 { "error": "Unauthorized" }`
  - Rate‑limit: `429 { "error": "Agent execution failed: rate limit", "retry_after_seconds": N }`
  - Alte erori: `500 { "error": "...", "details": "..." }`

Test rapid (după login):
```
curl -X POST http://127.0.0.1:8000/api/chat/sql/ \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"Cate rezervari sunt azi?\"}"
```

## Cum funcționează RAG Text‑to‑SQL
- În mod implicit folosește un agent LangChain cu `SQLDatabaseToolkit` care:
  - Listează tabelele și citește schema când are nevoie.
  - Generează SQL, îl rulează și returnează răspunsul.
- Pe fallback, folosește `SQLDatabaseChain` care inserează schema tabelelor direct în prompt la fiecare întrebare.
- Poți restrânge schema la tabelele relevante (ex. `backend_user`, `backend_obiect`, `backend_rezervare`).

## Probleme Frecvente (Troubleshooting)
- „Failed to connect SQLDatabase”:
  - Instalează drivere/pachete: `pip install sqlalchemy psycopg2-binary`
  - Verifică URL DB și parole cu caractere speciale (URL‑encode):
    - `postgresql+psycopg2://USER:P%40SS@HOST/DB?sslmode=require`
  - Pentru local: `CHAT_DATABASE_URL=sqlite:///C:/SmartHack_Django/db.sqlite3`
- „NotFound: 404 model ...”:
  - Modelul nu e disponibil pe proiectul tău; vezi lista printată în consolă la startup și setează `GOOGLE_MODEL`/fallback după numele real.
- „429 rate limit”:
  - Așteaptă `retry_after_seconds` sau folosește un model cu cote mai generoase.
  - Activează billing în Google AI Studio pentru cote mai mari.

## Securitate
- Evită să comiți chei în repo. `HARDCODED_GOOGLE_API_KEY` există doar pentru dev/test.
- Pentru producție, folosește variabile de mediu și conturi DB cu permisiuni minime (read‑only pentru interogări).

## Roadmap Scurt
- Persistență conversații + istorice per utilizator.
- Throttling per utilizator și caching răspunsuri.
- Prompting mai ghidat + restrângerea schemei la tabelele necesare.

---

Dacă vrei, pot configura acum agentul pe `SQLDatabaseChain` cu `include_tables` și mostre de rânduri pentru răspunsuri mai stabile și mai rapide.

