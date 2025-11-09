# SmartHack Django — Harta de rezervări + Chat cu AI (RAG SQL)

Un proiect care îmbină o hartă de birouri „drag & drop” cu un chat de tip „întrebi în română, primești răspuns din baza de date”. Sub capotă: Django + LangChain + Google Gemini (Text‑to‑SQL).

## Cum arată experiența
- Te loghezi, deschizi harta, vezi locuri/încăperi/zone, faci rezervări.
- În colțul dreapta‑jos ai o bulă de chat. Întreabă, de exemplu:
  - „Câte rezervări sunt azi?”
  - „Ce sală e liberă mâine la ora 10?”
  - „Câte rezervări am eu săptămâna viitoare?”
- Chatul traduce întrebarea în SQL, întreabă baza de date și îți răspunde pe loc.

## Ce știe să facă (pe scurt)
- Harta interactivă a spațiului + rezervări în timp real.
- Chat RAG Text‑to‑SQL cu Google Gemini (`gemini-2.5-flash`).
- Mesaje de eroare prietenoase (inclusiv când depășești cotele API) și fallback automat.
- La start, în consolă vezi ce modele Gemini ai disponibile.

## 1) Instalare rapidă
Ai Python 3.10+? Perfect. În mediul tău (ideal un venv):

```
pip install django dj-database-url \
    langchain langchain-community langchain-google-genai google-generativeai \
    sqlalchemy psycopg2-binary
```

## 2) Setează cheile și baza de date
- Cheia Gemini (varianta simplă, prin variabilă de mediu):
  - PowerShell (Windows):
    - `setx GOOGLE_API_KEY "AI...cheia_ta..."`
  - sau, pentru test local, în `smart_hack/settings.py` → `HARDCODED_GOOGLE_API_KEY = "AI..."`
- Modelul de AI folosit:
  - `smart_hack/settings.py` → `GOOGLE_MODEL = "gemini-2.5-flash"`
  - Fallback (tot flash): `GOOGLE_MODEL_FALLBACK = "gemini-2.5-flash"`
- Baza de date:
  - Postgres (prod/dev):
    - `postgresql+psycopg2://USER:PASS@HOST:PORT/DB?sslmode=require`
    - setezi ca `CHAT_DATABASE_URL` sau `DATABASE_URL`
  - Local (simplu): SQLite
    - `setx CHAT_DATABASE_URL "sqlite:///C:/SmartHack_Django/db.sqlite3"`

Șmecherie utilă: backend‑ul știe să curețe URL‑urile Postgres (scoate `channel_binding`, adaugă driverul `psycopg2`).

## 3) Pornește aplicația
```
python manage.py migrate
python manage.py runserver
```
Intră pe `http://127.0.0.1:8000/`, autentifică‑te și caută bulina de chat din colț.

La pornire, în consolă vei vedea ceva de genul:
```
[Gemini] Available models: gemini-2.5-flash, gemini-1.5-flash, ...
```

## Cum e organizat proiectul
- Chat UI (se vede doar pentru utilizatori logați):
  - `backend/templates/backend/_rag_chat.html` (HTML + logica mică de frontend)
  - `backend/static/backend/style.css` (stiluri pentru bulă + chat)
- Pagini principale:
  - `backend/templates/backend/index.html` (harta + popover de rezervare)
  - `backend/templates/backend/login.html`, `backend/templates/backend/profile.html`
- Backend (ce te interesează pentru chat):
  - `POST /api/chat/sql/` definit în `backend/views.py`
  - DB models: `backend/models.py` (`User`, `Obiect`, `Rezervare`)
  - Config aplicație: `backend/apps.py` (listează modelele Gemini la startup)
  - Setări: `smart_hack/settings.py`

## Ce conține concret proiectul
- `backend/` — aplicația Django (views, modele, rute, template‑uri, static).
- `backend/templates/backend/index.html` — conține planșa SVG inline (harta) + UI‑ul de booking.
- `backend/static/backend/index.js` — logica hărții: hover, popover, pan‑drag, fetch pentru disponibilitate/rezervare.
- `backend/templates/backend/_rag_chat.html` — widgetul de chat (apelă endpointul RAG SQL).
- `backend/views.py` — endpointurile REST (disponibilitate, rezervare, chat RAG), plus login/logout/profile.
- `backend/models.py` — schema bazei de date.
- `smart_hack/settings.py` — chei, model Gemini, DB; normalizează conexiunea.
- `README.md` — acest ghid.

## Cum am obținut SVG‑ul și cum reprezintă obiectele
- Punct de plecare: o planșă a spațiului (imagine). Am vectorizat‑o și/sau desenat deasupra în editor (ex. Inkscape/Figma):
  - Am trasat contururi pentru zone mari (pereți, coridoare) și obiecte interactive (scaune, săli, zone etc.).
  - Fiecărui element i‑am dat un `id` unic în SVG. Exemple: `conf1`, `conf2` (săli), `mg1..mg3` (manager desks), `pool1..pool2` (pool seats), `masaj`, `party`, și zeci de `path...` pentru scaune.
  - Am exportat ca „Plain SVG” și am inclus SVG‑ul inline în `backend/templates/backend/index.html` pentru control total din CSS/JS.
- Legătura cu aplicația:
  - Frontend: `backend/static/backend/index.js:1` pornește de la o listă de `ids` și grupează obiectele pe tipuri (scaune/beer/mg/conf/pool etc.) pentru efecte de hover și click.
  - Backend: în DB, fiecare obiect are `id_css` (coloană în tabelul `Obiect`) care corespunde exact cu `id`‑ul SVG. Asta face puntea între grafică și date.

## Baza de date (pe scurt)
- `User` — email, parolă (hash), avatar (opțional).
- `Obiect` — fiecare element interactiv de pe hartă: `tip_obiect` (ex. „scaun”, „sala”), `id_css` (ex. `conf1`).
- `Rezervare` — leagă un `User` de un `Obiect` la un moment (`data` + `data_si_ora`). Constrângere de unicititate: un obiect nu poate fi rezervat de două ori în același slot orar.
- Sloturi orare: definite pe ore întregi (08:00–19:00) și livrate de API ca opțiuni clicabile în popover.

## Cum funcționează totul cap‑coadă
- Click pe un obiect (id SVG) → frontend deschide popover și cere disponibilitatea la endpointul `GET /api/availability/<id_css>/?date=YYYY-MM-DD`.
- Alegi un slot → `POST /api/book/` cu `id_css`, `date`, `time`.
- Pagina de „Profile” listează rezervările tale active și oferă „Cancel”.
- Chatul (butonul 💬) este vizibil doar autentificat, și trimite întrebări la `POST /api/chat/sql/` → răspunsul vine din DB printr‑un agent SQL.

## Detalii despre RAG Text‑to‑SQL (Gemini)
- Endpoint: `POST /api/chat/sql/` (autentificat).
- Model: configurat în `smart_hack/settings.py` (`GOOGLE_MODEL`, fallback `GOOGLE_MODEL_FALLBACK`). Implicit: `gemini-2.5-flash`.
- Cheie: `HARDCODED_GOOGLE_API_KEY` sau variabila de mediu `GOOGLE_API_KEY`.
- Conexiune DB: citește `CHAT_DATABASE_URL`/`DATABASE_URL`; normalizează automat URL‑ul Postgres (șterge `channel_binding`, adaugă driver `psycopg2`, impune `sslmode=require` la distanță). Are fallback pe SQLite local dacă Postgres e indisponibil.
- Agent/Chain:
  - Încearcă un agent LangChain cu `SQLDatabaseToolkit` (LLM poate apela unelte pentru a lista tabele și a citi schema, apoi generează SQL).
  - Fallback la `SQLDatabaseChain` care introduce schema direct în prompt (garantând că modelul „vede” schema înainte de SQL).
- Rate‑limits & fallback‑uri model: dacă primește 429/NotFound, încearcă variantă fallback (de ex. „flash”/„flash‑latest”) și returnează un timp de retry în răspuns.
- Frontend: `backend/templates/backend/_rag_chat.html` gestionează trimis/afișat mesaje și erori (inclusiv „Retry in ~Xs”).

Sfaturi utile pentru RAG
- Pentru un comportament mai previzibil, limitează schema expusă către LLM la tabelele relevante (ex. `backend_user`, `backend_obiect`, `backend_rezervare`).
- Dacă întrebi des același lucru, poți adăuga caching la nivel de endpoint.

## API-ul de chat (pentru integrări)
- Endpoint: `POST /api/chat/sql/`
- Body: `{ "question": "Câte rezervări sunt azi?" }`
- Răspuns:
  - Succes: `{ "answer": "...", "model_used": "gemini-..."? }`
  - 400 input invalid / 401 fără login
  - 429 când cota e depășită (include `retry_after_seconds` dacă se poate)
  - 500 pentru alte erori (cu `details` utile)

Test rapid (după login):
```
curl -X POST http://127.0.0.1:8000/api/chat/sql/ \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"Cate rezervari sunt azi?\"}"
```

## Cum „gândește” AI-ul pe SQL
- Agentul LangChain cere schema tabelelor (nume coloane, tipuri) înainte să scrie SQL — deci nu „ghicește”.
- Dacă agentul nu merge, avem un fallback (`SQLDatabaseChain`) care pune schema direct în prompt.
- Poți limita explicit tabelele din DB care intră în joc (mai sigur/mai rapid): `include_tables=[...]`.

## Dacă apare vreo problemă
- „Failed to connect SQLDatabase”:
  - `pip install sqlalchemy psycopg2-binary`
  - verifică URL‑ul (caractere speciale în parolă → URL‑encode `%40` pentru `@` etc.)
  - pentru dev: `CHAT_DATABASE_URL=sqlite:///C:/SmartHack_Django/db.sqlite3`
- „404 model ...”:
  - modelul nu e disponibil pe proiectul tău; vezi lista printată în consolă la startup și setează `GOOGLE_MODEL` la un nume valid
- „429 rate limit”:
  - așteaptă `retry_after_seconds`, folosește un model mai ieftin sau activează billing în Google AI Studio

## Securitate (pe scurt)
- Nu comite chei în repo. `HARDCODED_GOOGLE_API_KEY` e DOAR pentru test local.
- În producție: variabile de mediu + utilizator DB cu drepturi minime (ideal read‑only pentru chat).

## Idei de extindere
- Istoric conversații pe utilizator și export.
- Throttling/caching la nivel de endpoint (costuri mai mici, mai rapid).
- Prompting mai „școlit” și restrângerea schemei la tabelele necesare pentru întrebarea curentă.

---

Întrebări? Idei? Deschide un ticket sau spune direct în chat ce ai vrea să adăugăm. 😊

## Galerie (capturi)
- Planșa de lucru (SVG extras dintr-o planșă imagine și integrat inline):

  ![Planșa birouri](docs/floorplan.png)

- Chat RAG (întrebări în română → SQL → răspuns din DB):

  ![Chat RAG în acțiune](docs/chat_screenshot.png)
