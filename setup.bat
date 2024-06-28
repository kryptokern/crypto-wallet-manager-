@echo off
REM Clone the repository if it doesn't exist
if not exist crypto-wallet-manager (
    git clone https://github.com/<username>/crypto-wallet-manager.git
)
cd crypto-wallet-manager

REM Set up virtual environment
if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate

REM Install dependencies
pip install web3 requests

REM Run the application
python wallet_manager.py
pause
