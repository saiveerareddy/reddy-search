# reddy-search
OSINT framework focused on gathering information.

# on Linux
git clone https://github.com/saiveerareddy/reddy-search.git
cd reddy-search
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # edit .env and paste your API keys
# run CLI
python3 main.py --type ip --value 8.8.8.8
# or run the web UI
python3 web_app.py
# open http://127.0.0.1:5000

