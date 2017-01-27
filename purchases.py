import falcon
import json
import mysql.connector

class PurchasesResource(object):

	#trae las ultimas 5 compras del usuario
	def on_get(self, req, resp):
		
		try:
			dni = 30564192
			cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='walletdb')
			cursor = cnx.cursor()
			query = "SELECT concepto.descripcion, movimiento.fecha, movimiento.monto FROM concepto INNER JOIN movimiento ON movimiento.id_concepto = concepto.id_concepto INNER JOIN cuenta ON cuenta.id_cuenta = movimiento.id_cuenta WHERE cuenta.dni = %(dni)s LIMIT 5"
			
			cursor.execute(query, {'dni':dni})			
			rows = cursor.fetchall()
			listado = []
			for row in rows:
				diccionario = {'descripcion':row[0], 'fecha':row[1], 'monto':row[2]}
				listado.append(diccionario)

			#ordeno por fecha
			listado_ordenado = sorted(listado, key=lambda k:k['fecha'])
			resp.body = json.dumps(listado_ordenado)
			resp.status = falcon.HTTP_200
			cursor.close()
			cnx.close()
		except mysql.connector.Error as e:
			resp.status = falcon.HTTP_504
			resp.body = "ERROR: {}".format(e)

		resp.status = falcon.HTTP_200
		
