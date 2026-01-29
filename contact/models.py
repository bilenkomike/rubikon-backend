from django.db import models


class Contact(models.Model):
    """Contact / feedback message from website."""

    name = models.CharField(
        max_length=150,
    )
    email = models.EmailField()

    message = models.TextField(
        max_length=2000,
    )

    is_processed = models.BooleanField(
        default=False,
        help_text="Handled by admin"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} – {self.email}"