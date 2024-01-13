from wsgiref.validate import validator
from flask import Flask, render_template,request, flash
import numpy as np
import pickle
import tkinter as tk
from tkinter import messagebox
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'

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

def vecindarioNum(vecindario: str):
    if (vecindario.upper() == 'ASTORIA'):
        vecin = 1
    elif (vecindario.upper() == 'HELL\'S KITCHEN'):
        vecin = 2
    elif (vecindario.upper() == 'LOWER MANHATTAN'):
        vecin = 3
    else:
        vecin = 4
    return vecin

def generoNum(genero: str):
    if (genero.upper() == 'FEMENINO'):
        gen = 1
    elif (genero.upper() == 'MASCULINO'):
        gen = 2
    elif (genero.upper() == 'OTRO'):
        gen = 3
    return gen

def productosNum(producto: str):
    if (producto.upper() == "¡NECESITO MI GRANO DE CAFÉ! CAMISETA"):
        prod = 1
    elif (producto.upper() == "¡NECESITO MI GRANO DE CAFÉ! TAZA DE CAFÉ CON LECHE"):
        prod = 2
    elif (producto.upper() == "¡NECESITO MI GRANO DE CAFÉ! TAZA DE CENA"):
        prod = 3
    elif (producto.upper() == "ABRIDOR DE OJOS PICANTE CHAI LG"):
        prod = 4
    elif (producto.upper() == "ABRIDOR DE OJOS PICANTE CHAI RG"):
        prod = 5
    elif (producto.upper() == "AMANECER DE LA MAÑANA CHAI"):
        prod = 6
    elif (producto.upper() == "AMANECER DE LA MAÑANA CHAI LG"):
        prod = 7
    elif (producto.upper() == "AMANECER DE LA MAÑANA CHAI RG"):
        prod = 8
    elif (producto.upper() == "ASADO MEDIO COLOMBIANO"):
        prod = 9
    elif (producto.upper() == "BISCOTTI DE AVELLANA"):
        prod = 10
    elif (producto.upper() == "BOLLO DE ARÁNDANO"):
        prod = 11
    elif (producto.upper() == "BOLLO DE AVENA"):
        prod = 12
    elif (producto.upper() == "BOLLO DE CREMA ESCOCESA"):
        prod = 13
    elif (producto.upper() == "BOLLO DE JENGIBRE"):
        prod = 14
    elif (producto.upper() == "BOLLO SALADO GIGANTE"):
        prod = 15
    elif (producto.upper() == "BRASILEÑO - ORGÁNICO"):
        prod = 16
    elif (producto.upper() == "CAPUCHINO"):
        prod = 17
    elif (producto.upper() == "CHAI DE MEZCLA TRADICIONAL"):
        prod = 18
    elif (producto.upper() == "CHAI MEZCLA TRADICIONAL LG"):
        prod = 19
    elif (producto.upper() == "CHAI PICANTE PARA ABRIR LOS OJOS"):
        prod = 20
    elif (producto.upper() == "CHAI RG DE MEZCLA TRADICIONAL"):
        prod = 21
    elif (producto.upper() == "CHILE MAYA"):
        prod = 22
    elif (producto.upper() == "CHOCOLATE AMARGO LG"):
        prod = 23
    elif (producto.upper() == "CHOCOLATE NEGRO"):
        prod = 24
    elif (producto.upper() == "CHOCOLATE NEGRO RG."):
        prod = 25
    elif (producto.upper() == "COLOMBIANO ASADO MEDIO LG"):
        prod = 26
    elif (producto.upper() == "COLOMBIANO ASADO MEDIO RG"):
        prod = 27
    elif (producto.upper() == "COLUMBIAN MEDIUM ROAST SM"):
        prod = 28
    elif (producto.upper() == "CON TROZOS DE CHOCOLATE BISCOTTI"):
        prod = 29
    elif (producto.upper() == "CONDE GRIS"):
        prod = 30
    elif (producto.upper() == "CUERNO"):
        prod = 31
    elif (producto.upper() == "CUERNO DE ALMENDRAS"):
        prod = 32
    elif (producto.upper() == "CUERNO DE CHOCOLATE"):
        prod = 33
    elif (producto.upper() == "DESAYUNO INGLÉS"):
        prod = 34
    elif (producto.upper() == "DESAYUNO INGLÉS LG"):
        prod = 35
    elif (producto.upper() == "DESAYUNO INGLÉS RG"):
        prod = 36
    elif (producto.upper() == "DISPARO DE OURO BRASILEIRO"):
        prod = 37
    elif (producto.upper() == "EARL GREY RG"):
        prod = 38
    elif (producto.upper() == "ETIOPÍA"):
        prod = 39
    elif (producto.upper() == "ETIOPÍA LG"):
        prod = 40
    elif (producto.upper() == "ETIOPÍA RG"):
        prod = 41
    elif (producto.upper() == "ETIOPÍA SM"):
        prod = 42
    elif (producto.upper() == "EXPRESO TOSTADO"):
        prod = 43
    elif (producto.upper() == "GALLETAS DE JENGIBRE"):
        prod = 44
    elif (producto.upper() == "GATO SIVERIANO"):
        prod = 45
    elif (producto.upper() == "GUATEMALTECO CULTIVADO SOSTENIBLEMENTE"):
        prod = 46
    elif (producto.upper() == "HIERBA DE LIMÓN LG"):
        prod = 47
    elif (producto.upper() == "HIERBA DE LIMÓN RG"):
        prod = 48
    elif (producto.upper() == "JARABE DE AVELLANA"):
        prod = 49
    elif (producto.upper() == "JARABE DE CARMELO"):
        prod = 50
    elif (producto.upper() == "LATTÉ"):
        prod = 51
    elif (producto.upper() == "LATTE RG"):
        prod = 52
    elif (producto.upper() == "LG BRASILEÑO"):
        prod = 53
    elif (producto.upper() == "LG EARL GREY"):
        prod = 54
    elif (producto.upper() == "LG ORGÁNICO CULTIVADO DE FORMA SOSTENIBLE"):
        prod = 55
    elif (producto.upper() == "MENTA"):
        prod = 56
    elif (producto.upper() == "MENTA LG"):
        prod = 57
    elif (producto.upper() == "MENTA RG"):
        prod = 58
    elif (producto.upper() == "MEZCLA ORGÚNICA DESCAFEINADA"):
        prod = 59
    elif (producto.upper() == "NUESTRA MEZCLA OLD TIME DINER"):
        prod = 60
    elif (producto.upper() == "NUESTRA MEZCLA PARA CENAR DE ANTAÑO LG"):
        prod = 61
    elif (producto.upper() == "NUESTRA MEZCLA RG PARA CENAS DE ANTAÑO"):
        prod = 62
    elif (producto.upper() == "NUESTRO OLD TIME DINER BLEND SM"):
        prod = 63
    elif (producto.upper() == "ORGÁNICO CULTIVADO DE FORMA SOSTENIBLE"):
        prod = 64
    elif (producto.upper() == "RG BRASILEÑO"):
            prod = 65
    elif (producto.upper() == "RG ORGÁNICO CULTIVADO DE FORMA SOSTENIBLE"):
        prod = 66
    elif (producto.upper() == "RÍO CAFÉ JAMAICANO LG"):
        prod = 67
    elif (producto.upper() == "RÍO CAFÉ JAMAICANO RG"):
        prod = 68
    elif (producto.upper() == "RÍO CAFÉ JAMAICANO SM"):
        prod = 69
    elif (producto.upper() == "RÍO DEL CAFÉ DE JAMAICA"):
        prod = 70
    elif (producto.upper() == "SERENIDAD TÉ VERDE RG"):
        prod = 71
    elif (producto.upper() == "SIROPE DE CHOCOLATE"):
        prod = 72
    elif (producto.upper() == "SIROPE DE VAINILLA SIN AZÚCAR"):
        prod = 73
    elif (producto.upper() == "SM BRASILEÑO"):
        prod = 74
    elif (producto.upper() == "TÉ VERDE SERENIDAD"):
        prod = 75
    elif (producto.upper() == "TOSTADO PRIMO ESPRESSO"):
        prod = 76
    elif (producto.upper() == "TRAGO DE EXPRESO"):
        prod = 77
    elif (producto.upper() == "LA HIERBA DE LIMÓN"):
        prod = 78
    elif (producto.upper() == "SERENIDAD TÉ VERDE LG"):
        prod = 79
    else:
        prod = 80
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
    else:
        gen = 6
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
    else:
        tip = 30
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
    else:
        desc = 52
    return desc

def unidadMedidaNum(medida: str):
    if (medida.upper() == '16 OZ'):
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
    else:
        med = 5
    return med

def mostrar_alerta():
    messagebox.showinfo("Alerta", "Este es un mensaje de alerta en Python")

class VentasForm(FlaskForm):
    vecindario = StringField('Vecindario', validators=[DataRequired()])
    genero = SelectField('Género', choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')], validators=[DataRequired()])
    producto = StringField('Productos', validators=[DataRequired()])
    grupo_producto = StringField('Grupo de Producto', validators=[DataRequired()])
    tipo_producto = StringField('Tipo de Producto', validators=[DataRequired()])
    descripcion_producto = StringField('Descripción del Producto', validators=[DataRequired()])
    unidad_medida = StringField('Unidad de Medida', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[NumberRange(min=1)])
    monto_linea_articulo = FloatField('Costo total de venta', validators=[DataRequired(), NumberRange(min=0)])

    submit = SubmitField('Predecir')


@app.route('/', methods=['POST', 'GET'])
def home():
    form = VentasForm(request.form)

    if request.method == 'POST' and form.validate():
        vecindario = form.vecindario.data
        genero = form.genero.data
        producto = form.producto.data
        grupoProducto = form.grupo_producto.data
        tipoProducto = form.tipo_producto.data
        descripcionProducto = form.descripcion_producto.data
        unidadMedida = form.unidad_medida.data
        cantidad = form.cantidad.data
        monto_linea_articulo = form.monto_linea_articulo.data

        # Process the data and make predictions
        vecindario = float(vecindarioNum(vecindario))
        genero = float(generoNum(genero))
        producto = float(productosNum(producto))
        grupoProducto = float(grupoProductoNum(grupoProducto))
        tipoProducto = float(tipoProductoNum(tipoProducto))
        descripcionProducto = float(descripcionProductoNum(descripcionProducto))
        unidadMedida = float(unidadMedidaNum(unidadMedida))
        cantidad = float(cantidad)
        monto_linea_articulo = float(monto_linea_articulo)

        result = model.predict([[vecindario, genero, producto, grupoProducto, tipoProducto, descripcionProducto, unidadMedida, cantidad, monto_linea_articulo]])[0]
        return render_template('indexVentas.html', form=form, result=result)


    return render_template('indexVentas.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)