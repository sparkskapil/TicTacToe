import socket
import threading
from ECS.Scriptable import Scriptable, Event, StateEvent
from ECS.Components import ButtonComponent, TagComponent, SpriteComponent, LabelComponent
import Global


class MenuButton(Scriptable):
    def __init__(self, scene, entity):
        Scriptable.__init__(self, scene, entity)

    def Setup(self):
        self.IsBusy = False
        self.Hosts = list()
        self.Lock = threading.Lock()
        self.IpCount = 0
        if Global.IsHost == False:
            entt = self.GetEntitiesByTag("LobbyLabel_1")[0]
            entt.GetComponent(LabelComponent).text = "Searching hosts"
            self.FindHosts()

    def Update(self, timestep):
        pass

    def __checkIpOnThread(self, sock, address, maxCount):
        if sock.connect_ex(address) == 0:
            self.Hosts.append(address[0])
        self.Lock.acquire()
        self.IpCount += 1
        if self.IpCount == maxCount:
            self.Busy = False
        self.Lock.release()

    def FindHosts(self):
        self.IsBusy = True
        # getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        # getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        # scan lan hosts
        ipArr = ip_address.split('.')
        gamePort = 8080
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for i in range(1, 255):
            ipArr[-1] = str(i)
            ip = '.'.join(ipArr)
            thread = threading.Thread(target=self.__checkIpOnThread,
                                      args=(sock, (ip, gamePort), 254))
            thread.start()
        sock.close()

    def onButtonClick(self, button):
        pass

    def onButtonHover(self, hovered, entity):
        pass
