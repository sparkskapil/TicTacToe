'''
Module contains all components supported by engine
'''
import math
import inspect

class Vector:
    # pylint: disable=invalid-name
    """
    Represents vectors in maths/physics.
    Vectors are used to represent quantity which have
    magnitude and direction
    """

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
        """
        Returns a vector with addition of the 2 operating vectors.

        Parameters:
        vector (Vector) : Vector to be added.

        Returns:
        Vector : New vector with addition of the 2 operating vectors.

        Raises:
        TypeError: If type of vector parameter is not Vector.
        """
        if not isinstance(vector, Vector):
            raise TypeError('Require vector to perform vector addition')
        return Vector(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def Subtract(self, vector):
        """
        Returns a vector with difference of the 2 operating vectors.

        Parameters:
        vector (Vector) : Vector to be subtracted.

        Returns:
        Vector : New vector with difference of the 2 operating vectors.

        Raises:
        TypeError: If type of vector parameter is not Vector.
        """
        if not isinstance(vector, Vector):
            raise TypeError('Require vector to perform vector subtraction')
        return Vector(self.x - vector.x, self.y - vector.y, self.z - vector.z)

    def Mult(self, scalar):
        """
        Returns a vector with product of the vector with scalar.
        This operation scales the magnitude of the operation vector.

        Parameters:
        scalar (int or float) : Vector to be subtracted.

        Returns:
        Vector : New vector with product of the vector with scalar.

        Raises:
        TypeError: If type of `scalar` parameter is not of type `int` or `float`.
        """
        if not isinstance(scalar, int) and isinstance(scalar, float):
            raise TypeError('Require scalar to perform scalar multiplication')
        return Vector(self.x*scalar, self.y*scalar, self.z*scalar)

    def Dot(self, vector):
        """
        Returns a scalar value for dot product of the 2 operating vectors.

        Parameters:
        vector (Vector) : Vector to perform dot product with.

        Returns:
        float : Scalar representing dot product 2 operating vectors.

        Raises:
        TypeError: If type of vector parameter is not Vector.
        """
        if not isinstance(vector, Vector):
            raise TypeError('Require vector to perform dot product')
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def Cross(self, vector):
        """
        Returns a Vector resulting from cross product of the 2 operating vectors.

        Parameters:
        vector (Vector) : Vector to perform cross product with.

        Returns:
        Vector : New vector with cross product of the 2 operating vectors.

        Raises:
        TypeError: If type of vector parameter is not Vector.
        """
        if not isinstance(vector, Vector):
            raise TypeError('Require vector to perform cross product')
        I = self.y * vector.z - self.z * vector.y
        J = - self.x * vector.z - self.z * vector.x
        K = self.x * vector.y - self.y * vector.x
        return Vector(I, J, K)

    def Magnitude(self):
        """
        Returns magnitude of this vector.
        Returns:
        float : Magnitude of this vector.
        """
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def Normalize(self):
        """
        Returns a unit vector along the direction of this vector.
        Magnitude of a normalized vector will always be 1.
        Returns:
        Vector : New unit vector along the direction of this vector.
        """
        magnitude = self.Magnitude()
        return Vector(self.x/magnitude, self.y/magnitude, self.z/magnitude)

    def __repr__(self):
        return '({})i + ({})j + ({})k'.format(self.x, self.y, self.z)


class TransformComponent:
    def __init__(self, position=Vector(), rotation=Vector()):
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
        return '[TransformComponent]\nPosition: {} \nRotation: {} radians'.format(self.position.__repr__(), self.rotation.__repr__())


class TagComponent:
    def __init__(self, name="Unnamed Object"):
        self.name = name

    def __repr__(self):
        return '[TagComponent]\nTag: {}'.format(self.name)


class SpriteComponent:
    class SpriteMode:
        Original = 1
        Fit = 2
        RespectAspect = 3

    def __init__(self, imagepath="", width=None, height=None, mode=SpriteMode.Original):
        self.image = imagepath
        self.width = width
        self.height = height
        self.mode = mode

    def __repr__(self):
        return '[SpriteComponent]\nImage: {}\nWidth: {}\nHeight:{}\n'.format(self.image, self.width, self.height)


class LabelComponent:
    def __init__(self, text="", font=None, fontSize=32, foreground=(255, 255, 255), background=None):
        self.text = text
        self.font = font
        self.size = fontSize
        self.color = foreground
        self.background = background

    def __repr__(self):
        return "[LabelComponent]\nText: {}\nFont: {}\nSize: {}\nColor: {}\nBackground:{}".format(self.text, self.font, self.size, self.color, self.background)


class ButtonComponent:
    def __init__(self, width, height, action, enabled=True):
        self.action = action
        self.width = width
        self.height = height
        self.enabled = enabled

    def GetActionName(self):
        action = self.action.__name__
        if action == "<lambda>":
            action = inspect.getsource(self.action).split("lambda:")[1].strip()
        return action

    def __repr__(self):
        action = self.GetActionName()
        return "[ButtonComponent]\nAction: {} \nWidth: {} \nHeight: {} \nEnabled: {}".format(action, self.width, self.height, self.enabled)


class ScriptComponent:
    def __init__(self, module="", classname=""):
        self.Module = module
        self.Class = classname

    def __repr__(self):
        return "[ScriptComponent]\nModule: {} \nClass: {}".format(self.Module, self.Class)


if __name__ == "__main__":
    transformComp = TransformComponent((1, 2), (0, 0))
    tagComponent = TagComponent("Cube")
    sprite = SpriteComponent("spriteImage.png", 100, 100)

    print(transformComp)
    print(tagComponent)
    print(sprite)
