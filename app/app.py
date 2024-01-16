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

def generoNum(genero: str):
    if (genero.upper() == 'FEMENINO'):
        gen = 1
    elif (genero.upper() == 'MASCULINO'):
        gen = 2
    elif (genero.upper() == 'OTRO'):
        gen = 3
    return gen

def unidadMedidaNum(medida: str):
    if (medida.upper() == '0.5 LB'):
        med = 1
    elif (medida.upper() == '0.9 OZ'):
        med = 2
    elif (medida.upper() == '1 LB'):
        med = 3
    elif (medida.upper() == '1 OZ'):
        med = 4
    elif (medida.upper() == '1.5 OZ'):
        med = 5
    elif (medida.upper() == '12 OZ'):
        med = 6
    elif(medida.upper() == '16 OZ'):
        med = 7
    elif (medida.upper() == '24 OZ'):
        med = 8
    elif (medida.upper() == '3.0 OZ'):
        med = 9
    elif (medida.upper() == '8 OZ'):
        med = 10
    elif (medida.upper() == 'BOMBA'):
        med = 11
    elif (medida.upper() == 'SOLO'):
        med = 12
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
    unidad_medida = SelectField('Medida', choices=[
        ('0.5 LB', '0.5 LB'),
        ('0.9 OZ', '0.9 OZ'),
        ('1 LB', '1 LB'),
        ('1 OZ', '1 OZ'),
        ('1.5 OZ', '1.5 OZ'),
        ('12 OZ', '12 OZ'),
        ('16 OZ', '16 OZ'),
        ('24 OZ', '24 OZ'),
        ('3.0 OZ', '3.0 OZ'),
        ('8 OZ', '8 OZ'),
        ('SOLO', 'SOLO')], validators=[DataRequired()])

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
        unidadMedida = form.unidad_medida.data
        cantidad = form.cantidad.data
        monto_linea_articulo = form.monto_linea_articulo.data

        vecindario = float(vecindario)
        genero = float(generoNum(genero))
        producto = float(producto)
        grupoProducto = float(grupoProducto)
        tipoProducto = float(tipoProducto)
        unidadMedida = float(unidadMedidaNum(unidadMedida))
        cantidad = float(cantidad)
        monto_linea_articulo = float(monto_linea_articulo)

        result = model.predict([[vecindario, genero, producto, grupoProducto, tipoProducto, unidadMedida, cantidad, monto_linea_articulo]])[0]
        return render_template('indexVentas.html', form=form, result=result)


    return render_template('indexVentas.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)