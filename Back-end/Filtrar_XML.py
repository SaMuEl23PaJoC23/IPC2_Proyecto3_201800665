from Crear_XML_Salida import Crear_XMLsalida

crearXML=Crear_XMLsalida()

class Filtrar:
    
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

        print(">>>>>>>>>>>FINALIZO FILTRACION<<<<<<<<<<")
        crearXML.CrearXMLSalida(ListaDatosFiltrados,DiferenteFecha)
        