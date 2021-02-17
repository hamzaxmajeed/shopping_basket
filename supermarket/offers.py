class AbstractOffer(object):
    """
    An interface for subclassing Offer classes.
    """

    def __init__(self, target_product):
        self.target_product = target_product

    def calculate_line_total(self, basket_item, market, *args):
        """
        All subclasses must implement this to return a new total for the basket_item.
        """
        raise NotImplementedError()


class NoOffer(AbstractOffer):
    """
    When there is no offer or discount available.
    """

    def calculate_line_total(self, basket_item, market, *args):
        """
        Returns the basket_item.get_line_total.
        """
        return basket_item.get_line_total(market)


class MultiBuyOffer(AbstractOffer):
    """
    When you buy a certain quantity to get another quantity for free.

    e.g. Buy two get one free would be in the form: MultiBuyOffer(2, 1, "biscuits")
    """

    def __init__(self, target_product, charge_for_quantity, free_quantity, *args, **kwargs):
        self.charge_for_quantity = charge_for_quantity
        self.free_quantity = free_quantity
        super(MultiBuyOffer, self).__init__(target_product, *args, **kwargs)

    def calculate_line_total(self, basket_item, market, *args):
        """
        Charge for multiples of the quotient and add remainder.
        """
        bundles, remainder = divmod(basket_item.quantity, self.charge_for_quantity + self.free_quantity)

        if remainder > self.charge_for_quantity:
            bundles += 1
            remainder = 0

        charge_quantity = (bundles * self.charge_for_quantity) + remainder
        return market.get_product_price(basket_item.product) * charge_quantity

class DependentDiscountOffer(AbstractOffer):

    """
    A percentage discount is applied to the target_product in the presence of another product.
    """

    def __init__(self, target_product, dependent_product, discount, *args, **kwargs):
        self.dependent_product = dependent_product
        self.discount = discount
        super(DependentDiscountOffer, self).__init__(target_product, *args, **kwargs)

    def calculate_line_total(self, basket_item, market, basket, *args):
        """
        Returns total for the basket_item taking into account the eligible
        discount that may apply in the presense of dependent products in the basket.
        """
        try:
            dependent_quantity = basket.get_item(self.dependent_product).quantity
        except AttributeError:
            return basket_item.get_line_total(market)
        else:
            # Number of target_product eligible for discount.
            eligible_for_discount = min(dependent_quantity, basket_item.quantity)

            # Full price of a single target_product.
            single_full_price = market.get_product_price(basket_item.product)

            # Subtotal for eligible target_products before discount.
            eligible_subtotal = eligible_for_discount * single_full_price

            # Total for the eligible target_product after discount.
            eligible_total = eligible_subtotal - (eligible_subtotal * self.discount)

            # Total for ineligible target_product.
            remainder_total = (basket_item.quantity - eligible_for_discount) * single_full_price

            return eligible_total + remainder_total