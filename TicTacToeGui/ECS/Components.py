import math


class Vector:
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, Vector):
            self.x = x.x
            self.y = x.y
            self.z = x.z

        elif isinstance(x, tuple):
            self.x = x[0] if len(x) > 0 else 0
            self.y = x[1] if len(x) > 1 else 0
            self.z = x[2] if len(x) > 2 else 0

        else:
            self.x = x
            self.y = y
            self.z = z

    def Add(self, vector):
        if not isinstance(vector, Vector):
            raise TypeError('Require vector to perform vector addition')
        return Vector(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def Subtract(self, vector):
        if not isinstance(vector, Vector):
            raise TypeError('Require vector to perform vector subtraction')
        return Vector(self.x - vector.x, self.y - vector.y, self.z - vector.z)

    def Mult(self, scalar):
        if not isinstance(n, int) and isinstance(n, float):
            raise TypeError('Require scalar to perform scalar multiplication')
        return Vector(self.x*scalar, self.y*scalar, self.z*scalar)

    def Dot(self, vector):
        if not isinstance(vector, Vector):
            raise TypeError('Require vector to perform dot product')
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def Cross(self, vector):
        if not isinstance(vector, Vector):
            raise TypeError('Require vector to perform dot product')
        I = self.y * vector.z - self.z * vector.y
        J = - self.x * vector.z - self.z * vector.x
        K = self.x * vector.y - self.y * vector.x
        return Vector(I, J, K)

    def Magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def Normalize(self):
        magnitude = self.Magnitude()
        return Vector(self.x/magnitude, self.y/magnitude, self.z/magnitude)

    def __repr__(self):
        return '({})i + ({})j + ({})k'.format(self.x, self.y, self.z)


class TransformComponent:
    def __init__(self, position, rotation):
        if not isinstance(position, Vector) and not isinstance(position, tuple):
            raise TypeError("Position must be a vector or tuple")
        if isinstance(position, tuple):
            position = Vector(position)
        self.position = position

        if not isinstance(rotation, Vector) and not isinstance(rotation, tuple):
            raise TypeError("Position must be a vector or tuple")
        if isinstance(rotation, tuple):
            rotation = Vector(rotation)
        self.rotation = rotation

    def __repr__(self):
        return 'Position: {} \nRotation: {} radians'.format(self.position.__repr__(), self.rotation.__repr__())


class TagComponent:
    def __init__(self, name="Unnamed Object"):
        self.name = name

    def __repr__(self):
        return 'Tag: {}'.format(self.name)


transformComp = TransformComponent((1, 2), (0, 0))
TagComponent = TagComponent("Cube")

print(transformComp)
print(TagComponent)
