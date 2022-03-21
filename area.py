import numpy as np
from shapely.geometry.polygon import Polygon
import math

class Area:

    def __init__(self, pontos):
        self.pontos = pontos
        np_pontos = np.array(self.pontos)
        self.lista_x = np_pontos[:,0]
        self.lista_y = np_pontos[:,1]
        self.poligonos = {}
        return


    def Criar_Poligono(self, nome, poligono_pontos):
        self.poligonos = {
            nome: Polygon([self.pontos[i] for i in poligono_pontos]),
        }
        return

    def get_poligono(self, nome):
        if nome in self.poligonos.keys():
            return self.poligonos[nome]
        return None

    def get_poligonos(self):
        return self.poligonos

    def achar_coordenada(self, p3, circle_intersection, result):
        if (circle_intersection[0] == 0 and circle_intersection[1] == 0):
            return (False, circle_intersection[2])

        if math.dist(p3, circle_intersection[0]) == result:
            return (True, circle_intersection[0])
        return (True, circle_intersection[1])