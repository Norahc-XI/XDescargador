import re
import requests
from shutil import rmtree
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip, concatenate_videoclips, os

def ObtenerListaDeLinks(Url):
    """Doc: Funcion encargada de descargar la lista de links"""
    LinkObtenido=requests.get(Url)
    AbrirArchivo=open("temp/ArchivoTemporal.dd", "wb")
    for bite in LinkObtenido.iter_content(100000):
        AbrirArchivo.write(bite)
    AbrirArchivo.close()

def DescargarVideos(Url, Num):
    """Doc: Descargar cada video de la lista, la funcion es llamada por un bucle <for>"""
    Videos=requests.get(Url)
    NombreArchivo="temp/"+str(Num)+".ts"
    AbrirArchivo2=open(NombreArchivo, "wb")
    for bite2 in Videos.iter_content(100000):
        AbrirArchivo2.write(bite2)
    AbrirArchivo2.close()

def AddLista(lista, NombreFinal):
    """Doc: Concatenar las letras de la lista"""
    UnirLetras="".join(lista)
    NombreFinal.append(UnirLetras)

# --------------------------- Pedir link del video --------------------------- #
def Main(EntradaLinkPagina, Resolucion):
    try:
        os.makedirs("temp")
    except:
        pass

    # ------------------------------- Comprobar Url ------------------------------ #
    if re.search("xnxx.com/video-", EntradaLinkPagina) is not None:
        pass
    else:
        print("[!] Url No Valida.")
        exit()

    # ---------------- Descargar la pagina para obtener los links ---------------- #
    ObtenerPagina=requests.get(EntradaLinkPagina)
    ContenidoPagina=BeautifulSoup(ObtenerPagina.content, "html.parser")
    Links=ContenidoPagina.find_all("script")

    # ------------------------- Obtener nombre del video ------------------------- #
    ListaDeLinks=[]
    for Parrafos in Links[7]:
        Index=Parrafos.find("html5player.setVideoTitle")
        Num=0
        for Letra in Parrafos:
            Num+=1
            if Num>Index:
                ListaDeLinks.append(Letra)
                if Letra==";":
                    break
        NombreSinParchar="".join(ListaDeLinks)
        NombreVideo=NombreSinParchar[27:-3]+".mp4"

    print("\n[!]Nombre del Video: "+NombreVideo)

    # ----------------- Filtrar los links del resto de la pagina ----------------- #
    ListaDeLinks=[]
    LinkRecortado=[]
    Entrar=False
    for Parrafos in Links[7]:
        Index=Parrafos.find("html5player.setVideoHLS")
        Num=0
        for Letra in Parrafos:
            Num+=1
            if Num>Index:
                ListaDeLinks.append(Letra)
                if Letra==";":
                    break
        LinksSinParchear="".join(ListaDeLinks)
        LinkParcheado=LinksSinParchear[25:-3]
        for Caracter in LinkParcheado:
            if Entrar==True:
                if Caracter=="u":
                    break
                else:
                    LinkRecortado.append(Caracter)
            elif Caracter=="m":
                Entrar=True
                LinkRecortado.append(Caracter)
            else:
                LinkRecortado.append(Caracter)
        LinkParcheVideo="".join(LinkRecortado)
        #Parchear: limpiar el texto para queadarse solo con lo que se desea.

    # --------------------- Descargar la lista de los videos --------------------- #

    ObtenerListaDeLinks(LinkParcheado)

    # ------------------------ Filtrar links de los demas ------------------------ #
    Contador=0
    Letras=[]
    NombreFinal=[]
    CortaFuegos=False
   
    AbrirArchivo3=open("temp/ArchivoTemporal.dd", "r")
    for Parrafos2 in AbrirArchivo3:
        for Caracter2 in Parrafos2:
            if CortaFuegos==True:
                if Caracter2=="#":
                    NombreFinal.append("".join(Letras)[:-1])
                    Letras.clear()
                    CortaFuegos=False
                    break
                Letras.append(Caracter2)
            elif Caracter2=="h":
                CortaFuegos=True
                Letras.append(Caracter2)
            Contador+=1
    Res250="".join(Letras)[:-1]
    NombreFinal.append(Res250)
    AbrirArchivo3.close()

    if len(NombreFinal)==1:
        Indice=0
    elif len(NombreFinal)==2:
        if Resolucion=="250p":
            Indice=1
        elif Resolucion=="360p":
            Indice=0
    elif len(NombreFinal)==3:
        if Resolucion=="250p":
            Indice=2
        elif Resolucion=="360p":
            Indice=1
        elif Resolucion=="480p":
            Indice=0
    elif len(NombreFinal)==4:
        if Resolucion=="250p":
            Indice=3
        elif Resolucion=="360p":
            Indice=2
        elif Resolucion=="480p":
            Indice=0
        elif Resolucion=="720p":
            Indice=1
    else:
        if Resolucion=="250p":
            Indice=4
        elif Resolucion=="360p":
            Indice=3
        elif Resolucion=="1080p":
            Indice=2
        elif Resolucion=="480p":
            Indice=0
        elif Resolucion=="720p":
            Indice=1

    # ------------------------- Descargar lista de videos ------------------------ #
    try:
        Redirrecion=LinkParcheVideo[:-6]+NombreFinal[Indice]
    except:
        print("Video no disponible en resolucion selecionada.")
        exit()
    ObtenerListaDeLinks(Redirrecion)

    # ------------------- Filtrar videos del resto de la lista ------------------- #
    Letras.clear()
    NombreFinal.clear()
    AbrirArchivo4=open("temp/ArchivoTemporal.dd", "r")
    for Parrafos3 in AbrirArchivo4:
        for Letras3 in Parrafos3:
            if Entrar==True:
                if Letras3=="#":
                    Entrar==False
                    AddLista(Letras[:-1], NombreFinal)
                    Letras.clear()
                    break
                Letras.append(Letras3)
            if Letras3=="h":
                Entrar=True
                if Contador==94:
                    Letras.append(Letras3)
            Contador+=1
    AbrirArchivo4.close()
    
    # --------------------- Descargar cada video de la lista --------------------- #
    Contador=0
    for UrlVideo in NombreFinal[6:]:
        Progreso=round(((Contador+1)/(len(NombreFinal)-6))*100)
        print("Completado: "+str(Progreso)+"%", end="\r")
        LinkParteVideo=LinkParcheVideo[:-6]+UrlVideo
        DescargarVideos(LinkParteVideo, Contador)
        Contador+=1
        
    # ----- Concatenar cada video, para dejarle al usuario su video final :D ----- #
    VideosAConcatenar=[]
    for Num in range(0,len(NombreFinal)-7):
        Video=VideoFileClip("temp/"+str(Num)+".ts")
        VideosAConcatenar.append(Video)

    VideoDeSalida=concatenate_videoclips(VideosAConcatenar)
    VideoDeSalida.write_videofile(NombreVideo, preset="ultrafast")
    rmtree("temp")