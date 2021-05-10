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
            flagFaltaDato=False
            flagCompleto=False
            
            ContadorLinea=1
            NumEvento=0

            for linea in lineas:
                if "<EVENTO>" in linea:
                    Datos_EtiquetaEvento.append(str(IndiceEvento))
                    IndiceEvento+=1
                    ContadorLinea=1
                    NumEvento+=1
                    flagFaltaDato=False
                    flagCompleto=False

                elif "<EVENTOS>" not in linea and "</EVENTO>" not in linea  and "</EVENTOS>" not in linea and flagFaltaDato==False:
                    
                    linea=re.sub("\t","",linea) #Forma 2 de eliminar caracteres no deseados con RegEx
                    linea=re.sub("<","",linea)
                    linea=re.sub(">","",linea)
                    linea=re.sub('"',"",linea)
                    linea=re.sub("\r","",linea)

                    if ContadorLinea == 1:
                        fecha=re.search(r'[0-9|/]+',linea)  #obtiene las fechas
                        if fecha != None and "/" in linea:
                            Datos_EtiquetaEvento.append(fecha.group())
                        else:
                            print("No Agrega-Fecha-",NumEvento)
                            flagFaltaDato=True

                    

                    elif ContadorLinea == 2:
                        reportador=re.search(r'([\w\.]+)@([\w\.]+)(\.[\w\.]+)',linea)   #Obtiene correo de quien reporta,
                        if reportador != None and "Reportado por:" in linea:                                          #no importando que se encuentre en Mayusculas
                            Datos_EtiquetaEvento.append(reportador.group())
                        else:
                            print("No Agrega-Quien Reporta-",NumEvento)
                            flagFaltaDato=True
                         
                        

                    elif ContadorLinea == 3:
                        afectados=re.findall(r'([\w\.]+@[\w\.]+\.[\w\.]+)',linea)   #Obtiene Correos de los afectados
                        if afectados != None and "Usuarios afectados:" in linea:
                            Datos_EtiquetaEvento.append(afectados)
                        else:
                            print("No Agrega-Afectados-",NumEvento)
                            flagFaltaDato=True



                    elif ContadorLinea == 4:
                        CodError=re.search(r'([0-9]{5,5})',linea)   #Obtiene Numero de error
                        MensajeErr=re.search(r'(-.+(\w)+)',linea)   #Obtiene descripcion de error
                        if CodError != None and "Error:" in linea:
                            Datos_EtiquetaEvento.append(CodError.group())
                            MensajeError+=MensajeErr.group()+" "
                            flagCompleto=True
                        else:
                            print("No Agrega-No.Error-",NumEvento)
                            flagFaltaDato=True
                        



                    elif ContadorLinea > 4:
                        MensajeErr=re.search(r'(\w.+)+',linea)   #Obtiene siguientes lineas de descripcion de error
                        if MensajeErr != None:
                            MensajeError+=MensajeErr.group()
                        else:
                            print("No Agrega-Desc.Error- siguiente linea",NumEvento)
                    
                    
                    ContadorLinea+=1

                elif "</EVENTO>" in linea:
                    if flagFaltaDato==False and flagCompleto==True:
                        Datos_EtiquetaEvento.append(MensajeError)
                        TodosLosDatos.append(Datos_EtiquetaEvento)
                    else:
                        IndiceEvento-=1
                        
                    MensajeError=""
                    Datos_EtiquetaEvento=[]
                    

                    
                    """linea=linea.replace("\n","") Forma 1 de eliminar caracteres no deseados
                    linea=linea.replace("\t","")
                    linea=linea.replace("<","")
                    linea=linea.replace(">","")
                    linea=linea.replace('"',"")"""

            print(">>>>>>>>>>>>>>FINALIZO ALMACENAMIENTO<<<<<<<<<<<<")
            return obj_filtracion.ClasificarDatos(TodosLosDatos)

        except FileNotFoundError:
            print("\n>>> Archivo NO existente...<<<\n")