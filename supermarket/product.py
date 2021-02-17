import csv
import codecs
from decimal import Decimal

class NoSuchProductError(Exception):
    pass

class ProductStore(object):
    """
    Mapping products to prices.
    """

    @classmethod
    def init_from_filepath(cls, filepath):
        """
        Returns an instance initialised from a CSV file.
        """
        with open(filepath, "rb") as csvfile:
            csvreader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'))
            items = []
            for row in csvreader:
                items.append((row[0], Decimal(row[1])))
        return cls(items)

    def __init__(self, items):
        """
        Expects items in the format:
            products = [
                ("pasta", Decimal("1.50")),
                ("twix", Decimal("0.80")),
                ("blueberries", Decimal("2.00")),
                ("fish", Decimal("3.20")),           
            ]
        """
        self.items = items


    def get_product_price(self, product_name):
        """
        Return the price corresponding the passed product_name.
        """
        product_price = next((prod[1] for prod in self.items if prod[0] == product_name), None)
        if product_price is None:
            raise NoSuchProductError("No such product '{product_name}' in this store.".format(product_name=product_name))
        else:
            return product_price