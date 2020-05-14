from djongo import models

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Announcement(models.Model):
    topic = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)
    text_of_announcement = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True,
                                  related_name='announcement')

    def __str__(self):
        return self.topic


class Comment(models.Model):
    text = models.TextField()
    announcement = models.ForeignKey(Announcement, related_name='ann',
                                     on_delete=models.CASCADE, null=True,
                                     default=None)

    def __str__(self):
        return self.text
