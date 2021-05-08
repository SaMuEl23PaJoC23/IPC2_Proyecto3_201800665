from flask import Flask, jsonify, request
from flask_cors import CORS

from Guardar_XML import Obtener_XML
from Ordenar_InfoConsulta import OrdenarPorConsulta
from prueba import Abrir_Documentacion

app = Flask(__name__)
CORS(app)
ListaConsultas=[]   #[0]=ListaDatosFiltrados=[fecha1,TotalReportes,[Reportador1,repReportador,....],[CodigoErr,RepCodigo,...],[Afectados]..]
                    #[1]=ExtraerFecha=[Indice,Fecha,Reportador,Afectados,Codigo Error,Mensaje Error]
ListaFechas=[]
Obj_XML=Obtener_XML()
Obj_Orden=OrdenarPorConsulta()
obj_Documentacion=Abrir_Documentacion()


#--------------Rutas hacia filtraciones y procesos en flask---------------------------

@app.route('/AlmacenarXML', methods=['POST'])
def GuardarXML():
    Datos=request.json['XMLdatos']
    Datos=Datos.split("\n")

    global ListaConsultas
    ListaConsultas=Obj_XML.ExtraerDatosXML(Datos)
    respuesta=jsonify({"mensaje":"archivo almacenado, exitosamente"})
    return respuesta



@app.route('/CargarXMLsalida', methods=['GET'])
def CargarXMLsalida():
    with open("estadisticas.xml") as archivo:
        lineas=archivo.readlines()
    respuesta=jsonify({"mensaje":lineas})
    return respuesta



@app.route('/ListaFechas', methods=['GET'])
def ListaComboBox():
    temporalFechas1=ListaConsultas[0]
    temporalFechas2=ListaConsultas[1]
    fechas=[]
    siguiente=0
    for elemento in temporalFechas1:
        if siguiente == len(temporalFechas1):
            break
        fechas.append(temporalFechas1[siguiente])
        siguiente+=5

    siguiente=0
    for elemento in temporalFechas2:
        fechas.append(elemento[1])
    
    respuesta=jsonify({"ListaFechas":fechas})
    return respuesta



@app.route('/OrdenarFecha', methods=['POST'])
def ConsultarFecha():
    ValorOrdenamiento=request.json['DatoFecha']
    resultadoConsulta=Obj_Orden.OrdenarPorFecha(ListaConsultas, ValorOrdenamiento)
    respuesta=jsonify({"mensaje":resultadoConsulta})

    return respuesta



@app.route('/OrdenarCodigo/<string:ValorOrdenamiento>', methods=['GET'])
def ConsultarCodigo(ValorOrdenamiento):

    resultadoConsulta=Obj_Orden.OrdenarporCodigo(ListaConsultas, ValorOrdenamiento)
    respuesta=jsonify({"mensaje":resultadoConsulta})
    
    return respuesta



@app.route('/AbrirDocumentacion', methods=['GET'])
def AbrirDocu():
    obj_Documentacion.AbrirDocumentacion()
    respuesta=jsonify({'mensaje':'Documentacion Abierta'})

    return respuesta



    
if __name__=='__main__':
    app.run(debug=True, port=4000)