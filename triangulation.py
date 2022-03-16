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
np_points = np.array(points)

polygons = {
    'a': Polygon([[0,0], [0,1.1], [1,1]]),
    'b': Polygon([[0,0], [1,0], [1,1]])
}
tri = Delaunay(points)

# plt.triplot(np_points[:,0], np_points[:,1], tri.simplices)
# plt.plot(np_points[:,0], np_points[:,1], 'o')
# plt.show()

app = Flask(__name__)
CORS(app)

@app.route('/')
def rooturl():
    print('hm')
    return 'incredible api'

@app.route('/delaunay', methods=['POST'])
def calcondelaunay():
    postpoint = Point(request.json['x'],request.json['y'])
    print(postpoint)
    for polygon_name, polygon in polygons.items():
        if polygon.contains(postpoint):
            print(f'ponto dentro de {polygon_name}')
            return {'Area': polygon_name}