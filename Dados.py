import json

def retornar_dados(e):
    with open('Values.json', 'r') as arquivo:
        dados = json.load(arquivo)
        usuario = dados["usuario"]
        senha = dados["senha"]
        url = dados["url"]

    if e == 'url':
        return url
    elif e == 'usuario':
        return usuario
    elif e == 'senha':
        return senha
    else:
        return 0    