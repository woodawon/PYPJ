# listen() - 연결 대기상태 코드 작성을 위한 모듈 import
import socket, _thread

# 서버에 접속하게 된 모든 클라이언트 목록 담을 리스트
client_sockets = []

# 서버 IP, 포트
HOST = "127.0.0.1"
PORT = 8080

# 서버 소켓 생성
print(">> Server Start")
# AF_INET 뜻 : 기본 네트워크 프로토콜(IPv4) / SOCK_STREAM : 소켓 타입
# socket(family, type) -> socket(네트워크 프로토콜 주소, 소켓 타입 지정)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SOL_SOCKET : 소켓 옵션의 레벨 지정(기본 레벨) /  SO_REUSEADDR : 소켓 옵션(재사용 가능)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# IP 및 PORT 할당 - HOST : IP 주소 , PORT : 열어줄 포트의 번호
server_socket.bind((HOST, PORT))
# 연결 대기 상태
server_socket.listen()


# 서버에 접속한 클라이언트마다 새로운 쓰레드가 생성되며 통신
def threaded(client_socket, addr):
    print(">> Connected by :", addr[0], ":", addr[1]) # addr 배열의 0번째 값 : IP 주소, 2번째 값 : client 고유 번호

    # 클라이언트가 접속을 끊을 때 까지 무한반복
    while True:
        try:
            # client_socket : 데이터 수신 소켓 / recv(1024) : 데이터 수신 메서드 -> 최대 1024바이트로 데이터를 한 번에 읽으라고 선언
            # recv() 메서드 : 데이터를 받으면 해당 데이터를 반환함.
            # 즉, data 변수에 클라이언트로부터 받은 데이터가 담기는 거임.
            data = client_socket.recv(1024)

            # 클라이언트로부터 데이터를 모두 받아왔다면, 더이상 받아올 데이터가 없기 때문에 통신 연결을 해제함.
            if not data:
                print(">> Disconnected by " + addr[0], ":", addr[1])
                break

            print(">> Received from " + addr[0], ":", addr[1], data.decode())

            # 서버에 접속한 클라이언트들에게 채팅 보내기
            # 메세지를 보낸 본인을 제외한 서버에 접속한 클라이언트에게 메세지 보내기
            for client in client_sockets:
                if client != client_socket:
                    client.send(data)

        # 연결 종료 후 데이터 전송 및 보안 및 네트워크 연결 문제 발생 시 발생하는 에러
        except ConnectionResetError as e:
            print(">> Disconnected by " + addr[0], ":", addr[1])
            break

    # 지워야 할 고객이 몇 명이나 남았는지 출력시켜줌.
    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print("remove client list : ", len(client_sockets))

    client_socket.close()


try:
    while True:
        print(">> Wait")

        # 클라이언트의 연결 요청 받아오기.
        client_socket, addr = server_socket.accept()
        # 클라이언트 목록 리스트에 클라이언트 값 담기
        client_sockets.append(client_socket)
        # 새로운 스레드 생성 -> 소켓을 배정해 통신
        _thread.start_new_thread(threaded, (client_socket, addr))
        print("참가자 수 : ", len(client_sockets))

except Exception as e:
    print("에러가 발생했습니다.", e)

finally:
    server_socket.close()
