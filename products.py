import falcon
import json
import mysql.connector

class ProductsResource(object):

	#trae los productos disponibles
	def on_get(self, req, resp):
		
		try:
			cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='walletdb')
			cursor = cnx.cursor()
			query = "SELECT * FROM productos"
			
			cursor.execute(query)			
			rows = cursor.fetchall()
			productos = []
			for row in rows:
				diccionario = {'descripcion':row[1], 'precio':row[2]}
				productos.append(diccionario)

			resp.body = json.dumps(productos)
			resp.status = falcon.HTTP_200
			cursor.close()
			cnx.close()
		except mysql.connector.Error as e:
			resp.status = falcon.HTTP_504
			resp.body = "ERROR: {}".format(e)

		resp.status = falcon.HTTP_200
		
