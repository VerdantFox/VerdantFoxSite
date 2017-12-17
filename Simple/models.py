from django.db import models


class Encryption(models.Model):
    encryption_key = models.CharField(max_length=40)
    plain_text = models.CharField(max_length=500)
    encrypted_text = models.CharField(max_length=500)

    def __str__(self):
        return "text: " + self.plain_text


class Decryption(models.Model):
    encryption_key = models.CharField(max_length=40)
    encrypted_text = models.CharField(max_length=500)
    decrypted_text = models.CharField(max_length=500)

    def __str__(self):
        return "text: " + self.decrypted_text

