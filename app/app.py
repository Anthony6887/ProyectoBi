from flask import Flask, render_template,request, flash
import numpy as np
import pickle

app = Flask(__name__)

# Carga del modelo entrenado
model = pickle.load(open('modelventas.sav', 'rb'))


def verificar(atributo: str):
    if request.form[atributo] != "":
        atribut = request.form[atributo]
    else:
        atribut = ""
    return atribut


def verificarNum(atributo: str):
    if request.form[atributo] != "" and request.form[atributo] != 0:
        atribut = int(request.form.get(atributo, 0))
    else:
        atribut = 0
    return atribut


def verificarNumF(atributo: str):
    if request.form[atributo] != "" and request.form[atributo] != 0:
        atribut = float(request.form.get(atributo, 0))
    else:
        atribut = 0
    return atribut


def normalizar(max: float, min: float, valor: float):
    if (valor > max):
        result = max
    elif (valor < min):
        result = min
    else:
        result = valor
    result = (result - min)/(max - min)
    return result

def vecindariooNum(vecindario: str):
    if (vecindario.upper() == 'ASTORIA'):
        vecin = 1
    elif (vecindario.upper() == 'HELL\'S KITCHEN'):
        vecin = 2
    elif (vecindario.upper() == 'LOWER MANHATTAN'):
        vecin = 3
    return vecin

def nombreEmpleadoNum(empleado: str):
    if (empleado.upper() == 'ADRIAN MACON'):
        empl = 1
    elif (empleado.upper() == 'AINSLEY EVELYN'):
        empl = 2
    elif (empleado.upper() == 'ALINE MELANIE'):
        empl = 3
    elif (empleado.upper() == 'AMELA CHADWICK'):
        empl = 4
    elif (empleado.upper() == 'BERK DEREK'):
        empl = 5
    elif (empleado.upper() == 'BRITANNI JORDEN'):
        empl = 6
    elif (empleado.upper() == 'CALDWELL VEDA'):
        empl = 7
    elif (empleado.upper() == 'DAMON SASHA'):
        empl = 8
    elif (empleado.upper() == 'EZEKIEL RASHAD'):
        empl = 9
    elif (empleado.upper() == 'HAMILTON EMI'):
        empl = 10
    elif (empleado.upper() == 'IMA WINIFRED'):
        empl = 11
    elif (empleado.upper() == 'JOELLE CHRISTEN'):
        empl = 12
    elif (empleado.upper() == 'JOSEPH BYRON'):
        empl = 13
    elif (empleado.upper() == 'KELSEY CAMERON'):
        empl = 14
    elif (empleado.upper() == 'KYLIE CANDACE'):
        empl = 15
    elif (empleado.upper() == 'ORSON BENEDICT'):
        empl = 16
    elif (empleado.upper() == 'PANDORA NEVILLE'):
        empl = 17
    elif (empleado.upper() == 'PETER PALOMA'):
        empl = 18
    elif (empleado.upper() == 'QUAIL OCTAVIA'):
        empl = 19
    elif (empleado.upper() == 'REED EVE'):
        empl = 20
    elif (empleado.upper() == 'REMEDIOS MARI'):
        empl = 21
    elif (empleado.upper() == 'RONAN MAGEE'):
        empl = 22
    elif (empleado.upper() == 'TAMEKAH MAYA'):
        empl = 23
    elif (empleado.upper() == 'TATUM LAUREL'):
        empl = 24
    elif (empleado.upper() == 'XENA RAHIM'):
        empl = 25
    return empl

def puestoEmpleadoNum(puesto: str):
    if (puesto.upper() == 'BARISTA'):
        pue = 1
    elif (puesto.upper() == 'GERENTE DE TIENDA'):
        pue = 2
    return pue

def generoNum(genero: str):
    if (genero.upper() == 'F'):
        gen = 1
    elif (genero.upper() == 'M'):
        gen = 2
    elif (genero.upper() == 'N'):
        gen = 3
    return gen

def productosNum(producto: str):
    if (producto.upper() == 'ARTÍCULOS PARA EL HOGAR'):
        prod = 1
    elif (producto.upper() == 'BOLLOS'):
        prod = 2
    elif (producto.upper() == 'CAFÉ DE FILTRO'):
        prod = 3
    elif (producto.upper() == 'CAFÉ EN GRANO GOURMET'):
        prod = 4
    elif (producto.upper() == 'CAFÉ EN GRANO PREMIUM'):
        prod = 5
    elif (producto.upper() == 'CAFÉ PREPARADO GOURMET'):
        prod = 6
    elif (producto.upper() == 'CAFÉ PREPARADO ORGÁNICO'):
        prod = 7
    elif (producto.upper() == 'CAFÉ PREPARADO PREMIUM'):
        prod = 8
    elif (producto.upper() == 'CAFÉ VERDE EN GRANO'):
        prod = 9
    elif (producto.upper() == 'CHOCOLATE CALIENTE'):
        prod = 10
    elif (producto.upper() == 'CHOCOLATE ORGÁNICO'):
        prod = 11
    elif (producto.upper() == 'CHOCOLATE PARA BEBER'):
        prod = 12
    elif (producto.upper() == 'ESPRESSO BARISTA'):
        prod = 13
    elif (producto.upper() == 'GALLETAS'):
        prod = 14
    elif (producto.upper() == 'GRANOS DE ESPRESO'):
        prod = 15
    elif (producto.upper() == 'GRANOS ORGÁNICOS'):
        prod = 16
    elif (producto.upper() == 'INFUSIÓN DE HIERBAS'):
        prod = 17
    elif (producto.upper() == 'JARABE COMÚN'):
        prod = 18
    elif (producto.upper() == 'JARABE SIN AZÚCAR'):
        prod = 19
    elif (producto.upper() == 'MEZCLA DE CAFÉ EN GRANO CASERO'):
        prod = 20
    elif (producto.upper() == 'PASTELERÍA'):
        prod = 21
    elif (producto.upper() == 'ROPA'):
        prod = 22
    elif (producto.upper() == 'TÉ CHAI'):
        prod = 23
    elif (producto.upper() == 'TÉ CHAI PREPARADO'):
        prod = 24
    elif (producto.upper() == 'TÉ DE HIERBAS'):
        prod = 25
    elif (producto.upper() == 'TÉ NEGRO'):
        prod = 26
    elif (producto.upper() == 'TÉ NEGRO PREPARADO'):
        prod = 27
    elif (producto.upper() == 'TÉ VERDE'):
        prod = 28
    elif (producto.upper() == 'TÉ VERDE PREPARADO'):
        prod = 29
    return prod

def grupoProductoNum(genero: str):
    if (genero.upper() == 'BEBIDAS'):
        gen = 1
    elif (genero.upper() == 'COMIDA'):
        gen = 2
    elif (genero.upper() == 'COMPLEMENTOS'):
        gen = 3
    elif (genero.upper() == 'GRANO ENTERO/TÉS'):
        gen = 4
    elif (genero.upper() == 'MERCANCÍA'):
        gen = 5
    return gen
def tipoProductoNum(tipo: str):
    if (tipo.upper() == 'ARTÍCULOS PARA EL HOGAR'):
        tip = 1
    elif (tipo.upper() == 'BOLLOS'):
        tip = 2
    elif (tipo.upper() == 'CAFÉ DE FILTRO'):
        tip = 3
    elif (tipo.upper() == 'CAFÉ EN GRANO GOURMET'):
        tip = 4
    elif (tipo.upper() == 'CAFÉ EN GRANO PREMIUM'):
        tip = 5
    elif (tipo.upper() == 'CAFÉ PREPARADO GOURMET'):
        tip = 6
    elif (tipo.upper() == 'CAFÉ PREPARADO ORGÁNICO'):
        tip = 7
    elif (tipo.upper() == 'CAFÉ PREPARADO PREMIUM'):
        tip = 8
    elif (tipo.upper() == 'CAFÉ VERDE EN GRANO'):
        tip = 9
    elif (tipo.upper() == 'CHOCOLATE CALIENTE'):
        tip = 10
    elif (tipo.upper() == 'CHOCOLATE ORGÁNICO'):
        tip = 11
    elif (tipo.upper() == 'CHOCOLATE PARA BEBER'):
        tip = 12
    elif (tipo.upper() == 'ESPRESSO BARISTA'):
        tip = 13
    elif (tipo.upper() == 'GALLETAS'):
        tip = 14
    elif (tipo.upper() == 'GRANOS DE ESPRESO'):
        tip = 15
    elif (tipo.upper() == 'GRANOS ORGÁNICOS'):
        tip = 16
    elif (tipo.upper() == 'INFUSIÓN DE HIERBAS'):
        tip = 17
    elif (tipo.upper() == 'JARABE COMÚN'):
        tip = 18
    elif (tipo.upper() == 'JARABE SIN AZÚCAR'):
        tip = 19
    elif (tipo.upper() == 'MEZCLA DE CAFÉ EN GRANO CASERO'):
        tip = 20
    elif (tipo.upper() == 'PASTELERÍA'):
        tip = 21
    elif (tipo.upper() == 'ROPA'):
        tip = 22
    elif (tipo.upper() == 'TÉ CHAI'):
        tip = 23
    elif (tipo.upper() == 'TÉ CHAI PREPARADO'):
        tip = 24
    elif (tipo.upper() == 'TÉ DE HIERBAS'):
        tip = 25
    elif (tipo.upper() == 'TÉ NEGRO'):
        tip = 26
    elif (tipo.upper() == 'TÉ NEGRO PREPARADO'):
        tip = 27
    elif (tipo.upper() == 'TÉ VERDE'):
        tip = 28
    elif (tipo.upper() == 'TÉ VERDE PREPARADO'):
        tip = 29
    return tip

def descripcionProductoNum(descripcion: str):
    if (descripcion.upper() == '¡CRUJIDO!'):
        desc = 1
    elif (descripcion.upper() == 'CERTIFICADO ORGÁNICO QUE CONTIENE INGREDIENTES DE LA MÁS ALTA CALIDAD.'):
        desc = 2
    elif (descripcion.upper() == 'CLÁSICO'):
        desc = 3
    elif (descripcion.upper() == 'COMERCIO JUSTO Y ORGÁNICO Y TIENE UN FINAL CÁLIDO.'):
        desc = 4
    elif (descripcion.upper() == 'COMO SOLÍA HACER LA ABUELA'):
        desc = 5
    elif (descripcion.upper() == 'COMODIDAD DE ANTANO'):
        desc = 6
    elif (descripcion.upper() == 'CUANDO NECESITES TENER LOS OJOS BIEN ABIERTOS.'):
        desc = 7
    elif (descripcion.upper() == 'CULTIVADO EN MONTAÑA Y COSECHADO EN EL MOMENTO ÓPTIMO.'):
        desc = 8
    elif (descripcion.upper() == 'DE LA CASA DEL CAFÉ.'):
        desc = 9
    elif (descripcion.upper() == 'DESDE RÍO'):
        desc = 10
    elif (descripcion.upper() == 'EL CAFÉ MÁS CARO DEL MUNDO; LOS GATOS HACEN TODO EL TRABAJO.'):
        desc = 11
    elif (descripcion.upper() == 'EL JUEGO DE TAZA Y PLATILLO ES LA MANERA PERFECTA DE DISFRUTAR TU CAFÉ CON LECHE EN CASA.'):
        desc = 12
    elif (descripcion.upper() == 'ELEGANTE Y ELEGANTE'):
        desc = 13
    elif (descripcion.upper() == 'EN CUALQUIER MOMENTO; EN CUALQUIER LUGAR'):
        desc = 14
    elif (descripcion.upper() == 'ENFRENTA LA MAÑANA DESPUÉS DE TU RUTINA DE YOGA.'):
        desc = 15
    elif (descripcion.upper() == 'ES COMO EL CARNAVAL EN UNA TAZA. LIMPIO Y SUAVE.'):
        desc = 16
    elif (descripcion.upper() == 'ESCAMOSO Y MANTECOSO'):
        desc = 17
    elif (descripcion.upper() == 'ESTE CHOCOLATE PARA BEBER ES SUAVE Y CREMOSO.'):
        desc = 18
    elif (descripcion.upper() == 'FAVORITO DE LA ABUELA'):
        desc = 19
    elif (descripcion.upper() == 'FRAGRANTE CON ESPECIAS; ESTE ES EL CHOCOLATE PARA BEBER MÁS SABROSO QUE ENCONTRARÉ.'):
        desc = 20
    elif (descripcion.upper() == 'FRESCO Y REFRESCANTE PARA AYUDAR A CALMAR LOS NERVIOS.'):
        desc = 21
    elif (descripcion.upper() == 'HOJUELAS DE CHOCOLATE'):
        desc = 22
    elif (descripcion.upper() == 'HOMBRE; EMPEZARÁ BIEN EL DÍA.'):
        desc = 23
    elif (descripcion.upper() == 'LA TAZA DE TÉ FAVORITA DE LA REINA POR LA MAÑANA.'):
        desc = 24
    elif (descripcion.upper() == 'LA TAZA TRADICIONAL PARA EMPEZAR EL DÍA.'):
        desc = 25
    elif (descripcion.upper() == 'LAS JUDÍAS VERDES LAS PUEDES TOSTAR TÉ MISMO.'):
        desc = 26
    elif (descripcion.upper() == 'LIGERAMENTE AMARGO; PERO AÚN ASÍ MUY RICO.'):
        desc = 27
    elif (descripcion.upper() == 'MEZCLA DE GRANOS EMPAQUETADA QUE RECUERDA A LA TAZA DE CAFÉ QUE SOLÍAS TOMAR EN UN RESTAURANTE.'):
        desc = 28
    elif (descripcion.upper() == 'MEZCLA DE NUESTRA CASA PARA UN BUEN TRAGO DE ESPRESSO.'):
        desc = 29
    elif (descripcion.upper() == 'NUESTRA MEZCLA DE FRIJOLES ORGÁNICOS SELECCIONADOS A MANO Y DESCAFEINADOS DE FORMA NATURAL.'):
        desc = 30
    elif (descripcion.upper() == 'NUESTRA ÚNICA FUENTE PREMIUM DE GRANOS TOSTADOS A MANO.'):
        desc = 31
    elif (descripcion.upper() == 'NUESTRO FAVORITO'):
        desc = 32
    elif (descripcion.upper() == 'PENSAROS QUE ERES TAILANDIA MIENTRAS BEBES TU TAZA DE TÉ.'):
        desc = 33
    elif (descripcion.upper() == 'PENSAROS QUE ESTÉS EN TAILANDIA.'):
        desc = 34
    elif (descripcion.upper() == 'PENSAROS QUE ESTÉS EN VENECIA CUANDO PRUEBES ESTE.'):
        desc = 35
    elif (descripcion.upper() == 'REBOSANTE DE SABOR A CHOCOLATE'):
        desc = 36
    elif (descripcion.upper() == 'REBOSANTE DE SABOR A NUEZ'):
        desc = 37
    elif (descripcion.upper() == 'RICO SABOR A CARAMELO'):
        desc = 38
    elif (descripcion.upper() == 'SIÉNTATE Y PIENSA EN LA BRISA TROPICAL.'):
        desc = 39
    elif (descripcion.upper() == 'SIENTE EL ESTRÉS ABANDONANDO TU CUERPO.'):
        desc = 40
    elif (descripcion.upper() == 'SIGUE SIENDO UNO DE LOS FAVORITOS EN CUANTO A BUEN CAFÉ PREMIUM.'):
        desc = 41
    elif (descripcion.upper() == 'SÓLO NOTAS PURAS DE ESPECIAS.'):
        desc = 42
    elif (descripcion.upper() == 'TRADICIÓN EN UNA TAZA.'):
        desc = 43
    elif (descripcion.upper() == 'UN POQUITO DE PICANTE'):
        desc = 44
    elif (descripcion.upper() == 'UNA HOJA COMPLETA DE ORANGE PEKOE MEZCLADA CON ACEITE ORGÁNICO DE BERGAMOTA.'):
        desc = 45
    elif (descripcion.upper() == 'UNA MEZCLA MÁS PICANTE PARA DESPERTAR TUS PAPILAS GUSTATIVAS.'):
        desc = 46
    elif (descripcion.upper() == 'UNA MEZCLA TRADICIONAL.'):
        desc = 47
    elif (descripcion.upper() == 'UNA TAZA ATREVIDA CUANDO QUIERES ALGO EXTRA.'):
        desc = 48
    elif (descripcion.upper() == 'UNA TAZA DE CAFÉ SUAVE A CUALQUIER HORA DEL DÍA.'):
        desc = 49
    elif (descripcion.upper() == 'UNA TAZA FRESCA Y REFRESCANTE.'):
        desc = 50
    elif (descripcion.upper() == 'UNA TAZA HONESTA DE CAFÉ.'):
        desc = 51
    return desc

def unidadMedidaNum(medida: str):
    if (medida.upper() == '16 0Z'):
        med = 7
    elif (medida.upper() == '24 OZ'):
        med = 8
    elif (medida.upper() == 'SOLO'):
        med = 12
    elif (medida.upper() == '8 OZ'):
        med = 10
    elif (medida.upper() == '1.5 OZ'):
        med = 5
    elif (medida.upper() == 'BOMBA'):
        med = 11
    elif (medida.upper() == '12 OZ'):
        med = 6
    elif (medida.upper() == '3.0 OZ'):
        med = 9
    elif (medida.upper() == '1 LB'):
        med = 3
    elif (medida.upper() == '0.9 OZ'):
        med = 2
    elif (medida.upper() == '0.5 LB'):
        med = 1
    elif (medida.upper() == '1 OZ'):
        med = 4
    return med

@app.route('/')
def home():
    result = ''
    return render_template('indexVentas.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    vecindariooNum = float(request.form['vecindario'])
    nombreEmpleadoNum = float(request.form['nombre_empleado'])
    puestoEmpleadoNum = float(request.form['puesto_empleado'])
    edad  = float(request.form['edad'])
    generoNum = float(request.form['genero'])
    productosNum = float(request.form['producto'])
    grupoProductoNum = float(request.form['grupo_producto'])
    tipoProductoNum = float(request.form['tipo_producto'])
    descripcionProductoNum = float(request.form['descripcion_producto'])
    unidadMedidaNum = float(request.form['unidad_medida'])
    cantidad = float(request.form['cantidad'])
    monto_linea_articulo = float(request.form['monto_linea_articulo'])
    
    result = model.predict([[vecindariooNum, nombreEmpleadoNum, puestoEmpleadoNum, edad, generoNum,productosNum,grupoProductoNum, tipoProductoNum, descripcionProductoNum, unidadMedidaNum, cantidad, monto_linea_articulo]])[0]
    return render_template('indexVentas.html', **locals())

if __name__ == '__main__':
    app.run(debug=True)