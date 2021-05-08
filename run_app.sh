export FLASK_APP=Agriculta
export FLASK_ENV=development
export DEBUG=1
export FLASK_RUN_PORT=5005
echo "localtunnel"
lt -h "https://test.pi" --port 5005
echo "end local tunnel"
echo $link
# flask run -h 192.168.1.155
flask run
