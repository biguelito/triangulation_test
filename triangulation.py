from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from flask import Flask
from flask_cors import CORS
from flask import request

points = [
    [0,0], [0, 1.1],
    [1, 0], [1,1], 
]
tri = Delaunay(points)

polygons = {
    'a': Polygon([[0,0], [0,1.1], [1,1]]),
    'b': Polygon([[0,0], [1,0], [1,1]])
}
np_points = np.array(points)

app = Flask(__name__)
CORS(app)

@app.route('/')
def rooturl():
    print('hm')
    return 'incredible api'


@app.route('/delaunay', methods=['POST'])
def calcondelaunay():
    plt.clf()
    plt.triplot(np_points[:,0], np_points[:,1], tri.simplices)
    plt.plot(np_points[:,0], np_points[:,1], 'o')

    postpoint = Point(request.json['x'],request.json['y'])
    print(postpoint)

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