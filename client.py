import socket, _thread

HOST = "127.0.0.1"
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 서버에서 bind() 메서드를 활용해 할당해준 IP주소와 PORT번호를 connect()로 클라이언트에 연결
client_socket.connect((HOST, PORT))


# 서버로부터 메세지를 받는 메소드.
def recv_data(client_socket):
    while True:
        # 메세지 받아옴
        data = client_socket.recv(1024)
        # 서버로부터 메시지를 받을 때, 기본적으로 encode 형식으로 받아지기 때문에 decode를 해줘야함.
        print("recive : ", repr(data.decode()))


# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
_thread.start_new_thread(recv_data, (client_socket,))
print(">> Connect Server")

while True:
    message = input("")
    if message == "quit":
        close_data = message
        break

    client_socket.send(message.encode()) # 인코드 형태로 보낸다 -> 서버에서 client_socket.recv(1024) 로 메시지를 받은 후 data.decode()로 디코드한 뒤 출력해 보여준다.

client_socket.close()
