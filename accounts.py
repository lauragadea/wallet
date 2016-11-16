import falcon
import json
import mysql.connector

class AccountsResource(object):

	#trae el saldo que tiene el usuario
	def on_get(self, req, resp):
	
		try:
			cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='walletdb')
			cursor = cnx.cursor()
			#dni = 30564192
			query = "SELECT saldo FROM cuentas where dni = %(dni)s"
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
	#viene con el dato de cuanta plata carga el usuario
	def on_post(self, req, resp):
		"""Handles POST requests"""
		try:
			cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='walletdb')
			cursor = cnx.cursor()
			
			#LEER parametro y guardar aca
			dni=30564192
			#LEER parametro y guardar aca
			saldo_a_cargar = 25
			query = "SELECT saldo FROM cuentas WHERE dni = %(dni)s"
			cursor.execute(query, {'dni':dni})			
			rows = cursor.fetchall()
			
			for row in rows:
				saldo_viejo = row[0]

			saldo_nuevo = saldo_viejo + saldo_a_cargar
			
			
			query2 = "UPDATE cuentas SET saldo = %(saldo)s WHERE DNI = %(dni)s"
			cursor.execute(query2, {'saldo':saldo_nuevo, 'dni':dni})
			
			cnx.commit()

			resp.body = json.dumps(saldo_nuevo)
			resp.status = falcon.HTTP_200
			cursor.close()
			cnx.close()
		except mysql.connector.Error as e:
			resp.status = falcon.HTTP_504
			resp.body = "ERROR: {}".format(e)

		resp.status = falcon.HTTP_200
		
