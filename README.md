# websockets-practice

# Proxy Sever

Sample usage (all in a different command prompt):
```
python data-request-server-2.py --port 8000
python data-proxy.py --port 8001 8000
netcat localhost 8001
```
Type anything into the netcat prompt and hit \<Enter\>.  You should some messages from the data-request-server and proxy-server.  The request server will return a random number to the netcat client.  

# Streaming Server

Sample usage (in different command prompts):
```
python data-streaming-server.py --port 8000
netcat localhost 8000
netcat localhost 8000
netcat localhost 8000
```

Each client will start receiving a random number every second once connected.  This is a very small pub-sub setup.  
