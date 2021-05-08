import webbrowser as wb

class Abrir_Documentacion:

    def AbrirDocumentacion(self):
        #abrirá unicamente si se ingresa la ruta completa de la hubicacion del archivo pdf
        wb.open_new(r'C:\Users\samal\Desktop\Proyecto_3\IPC2_Proyecto3_201800665\Back-end\documentacion.pdf')
