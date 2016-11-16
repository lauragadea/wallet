import falcon
import json
import mysql.connector
import datetime

#from settings.config import CONFIG



class PaymentResource(object):

	
	def on_get(self, req, resp):
		#resp.body = '{"pago": "ok"}'
		#resp.status = falcon.HTTP_200

		try:
			cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='walletdb')
			cursor = cnx.cursor()
			query = "SELECT id_producto, fecha FROM compras"
			
			cursor.execute(query)			
			rows = cursor.fetchall()
			compras = []
			for row in rows:
				diccionario = {'id_producto':row[0], 'fecha':row[1]}
				compras.append(diccionario)
				
			resp.body = json.dumps(compras)
			resp.status = falcon.HTTP_200
			cursor.close()
			cnx.close()
		except mysql.connector.Error as e:
			resp.status = falcon.HTTP_504
			resp.body = "ERROR: {}".format(e)

		resp.status = falcon.HTTP_200

	#realiza un pago
	def on_post(self, req, resp):
		#1. verificar cuanto es el total
		#2. verificar si le alcanza para pagarlo
		#	2.1 si no alcanza, enviar un json con codigo de error o msj
		#3. asentar en la tabla compras, y descontar del saldo
		try:
			cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='walletdb')
			cursor = cnx.cursor()
			#FECHA!!!
			
			#seleccionar todos los productos que me mande el cliente
			dni = 29718241
			producto = 2
			query = "SELECT * FROM productos WHERE id_producto = %(producto)s"
			

			cursor.execute(query, {'producto':producto})			
			fecha = datetime.datetime.now()
			
			#for row in rows:
			#	diccionario = {'id_producto'}
			for valor in cursor:
				id_producto = valor[0]
				#imprime el precio
				total = valor[2]
			
			query2 = "SELECT saldo FROM cuentas WHERE dni = %(dni)s"

			cursor.execute(query2, {'dni':dni})

			for valor in cursor:
				saldo = valor[0]
			print saldo
			
			if saldo > total:
				
				#no hardcodear id_producto, ni la fecha ni el dni
				producto = 3
				
				query3 = "INSERT INTO compras (dni, id_producto, fecha) VALUES (%s, %s, %s)"
				data = (dni, producto, fecha)
				cursor.execute(query3, data)
				cnx.commit()
				nuevo_saldo = saldo - total;
				#OJO CON LA FECHA, NO FUNCIONA
				query4 = "UPDATE cuentas SET saldo = %(saldo)s, fecha = %(fecha)s WHERE dni = %(dni)s"
				
				cursor.execute(query4, {'saldo':nuevo_saldo, 'fecha':fecha, 'dni':dni})
				cnx.commit()

			else:
				msj = "el saldo es insuficiente"
				resp.body = json.dumps(msj)
			#poner variable, no harcodeard 25
			#cursor.execute("UPDATE cuentas SET saldo = 425 WHERE DNI = 30564192")
			
			#cnx.commit()

			#resp.body = json.dumps()
			resp.status = falcon.HTTP_200
			cursor.close()
			cnx.close()
		except mysql.connector.Error as e:
			resp.status = falcon.HTTP_504
			resp.body = "ERROR: {}".format(e)

		resp.status = falcon.HTTP_200