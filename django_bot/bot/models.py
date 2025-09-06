from django.db import models

class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True, verbose_name="ID пользователя в Telegram")
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Никнейм")
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Фамилия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"
        ordering = ['-created_at']

    def __str__(self):
        if self.username:
            return f"@{self.username} ({self.user_id})"
        elif self.first_name or self.last_name:
            full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
            return f"{full_name} ({self.user_id})"
        else:
            return f"User {self.user_id}"

    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return None