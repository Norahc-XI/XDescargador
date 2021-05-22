import sys
from Assets.Xnxx import Main

ResolucionesPermitidas=['250p', '360p', '480p', '720p','1080p']

if len(sys.argv)==1 or sys.argv[1]=="--help":
    print("XDescargador.py [--xnxx] {-res o -resolution} Url")
elif sys.argv[1]=="--xnxx":
    try:
        if sys.argv[2]=="-res" or sys.argv[2]=="-resolution":
            if sys.argv[3] in ResolucionesPermitidas:
                Main(EntradaLinkPagina=sys.argv[4], Resolucion=sys.argv[3])
            else:
                print("[!] La Resolucion Selecionada No Esta Permitida.")
        else:
            raise IndexError
    except IndexError:
        Main(EntradaLinkPagina=sys.argv[2], Resolucion="360p")
else:
    print("[!] Argumentos Invalidos.")