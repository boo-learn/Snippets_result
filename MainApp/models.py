from django.db import models
from datetime import datetime

LANG_CHOICE = [
    ("py", "python"),
    ("cpp", "C++"),
    ("js", "JavaScript"),
]

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANG_CHOICE)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(default=datetime.now())
