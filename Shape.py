import math
class Point:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def get_x(self):
        return self._x

    def set_x(self, x):
        if isinstance(x, (int, float)):
            self._x = x
        else:
            print("Error: La coordenada x debe ser numérica.")

    def get_y(self):
        return self._y

    def set_y(self, y):
        if isinstance(y, (int, float)):
            self._y = y
        else:
            print("Error: La coordenada y debe ser numérica.")

    def __repr__(self):
        return f"Point({self._x}, {self._y})"

class Line:
    def __init__(self, start=None, end=None):
        # Si no se proporcionan puntos, inicializamos en (0,0)
        if start is None:
            start = Point()
        if end is None:
            end = Point()
        self._start = start
        self._end = end
        self._length = self.compute_length()
        self._slope = self.compute_slope()

    def get_start(self):
        return self._start

    def set_start(self, start):
        if isinstance(start, Point):
            self._start = start
            self._length = self.compute_length()
            self._slope = self.compute_slope()
        else:
            print("Error: El punto de inicio debe ser un objeto Point.")

    def get_end(self):
        return self._end

    def set_end(self, end):
        if isinstance(end, Point):
            self._end = end
            self._length = self.compute_length()
            self._slope = self.compute_slope()
        else:
            print("Error: El punto final debe ser un objeto Point.")

    def get_length(self):
        return self._length

    def get_slope(self):
        return self._slope

    # Método para calcular longitud usando distancia euclidiana
    def compute_length(self):
        dx = self._end.get_x() - self._start.get_x()
        dy = self._end.get_y() - self._start.get_y()
        length = math.sqrt(dx**2 + dy**2)
        return length

    # Método para calcular pendiente en grados
    def compute_slope(self):
        dx = self._end.get_x() - self._start.get_x()
        dy = self._end.get_y() - self._start.get_y()
        # Prevenir división por cero y casos verticales
        if dx == 0:
            slope_deg = 90.0 if dy > 0 else -90.0
        else:
            slope_rad = math.atan2(dy, dx)
            slope_deg = math.degrees(slope_rad)
        return slope_deg

    def __repr__(self):
        return f"Line(Start={self._start}, End={self._end})"

class Shape:
    def __init__(self, vertices=None, edges=None, inner_angles=None, is_regular=False):
        # Se usan listas vacías si no se proporcionan
        self._vertices = vertices if vertices is not None else []
        self._edges = edges if edges is not None else []
        self._inner_angles = inner_angles if inner_angles is not None else []
        self._is_regular = is_regular

    def get_vertices(self):
        return self._vertices

    def set_vertices(self, vertices):
        if isinstance(vertices, list) and all(isinstance(v, Point) for v in vertices):
            self._vertices = vertices
        else:
            print("Error: vertices debe ser una lista de objetos Point.")

    def get_edges(self):
        return self._edges

    def set_edges(self, edges):
        if isinstance(edges, list) and all(isinstance(e, Line) for e in edges):
            self._edges = edges
        else:
            print("Error: edges debe ser una lista de objetos Line.")

    def get_inner_angles(self):
        return self._inner_angles

    def set_inner_angles(self, angles):
        if isinstance(angles, list) and all(isinstance(a, (int, float)) for a in angles):
            self._inner_angles = angles
        else:
            print("Error: inner_angles debe ser una lista de números.")

    def get_is_regular(self):
        return self._is_regular

    def set_is_regular(self, is_regular):
        if isinstance(is_regular, bool):
            self._is_regular = is_regular
        else:
            print("Error: is_regular debe ser booleano.")

    def compute_area(self):
        print("compute_area no implementado para Shape base.")
        return None

    def compute_perimeter(self):
        print("compute_perimeter no implementado para Shape base.")
        return None

    def compute_inner_angles(self):
        print("compute_inner_angles no implementado para Shape base.")
        return None

class Triangle(Shape):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices=vertices, edges=edges)
        if vertices and len(vertices) == 3:
            self._edges = [
                Line(vertices[0], vertices[1]),
                Line(vertices[1], vertices[2]),
                Line(vertices[2], vertices[0])
            ]
        elif edges and len(edges) == 3:
            self._vertices = [
                edges[0].get_start(),
                edges[0].get_end(),
                edges[1].get_end()
            ]
        else:
            print("Error: Un triángulo debe tener 3 vértices o 3 aristas.")

    def compute_area(self):
        # Fórmula de Herón
        a = self._edges[0].get_length()
        b = self._edges[1].get_length()
        c = self._edges[2].get_length()
        s = (a + b + c) / 2
        try:
            area = math.sqrt(s * (s - a) * (s - b) * (s - c))
            return area
        except ValueError:
            print("Error: No es un triángulo válido para cálculo de área.")
            return 0

    def compute_perimeter(self):
        perimeter = sum(edge.get_length() for edge in self._edges)
        return perimeter

    def compute_inner_angles(self):
        # Calculamos usando la ley de cosenos
        a = self._edges[0].get_length()
        b = self._edges[1].get_length()
        c = self._edges[2].get_length()
        try:
            angle_A = math.degrees(math.acos((b**2 + c**2 - a**2) / (2*b*c)))
            angle_B = math.degrees(math.acos((a**2 + c**2 - b**2) / (2*a*c)))
            angle_C = 180 - angle_A - angle_B
            self._inner_angles = [angle_A, angle_B, angle_C]
            return self._inner_angles
        except ValueError:
            print("Error: Ángulos no válidos para triángulo.")
            return []

class Isosceles(Triangle):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices, edges)
        self.set_is_regular(False)
        # Validamos lados iguales
        lengths = [edge.get_length() for edge in self._edges]
        # Comprobamos si al menos dos lados son iguales (dentro de tolerancia)
        tolerance = 1e-6
        sides_equal = (
            abs(lengths[0] - lengths[1]) < tolerance or
            abs(lengths[1] - lengths[2]) < tolerance or
            abs(lengths[2] - lengths[0]) < tolerance
        )
        if not sides_equal:
            print("Advertencia: Este triángulo no cumple la condición de isósceles.")

class Equilateral(Triangle):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices, edges)
        self.set_is_regular(True)
        lengths = [edge.get_length() for edge in self._edges]
        tolerance = 1e-6
        if not (abs(lengths[0] - lengths[1]) < tolerance and abs(lengths[1] - lengths[2]) < tolerance):
            print("Advertencia: Este triángulo no es equilátero.")

class Scalene(Triangle):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices, edges)
        self.set_is_regular(False)
        lengths = [edge.get_length() for edge in self._edges]
        tolerance = 1e-6
        if (abs(lengths[0] - lengths[1]) < tolerance or
            abs(lengths[1] - lengths[2]) < tolerance or
            abs(lengths[2] - lengths[0]) < tolerance):
            print("Advertencia: Este triángulo no es escaleno (tiene lados iguales).")

class TriRectanble(Triangle):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices, edges)
        self.set_is_regular(False)
        self.compute_inner_angles()
        if 90 not in [round(angle) for angle in self._inner_angles]:
            print("Advertencia: Este triángulo no es rectángulo (no tiene un ángulo de 90 grados).")

class Rectangle(Shape):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices=vertices, edges=edges)
        self.set_is_regular(True)

        # Si vertices son dados, construimos las aristas
        if vertices and len(vertices) == 4:
            self._edges = [
                Line(vertices[0], vertices[1]),
                Line(vertices[1], vertices[2]),
                Line(vertices[2], vertices[3]),
                Line(vertices[3], vertices[0])
            ]
        elif edges and len(edges) == 4:
            self._vertices = [
                edges[0].get_start(),
                edges[0].get_end(),
                edges[1].get_end(),
                edges[2].get_end()
            ]
        else:
            print("Error: Un rectángulo debe tener 4 vértices o 4 aristas.")

        # Se asumen lados opuestos iguales
        self._width = self._edges[0].get_length()
        self._height = self._edges[1].get_length()

    def compute_area(self):
        return self._width * self._height

    def compute_perimeter(self):
        return 2 * (self._width + self._height)

    def compute_inner_angles(self):
        self._inner_angles = [90, 90, 90, 90]
        return self._inner_angles

class Square(Rectangle):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices, edges)
        self.set_is_regular(True)
        # Valida que todos los lados sean iguales
        sides = [edge.get_length() for edge in self._edges]
        tolerance = 1e-6
        if not all(abs(sides[0] - s) < tolerance for s in sides[1:]):
            print("Advertencia: Este cuadrado no tiene todos los lados iguales.")
