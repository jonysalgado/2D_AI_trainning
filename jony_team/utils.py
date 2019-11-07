import math

class Vector2(object):
    """
    Represents a bidimensional geometric vector.
    """
    def __init__(self, x, y):
        """
        Creates a bidimensional geometric vector.

        :param x: x coordinate.
        :type x: float
        :param y: y coordinate.
        :type y: float
        """
        self.x = x
        self.y = y
    
    def normalize(self):
        m = self.magnitude()
        if m == 0:
            self.x = 1
            m = 1
        self.x /= m
        self.y /= m

    def dot(self, v):
        return self.x * v.x + self.y * v.y

    def magnitude(self):
        return math.sqrt((self.x)**2 + (self.y)**2)

class Pose(object):
    """
    Represents a pose on the plane, i.e. a (x, y) position plus a rotation.
    """
    def __init__(self, x, y, rotation):
        """
        Creates a pose on the plane.

        :param x: x coordinate.
        :type x: float
        :param y: y coordinate.
        :type y: float
        :param rotation: rotation around z axis.
        :type rotation: float
        """
        self.position = Vector2(x, y)
        self.rotation = rotation

class TransformCartesian(object):

    def __init__(self, linear_speed, rotation):
        self.x = linear_speed * math.cos(rotation)
        self.y = linear_speed * math.sin(rotation)

class TransformPolar(object):
    
    def __init__(self, x, y):
        self.linear_speed = math.sqrt(x**2 + y**2)
        if x > 1.0e-03:
            self.rotation = math.atan(y/x)
        elif y > 0:
            self.rotation = math.pi
        else:
            self.rotation = -1*math.pi
        if x < 0:
            self.rotation += math.pi
        