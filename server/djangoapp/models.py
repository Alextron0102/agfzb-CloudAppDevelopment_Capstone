from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.TextField(null=True)
    def __str__(self):
        return self.name
    def get_name(self):
        return self.name
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    carmakes = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealer_id = models.IntegerField(null=False)
    type = models.CharField(null=False, max_length=30, choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Wagon', 'Wagon')])
    year = models.DateField(null=False)
    def get_name(self):
        return self.name
    def get_carmake_name(self):
        return self.carmakes.get_name()
    def get_year(self):
        return self.year.year
    def __str__(self):
        return self.name
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(object):
    def __init__(self, dealer_id, short_name, full_name, address, city, state, st, lat,long, zipcode):
        self.dealer_id = dealer_id
        self.city = city
        self.state = state
        self.st = st
        self.address = address
        self.zipcode = zipcode
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name
    def __str__(self):
        return self.full_name
        

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(object):
    def __init__(self, review_id,dealership,name,purchase,review,purchase_date,car_make,car_model,car_year,sentiment):
        self.id = review_id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
    def __str__(self):
        return self.name