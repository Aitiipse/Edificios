from flask import Flask, render_template, url_for , flash, request, redirect, session
from psycopg2 import connect
from config import *
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required


app = Flask(__name__)

app.secret_key='12345'
sesion = True

con_db = EstablecerConexion()

#-------------------------------------------------------------------------------------------------------------------

@app.route("/salir")
def salir():
	return render_template("login.html")

@app.route("/404")
def error():
	return render_template("404.html")

@app.route("/facturatotal")
def facturatotal():
	return render_template("facturatotal.html")

@app.route("/facturas")
def facturas():
    cursor=con_db.cursor()
    sql= "SELECT*FROM tabla_padre ORDER BY torre ASC"
    cursor.execute(sql)
    facturasRegistradas=cursor.fetchall()
    print("estamos en la de admin")
    return render_template('facturas.html',facturas=facturasRegistradas)

@app.route("/")
def index():
    cursor=con_db.cursor()
    sql= "SELECT*FROM usuarios"
    cursor.execute(sql)
    usuariosRegistradas=cursor.fetchall()
    print("inicio de la página")
    return render_template('index.html',usuarios=usuariosRegistradas)

@app.route("/ingreso")
def ingreso():
    cursor=con_db.cursor()
    sql= "SELECT*FROM usuarios"
    cursor.execute(sql)
    usuariosRegistradas=cursor.fetchall()
    print("inicio de la página")
    return render_template('ingreso.html',usuarios=usuariosRegistradas)

@app.route("/registros")
def registros():
    cursor=con_db.cursor()
    sql= "SELECT*FROM usuarios"
    cursor.execute(sql)
    usuariosRegistradas=cursor.fetchall()
    print("inicio de la página")
    return render_template('registros.html',usuarios=usuariosRegistradas)

@app.route("/layout")
def layout():
	print("estamos en layout")
	return render_template("layout.html")

@app.route("/login")
def login():
     cursor=con_db.cursor()
     sql= "SELECT*FROM tabla_padre ORDER BY torre ASC"
     cursor.execute(sql)
     facturasRegistradas=cursor.fetchall()
     print("estamos en la de admin")
     return render_template('login.html',facturas=facturasRegistradas)
	

@app.route("/registrarUsuario", methods=['POST'])
def registrarse():
	if request.method == 'POST':
		nombre = request.form['nombre']
		torre = request.form ['torre']
		apartamento = request.form['apartamento']
		cedula = request.form['cedula']
		contraseña = request.form['contraseña']
		# create_table_Usuarios()
		cur = con_db.cursor()
		cur.execute("INSERT INTO usuarios (nombre, torre, apartamento, cedula, contraseña) VALUES (%s, %s,%s,%s,%s)", (nombre, torre, apartamento,cedula, contraseña))
		con_db.commit()
		flash("registro de usuarios")
		print("registroexitoso")
		return redirect(url_for('registros'))
		
    
@app.route('/inicioSesion', methods=['GET', 'POST'])
def inicioSesion():
    cedula = request.form['cedula']
    contraseña = request.form['contraseña']
    cur = con_db.cursor()
    cur.execute("SELECT * FROM administrador WHERE cedula = %s AND contraseña = %s", (cedula, contraseña))
    con_db.commit()
    data = cur.fetchall()
    print("_-----------------------------------")
    print(data)
    if len(data) > 0:
        print("si hay datos")
        return redirect(url_for('facturas'))
    else:
        cur = con_db.cursor()
        cur.execute("SELECT * FROM usuarios WHERE cedula = %s AND contraseña = %s", (cedula, contraseña))
        con_db.commit()
        data = cur.fetchall()
        print("_-----------------------------------")
        print(data)
        if len(data) > 0:
            print("si hay datos")
            return redirect(url_for('login'))
        else:
            flash("Datos no encontrados")
            return redirect(url_for('registros'))

@app.route('/facturaIndividual', methods=['POST'])
def facturaIndividual():
    factura= request.form['idfactura']
    valor= request.form['valor']
    mes= request.form['mes']
    tipo= request.form['tipo']
    cur = con_db.cursor()
    
    if factura and valor and mes and tipo:
        create_table_facturas()
        cur = con_db.cursor()
        cur.execute("INSERT INTO facturas (factura, valor, mes, tipo) VALUES (%s, %s,%s,%s)", (factura, valor, mes, tipo))
        con_db.commit()
        return redirect(url_for('facturatotal'))
        #flash('Usuario agregado correctamente', 'alert-success')
    else:
        return redirect(url_for('facturatotal'))

#--------------------------------------------------------------------------

@app.route('/registrarFactura', methods=['POST']) 
def registrarFactura():
    mes = request.form['mes']
    torre = request.form['torre']
    linea = request.form['linea']
    # apartamento = request.form['apartamento']
    serviciogas = request.form['serviciogas']
    servicioagua = request.form['servicioagua']
    servicioenergia = request.form['servicioenergia']
    cur = con_db.cursor()  
    
    if mes and torre and linea and  serviciogas and servicioagua and servicioenergia:
        cur = con_db.cursor()
        cur.execute("INSERT INTO tabla_padre (mes, torre, linea,  serviciogas, servicioagua, servicioenergia) VALUES (%s, %s,%s,%s,%s,%s)", (mes, torre, linea, serviciogas, servicioagua, servicioenergia))
        con_db.commit()
        return redirect(url_for('facturas'))
        #flash('Usuario agregado correctamente', 'alert-success')
    
        
        



# @app.route ('/consultarFactura', methods=['POST'])
# def consultarFactura():
#     torre = request.form['numero_torre']
#     apt = request.form['numero_apt']
#     mes = request.form['mes']
#     servicio = request.form['servicio']
#     costoPago = operacion(servicio, apt, torre, mes)
#     flash('El costo del servicio es: '+ str(costoPago),'alert-success')
#     return url_for('facturas')

@app.route("/delete/<id>")
def delete_factura(id):
	cur = con_db.cursor()
	cur.execute("DELETE FROM tabla_padre WHERE id=%s", (id))
	con_db.commit()
	flash("Se elimino la factura correctamente", "warning")
	return redirect(url_for('facturas'))


@app.route("/update/<id>", methods=['POST'])
def get_factura(id):
	nombre = request.form['nombre']
	valor = request.form['valor']
	cantidad = request.form['cantidad']
	cur = con_db.cursor()
	if nombre and valor and cantidad:
		sql = """
			UPDATE productos
			SET nombre_producto = %s,
			valor_producto = %s,
			cantidad = %s
			WHERE idproducto = %s
		"""
		cur.execute(sql, (nombre, valor, cantidad, id))
		con_db.commit()
		flash("Producto actualizado correctamente", "success")
		return redirect(url_for('facturas'))
	else:
		return 'Error en la consulta'


#----------------------creacion de tablas------------------------------------

def create_table_facturas():
    cur = con_db.cursor()
    cur.execute("""
 			CREATE TABLE IF NOT EXISTS facturas(
				idfactura serial  NOT NULL,
				factura character varying (10)  NOT NULL,
				valor character varying(50),
				mes character varying(50),
				tipo character varying(50),
				CONSTRAINT pk_factura_id PRIMARY KEY (idfactura));
 		""")

con_db.commit()

def create_table_Usuarios():
    cur = con_db.cursor()
    cur.execute("""
 			CREATE TABLE IF NOT EXISTS usuarios(
				idusuario serial  NOT NULL,
				nombre character varying(50),
				torre character varying(50),
				apartamento character varying(50),
				cedula character varying(50),
				contraseña character varying(20),
				CONSTRAINT pk_usuarios_id PRIMARY KEY (idusuario));
 		""")

con_db.commit()

def create_table_apto():
	cur = con_db.cursor()
	cur.execute("""
 			CREATE TABLE IF NOT EXISTS apartamento(
 				id serial  NOT NULL,
 				usuario VARCHAR(50),
 				correo VARCHAR(30),
 				contraseña VARCHAR(200),
				CONSTRAINT pk_usuarios_id PRIMARY KEY (id));
 		""")

con_db.commit()

#----------------------------------------------------------------------------------------------------------------------





if __name__ == '__main__':
    
    app.run(debug=True, port=8003)
    