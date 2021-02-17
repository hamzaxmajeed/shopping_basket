import os
import unittest
from decimal import Decimal

from basket import Basket, BasketItem
from product import NoSuchProductError, ProductStore
from offers import NoOffer, MultiBuyOffer, DependentDiscountOffer


# Few test cases for the shopping basket and products with and without offers.


class ProductStoreTest(unittest.TestCase):

    def _create_product_store(self):
        """
        Helper method to create populated ProductStore.
        """
        products = [
            ("pasta", Decimal("1.50")),
            ("twix", Decimal("0.80")),
            ("blueberries", Decimal("2.00")),
            ("fish", Decimal("3.20")),           
        ]
        return ProductStore(products)

    def test_get_product_price(self):
        """
        ProductStore returns the price of the corresponding product.
        """
        product_store = self._create_product_store()
        self.assertEqual(product_store.get_product_price("pasta"), Decimal("1.50"))

    def test_get_product_price_no_product(self):
        """
        ProductStore raises exception when no product matches.
        """
        product_store = self._create_product_store()
        self.assertRaises(NoSuchProductError, product_store.get_product_price, 'bike')

    def test_init_from_filepath(self):
        """
        ProductStore object can be created from csv file.
        """
        csv_filepath = os.path.abspath('catalogue.csv')
        product_store = ProductStore.init_from_filepath(csv_filepath)
        self.assertEqual(len(product_store.items), 6)

    def test_add_single_item(self):
        """
        Basket.add() a single item is successful.
        """
        basket = Basket()
        basket.add("pasta")
        self.assertEqual(len(basket), 1)

    def test_add_two_items(self):
        """
        Adding more than one item increases basket length.
        """
        basket = Basket()
        basket.add("pasta")
        basket.add("twix")
        self.assertEqual(len(basket), 2)

    
    def test_nooffer_target(self):
        """
        NoOffer is correctly assigned.
        """
        no_offer_pasta = NoOffer("pasta")
        self.assertEqual(no_offer_pasta.target_product, "pasta")

    def test_nooffer_total(self):
        """
        NoOffer's calculate_line_total returns same value as basket item line total.
        """
        product_store = self._create_product_store()
        no_offer_pasta = NoOffer('pasta')
        basketitem = BasketItem('pasta')
        self.assertEqual(basketitem.get_line_total(product_store), no_offer_pasta.calculate_line_total(basketitem, product_store))


    def test_bogof_one_item(self):
        """
        Buy one get one free correct line total for item with 1 quantity.
        """
        product_store = self._create_product_store()
        bogof_blueberries = MultiBuyOffer("blueberries", 1, 1)
        basketitem = BasketItem("blueberries")
        self.assertEqual(bogof_blueberries.calculate_line_total(basketitem, product_store), Decimal("2.00"))

    def test_bogof_one_item_two_quantity(self):
        """
        Buy one get one free correct line total for item with 2 quantity.
        """
        product_store = self._create_product_store()
        bogof_blueberries = MultiBuyOffer("blueberries", 1, 1)
        basketitem = BasketItem("blueberries", 2)
        self.assertEqual(bogof_blueberries.calculate_line_total(basketitem, product_store), Decimal("2.00"))

    def test_multibuy_one_item_buy_2_1_free(self):
        """
        Buy two get one free correct line total for item with 1 quantity.
        """
        product_store = self._create_product_store()
        bogof_blueberries = MultiBuyOffer("blueberries", 2, 1)
        basketitem = BasketItem("blueberries")
        self.assertEqual(bogof_blueberries.calculate_line_total(basketitem, product_store), Decimal("2.00"))

    def test_multibuy_two_item_buy_2_1_free(self):
        """
        Buy two get one free correct line total for item with 2 quantity.
        """
        product_store = self._create_product_store()
        bogof_blueberries = MultiBuyOffer("blueberries", 2, 1)
        basketitem = BasketItem("blueberries", 2)
        self.assertEqual(bogof_blueberries.calculate_line_total(basketitem, product_store), Decimal("4.00"))


    def test_one_without_dependent(self):
        """
        One target product in the absence of its dependent product doesn't trigger discount.
        """
        product_store = self._create_product_store()
        twix_20_discount = DependentDiscountOffer("twix", "pasta", Decimal("0.2"))
        basket = Basket(product_store)
        twix_basketitem = basket.add("twix")
        self.assertEqual(twix_20_discount.calculate_line_total(twix_basketitem, product_store, basket), Decimal("0.80"))

    def test_one_with_one_dependent(self):
        """
        One target product in the presence of one dependent product triggers discount.
        """
        product_store = self._create_product_store()
        twix_20_discount = DependentDiscountOffer("twix", "pasta", Decimal("0.2"))
        basket = Basket(product_store)
        twix_basketitem = basket.add("twix")
        basket.add("pasta")
        self.assertEqual(twix_20_discount.calculate_line_total(twix_basketitem, product_store, basket), Decimal("0.64"))


    def test_get_total_with_one_offer(self):
        """
        Basket get_total returns correct value with a bogof offer applied.
        """
        product_store = self._create_product_store()
        bogof_blueberries = MultiBuyOffer("blueberries", 1, 1)
        basket = Basket(product_store)
        basket.add("blueberries", 2)
        basket.add("fish")
        self.assertEqual(basket.get_total(offers=[bogof_blueberries]), Decimal('5.20'))

    def test_get_total_with_dependent_discount_offer(self):
        """
        Basket get_total returns correct value with dependent discount offer applied.
        """
        product_store = self._create_product_store()
        twix_pasta_20_discount = DependentDiscountOffer("twix", "pasta", Decimal("0.2"))
        basket = Basket(product_store)
        basket.add("twix", 2)
        basket.add("pasta")
        self.assertEqual(basket.get_total(offers=[twix_pasta_20_discount]), Decimal('2.94'))

if __name__ == "__main__":
    unittest.main()