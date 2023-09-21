from django.db import models
from users.models import User

# Create your models here.
# Таблица для базы данных
# Наследуемся от класса Model. Он позволяет нам обычный питоновский класс проброзить в модель
# и в дальнейшем переносить в структуру

class ProductCategory(models.Model):
    objects = True
    name = models.CharField(max_length=120,unique=True)
    description = models.TextField(null=True,blank=True) # Это значит что это` поле может быть пустым

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категория'

    def __str__(self):
        return self.name



class Product(models.Model):
    objects = True
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2) # Длина до запятой и после запятой
    quantity = models.PositiveIntegerField(default=0) # Количество товаров на складе
    image = models.ImageField(upload_to='products_images') # Это означает в какую папку буду загружаться фотки
    category = models.ForeignKey(to=ProductCategory,on_delete=models.CASCADE)# Этот класс связывает одну таблицу с другой.

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт : {self.name} Категория: {self.category.name}'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    objects = True
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity