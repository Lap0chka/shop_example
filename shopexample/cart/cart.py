class Cart:
    def __init__(self, request):

        self.session = request.session
        self.cart = self.cart_init()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def cart_init(self):
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        return cart

    def add(self, product, quantity):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}

        self.cart[product_id]['quantity'] = quantity
        self.session.modified = True

