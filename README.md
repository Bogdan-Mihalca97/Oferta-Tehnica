# Generator Propunere Tehnică – Parc Fotovoltaic

Aplicație Python pentru generarea automată a secțiunilor dintr-o **Propunere Tehnică de Execuție** pentru parcuri fotovoltaice, în contextul achizițiilor publice din România.

Textul sursă (metodologii, anunțuri, fișe de date, ATR) este extras din fișiere PDF și trimis către **Claude API (Anthropic)**, iar rezultatul este salvat ca document **DOCX** formatat.

---

## Secțiuni implementate

| Secțiune | Descriere | Status |
|---|---|---|
| 3.5.2 Generator PTE | Proceduri Tehnice de Execuție din Metodologia de Execuție | ✅ |
| 1. Rezumat | Date generale, obiectul contractului, avantaje competitive | ✅ |
| 2. Metodologia de executare | Descrierea lucrărilor și echipamentelor | 🔜 |
| 3.6 Puncte de control calitate | Verificări și teste pe faze de execuție | 🔜 |
| 5. Personal propus | Echipa de proiect și responsabilități | 🔜 |

---

## Structura proiectului

```
.
├── app.py                  # Logica principală + interfață GUI (Tkinter)
├── main.py                 # Entry point
├── generate_s01.py         # Utilitar pentru contextul S01
├── prompts/
│   ├── system_pte.txt      # System prompt pentru generarea PTE
│   ├── user_pte.txt        # User prompt template pentru PTE
│   ├── system_rezumat.txt  # System prompt pentru Rezumat
│   └── user_rezumat.txt    # User prompt template pentru Rezumat
├── config/
│   ├── config.py           # Încarcă config.json și expune variabilele
│   └── config.example.json # Template configurare (copiază în config.json)
├── input/                  # Fișiere PDF de intrare (gitignored)
└── output/                 # Documente DOCX generate (gitignored)
```

---

## Instalare

### Cerințe

- Python 3.10+
- Cont Anthropic cu acces la API

### Dependențe

```bash
pip install anthropic pymupdf python-docx
```

### Configurare

1. Copiază fișierul de configurare:
   ```bash
   cp config/config.example.json config/config.json
   ```

2. Completează `config/config.json` cu valorile reale:
   ```json
   {
       "anthropicApiKey": "sk-ant-api03-...",
       "creatioBaseUrl": "http://your-creatio-instance.com",
       "creatioAuthSecret": "your-auth-secret",
       "listeningHost": "0.0.0.0",
       "listeningPort": "8080"
   }
   ```

---

## Utilizare

```bash
python main.py
```

Se deschide interfața grafică. Din pagina principală se poate accesa fiecare secțiune disponibilă.

### Generator PTE (3.5.2)

1. Alege fișierul PDF cu **Metodologia de Execuție**
2. Alege locația fișierului DOCX de ieșire
3. Apasă **Generează PTE**

Pentru documente scurte (≤30.000 caractere) se face un singur apel API; pentru documente mari se împart în 2 cereri.

### Rezumat (1.)

1. Alege cele 3 fișiere PDF de intrare: **Anunț de participare**, **Fișa de date**, **ATR**
2. Alege locația fișierului DOCX de ieșire
3. Apasă **Generează Rezumat**

---

## Modele suportate

| Model | Recomandat pentru |
|---|---|
| `claude-haiku-4-5-20251001` | Testare rapidă, cost redus |
| `claude-sonnet-4-20250514` | Producție (implicit) |
| `claude-opus-4-20250514` | Calitate maximă |

---

## Note

- `config/config.json` și `input/`, `output/` sunt excluse din repository (`.gitignore`)
- Prompt-urile sunt în fișiere `.txt` separate în `prompts/` pentru editare ușoară fără modificarea codului
