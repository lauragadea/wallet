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
			id_cuenta = 1
			id_concepto = 1
			total = 100
			
			fecha = datetime.datetime.now()
			
			query2 = "SELECT saldo FROM cuenta WHERE dni = %(dni)s"

			cursor.execute(query2, {'dni':dni})

			for valor in cursor:
				saldo = valor[0]
			print saldo
			
			if saldo > total:
				
									
				query3 = "INSERT INTO movimiento (id_concepto, id_cuenta, monto, fecha) VALUES (%s, %s, %s, %s)"
				data = (id_concepto, id_cuenta, total, fecha)
				cursor.execute(query3, data)
				cnx.commit()
				nuevo_saldo = saldo - total;
				#OJO CON LA FECHA, NO FUNCIONA
				query4 = "UPDATE cuenta SET saldo = %(saldo)s, fecha = %(fecha)s WHERE dni = %(dni)s"
				
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