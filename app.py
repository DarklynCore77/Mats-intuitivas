from flask import Flask, render_template, request, redirect, url_for, session, jsonify  
import random
from sympy import symbols, simplify, expand 
from fractions import Fraction
import json
# from sympy.abc import x


app = Flask(__name__)
app.secret_key = "clave-secreta-muy-buena"  # Necesaria para usar sesiones

@app.route("/")
def inicio():
    return redirect(url_for("portada"))

@app.route("/indice")
def portada():
    return render_template("portada.html")

@app.route('/propiedades')
def propiedades():
    return render_template('propiedades.html')


@app.route("/orden")
def jerarquia():
    return render_template("jerarquia.html") 

@app.route("/ops", methods=["GET", "POST"])
def opbasicas():
    errores = []
    operaciones = session.get("operaciones", [])

    # Si el usuario envía respuestas (POST)
    if request.method == "POST":
        respuestas_usuario = request.form  # Diccionario con las respuestas enviadas

        for op in operaciones:
            respuesta_usuario = respuestas_usuario.get(str(op["id"]))
            if respuesta_usuario:
                try:      #convertir la respuesta del usuario a fraction 
                    respuesta_frac = Fraction(respuesta_usuario).limit_denominator()
                    if respuesta_frac != op["respuesta"]:
                        errores.append(
                            f"Error en '{op['operacion']}': ingresaste {respuesta_usuario}, pero la respuesta correcta es {op['respuesta']}."
                        )
                except ValueError:
                    errores.append(
                        f"Respuesta inválida para '{op['operacion']}': {respuesta_usuario} no es un número."
                    )
    else:
        # Si el usuario apenas entra a la página (GET)
        operaciones = []
        for i in range(1, 8):
            if random.choice([True, False]): 
                # fracciones 
                a, b = random.randint(1, 10), random.randint(1, 10)
                c, d = random.randint(1, 10), random.randint(1, 10)
                
                fr1 = Fraction(a, b)
                fr2 = Fraction(c, d)
                operador = random.choice(["+", "-", "*", "/"])

                # Asegurar que no haya divisiones por cero
                if operador == "+":
                    resultado = fr1 + fr2
                elif operador == "-":
                    resultado = fr1 - fr2
                elif operador == "*":
                    resultado = fr1 * fr2
                elif operador == "/":
                    while fr2 == 0:
                        c, d = random.randint(1, 10), random.randint(1, 10)
                        fr2 = Fraction(c, d)
                    resultado = fr1 / fr2

                operacion = f"{fr1} {operador} {fr2}"
            else:
                # enteros
                a, b = random.randint(1, 10),  random.randint(1, 10)
                operador = random.choice(["+", "-", "*", "/"])

                if operador == "+":
                    resultado = a + b
                elif operador == "-":
                    resultado = a - b
                elif operador == "*":
                    resultado = a * b
                elif operador == "/":
                    while b == 0:
                        b = random.randint(1, 10)
                    resultado = Fraction(a, b)

                operacion = f"{a} {operador} {b}"

            operaciones.append({
                "id": i,
                "operacion": operacion,
                "respuesta": resultado
            })

    session["operaciones"] = operaciones 

    return render_template('opbasicas.html', operaciones=operaciones, errores=errores)


@app.route("/arit")
def aritmetica():
    return render_template("aritmetica.html") 


@app.route("/poty", methods=["GET", "POST"])
def potyexpo():
    resultado: int = 0
    if request.method == "POST":
        base = int(request.form["base"])
        exponente = int(request.form["exponente"])
        resultado = base ** exponente
    return render_template('potyexpo.html', resultado=resultado)
# Función para generar un nuevo ejercicio de potencias











@app.route("/alge")
def algebra():
    return render_template("algebra.html") 


x = symbols('x')  # Definimos la variable simbólica x


@app.route("/nivel1", methods=["GET", "POST"])
def nivel1():
    mensaje = ""
    nivel = session.get("nivel", 1)
    intentos = session.get("intentos", 0)

    if request.method == "POST":
        respuesta_usuario = request.form.get("respuesta")
        correcta = session.get("resultado")
    
        try:
            if simplify(respuesta_usuario) == simplify(correcta):
                mensaje = "✅ ¡Correcto! Se genera una nueva operación."
                intentos += 1
                if intentos >= 5:  # tras 5 aciertos, podrías pasar al siguiente nivel
                    mensaje += " Has completado el nivel 1."
                    nivel += 1
                    intentos = 0
                session["nivel"] = nivel
            else:
                mensaje = f"❌ Incorrecto. La respuesta correcta era: {correcta}"

        except Exception:
            mensaje = "⚠️ Error: la expresión ingresada no es válida."

    # Generamos una nueva operación y la guardamos en sesión
    operacion = generar_operacion()
    session["resultado"] = str(operacion["resultado"])

    return render_template("nivel1.html",
                        expresion=operacion["texto"],
                        mensaje=mensaje,
                        nivel=nivel,
                        intentos=intentos)
def generar_polinomio():
    # Genera un polinomio aleatorio de grado 1 o 2 con coeficientes entre -5 y 5
    grado = random.choice([1, 2])
    if grado == 1:
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        return a * x + b
    else:
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        return a * x**2 + b * x + c

def generar_operacion():
    p1 = generar_polinomio()
    p2 = generar_polinomio()
    operacion = random.choice(["+", "-", "*"])

    if operacion == "+":
        resultado = simplify(p1 + p2)
    elif operacion == "-":
        resultado = simplify(p1 - p2)
    elif operacion == "*":
        resultado = simplify(expand(p1 * p2))  # expandimos para que sea una forma normal

    return {
        "texto": f"({p1}) {operacion} ({p2})",  # Lo que verá el usuario
        "resultado": resultado  # Resultado que debe escribir el usuario
    }

    # Generamos una nueva operación y la guardamos en sesión
    operacion = generar_operacion()
    session["resultado"] = str(operacion["resultado"])

    return render_template("nivel1.html",
                        expresion=operacion["texto"],
                    mensaje=mensaje,
                        nivel=nivel,
                        intentos=intentos)



@app.route("/programacion")
def programacion():
    return render_template("programacion.html")

@app.route("/datos/<lenguaje>")
def datos(lenguaje):
    with open("lenguajes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if lenguaje in data:
        return jsonify(data[lenguaje])
    else:
        return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)
