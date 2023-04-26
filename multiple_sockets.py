import socket
from threading import Thread
from multiprocessing import Process, Queue, Array, Value
import time

import os
from _thread import *

    
def init_machine(config):
    HOST = str(config[0])
    PORT = int(config[1])
    print("starting server| port val:", PORT)#, "clock rate:", clock_rate)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        start_new_thread(consumer, (conn,addr,))
        print("consumer thread started for connection", addr)
    # close connection
    s.close()
    print("server closed", addr)

def consumer(conn,addr):
    # each machine listens on its own consumer thread, which initializes its queue
    print("consumer accepted connection" + str(addr)+"\n")
    while True: 
        data = conn.recv(1024)
        dataVal = data.decode('ascii')



def producer(portVal1, portVal2):
    # tries to initiate connection to another port

    host = "127.0.0.1" # localhost
    port_first = int(portVal1)
    port_second = int(portVal2)
    s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # TODO: keep track of which port is connected to which socket

    #sema acquire
    try:
        s1.connect((host,port_first))
        print("Client-side connection success to port val:" + str(portVal1) + "\n")
        s2.connect((host,port_second))
        print("Client-side connection success to port val:" + str(portVal2) + "\n")

        while True:
            # close old connections
            if len(remove_port_queue) > 0:
                old_port = remove_port_queue.pop()
                print("old port received: ", old_port)
                if old_port == port_first:
                    s1.close()
                    print("Client-side connection closed to port val:" + str(portVal1) + "\n")
                elif old_port == port_second:
                    s2.close()
                    print("Client-side connection closed to port val:" + str(portVal2) + "\n")

            # start up new connections
            if len(add_port_queue) > 0:
                new_port = add_port_queue.pop()
                print("new port received: ", new_port)
                s3 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s3.connect((host,new_port)) # 5555 not set up to listen yet
            

    except socket.error as e:
        print ("Error connecting producer: %s" % e)



def machine(config):
    config.append(os.getpid())

    # initialize number of available ports
    global num_ports
    num_ports = 100 # make dynamic


    # initialize the add_port and remove_port queues for the process
    global add_port_queue
    add_port_queue = []

    global remove_port_queue
    remove_port_queue = []

    global my_port
    my_port = config[1]

    # initialize listeners
    init_thread = Thread(target=init_machine, args=(config,)) # start a thread for the consumer, to listen
    init_thread.start()

    #add delay to initialize the server-side logic on all processes
    time.sleep(3)

    # extensible to multiple producers, we just use one producer that connects to two threads though
    prod_thread = Thread(target=producer, args=(config[2], config[3],)) # start a thread for the producer, to send
    prod_thread.start()
    
    arr = config[4]
    # if current server is a switch server, then it will listen for changes in the global edges list
    
    if my_port%10 == 1:
        print("hi!")
        while True:
            if arr[0] == 5:
                print("switch server", my_port, "is listening for changes in the global edges list")
                arr[0] = 0
                print(arr[:])
            # check if global edges list has changed; if so update the links

        # add delay to initialize the client-side logic on all processes
        # time.sleep(3)
        # add_port_queue.append(5555)
        time.sleep(2)
        remove_port_queue.append(5551)




localHost= "127.0.0.1"
    

if __name__ == '__main__':
    port1 = 5551
    port2 = 5552
    port3 = 5553
    
    arr = Array('i', 10)
    arr[0] = 5

    # each config is structured as [host, listening port, sending port 1, sending port 2]
    config1=[localHost, port1, port2, port3, arr]
    p1 = Process(target=machine, args=(config1,))
    config2=[localHost, port2, port3, port1, arr]
    p2 = Process(target=machine, args=(config2,))
    config3=[localHost, port3, port1, port2, arr]
    p3 = Process(target=machine, args=(config3,))
    
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()

    print("here")
    time.sleep(12)
    print("here2")
    arr[0]=5

    