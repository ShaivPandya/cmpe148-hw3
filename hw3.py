from socket import *
import ssl
import base64
from getpass import getpass

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

email = input("Email: ")
pw = getpass()

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.gmail.com", 587)

print("Started, creating socket!")
# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

print("Connected, listening!")
recv = clientSocket.recv(1024).decode()
print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO smtp.gmail.com\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)

if recv1[:3] != '250':
    print('250 reply not received from server.')

command = "STARTTLS\r\n"
clientSocket.send(command.encode())
recvdiscard = clientSocket.recv(1024)
print(recvdiscard)

clientSocket = ssl.wrap_socket(clientSocket)

clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)

#Send AUTH first
authMesg = 'AUTH LOGIN\r\n'
crlfMesg = '\r\n'

clientSocket.send(authMesg.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)

e = base64.b64encode(email.encode())
clientSocket.send(e)
clientSocket.send(crlfMesg.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)

p = base64.b64encode(pw.encode())
clientSocket.send(p)
clientSocket.send(crlfMesg.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)

# Send MAIL FROM command and print server response.
mailFromCommand = 'MAIL FROM: <' + email + '>\r\n'
clientSocket.send(mailFromCommand.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptToCommand = 'RCPT TO: <' + email + '>\r\n'
clientSocket.send(rcptToCommand.encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)
if recv7[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv8 = clientSocket.recv(1024).decode()
print(recv8)
if recv8[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
clientSocket.send(msg.encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)
if recv9[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv10 = clientSocket.recv(1024).decode()
print(recv10)
if recv10[:3] != '221':
    print('221 reply not received from server.')
