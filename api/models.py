from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

SCORE_CHOICES = zip(range(1, 11), range(1, 11))


class Review(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
            Review, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
