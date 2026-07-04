from carrello import Carrello

def carrello_totale(request):
    #rende il carrello disponibile in tutti i template

    cart = Carrello(request)
    return {'carrello': cart}