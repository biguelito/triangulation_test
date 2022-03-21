from shapely.geometry import Point
from flask import Flask
from flask_cors import CORS
from flask import request
from area.area import Area
from beacon.beacons import Beacons
from circle.circle import Circle

area_pontos = [
    [0,0], [6.7, 0], [10.05, 0], [13.4, 0], 
    [0, 3.3], [2.75, 3.3], [6.7, 3.3], [10.05, 3.3], [13.4, 3.3],
    [0, 5.2], [2.75, 5.2], [6.7, 5.2], [13.4, 5.2]
]

area = Area(area_pontos)
area.Criar_Poligono('cafe', [[6.7, 3.3], [6.7, 5.2], [13.4, 5.2], [13.4, 3.3]])
area.Criar_Poligono('sala_reuniao', [[10.05, 0], [10.05, 3.3], [13.4, 3.3], [13.4, 0]])
area.Criar_Poligono('sala_socios', [[6.7, 0], [6.7, 3.3], [10.05, 3.3], [10.05, 0]])
area.Criar_Poligono('copa', [[0, 3.3], [0, 5.2], [2.75, 5.2], [2.75, 3.3]])
area.Criar_Poligono('area_trabalho', [[0, 0], [6.7, 0], [6.7, 3.3], [6.7, 5.2], [2.75, 5.2], [2.75, 3.3], [0, 3.3]])

beacons = Beacons()
beacons.criar(1, 8.375, 3.3)
beacons.criar(2, 13.4, 4.5)
beacons.criar(3, 2.75, 4.5)
beacons.criar(4, 0, 1.5)
beacons.criar(5, 10.05, 1.5)

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
    nearests_beacons = [(beacons.get_beacon(posted_beacons[i]["id"]).point, round(posted_beacons[i]["distance"], precision)) for i in range(len(posted_beacons))]  
    sorted_distances = sorted(nearests_beacons, key=lambda x : x[1])

    p1, r1 = sorted_distances[0]
    p2, r2 = sorted_distances[1]
    p3, r3 = sorted_distances[2]

    circle_p1 = Circle(p1[0], p1[1], r1)
    circle_p2 = Circle(p2[0], p2[1], r2)
    resultado, p4 = area.achar_coordenada(p3, circle_p1.circle_intersect(circle_p2), r3) 
    if not resultado:
        return {'Erro': p4} 

    point_n = Point(p4[0], p4[1])
    
    retorno = {
        'Area': None,
        'x': None,
        'y': None,
        'Erro': None
    }
    try: 
        
        for polygon_name, polygon in area.get_poligonos().items():
            if polygon[0].contains(point_n):
                area.desenhar_ponto(point_n.x, point_n.y, 'g*')
                area.desenhar_area(beacons.get_beacons())

                retorno['Area'] = polygon_name
                retorno['x'] = point_n.x
                retorno['y'] = point_n.y
                return retorno
        
        retorno['x'] = point_n.x
        retorno['y'] = point_n.y
        return retorno
    
    except Exception as e:
        retorno['Erro'] = e.args
        return retorno