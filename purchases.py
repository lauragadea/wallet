import falcon
import json
import mysql.connector

class PurchasesResource(object):

	#trae las ultimas 5 compras del usuario
	def on_get(self, req, resp):
		
		try:
			cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='walletdb')
			cursor = cnx.cursor()
			query = "SELECT  descripcion, precio, fecha FROM compras INNER JOIN productos ON compras.id_producto = productos.id_producto where dni = 30564192 limit 5"
			
			cursor.execute(query)			
			rows = cursor.fetchall()
			listado = []
			for row in rows:
				diccionario = {'descripcion':row[0], 'precio':row[1], 'fecha':row[2]}
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
		
