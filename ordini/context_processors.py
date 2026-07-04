from .carrello import Carrello

def carrello_totale(request):
    #rende il carrello disponibile in tutti i template

    carrello = Carrello(request)
    return {'carrello': carrello}