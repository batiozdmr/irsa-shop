from decimal import Decimal

from django.conf import settings

from apps.product.models import Product, ShippingMethod
from apps.checkout.models import CouponCodeList


class Basket:
    """

    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty, variant_color="", variant_option="", variant_explanation=""):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        product_key = product_id + '_' + variant_option + '_' + variant_explanation
        if product_key in self.basket:
            if self.basket[product_key]["variant_option"] == variant_option:
                self.basket[product_key]["qty"] = self.basket[product_key]["qty"] + qty
            elif self.basket[product_key]["variant_color"] == variant_color:
                self.basket[product_key]["qty"] = self.basket[product_key]["qty"] + qty
            elif self.basket[product_key]["variant_explanation"] == variant_explanation:
                self.basket[product_key]["qty"] = self.basket[product_key]["qty"] + qty
            else:
                self.basket[product_key]["qty"] = self.basket[product_key]["qty"] + qty
                self.basket[product_key]["variant_color"] = variant_color
                self.basket[product_key]["variant_option"] = variant_option
                self.basket[product_key]["variant_explanation"] = variant_explanation

        else:
            self.basket[product_key] = {"price": str(product.price), "qty": qty,
                                        "variant_color": str(variant_color), "variant_option": str(variant_option),
                                        "variant_explanation": str(variant_explanation)}

        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = []
        for keyss in self.basket.keys():
            product_ids.append(keyss.split('_')[0])

        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            for keyss in self.basket.keys():
                if keyss.split('_')[0] == str(product.id):
                    variant_option = keyss.split('_')[1]
                    variant_explanation = keyss.split('_')[2]
                    basket[str(product.id) + '_' + variant_option + '_' + variant_explanation]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item["qty"] for item in self.basket.values())

    def count(self):

        product_qty = self.__len__()
        if not product_qty:
            product_qty = 0

        return product_qty

    def update(self, product, qty):
        """
        Update values in session data
        """

        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        self.save()

    def update_note(self, product, note=""):
        """
        Update values in session data (note)
        """
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]["note"] = note
        self.save()

    def get_subtotal_price(self):

        return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

    """
    def get_delivery_price(self):
        newprice = 0.00

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice
    """

    """
    """

    def get_total_price(self):
        shipping_methods = ShippingMethod.objects.filter(is_active=True).last()
        newprice = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        """
        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price
        """
        total = subtotal + Decimal(newprice) + Decimal(shipping_methods.fee) - Decimal(
            self.session['coupon_code_price'])
        if total < 0:
            total = 0
        else:
            total = total

        return total

    """
    def basket_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        total = subtotal + Decimal(deliveryprice)
        return total
    """

    def delete(self, product):
        """

        :param product: Product id
        :return:
        """

        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        # del self.session["address"]
        # del self.session["purchase"]
        self.save()

    def save(self):
        self.session.modified = True
