import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from flask import Flask
from flask_cors import CORS
from flask import request
from beacon import Beacon
import math
from circle import Circle

def connectpoints(p1,p2):
    x1, x2 = x_list[p1], x_list[p2]
    y1, y2 = y_list[p1], y_list[p2]
    plt.plot([x1,x2],[y1,y2],'k-')
    return

def connecting(p):
    points = p + [p[0]]
    for p in range(len(points)-1):
        connectpoints(points[p], points[p+1])
    
    return

def create_sala_blue():
    plt.plot(x_list, y_list, 'o')

    connecting(pontos_cafe)
    connecting(pontos_sala_reuniao)
    connecting(pontos_sala_socios)
    connecting(pontos_copa)
    connecting(pontos_area_trabalho)
    
    plt.plot(beacon_1.get_x(), beacon_1.get_y(), 'ro')
    plt.text(beacon_1.get_x()+0.2, beacon_1.get_y(), '1')
    plt.plot(beacon_2.get_x(), beacon_2.get_y(), 'ro')
    plt.text(beacon_2.get_x()-0.5, beacon_2.get_y(), '2')
    plt.plot(beacon_3.get_x(), beacon_3.get_y(), 'ro')
    plt.text(beacon_3.get_x()+0.2, beacon_3.get_y(), '3')
    plt.plot(beacon_4.get_x(), beacon_4.get_y(), 'ro')
    plt.text(beacon_4.get_x()+0.2, beacon_4.get_y(), '4')
    plt.plot(beacon_5.get_x(), beacon_5.get_y(), 'ro')
    plt.text(beacon_5.get_x()-0.5, beacon_5.get_y(), '5')
    
    return

def find_fourth_coordinate(p3, circle_intersection, result):
    if (circle_intersection[0] == 0 and circle_intersection[1] == 0):
        return (False, circle_intersection[2])

    if math.dist(p3, circle_intersection[0]) == result:
        return (True, circle_intersection[0])
    return (True, circle_intersection[1])


sala_blue = [
    [0,0], [6.7, 0], [10.05, 0], [13.4, 0], 
    [0, 3.3], [2.75, 3.3], [6.7, 3.3], [10.05, 3.3], [13.4, 3.3],
    [0, 5.2], [2.75, 5.2], [6.7, 5.2], [13.4, 5.2]
]

np_sala_blue = np.array(sala_blue)
x_list = np_sala_blue[:,0]
y_list = np_sala_blue[:,1]

pontos_cafe = [6,11,12,8]
pontos_sala_reuniao = [2,7,8,3]
pontos_sala_socios = [1,6,7,2]
pontos_copa = [4,9,10,5]
pontos_area_trabalho = [0,1,6,11,10,5,4]

polygons = {
    "sala_reuniao": Polygon([sala_blue[i] for i in pontos_sala_reuniao]),
    "copa": Polygon([sala_blue[i] for i in pontos_copa]),
    "cafe": Polygon([sala_blue[i] for i in pontos_cafe]),
    "area_trabalho": Polygon([sala_blue[i] for i in pontos_area_trabalho]),
    "sala_socios": Polygon([sala_blue[i] for i in pontos_sala_socios]),
}

beacon_1 = Beacon(1, 8.375, 3.3)
beacon_2 = Beacon(2, 13.4, 4.5)
beacon_3 = Beacon(3, 2.75, 4.5)
beacon_4 = Beacon(4, 0, 1.5)
beacon_5 = Beacon(5, 10.05, 1.5)
beacons = {
    beacon_1.id: beacon_1,
    beacon_2.id: beacon_2,
    beacon_3.id: beacon_3,
    beacon_4.id: beacon_4,
    beacon_5.id: beacon_5
}

app = Flask(__name__)
CORS(app)

@app.route('/')
def rooturl():
    print('hm')
    return 'incredible api'


@app.route('/locate', methods=['POST'])
def locate():
    posted_beacons = request.json['beacons']
    precision = 5
    nearests_beacons = [(beacons[posted_beacons[i]["id"]].point, round(posted_beacons[i]["distance"], precision)) for i in range(len(posted_beacons))]
    sorted_distances = sorted(nearests_beacons, key=lambda x : x[1])

    p1, r1 = sorted_distances[0]
    p2, r2 = sorted_distances[1]
    p3, r3 = sorted_distances[2]
    for i in sorted_distances:
        print(i)

    circle_p1 = Circle(p1[0], p1[1], r1)
    circle_p2 = Circle(p2[0], p2[1], r2)
    resultado, p4 = find_fourth_coordinate(p3, circle_p1.circle_intersect(circle_p2), r3) 
    if not resultado:
        return {'Erro': p4} 

    point_n = Point(p4[0], p4[1])
    try: 
        for polygon_name, polygon in polygons.items():
            if polygon.contains(point_n):
                create_sala_blue()    
                plt.plot(point_n.x, point_n.y, 'g*')
                plt.savefig('test_fig.png')
                plt.close()
        
                return {
                    'Area': polygon_name,
                    'x': point_n.x,
                    'y': point_n.y,
                    'Erro': None
                }
        return {
            'Area': None,
            'x': point_n.x,
            'y': point_n.y,
            'Erro': None
        }
    
    except Exception as e:
        return {
            'Area': None,
            'x': None,
            'y': None,
            'Erro': e.args
        }