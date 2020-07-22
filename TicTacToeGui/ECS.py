import inspect


def isclass(object):
    """Return true if the object is a class.

    Class objects provide these attributes:
        __doc__         documentation string
        __module__      name of module in which this class was defined"""
    return inspect.isclass(object)


def GetTypeName(object):
    if isclass(object):
        return object.__name__
    else:
        return object.__class__.__name__


class ECS:
    ENTITYId = 0
    entities = list()
    components = dict()
    repository = dict()

    def CreateEntity():
        entity = ECS.ENTITYId+1
        ECS.entities.append(entity)
        return entity

    def AttachComponent(entity, component):
        Type = GetTypeName(component)
        if not entity in ECS.components.keys():
            ECS.components[entity] = dict()
        ECS.components[entity][Type] = component

        if not Type in ECS.repository.keys():
            ECS.repository[Type] = list()
        ECS.repository[Type].append((component, entity))

    def GetEntity(component):
        Type = GetTypeName(component)
        for comp, ent in ECS.repository[Type]:
            if comp == component:
                return ent

    def GetComponentsByType(typename):
        Type = GetTypeName(typename)
        return ECS.repository[Type]

    def GetComponent(entity, typename):
        Type = GetTypeName(typename)
        return ECS.components[entity][Type]

    def GetComponentsGroup(entity):
        ECS.componentsGroup = ECS.components[entity]
        result = list()
        for Type, component in ECS.componentsGroup.items():
            result.append(component)
        return result


if __name__ == "__main__":
    class TransformComponent:
        def __init__(self):
            self.position = (0, 0, 0)
            self.rotation = (0, 0, 0)
            self.scale = 1

        def __repr__(self):
            return "Position:{}, Rotation:{}, Scale:{}".format(self.position, self.rotation, self.scale)

    entity = ECS.CreateEntity()
    ECS.AttachComponent(entity, TransformComponent())
    component = ECS.GetComponent(entity, TransformComponent)
    e = ECS.GetEntity(component)
    print(e)
