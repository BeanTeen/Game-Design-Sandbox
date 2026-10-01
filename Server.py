import socket
import threading
import pickle

players={}

def threaded_client(conn, player_id):
    if player_id not in players:
        start_y=200 if player_id % 2==0 else 300
        start_color="blue" if player_id % 2==0 else "green"
        players[player_id]={"x":200, "y": start_y, "color": start_color, "facing_right": True}
    
    conn.send(pickle.dumps(players[player_id]))
    
    while True:
        try:
            data=pickle.loads(conn.recv(2048))
            
            if not data:
                print("Disconnected")
                break
            else:
                players[player_id]=data
                
                conn.sendall(pickle.dumps(players))
        except:
            break
        
    print(f"Player {player_id} Disconnected")
    if player_id in players:
        del players[player_id]
    conn.close()

def start_server(host="0.0.0.0", port=5555):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((host, port))
    except socket.error as e:
        print(f"server bind error: {e}")

    s.listen()
    print(f"server listening on {host}:{port}")

    p_count=0
    while True:
        try:
            conn, addr = s.accept()
            print(f"Connected to {addr}")
            thread=threading.Thread(target=threaded_client, args=(conn, p_count), daemon=True)
            thread.start()
            p_count+=1
        except Exception as e:
            print(f"Accept Error: {e}")
            break
if __name__ == "__main__":
    start_server("127.0.0.1", 5555)