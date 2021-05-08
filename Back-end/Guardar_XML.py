import re
from Filtrar_XML import Filtrar

obj_filtracion=Filtrar()

class Obtener_XML:

    def ExtraerDatosXML(self, ListaDatos):
        try:
            TodosLosDatos=[]
            Datos_EtiquetaEvento=[] #[Indice,Fecha,Reportador,Afectados,Codigo Error,Mensaje Error]
            IndiceEvento=1
            MensajeError=""
            lineas=ListaDatos
            

            for linea in lineas:
                if "<EVENTO>" in linea:
                    Datos_EtiquetaEvento.append(str(IndiceEvento))
                    IndiceEvento+=1
                    flagSiguienteLinea=False

                elif "<EVENTOS>" not in linea and "</EVENTO>" not in linea  and "</EVENTOS>" not in linea:
                    
                    linea=re.sub("\t","",linea) #Forma 2 de eliminar caracteres no deseados con RegEx
                    linea=re.sub("<","",linea)
                    linea=re.sub(">","",linea)
                    linea=re.sub('"',"",linea)
                    linea=re.sub("\r","",linea)

                    if "Guatemala" in linea:
                        fecha=re.search(r'[0-9|/]+',linea)  #obtiene las fechas de (0-9)(0-9)/(0-9)(0-9)/(0-9)(0-9)
                        if fecha != None:
                            Datos_EtiquetaEvento.append(fecha.group())
                        else:
                            print("No Agrega-Fecha-")
                    

                    elif "Reportado por" in linea:
                        reportador=re.search(r'([\w\.]+)@([\w\.]+)(\.[\w\.]+)',linea)   #Obtiene correo de quien reporta
                        if reportador != None:
                            Datos_EtiquetaEvento.append(reportador.group())
                        else:
                            print("No Agrega-Quien Reporta-")
                         
                        
                    elif "Usuarios afectados" in linea:
                        afectados=re.findall(r'([\w\.]+@[\w\.]+\.[\w\.]+)',linea)   #Obtiene Correos de los afectados
                        if afectados != None:
                            Datos_EtiquetaEvento.append(afectados)
                        else:
                            print("No Agrega-Afectados-")


                    elif "Error" in linea:
                        CodError=re.search(r'([0-9]{5,5})',linea)   #Obtiene Numero de error
                        MensajeErr=re.search(r'(-.+(\w)+)',linea)   #Obtiene descripcion de error
                        if CodError != None:
                            Datos_EtiquetaEvento.append(CodError.group())
                        else:
                            print("No Agrega-No.Error-")

                        if MensajeErr != None:
                            MensajeError+=MensajeErr.group()+" "
                            flagSiguienteLinea=True
                        else:
                            print("No Agrega-Desc.Error-")


                    elif flagSiguienteLinea == True:
                        MensajeErr=re.search(r'(\w.+)+',linea)   #Obtiene siguientes lineas de descripcion de error
                        if MensajeErr != None:
                            MensajeError+=MensajeErr.group()
                        else:
                            print("No Agrega-Desc.Error- siguiente linea")
                    
                    flagSiguienteLinea=False

                elif "</EVENTO>" in linea:
                    Datos_EtiquetaEvento.append(MensajeError)
                    TodosLosDatos.append(Datos_EtiquetaEvento)
                    MensajeError=""
                    Datos_EtiquetaEvento=[]
                    

                    
                    """linea=linea.replace("\n","") Forma 1 de eliminar caracteres no deseados
                    linea=linea.replace("\t","")
                    linea=linea.replace("<","")
                    linea=linea.replace(">","")
                    linea=linea.replace('"',"")"""

            print("---------Datos Filtrados-------")
            for i in range(len(TodosLosDatos)):
                print("-------GRUPO: "+str(i+1))
                for j in range(6):
                    print(TodosLosDatos[i][j])


            print(">>>>>>>>>>>>>>FINALIZO ALMACENAMIENTO<<<<<<<<<<<<")
            return obj_filtracion.ClasificarDatos(TodosLosDatos)

        except FileNotFoundError:
            print("\n>>> Archivo NO existente...<<<\n")