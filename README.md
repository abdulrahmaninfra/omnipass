<div align="center">

# OmniPass

**A password generator with Arabic letter and tashkeel support**

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.14+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139-blue)

</div>

---

## Features

- **Cryptographically secure** passwords using Python's `secrets` module
- **Arabic character support** — includes Arabic letters (U+0621–U+064A) and tashkeel diacritical marks (U+064B–U+0652)
- **Latin characters, digits, and punctuation** — full ASCII coverage
- **Configurable length** — passwords from 8 to 256 characters
- **REST API** — FastAPI backend with auto-generated OpenAPI docs
- **Browser extension** — Chrome Extension (Manifest V3) included
- **Static frontend** — dark-themed HTML/CSS/JS UI
- **Docker support** — run with a single command
- **Vercel-ready** — deploy serverless in minutes

## Architecture

```
omnipass/
├── backend/              # FastAPI Python API
│   ├── main.py           # Application logic & API endpoint
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Container build
│   ├── run.sh            # Development launcher
│   └── .env              # Configuration
├── frontend/             # Web UI & Browser Extension
│   ├── index.html        # Standalone web page
│   ├── popup.html        # Chrome extension popup
│   ├── popup.js          # Extension logic
│   ├── manifest.json     # Extension manifest (V3)
│   └── Dockerfile        # Nginx container build
├── docker-compose.yml    # Full-stack orchestration
└── vercel.json           # Vercel deployment config
```

## Quick Start

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py
# → http://localhost:8000
# → Swagger UI: http://localhost:8000/docs
```

### Docker

```bash
docker-compose up --build
# Backend: http://localhost:8000
# Frontend: http://localhost:80
```

### Chrome Extension

1. Open `chrome://extensions/`
2. Enable **Developer mode**
3. Click **Load unpacked**
4. Select the `frontend/` directory

## API

### `GET /generate`

Generate a random password.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `length` | `int` | `16` | Password length (8–256) |
| `include_arabic` | `bool` | `false` | Include Arabic letters & tashkeel |

**Response** (`200 OK`):

```json
{
  "password": "aB3$كَْZx9#مُّQw!",
  "length": 16,
  "includes_arabic": true
}
```

## Character Sets

| Set | Characters | Range |
|-----|------------|-------|
| Lowercase | `a–z` | ASCII |
| Uppercase | `A–Z` | ASCII |
| Digits | `0–9` | ASCII |
| Punctuation | `` !"#$%&'()*+,-./:;<=>?@[\]^_`{\|}~ `` | ASCII |
| Arabic Letters | ء–ى (40 chars) | U+0621–U+064A |
| Arabic Tashkeel | Fatha, Damma, Kasra, Sukoon, etc. (8 chars) | U+064B–U+0652 |

## Deployment

### Vercel

The project is pre-configured for Vercel. Simply connect your repository:

```bash
vercel --prod
```

The `vercel.json` routes:
- `/generate` → FastAPI serverless function
- All other routes → static frontend

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MIN_PASSWORD_LENGTH` | `8` | Minimum allowed length |
| `MAX_PASSWORD_LENGTH` | `256` | Maximum allowed length |
| `HOST` | `0.0.0.0` | Backend bind address |
| `PORT` | `8000` | Backend port |

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn, Pydantic
- **Frontend**: Vanilla HTML/CSS/JS, Chrome Extensions API
- **Infrastructure**: Docker, Vercel, Nginx

## License

[MIT](LICENSE)

## Author

**AbdelRahman Soliman** — [github.com/abdulrahmaninfra](https://github.com/abdulrahmaninfra)
