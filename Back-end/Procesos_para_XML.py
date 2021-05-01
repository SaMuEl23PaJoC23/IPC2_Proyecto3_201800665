from tkinter import *
from tkinter import filedialog
from xml.dom import minidom
import xml.etree.cElementTree as ET
import re


class Obtener_XML:

    def GuardarArchivoXML(self, ListaDatos):
        try:
            TodosLosDatos=[]
            Datos_EtiquetaEvento=[] #[Indice,Fecha,Reportador,Afectados,Codigo Error,Mensaje Error]
            IndiceEvento=1
            MensajeError=""
            lineas=ListaDatos

            ContadorLinea=1
            

            for linea in lineas:
                if "<EVENTO>" in linea:
                    Datos_EtiquetaEvento.append(str(IndiceEvento))
                    IndiceEvento+=1
                    ContadorLinea=1

                elif "<EVENTOS>" not in linea and "</EVENTO>" not in linea  and "</EVENTOS>" not in linea:
                    
                    linea=re.sub("\t","",linea) #Forma 2 de eliminar caracteres no deseados con RegEx
                    linea=re.sub("<","",linea)
                    linea=re.sub(">","",linea)
                    linea=re.sub('"',"",linea)

                    if ContadorLinea == 1:
                        fecha=re.search(r'[0-9|/]+',linea)  #obtiene las fechas de (0-9)(0-9)/(0-9)(0-9)/(0-9)(0-9)
                        if fecha != None:
                            Datos_EtiquetaEvento.append(fecha.group())
                        else:
                            print("No Agrega-Fecha-")
                    

                    elif ContadorLinea == 2:
                        reportador=re.search(r'([\w\.]+)@([\w\.]+)(\.[\w\.]+)',linea)   #Obtiene correo de quien reporta
                        if reportador != None:
                            Datos_EtiquetaEvento.append(reportador.group())
                        else:
                            print("No Agrega-Quien Reporta-")
                         
                        
                    elif ContadorLinea == 3:
                        afectados=re.findall(r'([\w\.]+@[\w\.]+\.[\w\.]+)',linea)   #Obtiene Correos de los afectados
                        if afectados != None:
                            Datos_EtiquetaEvento.append(afectados)
                        else:
                            print("No Agrega-Afectados-")


                    elif ContadorLinea == 4:
                        CodError=re.search(r'([0-9]{5,5})',linea)   #Obtiene Numero de error
                        MensajeErr=re.search(r'(-.+(\w)+)',linea)   #Obtiene descripcion de error
                        if CodError != None:
                            Datos_EtiquetaEvento.append(CodError.group())
                        else:
                            print("No Agrega-No.Error-")

                        if MensajeErr != None:
                            MensajeError+=MensajeErr.group()+" "
                        else:
                            print("No Agrega-Desc.Error-")


                    elif ContadorLinea > 4:
                        MensajeErr=re.search(r'(\w.+)+',linea)   #Obtiene siguientes lineas de descripcion de error
                        if MensajeErr != None:
                            MensajeError+=MensajeErr.group()
                        else:
                            print("No Agrega-Desc.Error- siguiente linea")
                    
                    ContadorLinea+=1

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

            self.ClasificarDatos(TodosLosDatos)
            
        except FileNotFoundError:
            print("\n>>> Archivo NO existente...<<<\n")



    def ClasificarDatos(self, ListaDatos):
        
        MismaFecha=[]
        DiferenteFecha=[]
        DatosPorFechas=[]   #Contendrá todas las fechas clasificadas
        FechaComparar=""
        posicion=1
        siguiente=1
        listaFechasAgregadas=[]    #lista de fechas registradas
        

        #Clasifica datos por fecha, misma fecha y diferente fecha
            #ListaDatos contiene varias listas con estructura de --ExtraerFecha---
        for ExtraerFecha in ListaDatos: #ExtraerFecha=[Indice,Fecha,Reportador,Afectados,Codigo Error,Mensaje Error]
            FlagExistente=False
            FechaComparar=ExtraerFecha[1]

            if listaFechasAgregadas != []:
                for fecha1 in listaFechasAgregadas:
                    if FechaComparar == fecha1:
                        FlagExistente=True
                        break

            
            if FlagExistente == False:
                for i in ListaDatos:
                    if posicion == len(ListaDatos):
                        break

                        #pos. fecha de un dato
                    elif ListaDatos[posicion][1] == FechaComparar:
                        MismaFecha.append(ListaDatos[posicion])

                    posicion+=1
                
                if MismaFecha == []:
                    DiferenteFecha.append(ExtraerFecha) 
                
                else:
                    MismaFecha.insert(0,ExtraerFecha)
                    DatosPorFechas.append(MismaFecha)
                    MismaFecha=[]
                    listaFechasAgregadas.append(FechaComparar)

            siguiente+=1
            posicion=siguiente
            
        #mostrar captura de fechas
        print("---------AGRUPACION POR FECHA----------------------")
        print("--MISMA FECHA----")
        for listaFecha in DatosPorFechas:
            print("Fecha: "+str(listaFecha[0][1]))
            for dato in listaFecha:
                print(dato)

        print("\n----------------------------------------------------")
        print("--DISTINTA FECHA----")
        for dato in DiferenteFecha:
            print(dato)
            print("----------------------------------")


        #Filtrar informacion por repeticion de -Reportador-
        
        
        #Estructura de Datos almacenados
           #--Fecha1--   --Fecha2--    --Fecha3--
        #[[Conj.Datos1],[Conj.Datos2],[Conj.Datos3]] ->> NombreLista:Datos por fecha
            #---Fecha1-----
        #Conj.Datos1=[ListaDatos1],[ListaDatos2]
            #---ListaDatos1---
        #[Indice,Fecha,Reportador,Afectados,Codigo Error,Mensaje Error]


        
        print("---------------------------------")
        print("-----ULTIMA FILTRACION------")
        ReportadorRegistrado=[]     #[Reportador1,Repeticion1,Reportador2,Repeticion2,...]
        totalReportadores=0
        CodigoRegistrado=[]     #[CodigoE1,Repeticion1,CodigoE2,Repeticion2,...]
        afectados=[]        #[...,[...,...],...]
        ListaDatosFiltrados=[]  #Datos para XMLsalida
        ReportadorComparar=""
        CodigoComparar=""

        
        

        #Clasifica datos por repeticion de Reportador y codigoError
        for listaFecha in DatosPorFechas:
            for lista1 in listaFecha:
                FlagExistenteRep=False
                FlagExistenteCod=False
                ReportadorComparar=lista1[2]
                CodigoComparar=lista1[4]

                if ReportadorRegistrado != []:
                    iteradorCheck=0
                    for iteracion1 in ReportadorRegistrado:
                        if iteradorCheck == len(ReportadorRegistrado):
                            break
                        if ReportadorComparar == ReportadorRegistrado[iteradorCheck]:
                            ReportadorRegistrado[iteradorCheck+1]=ReportadorRegistrado[iteradorCheck+1]+1
                            FlagExistenteRep=True
                            totalReportadores+=1
                            break

                        iteradorCheck+=2
                
                if CodigoRegistrado != []:
                    iteradorCheck=0
                    for iteracion1 in CodigoRegistrado:
                        if iteradorCheck == len(CodigoRegistrado):
                            break
                        if CodigoComparar == CodigoRegistrado[iteradorCheck]:
                            CodigoRegistrado[iteradorCheck+1]=CodigoRegistrado[iteradorCheck+1]+1
                            FlagExistenteCod=True
                            break

                        iteradorCheck+=2
            
                if FlagExistenteRep == False:
                    ReportadorRegistrado.append(ReportadorComparar)
                    ReportadorRegistrado.append(1)
                    totalReportadores+=1

                if FlagExistenteCod == False:
                    CodigoRegistrado.append(CodigoComparar)
                    CodigoRegistrado.append(1)

                afectados.append(lista1[3]) #Obtiene todos los afectados de un Reportador
            
            ListaDatosFiltrados.append(lista1[1])   #se agrega fecha
            ListaDatosFiltrados.append(totalReportadores)   #Se agrega total de Reportes de esta fecha
            ListaDatosFiltrados.append(ReportadorRegistrado)  #se agrega reportador con cant. repeticiones
            ListaDatosFiltrados.append(CodigoRegistrado)    #se agrega codigo error con cant. repeticiones      
            ListaDatosFiltrados.append(afectados)   #Se agrega todos los afedtados de esta fecha

            #ListaDatosFiltrados=[fecha1,TotalReportes,[Reportador1,repReportador,....],[CodigoErr,RepCodigo,...],[Afectados]..]

            #Mostrar filtracion de datos con repeticion
            print("------------------------")
            print(lista1[1])
            print(totalReportadores)
            print(ReportadorRegistrado)
            print(CodigoRegistrado)
            print("--afectados--")
            for d in afectados:
                print(d)

            
            ReportadorRegistrado=[]
            CodigoRegistrado=[]
            afectados=[]
            totalReportadores=0
        
        #ExtraerFecha=[Indice,Fecha,Reportador,Afectados,Codigo Error,Mensaje Error]
        print("------------------------")
        print("--DISTINTA FECHA----")
        for dato in DiferenteFecha:
            print(dato[1])
            print(1)
            print(dato[2])
            print(dato[4])
            print("--afectados--")
            print(dato[3])
            print("-----------------")

        self.CrearXMLSalida(ListaDatosFiltrados,DiferenteFecha)

#----------------Creacion de archivo XML Salida--------------------------------------------
#ListaDatosFiltrados=[fecha1,TotalReportes,[Reportador1,repReportador,....],[CodigoErr,RepCodigo,...],[Afectados,[...],...]..]
    def CrearXMLSalida(self, ListaDatosFiltrados,ListaDatosDiferentes):
        
        CantFechasAgrupadas=0   #cantidad de fechas que contienen a un grupo de personas
        siguiente=0
        for i in range(len(ListaDatosFiltrados)):
            if siguiente == len(ListaDatosFiltrados):
                break
            CantFechasAgrupadas+=1
            siguiente+=5
            
        
        Etiqueta_Estadisticas=ET.Element("ESTADISTICAS")

#--------Se agregan todos los datos que poseen mas de un reportador por fecha--------------------------
        PosicionFecha=0
        for repetir in range(CantFechasAgrupadas):

            #Se crea la etiqueta "ESTADISTICA", y se agrega a la etiqueta "ESTADISTICAS"
            Etiqueta_Estadistica=ET.SubElement(Etiqueta_Estadisticas,"ESTADISTICA")
            Etiqueta_Fecha=ET.SubElement(Etiqueta_Estadistica,"FECHA").text=ListaDatosFiltrados[PosicionFecha]
            Etiqueta_TotalMensajes=ET.SubElement(Etiqueta_Estadistica,"TOTAL_MENSAJES").text=str(ListaDatosFiltrados[PosicionFecha+1])
            Etiqueta_ReportadoPor=ET.SubElement(Etiqueta_Estadistica,"REPORTADO_POR")
            
            #se itera cada persona que reportó en esta fecha
            TemporalListaReportadores=ListaDatosFiltrados[PosicionFecha+2]
            PosDatoReporta=0
            for j in range(len(TemporalListaReportadores)):
                if PosDatoReporta == len(TemporalListaReportadores):
                    break
                Etiqueta_Usuario=ET.SubElement(Etiqueta_ReportadoPor,"USUARIO")
                Etiqueta_Email=ET.SubElement(Etiqueta_Usuario,"EMAIL").text=TemporalListaReportadores[PosDatoReporta]
                Etiqueta_MensajesReportados=ET.SubElement(Etiqueta_Usuario,"MENSAJES_REPORTADOS").text=str(TemporalListaReportadores[PosDatoReporta+1])
                PosDatoReporta+=2

            Etiqueta_Afectados=ET.SubElement(Etiqueta_Estadistica,"AFECTADOS")

            #Se itera cada afectado de esta fecha
            TemporalAfectados=ListaDatosFiltrados[PosicionFecha+4]
            
            for datoAfectado1 in TemporalAfectados:
                for elemento in datoAfectado1:
                    if len(elemento)==1:
                        Etiqueta_Afectado=ET.SubElement(Etiqueta_Afectados,"AFECTADO").text=datoAfectado1
                        break
                    else:
                        Etiqueta_Afectado=ET.SubElement(Etiqueta_Afectados,"AFECTADO").text=elemento
                    
            
            Etiqueta_Errores=ET.SubElement(Etiqueta_Estadistica,"ERRORES")

            #Se itera cada error de esta fecha
            TemporalErrores=ListaDatosFiltrados[PosicionFecha+3]
            PosDatoError=0
            for dato in TemporalErrores:
                if PosDatoError == len(TemporalErrores):
                    break
                Etiqueta_Error=ET.SubElement(Etiqueta_Errores,"ERROR")
                Etiqueta_Codigo=ET.SubElement(Etiqueta_Error,"CODIGO").text=str(TemporalErrores[PosDatoError])
                Etiqueta_MensajesGenerados=ET.SubElement(Etiqueta_Error,"MENSAJES_GENERADOS").text=str(TemporalErrores[PosDatoError+1])
                PosDatoError+=2

            PosicionFecha+=5

#----------Se agrega todos los datos que solo poseen un Reportador por fecha---------------
            for fecha2 in ListaDatosDiferentes: #fecha2=[Indice,Fecha,Reportador,Afectados,Codigo Error,Mensaje Error]
                Etiqueta_Estadistica=ET.SubElement(Etiqueta_Estadisticas,"ESTADISTICA")

                Etiqueta_Fecha=ET.SubElement(Etiqueta_Estadistica,"FECHA").text=fecha2[1]
                Etiqueta_TotalMensajes=ET.SubElement(Etiqueta_Estadistica,"TOTAL_MENSAJES").text=str(1)
                 
                Etiqueta_ReportadoPor=ET.SubElement(Etiqueta_Estadistica,"REPORTADO_POR")
                Etiqueta_Usuario=ET.SubElement(Etiqueta_ReportadoPor,"USUARIO")
                Etiqueta_Email=ET.SubElement(Etiqueta_Usuario,"EMAIL").text=fecha2[2]
                Etiqueta_MensajesReportados=ET.SubElement(Etiqueta_Usuario,"MENSAJES_REPORTADOS").text=str(1)

                Etiqueta_Afectados=ET.SubElement(Etiqueta_Estadistica,"AFECTADOS")

                TemporalAfectados=fecha2[3]
                for datoAfectado1 in TemporalAfectados:
                    for elemento in datoAfectado1:
                        if len(elemento)==1:
                            Etiqueta_Afectado=ET.SubElement(Etiqueta_Afectados,"AFECTADO").text=datoAfectado1
                            break
                        else:
                            Etiqueta_Afectado=ET.SubElement(Etiqueta_Afectados,"AFECTADO").text=elemento

                Etiqueta_Errores=ET.SubElement(Etiqueta_Estadistica,"ERRORES")

                Etiqueta_Error=ET.SubElement(Etiqueta_Errores,"ERROR")
                Etiqueta_Codigo=ET.SubElement(Etiqueta_Error,"CODIGO").text=fecha2[4]
                Etiqueta_MensajesGenerados=ET.SubElement(Etiqueta_Error,"MENSAJES_GENERADOS").text=str(1)


        #Se escribe y genera el nuevo archivo XML  
        NuevoArchivoXML=ET.ElementTree(Etiqueta_Estadisticas)
        NuevoArchivoXML.write("SalidaXML.xml")
        print("\n>>>Se escribió el NUEVO archivo !!!<<<")