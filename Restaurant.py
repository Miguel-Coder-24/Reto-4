class MenuItem:
    def __init__(self, name: str, price: float, amount: int, type_: str = None):
        self.__name = None
        self.__price = None
        self.__amount = None
        self.__type = type_
        
        self.set_name(name)
        self.set_price(price)
        self.set_amount(amount)
    
    # Getters y setters con validaciones
    
    def get_name(self) -> str:
        return self.__name
    
    def set_name(self, name: str):
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non-empty string")
        self.__name = name.strip()
    
    def get_price(self) -> float:
        return self.__price
    
    def set_price(self, price: float):
        if not (isinstance(price, (int, float)) and price >= 0):
            raise ValueError("Price must be a non-negative number")
        self.__price = float(price)
    
    def get_amount(self) -> int:
        return self.__amount
    
    def set_amount(self, amount: int):
        if not (isinstance(amount, int) and amount >= 0):
            raise ValueError("Amount must be a non-negative integer")
        self.__amount = amount
    
    def get_type(self) -> str:
        return self.__type
    
    def set_type(self, type_: str):
        self.__type = type_
    
    def total_price(self) -> float:
        return self.get_price() * self.get_amount()
    
    def __str__(self):
        return f"{self.get_type()} - {self.get_name()} - ${self.get_price():.2f} x {self.get_amount()}"


class Beverage(MenuItem):
    def __init__(self, name: str, price: float, amount: int, flavour: str, type_: str = "Beverage"):
        super().__init__(name, price, amount, type_)
        self.__flavour = None
        self.set_flavour(flavour)
    
    def get_flavour(self) -> str:
        return self.__flavour
    
    def set_flavour(self, flavour: str):
        if not isinstance(flavour, str) or flavour.strip() == "":
            raise ValueError("Flavour must be a non-empty string")
        self.__flavour = flavour.strip()
    
    def __str__(self):
        return f"{self.get_type()} - {self.get_name()} ({self.get_flavour()}) - ${self.get_price():.2f} x {self.get_amount()}"


class MainCourse(MenuItem):
    def __init__(self, name: str, price: float, amount: int, appetizer: str, type_: str = "Main Course"):
        super().__init__(name, price, amount, type_)
        self.__appetizer = None
        self.set_appetizer(appetizer)
    
    def get_appetizer(self) -> str:
        return self.__appetizer
    
    def set_appetizer(self, appetizer: str):
        if not isinstance(appetizer, str):
            raise ValueError("Appetizer must be a string")
        self.__appetizer = appetizer.strip()
    
    def __str__(self):
        return f"{self.get_type()} - {self.get_name()} with appetizer {self.get_appetizer()} - ${self.get_price():.2f} x {self.get_amount()}"


class Order:
    def __init__(self, order_number: int, discount: float = 0):
        self.__order_number = None
        self.__items = []
        self.__discount = discount
        
        self.set_order_number(order_number)
    
    def get_order_number(self) -> int:
        return self.__order_number
    
    def set_order_number(self, order_number: int):
        if not (isinstance(order_number, int) and order_number > 0):
            raise ValueError("Order number must be a positive integer")
        self.__order_number = order_number
    
    def get_items(self) -> list:
        return self.__items
    
    def add_item(self, item: MenuItem):
        if not isinstance(item, MenuItem):
            raise TypeError("Only MenuItem instances can be added")
        self.__items.append(item)
    
    def remove_item(self, item: MenuItem):
        if item in self.__items:
            self.__items.remove(item)
        else:
            print("Item not found in the order.")
    
    def total_price(self) -> float:
        return sum(item.total_price() for item in self.__items)
    
    def count_by_type(self, type_: str) -> int:
        return sum(item.get_amount() for item in self.__items if item.get_type() == type_)
    
    def total_by_type(self, type_: str) -> float:
        return sum(item.total_price() for item in self.__items if item.get_type() == type_)
    
    def calculate_discount(self) -> tuple:
        total = self.total_price()
        discount = 0
        message = "No discount applied"
        
        # 20% off if total > 80,000
        if total > 80000:
            discount = total * 0.20
            message = "20% discount on total order"
        # 30% off beverages if more than 4 desserts
        elif self.count_by_type("Dessert") > 4:
            discount = self.total_by_type("Beverage") * 0.30
            message = "30% discount on beverages for ordering >4 desserts"
        # 10% off seafood if seafood total > 50,000
        elif self.total_by_type("Sea Food") > 50000:
            discount = self.total_by_type("Sea Food") * 0.10
            message = "10% discount on seafood"
        # 10% off beverages if main course ordered
        elif self.count_by_type("Main Course") > 0:
            discount = self.total_by_type("Beverage") * 0.10
            message = "10% discount on beverages with main course"
        # 15% off beverages if dessert ordered
        elif self.count_by_type("Dessert") > 0:
            discount = self.total_by_type("Beverage") * 0.15
            message = "15% discount on beverages with dessert"
        
        total_after_discount = total - discount
        return total_after_discount, f"{message}: -${discount:.2f}" if discount > 0 else message
    
    def apply_discount(self):
        return self.calculate_discount()
    
    def __str__(self):
        text = f"Order #{self.get_order_number()}\nItems:\n"
        for item in self.__items:
            text += f" - {item}\n"
        total, discount_message = self.calculate_discount()
        text += discount_message + "\n"
        text += f"Total after discount: ${total:.2f}"
        return text


class Payment:
    def __init__(self, order: Order, payment_method):
        self.__order = order
        self.__payment_method = payment_method
    
    def get_order(self) -> Order:
        return self.__order
    
    def set_order(self, order: Order):
        if not isinstance(order, Order):
            raise TypeError("Must be an Order instance")
        self.__order = order
    
    def get_payment_method(self):
        return self.__payment_method
    
    def set_payment_method(self, payment_method):
        self.__payment_method = payment_method
    
    def make_payment(self):
        total, message = self.__order.calculate_discount()
        print(f"Total to pay: ${total:.2f}")
        self.__payment_method.pay(total)


class PaymentMethod:
    def pay(self, amount: float):
        raise NotImplementedError("Subclasses must implement this method")


class Card(PaymentMethod):
    def __init__(self, number: str, cvv: str):
        self.__number = None
        self.__cvv = None
        
        self.set_number(number)
        self.set_cvv(cvv)
    
    def get_number(self) -> str:
        return self.__number
    
    def set_number(self, number: str):
        if not (isinstance(number, str) and number.isdigit() and len(number) in [13, 16]):
            raise ValueError("Card number must be 13 or 16 digits")
        self.__number = number
    
    def get_cvv(self) -> str:
        return self.__cvv
    
    def set_cvv(self, cvv: str):
        if not (isinstance(cvv, str) and cvv.isdigit() and len(cvv) == 3):
            raise ValueError("CVV must be 3 digits")
        self.__cvv = cvv
    
    def pay(self, amount: float):
        print(f"Paying ${amount:.2f} with card ending in {self.__number[-4:]}")


class Cash(PaymentMethod):
    def __init__(self, cash_given: float):
        self.__cash_given = None
        self.set_cash_given(cash_given)
    
    def get_cash_given(self) -> float:
        return self.__cash_given
    
    def set_cash_given(self, amount: float):
        if not (isinstance(amount, (int, float)) and amount >= 0):
            raise ValueError("Cash given must be non-negative")
        self.__cash_given = amount
    
    def pay(self, amount: float):
        if self.__cash_given >= amount:
            change = self.__cash_given - amount
            print(f"Payment successful. Change: ${change:.2f}")
        else:
            shortage = amount - self.__cash_given
            print(f"Insufficient funds. Need additional ${shortage:.2f}")


# Bloque para probar
if __name__ == "__main__":
    try:
        b1 = Beverage("Cola", 3500, 3, "Cola")
        m1 = MainCourse("Steak", 15000, 1, "Salad")
        d1 = Beverage("Lemonade", 2500, 2, "Lemon")
        
        order = Order(1)
        order.add_item(b1)
        order.add_item(m1)
        order.add_item(d1)
        
        print(order)
        
        card = Card("1234567890123456", "123")
        payment = Payment(order, card)
        payment.make_payment()
    
    except Exception as e:
        print(f"Error: {e}")
