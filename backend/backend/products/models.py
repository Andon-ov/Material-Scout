from django.db import models

# Create your models here.


# class TravelOffer(models.Model):
#     title = models.CharField(max_length=255)
#     destination = models.CharField(max_length=255)
#     transport = models.CharField(max_length=50)
#     duration_days = models.IntegerField()
#     duration_nights = models.IntegerField()
#     departure_date = models.DateField()
#     price_bgn = models.DecimalField(max_digits=10, decimal_places=2)
#     price_eur = models.DecimalField(max_digits=10, decimal_places=2)
#     phone_numbers = models.TextField()
#     itinerary = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)


# from django.db import models

class TravelOffer(models.Model):
    title = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    transport = models.CharField(max_length=50)
    duration_days = models.IntegerField()
    duration_nights = models.IntegerField()
    departure_date = models.DateField()
    price_bgn = models.DecimalField(max_digits=10, decimal_places=2)
    price_eur = models.DecimalField(max_digits=10, decimal_places=2)
    phone_numbers = models.TextField()
    itinerary = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    source_url = models.URLField(null=True, blank=True)

    # Новите полета
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    standard_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    single_room_extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.TextField(null=True, blank=True)
    min_participants = models.IntegerField(null=True, blank=True)
    required_documents = models.JSONField(null=True, blank=True)


    # Списъци – тук е добре да се използва JSONField, за да може да пази масиви
    price_includes = models.JSONField(null=True, blank=True)
    price_excludes = models.JSONField(null=True, blank=True)
    extras_pre = models.JSONField(null=True, blank=True)
    extras_on_spot = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
