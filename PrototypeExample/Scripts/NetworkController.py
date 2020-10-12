import socket
import threading
from ECS.Scriptable import Scriptable, Event, StateEvent
from ECS.Components import ButtonComponent, TagComponent, LabelComponent
from ECS.Components import Vector, TransformComponent
import Global


class MenuButton(Scriptable):
    def __init__(self, scene, entity):
        Scriptable.__init__(self, scene, entity)

    def Setup(self):
        self.IsBusy = None
        self.Hosts = list()
        self.Lock = threading.Lock()
        self.IpCount = 0
        if Global.IsHost == False:
            entt = self.GetEntitiesByTag("LobbyLabel_1")[0]
            label = entt.GetComponent(LabelComponent)
            label.text = "Searching hosts"
            self.IsBusy = True
            self.FindHosts()

    def Update(self, timestep):
        if self.IsBusy == False and len(self.Hosts):
            position = Vector(150, 265, 0)
            for i, host in enumerate(self.Hosts):
                position.y += i*50
                ent = self.CreateEntity()
                ent.GetComponent(TransformComponent).position = position
                label = ent.AddComponent(LabelComponent(host, 'Fonts/FreeSansBold.ttf'))
            self.IsBusy = None
        if self.IsBusy == False and len(self.Hosts) == 0:
            position = Vector(125, 265, 0)
            ent = self.CreateEntity()
            ent.GetComponent(TransformComponent).position = position
            label = ent.AddComponent(LabelComponent())
            label.text = 'No hosts available.'
            label.font = 'Fonts/FreeSansBold.ttf'
            label.size = 24
            self.IsBusy = None

    def __checkIpOnThread(self, sock, address, maxCount):
        connected = False
        if sock.connect_ex(address) == 0:
            connected = True
        self.Lock.acquire()
        self.IpCount += 1
        if connected:
            self.Hosts.append(address[0])
        if self.IpCount == maxCount:
            self.IsBusy = False
        self.Lock.release()

    def FindHosts(self):
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
