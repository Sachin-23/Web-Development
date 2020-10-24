from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    contact = models.IntegerField(blank=True, null=True)


class Pet(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to="images/")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    genders = (("Male", "Male"), ("Female", "Female"))
    sex = models.CharField(max_length=10, choices=genders)
    zip_code = models.IntegerField()
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    age_groups = (("Young", "Young"), ("Adult", "Adult"), ("Senior", "Senior"))
    age_group = models.CharField(max_length=6, choices=age_groups)
    types = (("Dog", "Dog"), ("Cat", "Cat"), ("Other", "Other"))
    pet_type = models.CharField(max_length=256, choices=types)
    about = models.CharField(max_length=1024)
    added_at = models.DateTimeField(auto_now_add=True)
    adopted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return f"Id: {self.id}, \
                Name: {self.name}, \
                User: {self.owner.username}, \
                zip_code: {self.zip_code},\
                city: {self.city}, \
                age: {self.age_group}, \
                sex: {self.sex}, \
                state: {self.state}, \
                pet_type: {self.pet_type}, \
                about: {self.about}, \
                added_at: {self.added_at}, \
                adopted: {self.adopted}"

    def serialize(self):
        return {
                "id": self.id ,"name": self.name, "owner": self.owner.username, \
                "sex": self.sex, "zip_code": self.zip_code, "city": self.city, \
                "state": self.state, "age": self.age_group, \
                "type": self.pet_type, "about": self.about
                }


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlisted_user")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} wishlisted {self.pet.name}"

