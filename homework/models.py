from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return self.quantity >= quantity


    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if not self.check_quantity(quantity):
            raise ValueError(f"Недостаточно товара {self.name} на складе")
        self.quantity -= quantity

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int] #Эта запись не создает переменную, а просто указывает, какого она типа. Это подсказка

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):#:
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product not in self.products:
            return

        # Если remove_count не указан или больше текущего количества - удалить полностью
        if remove_count is None or remove_count >= self.products[product]:
            del self.products[product]
        else:
            self.products[product] -= remove_count

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        return sum(product.price * quantity for product, quantity in self.products.items())

    def buy(self):
        """
        Метод покупки.
        Сначала проверяем, хватает ли всех товаров.
        Если хотя бы одного не хватает — выбрасываем ValueError.
        Если всё в наличии — списываем товары.
        """
        # Проверяем, хватает ли всех товаров на складе
        for product, quantity in self.products.items():
            if not product.check_quantity(quantity):
                raise ValueError(f'Недостаточно товара {product.name} на складе')

        # Если проверки пройдены, списываем товары
        for product, quantity in self.products.items():
            product.buy(quantity)

        self.clear()
