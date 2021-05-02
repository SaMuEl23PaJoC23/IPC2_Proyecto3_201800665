from flask import Flask, jsonify, request
from flask_cors import CORS

from Guardar_XML import Obtener_XML

app = Flask(__name__)
CORS(app)

Obj_XML=Obtener_XML()

#--------------Rutas hacia filtraciones y procesos en flask---------------------------

@app.route('/AlmacenarXML', methods=['POST'])
def GuardarXML():
    Datos=request.json['XMLdatos']
    Datos=Datos.split("\n")
    Obj_XML.ExtraerDatosXML(Datos)
    respuesta=jsonify({"mensaje":"archivo almacenado, exitosamente"})
    return respuesta


@app.route('/CargarXMLsalida', methods=['GET'])
def CargarXMLsalida():
    with open("salidaXML.xml") as archivo:
        lineas=archivo.readlines()
    respuesta=jsonify({"mensaje":lineas})
    return respuesta



    
if __name__=='__main__':
    app.run(debug=True, port=4000)