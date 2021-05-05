
class Crear_XMLsalida:

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

        SalidaXML=open("estadisticas.xml","w")    
        SalidaXML.write("<ESTADISTICAS>\n")

        PosicionFecha=0
        for repetir in range(CantFechasAgrupadas):
            SalidaXML.write("\t<ESTADISTICA>\n")
            SalidaXML.write("\t\t<FECHA>"+ListaDatosFiltrados[PosicionFecha]+"</FECHA>\n")
            SalidaXML.write("\t\t<TOTAL_MENSAJES>"+str(ListaDatosFiltrados[PosicionFecha+1])+"</TOTAL_MENSAJES>\n")
            SalidaXML.write("\t\t\t<REPORTADO_POR>\n")
            #se itera cada persona que reportó en esta fecha
            TemporalListaReportadores=ListaDatosFiltrados[PosicionFecha+2]
            PosDatoReporta=0
            for j in range(len(TemporalListaReportadores)):
                if PosDatoReporta == len(TemporalListaReportadores):
                    break
                SalidaXML.write("\t\t\t\t<USUARIO>\n")
                SalidaXML.write("\t\t\t\t\t<EMAIL>"+TemporalListaReportadores[PosDatoReporta]+"</EMAIL>\n")
                SalidaXML.write("\t\t\t\t\t<MENSAJES_REPORTADOS>"+str(TemporalListaReportadores[PosDatoReporta+1])+"</MENSAJES_REPORTADOS>\n")
                SalidaXML.write("\t\t\t\t</USUARIO>\n")
                PosDatoReporta+=2
            SalidaXML.write("\t\t\t</REPORTADO_POR>\n")
            SalidaXML.write("\t\t\t<AFECTADOS>\n")
            #Se itera cada afectado de esta fecha
            TemporalAfectados=ListaDatosFiltrados[PosicionFecha+4]
            
            for datoAfectado1 in TemporalAfectados:
                for elemento in datoAfectado1:
                    if len(elemento)==1:
                        SalidaXML.write("\t\t\t\t<AFECTADO>"+datoAfectado1+"</AFECTADO>\n")
                        break
                    else:
                        SalidaXML.write("\t\t\t\t<AFECTADO>"+elemento+"</AFECTADO>\n")
            SalidaXML.write("\t\t\t</AFECTADOS>\n")
            SalidaXML.write("\t\t\t<ERRORES>\n")
            #Se itera cada error de esta fecha
            TemporalErrores=ListaDatosFiltrados[PosicionFecha+3]
            PosDatoError=0
            for dato in TemporalErrores:
                if PosDatoError == len(TemporalErrores):
                    break
                SalidaXML.write("\t\t\t\t<ERROR>\n")
                SalidaXML.write("\t\t\t\t\t<CODIGO>"+str(TemporalErrores[PosDatoError])+"</CODIGO>\n")
                SalidaXML.write("\t\t\t\t\t<MENSAJES_GENERADOS>"+str(TemporalErrores[PosDatoError+1])+"</MENSAJES_GENERADOS>\n")
                PosDatoError+=2
                SalidaXML.write("\t\t\t\t</ERRROR>\n")
            SalidaXML.write("\t\t\t</ERRORES>\n")
            SalidaXML.write("\t</ESTADISTICA>\n")
            PosicionFecha+=5

#----------Se agrega todos los datos que solo poseen un Reportador por fecha---------------
        for fecha2 in ListaDatosDiferentes: #fecha2=[Indice,Fecha,Reportador,Afectados,Codigo Error,Mensaje Error]
            SalidaXML.write("\t<ESTADISTICA>\n")
            SalidaXML.write("\t\t<FECHA>"+fecha2[1]+"</FECHA>\n")        
            SalidaXML.write("\t\t<TOTAL_MENSAJES>1</TOTAL_MENSAJES>\n")
            SalidaXML.write("\t\t\t<REPORTADO_POR>\n")
            SalidaXML.write("\t\t\t\t<USUARIO>\n")
            SalidaXML.write("\t\t\t\t\t<EMAIL>"+fecha2[2]+"</EMAIL>\n")
            SalidaXML.write("\t\t\t\t\t<MENSAJES_REPORTADOS>1</MENSAJES_REPORTADOS>\n")
            SalidaXML.write("\t\t\t\t</USUARIO>\n")
            SalidaXML.write("\t\t\t</REPORTADO_POR>\n")
            SalidaXML.write("\t\t\t<AFECTADOS>\n")
            TemporalAfectados=fecha2[3]
            for datoAfectado1 in TemporalAfectados:
                for elemento in datoAfectado1:
                    if len(elemento)==1:
                        SalidaXML.write("\t\t\t\t<AFECTADO>"+datoAfectado1+"</AFECTADO>\n")
                        break
                    else:
                        SalidaXML.write("\t\t\t\t<AFECTADO>"+elemento+"</AFECTADO>\n")
            SalidaXML.write("\t\t\t</AFECTADOS>\n")
            SalidaXML.write("\t\t\t<ERRORES>\n")
            SalidaXML.write("\t\t\t\t<ERROR>\n")
            SalidaXML.write("\t\t\t\t\t<CODIGO>"+fecha2[4]+"</CODIGO>\n")
            SalidaXML.write("\t\t\t\t\t<MENSAJES_GENERADOS>1</MENSAJES_GENERADOS>\n")
            SalidaXML.write("\t\t\t\t</ERROR>\n")
            SalidaXML.write("\t\t\t</ERRORES>\n")
            SalidaXML.write("\t</ESTADISTICA>\n")

        SalidaXML.write("</ESTADISTICAS>")
        SalidaXML.close()
        print("\n>>>Se escribió el NUEVO archivo !!!<<<")