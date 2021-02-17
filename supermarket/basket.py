from decimal import Decimal


class Basket(object):

    def __init__(self, market=None):
        self.items = []
        self.product_market = market

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        self.items[key]

    def get_total(self, offers=None):
        """
        Returns sum of the items in the basket as a decimal.

        If a list of products with offers are given, then these are applied.
        Where multiple offers may apply to a product, the cheapest is used.
        """
        totals = []
        for item in self.items:
            # The original sub_total without any offers applied.
            line_total = item.get_line_total(self.product_market)

            if offers is not None:
                # Apply each offer in turn.
                for offer in offers:
                    if offer.target_product == item.product:
                        offer_total = offer.calculate_line_total(item, self.product_market, self)
                        # Retain cheapest total to append to totals list.
                        if offer_total < line_total:
                            line_total = offer_total

            totals.append(line_total)
        
        return Decimal(sum(totals))

    def add(self, item, quantity=1):
        """
        Add an item to the basket, then return the basket item.

        The quantity will increase on an existing item by the amount passed with the quantity parameter.
        """
        basket_item = self.get_item(item)
        if basket_item is None:
            basket_item = BasketItem(item, quantity)
            self.items.append(basket_item)
        else:
            basket_item.quantity += quantity
        return basket_item

    def get_item(self, item_name):
        """
        Return BasketItem where product corresponds with item_name.
        """
        return next((item for item in self.items if item.product == item_name), None)


class BasketItem(object):

    def __init__(self, product, quantity=1):
        self.product = product
        self.quantity = quantity

    def get_line_total(self, market):
        """
        Return total derived from product in market.
        """
        return market.get_product_price(self.product) * self.quantity