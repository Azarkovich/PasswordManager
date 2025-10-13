
#!/bin/sh
set -eu 

cd /media/snow/DATA/Code/PassMan

. .venv/bin/activate

exec python app.py
