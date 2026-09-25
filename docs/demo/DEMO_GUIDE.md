\# ManakAI Demo Guide



\## 1. Purpose



This guide explains how to run the ManakAI prototype locally and verify the main application workflow.



ManakAI consists of a React frontend and a FastAPI backend.



\## 2. Prerequisites



Install:



\- Python 3.10 or newer.

\- Node.js 18 or newer.

\- npm.



\## 3. Start the Backend



Open PowerShell in the repository root:



```powershell

cd backend

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

pip install -r requirements.txt

python -m uvicorn main:app --host 127.0.0.1 --port 8000
