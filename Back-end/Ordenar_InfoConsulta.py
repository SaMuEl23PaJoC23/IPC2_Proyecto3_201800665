from graphviz import render
from io import open
import webbrowser

class OrdenarPorConsulta:

    def OrdenarPorFecha(self,ListaDatosFiltrados,DatoFecha):
        listaDatos=ListaDatosFiltrados
        FechaBuscar=DatoFecha
        flagEncontrado=False

        MostrarDatos=[]

        Agrupados=listaDatos[0] #ListaDatosFiltrados=[fecha1,TotalReportes,[Reportador1,repReportador,....],[CodigoErr,RepCodigo,...],[Afectados,[...],...] , ...]
        Distintos=listaDatos[1] #ExtraerFecha=[Indice,Fecha,Reportador,Afectados,Codigo Error,Mensaje Error]
        siguiente=0

        for i in range(len(Agrupados)):
            if siguiente == len(Agrupados):
                break
            if Agrupados[siguiente] == FechaBuscar:
                siguienteReportador=0
                ListaReportadores=Agrupados[siguiente+2]
                for reportador in ListaReportadores:
                    if siguienteReportador == len(ListaReportadores):
                        break
                    MostrarDatos.append(ListaReportadores[siguienteReportador])
                    siguienteReportador+=2
                flagEncontrado=True
                break

            siguiente+=5
            

        if flagEncontrado == False:
            siguiente=0
            for i in range(len(Distintos)):
                if siguiente == len(Distintos):
                    break
                if Distintos[siguiente][1] == FechaBuscar:
                    MostrarDatos.append(Distintos[siguiente][2])
                    flagEncontrado=True
                    break

                siguiente+=1


        if flagEncontrado == True:  #Se crea el grafo
            NombrePictureSalida="fecha.dot"

            Crear_escribirArchivo=open(NombrePictureSalida,'w')
            Crear_escribirArchivo.write('digraph G {\n')
            Crear_escribirArchivo.write('node [shape=plaintext] \n')
            Crear_escribirArchivo.write('a [label=<<table border="0" cellborder="1" cellspacing="0"> \n')

            Crear_escribirArchivo.write('<tr><td colspan="2" bgcolor="green">FILTRACION POR FECHA</td></tr> \n')
            Crear_escribirArchivo.write('<tr><td bgcolor="orange">FECHA:</td><td>'+FechaBuscar+'</td></tr> \n')
            Crear_escribirArchivo.write('<tr> \n')
            Crear_escribirArchivo.write('<td bgcolor="green">INDICE</td>\n')
            Crear_escribirArchivo.write('<td bgcolor="green">REPORTADOR</td>\n')
            Crear_escribirArchivo.write('</tr> \n')

            indice=1
            for reportador in MostrarDatos:
                Crear_escribirArchivo.write('<tr> \n')
                Crear_escribirArchivo.write('<td>'+str(indice)+'</td>\n')
                Crear_escribirArchivo.write('<td>'+reportador+'</td>\n')
                indice+=1
                Crear_escribirArchivo.write('</tr>\n')
            
            Crear_escribirArchivo.write('</table>>];')
            Crear_escribirArchivo.write('}')
            Crear_escribirArchivo.close()
            render('dot','png',NombrePictureSalida)
            webbrowser.open_new_tab('fecha.dot.png')
            print("--- Se generó archivo .dot ---")

            respuesta="!! Filtracion por fecha generada exitosamente !!"

            return respuesta
        
        else:
            respuesta="!! Fecha no existente !!"
            return respuesta

#--------------------------------------------------------------------------------
    def OrdenarporCodigo(self,ListaDatosFiltrados, DatoCodigo):
        listaDatos=ListaDatosFiltrados
        CodigoBuscar=DatoCodigo

        MostrarDatos=[] #[fecha,Cant.repeticiones,...]

        Agrupados=listaDatos[0] #ListaDatosFiltrados=[fecha1,TotalReportes,[Reportador1,repReportador,....],[CodigoErr,RepCodigo,...],[Afectados,[...],...] , ...]
        Distintos=listaDatos[1] #ExtraerFecha=[Indice,Fecha,Reportador,Afectados,Codigo Error,Mensaje Error]
        siguienteFecha=0
        siguiente=3 #Permite moverse hacia la siguiente fecha

        for i in range(len(Agrupados)): #Se busca entre los agrupados
            if siguiente >= len(Agrupados):
                break
            siguienteCodigo=0   #Permite moverse entre los codigos de error de una misma fecha
            ListaCodigos=Agrupados[siguiente]
            for i in range(len(ListaCodigos)):
                if siguienteCodigo == len(ListaCodigos):
                    break
                if ListaCodigos[siguienteCodigo] == CodigoBuscar:
                    MostrarDatos.append(Agrupados[siguienteFecha])
                    MostrarDatos.append(str(ListaCodigos[siguienteCodigo+1]))
                siguienteCodigo+=2

            siguienteFecha+=5
            siguiente+=5


        siguienteFecha=1
        siguiente=0
        for i in range(len(Distintos)): #Se busca entre los datos des-agrupados
            if siguiente == len(Distintos):
                break
            ListaDatos=Distintos[siguiente]
            if ListaDatos[4]== CodigoBuscar:
                MostrarDatos.append(ListaDatos[siguienteFecha])
                MostrarDatos.append(str(1))
            
            siguiente+=1



        if MostrarDatos != []:
            NombrePictureSalida="codigoE.dot"

            Crear_escribirArchivo=open(NombrePictureSalida,'w')
            Crear_escribirArchivo.write('digraph G {\n')
            Crear_escribirArchivo.write('node [shape=plaintext] \n')
            Crear_escribirArchivo.write('a [label=<<table border="0" cellborder="1" cellspacing="0"> \n')

            Crear_escribirArchivo.write('<tr><td colspan="3" bgcolor="green">FILTRACION POR CODIGO DE ERROR</td></tr> \n')
            Crear_escribirArchivo.write('<tr><td bgcolor="orange">CODIGO DE ERROR:</td><td colspan="2">'+CodigoBuscar+'</td></tr> \n')
            Crear_escribirArchivo.write('<tr> \n')
            Crear_escribirArchivo.write('<td bgcolor="green">INDICE</td>\n')
            Crear_escribirArchivo.write('<td bgcolor="green">FECHA</td>\n')
            Crear_escribirArchivo.write('<td bgcolor="green">CANT.MENSAJES</td>\n')
            Crear_escribirArchivo.write('</tr> \n')

            indice=1
            siguiente=0
            for i in MostrarDatos:
                if siguiente == len(MostrarDatos):
                    break
                Crear_escribirArchivo.write('<tr> \n')
                Crear_escribirArchivo.write('<td>'+str(indice)+'</td>\n')
                Crear_escribirArchivo.write('<td>'+MostrarDatos[siguiente]+'</td>\n')   #Fecha
                Crear_escribirArchivo.write('<td>'+MostrarDatos[siguiente+1]+'</td>\n') #Cant.mensajes
                indice+=1
                siguiente+=2
                Crear_escribirArchivo.write('</tr>\n')
            
            Crear_escribirArchivo.write('</table>>];')
            Crear_escribirArchivo.write('}')
            Crear_escribirArchivo.close()
            render('dot','png',NombrePictureSalida)
            webbrowser.open_new_tab('codigoE.dot.png')
            print("--- Se generó archivo .dot ---")

            respuesta="!! Filtracion por codigo generada exitosamente !!"

            return respuesta
        
        else:
            respuesta="!! Codigo no existente !!"
            return respuesta

        

        



