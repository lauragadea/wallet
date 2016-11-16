import falcon
import json
import mysql.connector

class UsersResource(object):

	#trae datos de usuario y saldo
	def on_get(self, req, resp):
		
		try:
			cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='walletdb')
			cursor = cnx.cursor()
			dni = 30564192
			query = "SELECT persona.dni, nombre, apellido, saldo FROM persona INNER JOIN cuentas ON persona.dni = cuentas.dni where persona.dni = %(dni)s"
			
			cursor.execute(query, {'dni':dni})			
			rows = cursor.fetchall()
			usuario = []
			for row in rows:
				diccionario = {'dni':row[0], 'nombre':row[1], 'apellido':row[2], 'saldo':row[3]}
				usuario.append(diccionario)

			resp.body = json.dumps(usuario)
			resp.status = falcon.HTTP_200
			cursor.close()
			cnx.close()
		except mysql.connector.Error as e:
			resp.status = falcon.HTTP_504
			resp.body = "ERROR: {}".format(e)

		resp.status = falcon.HTTP_200
		

