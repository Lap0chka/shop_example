class Cart:
    def __init__(self, request):

        self.session = request.session
        self.cart = self.cart_init()

    def cart_init(self):
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        return cart
