import falcon
import json
import mysql.connector
import datetime

class AccountsResource(object):

	#trae el saldo que tiene el usuario
	def on_get(self, req, resp):
	
		try:
			cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='walletdb')
			cursor = cnx.cursor()
			#dni = 30564192
			query = "SELECT saldo FROM cuenta where dni = %(dni)s"
			#LEER parametro y guardar aca
			dni = 30564192
			cursor.execute(query, {'dni':dni })			

			data = {}
			#print cursor
			for valor in cursor:
				data["saldo"] = valor 
				

				#data["nombre"] = nombre
				#data["apellido"] = apellido
				#data["domicilio"] = domicilio

			resp.body = json.dumps(data)
			resp.status = falcon.HTTP_200
			cursor.close()
			cnx.close()

		except mysql.connector.Error as e:
			resp.status = falcon.HTTP_504
			resp.body = "ERROR: {}".format(e)

		resp.status = falcon.HTTP_200

	#carga credito en la billetera virtual
	#viene con el dato del nuevo saldo
	def on_post(self, req, resp, saldo_nuevo):
		"""Handles POST requests"""
		try:
			cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='walletdb')
			cursor = cnx.cursor()
			
			fecha = datetime.datetime.today().strftime("%Y-%m-%d")
			print fecha
			
			
			#LEER parametro y guardar aca
			dni=30564192
			#ojooo, nTENDRIA QUE TRAERME EL SALDO VIEJO PARA ASENTAR EN MOVIMIENTOS EL SALDo QUE CARGO
			monto = 0
			query0 = "SELECT saldo FROM cuenta where dni = %(dni)s"
			cursor.execute(query0, {'dni':dni})

			for valor in cursor:
				saldo_viejo = valor[0] 
			print saldo_viejo
			monto = int(saldo_nuevo) - saldo_viejo
			
			
			query = "UPDATE cuenta SET saldo = %(saldo)s WHERE DNI = %(dni)s"
			cursor.execute(query, {'saldo':saldo_nuevo,'dni':dni})
			
			cnx.commit()

			query2 = "INSERT INTO movimiento (id_concepto, id_cuenta, monto, fecha) VALUES (%s, %s, %s, %s)"
			#NO HARDCODEAR
			id_concepto = 2
			id_cuenta = 1
			#fecha = '2017-02-02'
			data = (id_concepto, id_cuenta, monto, fecha)

			cursor.execute(query2, data)

			cnx.commit()

			resp.body = json.dumps(saldo_nuevo)
			resp.status = falcon.HTTP_200
			cursor.close()
			cnx.close()
		except mysql.connector.Error as e:
			resp.status = falcon.HTTP_504
			resp.body = "ERROR: {}".format(e)

		resp.status = falcon.HTTP_200
		
