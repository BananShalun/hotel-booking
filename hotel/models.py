from django.db import models
from django.conf import settings

class RoomCategory(models.Model):
    name = models.CharField("Название категории", max_length=100, unique=True)
    base_price = models.DecimalField("Базовая цена за ночь", max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField("Вместимость (чел.)", default=2)

    class Meta:
        verbose_name = "Категория номера"
        verbose_name_plural = "Категории номеров"

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField("Название услуги", max_length=150, unique=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Дополнительная услуга"
        verbose_name_plural = "Дополнительные услуги"

    def __str__(self):
        return f"{self.name} ({self.price} ₽)"


class Booking(models.Model):
    # Связь с пользователем (гостем)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Гость",
    )
    # Связь со справочником категорий
    room_category = models.ForeignKey(
        RoomCategory,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Категория номера",
    )
    # Связь многие-ко-многим с услугами
    services = models.ManyToManyField(
        Service,
        blank=True,
        related_name="bookings",
        verbose_name="Дополнительные услуги",
    )
    # Текстовое поле для поиска
    guest_name = models.CharField("Имя гостя", max_length=200, db_index=True)
    # Длинный текст
    comment = models.TextField("Комментарий к брони", blank=True)
    # Поле статуса
    STATUS_CHOICES = [
        ("pending", "Ожидает подтверждения"),
        ("confirmed", "Подтверждена"),
        ("cancelled", "Отменена"),
        ("completed", "Завершена"),
    ]
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True
    )
    # Даты заезда и выезда
    check_in = models.DateField("Дата заезда", db_index=True)
    check_out = models.DateField("Дата выезда", db_index=True)
    # Даты создания и изменения (заполняются автоматически)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["room_category", "status"]),
            models.Index(fields=["check_in", "check_out"]),
        ]

    def __str__(self):
        return f"Бронь #{self.pk} — {self.guest_name} ({self.check_in} → {self.check_out})"