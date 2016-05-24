class Text(object):
    def __init__(self, text):
        self.text = text

    def to_dict(self):
        return {
            'text': self.text
        }


class Image(object):
    def __init__(self, url):
        self.url = url

    def to_dict(self):
        return {
            'attachment': {
                'type': 'image',
                'payload': {
                    'url': self.url
                }
            }
        }


class Button(object):
    def __init__(self, title, url=None, payload=None):
        if len(title) > 20:
            raise ValueError('Title cannot be longer 20 characters.')
        self.title = title
        self.url = url
        self.payload = payload

    def to_dict(self):
        data = {
            'title': self.title
        }
        if self.url:
            data['type'] = 'web_url'
            data['url'] = self.url
        elif self.payload:
            data['type'] = 'postback'
            data['payload'] = self.payload

        return data


class Element(object):
    """
    To be used with the generic template to create a carousel
    """

    def __init__(self, title, item_url=None, image_url=None,
                 subtitle=None, buttons=None, quantity=None,
                 price=None, currency=None):

        self._title = title
        self.item_url = item_url
        self.image_url = image_url
        self._subtitle = subtitle
        self.buttons = buttons
        self.quantity = quantity
        self.price = price
        self.currency = currency

    @property
    def title(self):
        if len(self._title) > 45:
            raise ValueError(
                'Title cannot be longer 45 characters'
            )
        return self._title

    @property
    def subtitle(self):
        if self._subtitle:
            if len(self._subtitle) > 80:
                raise ValueError('Subtitle cannot be longer 80 characters')
        return self._subtitle

    def to_dict(self):
        data = {
            'title': self.title,
        }
        if self.item_url:
            data['item_url'] = self.item_url
        if self.image_url:
            data['image_url'] = self.image_url
        if self._subtitle:
            data['subtitle'] = self.subtitle
        if self.quantity:
            data['quantity'] = self.quantity
        if self.price:
            data['price'] = self.price
        if self.currency:
            data['currency'] = self.currency
        if self.buttons:
            data['buttons'] = [
                button.to_dict() for button in self.buttons
            ]

        return data


class Adjustment(object):
    def __init__(self, name=None, amount=None):
        # Optional
        self.name = name
        self.amount = amount

    def to_dict(self):
        return {
            'name': self.name,
            'amount': self.amount
        }


class Address(object):
    def __init__(self, street_1, city, postal_code,
                 state, country, street_2=''):
        # Required
        self.street_1 = street_1
        self.city = city
        self.postal_code = postal_code
        self.state = state
        self.country = country
        # Optional
        self.street_2 = street_2

    def to_dict(self):
        return {
            'street_1': self.street_1,
            'street_2': self.street_2,
            'city': self.city,
            'postal_code': self.postal_code,
            'state': self.state,
            'country': self.country,
        }


class Summary(object):
    def __init__(self, total_cost, subtotal=None, shipping_cost=None, total_tax=None):
        # Required
        self.total_cost = total_cost
        # Optional
        self.subtotal = subtotal
        self.shipping_cost = shipping_cost
        self.total_tax = total_tax

    def to_dict(self):
        return {
            'subtotal': self.subtotal,
            'shipping_cost': self.shipping_cost,
            'total_tax': self.total_tax,
            'total_cost': self.total_cost
        }
