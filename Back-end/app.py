from flask import Flask, jsonify, request
from flask_cors import CORS

from Procesos_para_XML import Obtener_XML

app = Flask(__name__)
CORS(app)

Obj_XML=Obtener_XML()

#--------------Rutas hacia filtraciones y procesos en flask---------------------------

@app.route('/AlmacenarXML', methods=['POST'])
def GuardarXML():

    Datos=request.json['XMLdatos']
    Datos=Datos.split("\n")

    Obj_XML.GuardarArchivoXML(Datos)
    
    mensaje=jsonify({"mensaje":"paso..."})
    return mensaje



    
if __name__=='__main__':
    app.run(debug=True, port=4000)