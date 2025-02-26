import requests
import xml.etree.ElementTree as ET
import html
from Localizar import empresa
from Preencher import geraracordo

itoken = input("Informe o token: ")
icarteiratoken = input("Informe a carteira do token: ")
icarteira = input("Informe a carteira do devedor: ")
iempresa = input("Informe a empresa do devedor: ")
idevedor = input("Informe o devid do devedor: ")
idata = input("Informe a data do calculo (dd/mm/aaaa): ")

iempresa= int(iempresa)

url = empresa(iempresa)

xml = f"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sis="siscobra">
    <soapenv:Header />
    <soapenv:Body>
        <sis:WSAssessoria.Execute>
            <sis:Token>{itoken}</sis:Token>
            <sis:Carcod>{icarteiratoken}</sis:Carcod>
            <sis:Metodo>OBTER_DIVIDA_CALCULADA</sis:Metodo>
            <sis:Xmlin>
                &lt;obter_divida_calculada&gt;
                    &lt;cod_assessoria&gt;{icarteira}&lt;/cod_assessoria&gt;
                    &lt;emp_cliente&gt;{iempresa}&lt;/emp_cliente&gt;
                    &lt;cod_cliente&gt;{idevedor}&lt;/cod_cliente&gt;
                    &lt;data_calculo&gt;{idata}&lt;/data_calculo&gt;
                &lt;/obter_divida_calculada&gt;
            </sis:Xmlin>
        </sis:WSAssessoria.Execute>
    </soapenv:Body>
</soapenv:Envelope>
"""
response = requests.post(url,data=xml)

tresponse = response.text

start = tresponse.find("<Xmlout>") + len("<Xmlout>")
end = tresponse.find("</Xmlout>")
tresponse = html.unescape(tresponse[start:end])

root = ET.fromstring(tresponse)

formas_de_negociacao = root.findall(".//forma_negociacao")
if not formas_de_negociacao:
    print("Nenhuma forma de negociação encontrada.")
    exit()

print("\nFormas de recebimento disponíveis:")
for idx, forma in enumerate(formas_de_negociacao, start=1):
    for_cod = forma.find("for_cod").text
    for_nom = forma.find("for_nom").text
    print(f"{idx}. {for_nom} (Código: {for_cod})")

    
while True:
    try:
        iforma = int(input("\nRealizar acordo com qual forma de recebimento? "))
        if 1 <= iforma <= len(formas_de_negociacao):
            break
        else:
            print("Número inválido. Escolha um dos disponíveis.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

forcod = formas_de_negociacao[iforma - 1].find("for_cod").text
print(f"Forma de recebimento escolhida: {forcod}")

xmlacordo = geraracordo(tresponse, forcod,itoken,icarteiratoken,iempresa,idevedor,idata)

responseacordo = requests.post(url,data=xmlacordo)

