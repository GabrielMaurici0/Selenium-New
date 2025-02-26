import xml.etree.ElementTree as ET
import datetime


def geraracordo(response,forma,token,carteiratoken,empresa,devedor,data):
    
    root = ET.fromstring(response)

    for x in root.findall(".//forma_negociacao"):
        for_cod = x.find("for_cod").text
        if for_cod == forma:

            print("\nTitulos disponíveis:")
            parcelas = x.findall(".//parcela")
            for idp, parcela in enumerate(parcelas,start=1):
                par_cod = parcela.find("par_cod").text
                print(f"{idp}. (Titulo: {par_cod})")

            while True:
                try:
                    iparcela = int(input("\nRealizar acordo com qual titulo? "))
                    if 1 <= iparcela <= len(parcelas):
                        parcela_escolhida = parcelas[iparcela - 1]
                        contrato = parcela_escolhida.find("con_cod").text
                        titulo = parcela_escolhida.find("par_cod").text
                        franquia = parcela_escolhida.find("con_fra").text
                        vencimento = parcela_escolhida.find("par_ven").text
                        lancamentos = parcela_escolhida.findall(".//lancamentos/item")
                        
                        for item in lancamentos:
                            codigo = item.find("codigo").text
                            valor_texto = item.find("valor").text
                            
                            if valor_texto is not None:
                                valor_float = corrigir_valor(valor_texto)  

                                if codigo == "1":
                                    principal = valor_float
                                elif codigo == "1001":
                                    juros = valor_float
                                elif codigo == "1002":
                                    multa = valor_float
                        break
                    else:
                        print("Número inválido. Escolha um dos disponíveis.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
            
            regras_acordo = x.find(".//regras_acordo")
            subregra_acordo = regras_acordo.find(".//regra_acordo")
            acordoRegraCodigo = subregra_acordo.find("aco_regcod").text
            primeiroVencimento = subregra_acordo.find("aco_datentmax").text
            regranome = subregra_acordo.find("aco_regnom").text
            
    if "A VISTA" not in regranome:
        parcelamento = input("Realizar o acordo com quantas parcelas? ")
    else:
        parcelamento = 1

        
    valorAcordo = principal+juros+multa

    principal = formatar_valor(principal)
    juros = formatar_valor(juros)
    multa = formatar_valor(multa)
    valorAcordo = formatar_valor(valorAcordo)

    enviaWpp = input("Enviar Whatsapp? (S ou N): ")
    if enviaWpp.upper() == "S":
        telefone = input("Informe o telefone que será enviado o Whatsapp: ")
    else:
        telefone = ""
    enviaEmail = input("Enviar Email? (S ou N): ")
    if enviaEmail.upper() == "S":
        email = input("Informe o e-mail que receberá a notificação: ")
    else:
        email = ""

    formaPagamento = input("Informe a forma de pagamento (B - Boleto, L - Link Cartão, C - Cartão de Crédito): ")
    while formaPagamento.upper() not in ["B", "L", "C"]:
        print("Forma de recebimento incorreta!")
        formaPagamento = input("Informe a forma de pagamento (B - Boleto, L - Link Cartão, C - Cartão de Crédito): ")


    xmlgeraracordo = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sis="siscobra">
        <soapenv:Header />
        <soapenv:Body>
            <sis:WSAssessoria.Execute>
                <sis:Token>{token}</sis:Token>
                <sis:Carcod>{carteiratoken}</sis:Carcod>
                <sis:Metodo>GERAR_ACORDO</sis:Metodo>
                <sis:Xmlin>
                    &lt;gerar_acordo&gt;
                        &lt;dividas&gt;
                            &lt;cod_assessoria&gt;0&lt;/cod_assessoria&gt;
                            &lt;emp_cliente&gt;{empresa}&lt;/emp_cliente&gt;
                            &lt;cod_cliente&gt;{devedor}&lt;/cod_cliente&gt;
                            &lt;data_calculo&gt;{data}&lt;/data_calculo&gt;
                            &lt;forma_negociacao&gt;{forma}&lt;/forma_negociacao&gt;
                            &lt;envia_whatsapp &gt;{enviaWpp}&lt;/envia_whatsapp&gt; 
                            &lt;cliente_whatsapp&gt;{telefone}&lt;/cliente_whatsapp&gt;
                            &lt;envia_email&gt;{enviaEmail}&lt;/envia_email&gt;
                            &lt;cliente_email&gt;{email}&lt;/cliente_email&gt;
                            &lt;aco_forpag&gt;{formaPagamento}&lt;/aco_forpag&gt; 
                            &lt;divida&gt;
                                &lt;con_cod&gt;{contrato}&lt;/con_cod&gt;
                                &lt;con_fil&gt;0&lt;/con_fil&gt;
                                &lt;con_fra&gt;{franquia}&lt;/con_fra&gt;
                                &lt;par_cod&gt;{titulo}&lt;/par_cod&gt;
                                &lt;par_num&gt;1&lt;/par_num&gt;
                                &lt;par_ven&gt;{vencimento}&lt;/par_ven&gt;
                                &lt;lancamentos&gt;
                                    &lt;item&gt;
                                        &lt;codigo&gt;1&lt;/codigo&gt;
                                        &lt;descricao&gt;PRINCIPAL&lt;/descricao&gt;
                                        &lt;tipo&gt;C&lt;/tipo&gt;
                                        &lt;valor&gt;{principal}&lt;/valor&gt;
                                        &lt;desconto&gt;0&lt;/desconto&gt;
                                    &lt;/item&gt;
                                    &lt;item&gt;
                                        &lt;codigo&gt;1001&lt;/codigo&gt;
                                        &lt;descricao&gt;PRINCIPAL&lt;/descricao&gt;
                                        &lt;tipo&gt;E&lt;/tipo&gt;
                                        &lt;valor&gt;{juros}&lt;/valor&gt;
                                        &lt;desconto&gt;0&lt;/desconto&gt;
                                    &lt;/item&gt;
                                &lt;item&gt;
                                        &lt;codigo&gt;1002&lt;/codigo&gt;
                                        &lt;descricao&gt;PRINCIPAL&lt;/descricao&gt;
                                        &lt;tipo&gt;E&lt;/tipo&gt;
                                        &lt;valor&gt;{multa}&lt;/valor&gt;
                                        &lt;desconto&gt;0&lt;/desconto&gt;
                                    &lt;/item&gt;
                                &lt;/lancamentos&gt;
                            &lt;/divida&gt;
                        &lt;/dividas&gt;
                        &lt;acordo&gt;
                            &lt;aco_regcod&gt;{acordoRegraCodigo}&lt;/aco_regcod&gt;
                            &lt;aco_valent&gt;0,00&lt;/aco_valent&gt;
                            &lt;aco_datent&gt;&lt;/aco_datent&gt;
                            &lt;aco_datpriven&gt;{primeiroVencimento}&lt;/aco_datpriven&gt;
                            &lt;aco_plaseq&gt;{parcelamento}&lt;/aco_plaseq&gt;
                            &lt;aco_valaco&gt;{valorAcordo}&lt;/aco_valaco&gt;
                        &lt;/acordo&gt;
                    &lt;/gerar_acordo&gt;
                </sis:Xmlin>
            </sis:WSAssessoria.Execute>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    return xmlgeraracordo

def corrigir_valor(valor):
    """ Converte string numérica para float, corrigindo separadores """
    if isinstance(valor, float): 
        return round(valor, 2)
    elif isinstance(valor, str):  
        valor_corrigido = valor.replace(".", "").replace(",", ".")  
        return round(float(valor_corrigido), 2)
    else:
        raise ValueError("Tipo de valor inválido em corrigir_valor()")

def formatar_valor(valor):
    """ Formata float para string com separador decimal como vírgula """
    return f"{valor:,.2f}".replace(".", ",")