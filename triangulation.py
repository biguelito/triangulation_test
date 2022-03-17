import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from flask import Flask
from flask_cors import CORS
from flask import request

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


app = Flask(__name__)
CORS(app)

@app.route('/')
def rooturl():
    print('hm')
    return 'incredible api'


@app.route('/locate', methods=['POST'])
def locate():
    postpoint = Point(request.json['x'],request.json['y'])
    print(postpoint)
    create_sala_blue()
    try: 
        for polygon_name, polygon in polygons.items():
            if polygon.contains(postpoint):
                print(f'ponto dentro de {polygon_name}')
                plt.plot(postpoint.x, postpoint.y, 'g*')
                plt.savefig('example_fig.png')
                plt.close()
                return {'Area': polygon_name}
        return {'Area': "nenhuma"}
    except Exception as e:
        return {'Erro': e.args()}