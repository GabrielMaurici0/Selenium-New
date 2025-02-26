from requests import get
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

def dados_usuario(e):

    url = r'https://api.invertexto.com/v1/faker'
    response =  get(url, {'token': '17960|ZKnbEps9gvqnOl3MR8qvPE7cDdAwSweK', 'locale':'pt_BR'})
    resposta = json.loads(response.text)

    nome = resposta["name"]
    cpf = resposta["cpf"]
    email = resposta["email"]
    if e == 'name':
        return nome
    elif e == "cpf":
        return cpf
    elif e == 'email':
        return email
    else:
        return 0 