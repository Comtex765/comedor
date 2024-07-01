def check_cedula(cedula):
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0

    if len(cedula) != 10:
        return False

    try:
        int(cedula)
    except ValueError:
        return False

    provincia = int(cedula[:2])
    if provincia < 1 or provincia > 24:
        return False

    tercer_digito = int(cedula[2])
    if tercer_digito >= 6:
        return False

    for i in range(9):
        producto = int(cedula[i]) * coeficientes[i]
        if producto >= 10:
            producto -= 9
        suma += producto

    digito_verificador = 10 - (suma % 10)
    if digito_verificador == 10:
        digito_verificador = 0

    return digito_verificador == int(cedula[9])
