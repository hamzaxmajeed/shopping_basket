Shopping Basket in Python
===

## ProductStore

Products are stored in a `ProductStore` object. This can either be created from a list of product tuples or initialized from a CSV file.

```python
from decimal import Decimal
from product import ProductStore

products = [
    ("pasta", Decimal("1.50")),
    ("twix", Decimal("0.80")),
    ("blueberries", Decimal("2.00")),
    ("fish", Decimal("3.20")),           
]
product_store = ProductStore(products)

# or

import os

csv_filepath = os.path.abspath('catalogue.csv')
product_store = ProductStore.init_from_filepath(csv_filepath)
```

The price for a product can be retrieved with `get_product_price()`.

```python
price = product_store.get_product_price("twix")
```

## Basket

Baskets should be created with a ProductStore instance from which the basket can derive prices.

```python
from basket import Basket

my_basket = Basket(product_store)
```

Products can be added to a basket by name, with an optional quantity parameter.

```python
basket.add("pasta")
basket.add("twix", 3)
```

The total for the basket can be calculated with `get_total()`. This method optionally takes a list of [Offer](#offers) objects that are applied to items in the basket when calculating the total.

```python
total = basket.get_total()

# with offers
total_with_offers = basket.get_total(offers=[offer_one, offer_two, offer_three])
```