import numpy as np
from shapely.geometry.polygon import Polygon
import math
import matplotlib.pyplot as plt

class Area:

    def __init__(self, pontos):
        self.pontos = pontos
        np_pontos = np.array(self.pontos)
        self.lista_x = np_pontos[:,0]
        self.lista_y = np_pontos[:,1]
        self.poligonos = {}
        return


    def Criar_Poligono(self, nome, poligono_pontos):
        self.poligonos[nome] = Polygon([i for i in poligono_pontos]),
        return

    def get_poligono(self, nome):
        if nome in self.poligonos.keys():
            return self.poligonos[nome]
        return None

    def get_poligonos(self):
        return self.poligonos

    def connectpoints(self, p1,p2):
        x1, x2 = p1[0], p2[0]
        y1, y2 = p1[1], p2[1]
        plt.plot([x1,x2],[y1,y2],'k-')
        return

    def connecting(self, points):
        for p in range(len(points)-1):
            self.connectpoints(points[p], points[p+1])
    
        return

    def desenhar_ponto(self, x, y, marcador):
        plt.plot(x, y, marcador)
        return
        
    def desenhar_area(self, beacons=[]):        
        for pol in self.poligonos.values():
            self.connecting(pol[0].exterior.coords[:])

        plt.plot(self.lista_x, self.lista_y, 'o')

        if beacons:
            for pos, beacon in enumerate(beacons):
                plt.plot(beacon.get_x(), beacon.get_y(), 'ro')
                plt.text(beacon.get_x()+0.2, beacon.get_y()+0.1, str(pos+1))
            
        plt.savefig('area/area.png')
        plt.close()

        return

    def achar_coordenada(self, p3, circle_intersection, result):
        if (circle_intersection[0] == 0 and circle_intersection[1] == 0):
            return (False, circle_intersection[2])

        if math.dist(p3, circle_intersection[0]) == result:
            return (True, circle_intersection[0])
        return (True, circle_intersection[1])