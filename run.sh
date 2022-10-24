cp helper.py server/
cd server/
xfce4-terminal -e "python3 server.py $1"
cd ..
cp helper.py client/
cd client/
python3 client.py localhost $1
