from django.db import models
from store.validators import validate_file_size
from django.core.validators import MinValueValidator

class Collection(models.Model):
    title = models.CharField(max_length=255)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    title = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    SIZE_CHOICES = [('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('35', '35'), ('36', '36'), ('40', '40'), ('43', '43')]
    GENDER_CHOICES = [('Man', 'Man'), ('Woman', 'Woman'), ('Kids', 'Kids')]

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='store/images', validators=[validate_file_size])
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    size = models.CharField(max_length=7, choices=SIZE_CHOICES)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']
