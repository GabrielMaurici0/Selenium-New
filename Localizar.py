def empresa(empcod):
    match empcod:
        case 1:
            return "https://www.moozcobranca.com.br/homologacao/servlet/awsassessoria"
        case _:
            return "https://app.beeceptor.com/console/enriquecimento"
        