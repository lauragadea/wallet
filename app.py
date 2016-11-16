import falcon
import accounts
import users
import payment	
import products
import purchases

api = application = falcon.API()

users = users.UsersResource()
account = accounts.AccountsResource()
payment = payment.PaymentResource()
products = products.ProductsResource()
purchases = purchases.PurchasesResource()

api.add_route('/usuario', users)
api.add_route('/saldo', account)
api.add_route('/pago', payment)
api.add_route('/productos', products)
api.add_route('/compras', purchases)
