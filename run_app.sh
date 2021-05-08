export FLASK_APP=Agriculta
export FLASK_ENV=development
export DEBUG=1
export FLASK_RUN_PORT=5005

lxterminal --command="lt --port 5005 --subdomain agriculta"
# flask run -h 192.168.1.155
flask run
