from django.db import models


class Intent(models.Model):
    """
    Stores deterministic assistant intents.
    """

    intent_name = models.CharField(
        max_length=100,
        unique=True
    )

    trigger_phrase = models.TextField(
        help_text=(
            "Comma separated trigger words or phrases"
        )
    )

    response = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        ordering = [
            "intent_name"
        ]


    def __str__(self) -> str:
        return self.intent_name