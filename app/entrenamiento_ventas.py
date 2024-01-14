import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

class ModeloRedNeuronal:
    def __init__(self, ruta_datos='DatasetCafeteriaNormalizado.csv'):
        self.df = pd.read_csv(ruta_datos, delimiter=';')
        self.caracteristicas = ['vecindario', 'genero', 'producto', 'grupo_producto',
                        'tipo_producto', 'descripcion_producto', 'unidad_medida', 'cantidad',
                        'monto_linea_articulo', 'etiqueta']
        self.df = self.df[self.caracteristicas]
        self.x_datos = self.df.drop('etiqueta', axis=1)
        self.y_datos = self.df['etiqueta']
        self.x_entrenamiento, self.x_prueba, self.y_entrenamiento, self.y_prueba = train_test_split(self.x_datos, self.y_datos, test_size=0.3)
        self.rn_modelo = MLPClassifier(hidden_layer_sizes=(7, 5, 5), activation='relu', solver='lbfgs', max_iter=10)

    def entrenar_modelo(self):
        self.rn_modelo.fit(self.x_entrenamiento, self.y_entrenamiento)

    def evaluar_modelo(self):
        y_prediccion = self.rn_modelo.predict(self.x_prueba)
        exactitud_prueba = accuracy_score(self.y_prueba, y_prediccion)
        print('Exactitud en la prueba:', exactitud_prueba)

    def puntuaciones_cruzadas(self, cv=5):
        puntuaciones = cross_val_score(self.rn_modelo, self.x_entrenamiento, self.y_entrenamiento, cv=cv)
        return puntuaciones

    def guardar_modelo(self, nombre_archivo='modelventas.sav'):
        pickle.dump(self.rn_modelo, open(nombre_archivo, 'wb'))
        print('Modelo guardado exitosamente.')

    def cargar_y_predecir(self, datos_entrada, nombre_modelo='modelventas.sav'):
        modelo_cargado = pickle.load(open(nombre_modelo, 'rb'))
        prediccion = modelo_cargado.predict([datos_entrada])
        return prediccion