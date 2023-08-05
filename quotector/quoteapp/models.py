from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=127, null=False, unique=True)
    description = models.TextField(null=False, default="")
    born_location = models.CharField(max_length=127, null=False, default="")
    born_date = models.DateField(null=False)

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField(unique=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        quotext = self.quote
        if len(quotext) > 60:
            quotext = quotext[0:60] + "..."

        return quotext
