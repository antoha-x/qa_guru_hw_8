"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_newspaper():
    return Product("newspaper", 10, "This is a newspaper", 100)


@pytest.fixture
def cart():
    return Cart()


@pytest.fixture
def cart_with_products(product, product_newspaper):
    cart = Cart()
    cart.add_product(product, 10)
    cart.add_product(product_newspaper, 10)
    return cart


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity

        assert product.check_quantity(0)
        assert product.check_quantity(-1)
        assert product.check_quantity(999)
        assert product.check_quantity(1000)
        assert not product.check_quantity(1001)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy

        expected = product.quantity - 1
        product.buy(1)
        actual = product.quantity
        assert actual == expected

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии

        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_cart(self, product, cart):
        cart.add_product(product)
        assert product in cart.products
        assert cart.products[product] == 1

        cart.add_product(product, 2)
        assert cart.products[product] == 3

    def test_remove_product_cart(self, cart_with_products, product, product_newspaper):
        cart_with_products.remove_product(product, 5)
        assert cart_with_products.products[product] == 5

        cart_with_products.remove_product(product)
        assert product not in cart_with_products.products

        cart_with_products.remove_product(product_newspaper, 11)
        assert product_newspaper not in cart_with_products.products

    def test_clear_cart(self, cart_with_products):
        cart_with_products.clear()
        assert len(cart_with_products.products) == 0

    def test_get_total_price_cart(self, cart, cart_with_products):
        assert cart.get_total_price() == 0.0
        assert cart_with_products.get_total_price() == 1100

    def test_buy_cart(self, cart_with_products, product, product_newspaper):
        cart_with_products.buy()
        assert product.quantity == 990
        assert product_newspaper.quantity == 90
        assert len(cart_with_products.products) == 0

    def test_buy_cart_rase_value_error(self, cart, product_newspaper):
        cart.add_product(product_newspaper, 101)
        with pytest.raises(ValueError):
            cart.buy()
