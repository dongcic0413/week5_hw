from django.conf import settings

#Create your ideas here.
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    CATEGORY_CHOICES = [
        ("기쁨", "기쁨"),
        ("설렘", "설렘"),
        ("평온", "평온"),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="평온")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def mood_class(self):
        mood_class_map = {
            "기쁨": "mood-tag--joy",
            "설렘": "mood-tag--excited",
            "평온": "mood-tag--calm",
        }
        return mood_class_map.get(self.category, "mood-tag--calm")


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.content

MOOD_CLASS_MAP = {
    Category.JOY: 'mood-tag--joy',
    Category.EXCITED: 'mood-tag--excited',
    Category.CALM: 'mood-tag--calm',
    }

@property
def mood_class(self):
    return self.MOOD_CLASS_MAP.get(self.category, 'mood-tag--calm')