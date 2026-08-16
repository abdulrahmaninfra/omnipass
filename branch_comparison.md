# Branch Comparison: `main` vs `refactoring`

This document outlines the key differences, architectural improvements, and new features introduced in the `refactoring` branch compared to the `main` branch.

## 1. Backend Modularization 🏗️
- **Main Branch:** The entire backend was tightly coupled and packed into a single monolithic `backend/main.py` file.
- **Refactoring Branch:** The backend has been completely restructured into a clean, scalable architecture under `backend/src/`. Concerns are now cleanly separated:
  - `src/api/` contains API routing and endpoints.
  - `src/core/` handles configurations, constants, and the core password generation logic.
  - `src/models/` contains Pydantic schemas for request and response validation.

## 2. Performance & Connection Management ⚡
- **Main Branch:** Handled connections without robust lifecycle management or pooling optimizations.
- **Refactoring Branch:** 
  - **Backend:** Implemented HTTP connection pooling via FastAPI's `lifespan` context manager using `httpx.AsyncClient`. Explicit connection limits (`max_connections` and `max_keepalive_connections`) ensure stability and performance under load.
  - **Frontend/Extension:** Implemented request cancellation using `AbortController` and `keepalive: true`. If a user rapidly moves the length slider, stale requests are immediately aborted to prevent queuing and reduce server load.

## 3. Configuration and Security 🔒
- **Main Branch:** CORS allowed all origins (`["*"]`), and environment variables were fetched directly using `os.getenv` without type safety.
- **Refactoring Branch:** 
  - Environment variables are now validated and managed centrally using Pydantic Settings in `src/core/config.py`.
  - CORS is dynamically restricted via an `ALLOWED_ORIGINS` setting, ensuring the Vercel deployment only accepts traffic from explicitly allowed domains (such as the browser extension).

## 4. Frontend Features ✨
- **Main Branch:** Only included a "Copy" button.
- **Refactoring Branch:** Added a new **"Regenerate"** button next to the "Copy" button on both the main website (`index.html`) and the browser extension (`popup.html`). This gives users a clear, 1-click way to generate a new password without adjusting the existing settings.

## 5. CI/CD Integration 🤖
- **Main Branch:** Lacked automated testing or code validation pipelines.
- **Refactoring Branch:** Introduced a GitHub Actions workflow (`.github/workflows/ci.yml`) to automatically run linting and `pytest` for the backend on every push or pull request, ensuring continuous integration and code quality.

## Summary
The `refactoring` branch elevates the OmniPass backend from a simple monolithic script to a robust, scalable application with best practices in API architecture, security, and connection management.
