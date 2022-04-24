from flask import Flask, render_template,request,redirect, url_for
import pyrebase
from flask import url_for
import json
from Modelo.Usuario import Usuario
from Modelo.UsuarioSistema import UsuarioSistema
from Modelo.sensores import Registro_sensores

#variable de configuracion
config={

    "apiKey": "AIzaSyARlYEiJur-1QdKuae9fXmXtBjG5tPqjxY",
    "authDomain": "signos-vitales-623a0.firebaseapp.com",
    "databaseURL": "https://signos-vitales-623a0-default-rtdb.firebaseio.com",
    "projectId": "signos-vitales-623a0",
    "storageBucket": "signos-vitales-623a0.appspot.com",
   " messagingSenderId": "496671830855",
    "appId": "1:496671830855:web:dc897da0954b60ec339262"

}

firebase=pyrebase.initialize_app(config)
db=firebase.database()


app= Flask(__name__)


@app.route('/')
def hello_world(): # put application's coAde here
    lista = db.child("primero").get().val()
    try:
        lista_personas=lista
        lista_indices=lista_personas.keys()
        lista_indice_final=list(lista_indices)
        return render_template("uno.html", lista_personas=lista.values(),lista_indice_final=lista_indice_final)
    except:
        return render_template("uno.html")


#ruta para mostrar formulario de registro
@app.route('/add')
def add():
    return render_template("alta_personas.html")
#----------------------------------------------------------------------------
#capturar los datos del formulario y guardarlos en FB
@app.route('/save_data',methods=['POST'])
def save_data():
    hora=request.form.get('hora')
    nombre=request.form.get('nombre')
    carrera=request.form.get('carrera')
    materia=request.form.get('materia')
    grad=request.form.get('grad')
    aula=request.form.get('aula')
    dia=request.form.get('dia')
    nueva_persona=Usuario(hora,nombre,carrera,materia,grad,aula,dia)
    objeto_enviar = json.dumps(nueva_persona.__dict__)
    formato = json.loads(objeto_enviar)
    db.child("primero").push(formato)

    return redirect(url_for('hello_world'))



#eliminar un registro de la tabla
@app.route('/eliminar_persona',methods=["GET"])
def eliminar_persona():
    id= request.args.get("id")
    db.child("primero").child(str(id)).remove()
    return redirect(url_for('hello_world'))


#------------------mostra el formulario de registro-----------------------------------
@app.route('/actualizar_persona/<id>')
def actualizar_persona(id):
    lista = db.child("primero").child(str(id)).get().val()
    return render_template("formulario_actualizar.html",lista=lista,id_persona=id)

#-----------------ruta para obteter los datos y despues actualizar----------------------
@app.route('/update',methods=["POST"])
def update_persona():
    #variable para obtener informacion del formulario
    idpersona=request.form.get('id')
    hora= request.form.get('hora')
    nombre= request.form.get('nombre')
    carrera= request.form.get('carrera')
    materia= request.form.get('materia')
    grad=request.form.get('grad')
    aula= request.form.get('aula')
    dia= request.form.get('dia')

    modificar_persona = Usuario(hora,nombre,carrera,materia,grad,aula,dia)

    objeto_enviar = json.dumps(modificar_persona.__dict__)
    datos_completos = json.loads(objeto_enviar)
    db.child("primero").child(str(idpersona)).update(datos_completos)
    return redirect(url_for('hello_world'))

#-----------------formulario de resgistro de usuario del sistema---------------
@app.route('/altausuarios')
def altausuarios():
    return render_template("alta_usuarios_sistema.html")

#---------------- ruta para obtener los datos del formulario y crear el usuario.--------------
@app.route('/guardarusuariosistema',methods=['POST'])
def guardarusuariosistema():
    if request.method=='POST':
        nombre=request.form.get('nombre')
        correo=request.form.get('correo')
        usuario_sistema=request.form.get('usuario')
        password=request.form.get('password')
        telefono=request.form.get('telefono')
        tipo=request.form.get('tipo')
        try:
            usuario_sistema_nuevo=UsuarioSistema(nombre,correo,usuario_sistema,password,telefono,tipo)
            objeto_enviar = json.dumps(usuario_sistema_nuevo.__dict__)
            y=json.loads(objeto_enviar)
            db.child("usuarios").push(y)

        except:
            print("error")

    return render_template("alta_usuarios_sistema.html")


#RUTA PARA OBTENER DATOS DE LOS SENSORES
@app.route('/sensores', methods=['GET'])
def sensores():
   lista_registro_sensores = db.child("Jasir_School").child("IoT").child("23-04-22").get().val()
   return render_template('sensores.html', elemento_sensores=lista_registro_sensores.values())


@app.route('/formulariosensores',methods=['GET'])
def formulariosensores():
    return render_template('formulariosensores.html')

@app.route('/save_data_sensors',methods=['POST'])
def save_data_sensors():
    Aula_Entrada = request.form.get('Aula_Entrada')
    Aula_Sala=request.form.get('Aula_Sala')
    fechaHora = request.form.get('fechaHora')

    # Objeto de la clase Sensores
    nuevo_objeto_sensor = Registro_sensores(Aula_Entrada,Aula_Sala,fechaHora)
    objeto_enviar_sensores = json.dumps(nuevo_objeto_sensor.__dict__)
    formato_sensores = json.loads(objeto_enviar_sensores)
    db.child("Jasir_School").child("IoT").child("23-04-22").push(formato_sensores)
    return redirect(url_for('sensores'))


#




#-------------------------politicas
@app.route('/developer_information')
def developer_information():
    return render_template("developer information.html")

#-------------------------terminos
@app.route('/terminos')
def terminos():
    return render_template("terminos.html")

@app.route('/quienes')
def quienes():
    return render_template("quienes.html")

if __name__ == '__main__':
    app.run(debug=True)