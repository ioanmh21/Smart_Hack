from django.db import models
from django.utils import timezone


class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    parola = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.email


class Obiect(models.Model):
    id_obiect = models.AutoField(primary_key=True)
    tip_obiect = models.CharField(max_length=100)
    id_css = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.tip_obiect} ({self.id_css})"


class Rezervare(models.Model):
    id_rez = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="rezervari", on_delete=models.CASCADE)
    obiect = models.ForeignKey(Obiect, related_name="rezervari", on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    data_si_ora = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["obiect", "data_si_ora"], name="unique_rezervare_slot"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.email} -> {self.obiect.tip_obiect} @ {self.data_si_ora}"
