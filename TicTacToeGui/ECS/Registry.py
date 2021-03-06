import inspect


def isclass(obj):
    """Return true if the object is a class.

    Class objects provide these attributes:
        __doc__         documentation string
        __module__      name of module in which this class was defined"""
    return inspect.isclass(obj)


def GetTypeName(obj):
    if isclass(obj):
        return obj.__name__
    else:
        return obj.__class__.__name__


class Registry:
    ENTITYId = 0

    def __init__(self):
        self.entities = list()
        self.components = dict()
        self.repository = dict()

    def CreateEntity(self):
        self.ENTITYId += 1
        entity = self.ENTITYId
        self.entities.append(entity)
        self.components[entity] = dict()
        return entity

    def AttachComponent(self, entity, component):
        Type = GetTypeName(component)
        self.components[entity][Type] = component
        if not Type in self.repository.keys():
            self.repository[Type] = list()
        self.repository[Type].append((component, entity))

        return component

    def GetEntity(self, component):
        Type = GetTypeName(component)
        for comp, ent in self.repository[Type]:
            if comp == component:
                return ent
        return None

    def GetComponentsByType(self, typename):
        Type = GetTypeName(typename)
        if Type in self.repository.keys():
            return self.repository[Type]
        return list()

    def GetComponent(self, entity, typename):
        Type = GetTypeName(typename)
        if entity in self.components.keys() and Type in self.components[entity].keys():
            return self.components[entity][Type]
        return None

    def GetComponentsGroup(self, entity):
        self.componentsGroup = self.components[entity]
        result = list()
        for Type, component in self.componentsGroup.items():
            result.append(component)
        return result

    def RemoveComponent(self, entity, component):
        Type = GetTypeName(component)
        removedComponent = self.components[entity].pop(Type)
        if (removedComponent, entity) in self.repository[Type]:
            self.repository[Type].remove((removedComponent, entity))
        return removedComponent

    def RemoveEntity(self, entity):
        self.entities.remove(entity)
        componentsToRemove = self.components.pop(entity)
        for Type in componentsToRemove.keys():
            self.repository[Type].remove((componentsToRemove[Type], entity))
    
    def HasComponent(self, entity, component):
        Type = GetTypeName(component)
        return Type in self.components[entity].keys()
            


if __name__ == "__main__":
    class TransformComponent:
        def __init__(self):
            self.position = (0, 0, 0)
            self.rotation = (0, 0, 0)
            self.scale = 1

        def __repr__(self):
            return "Position:{}, Rotation:{}, Scale:{}".format(self.position, self.rotation, self.scale)
    reg = Registry()
    entity = reg.CreateEntity()
    reg.AttachComponent(entity, TransformComponent())
    component = reg.GetComponent(entity, TransformComponent)
    e = reg.GetEntity(component)
    print(e)
