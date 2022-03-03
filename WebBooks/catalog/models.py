from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter book genre",
                            verbose_name="Book genre")

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=20, help_text="Enter language",
                            verbose_name="Book language")

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text="Enter author's name",
                                  verbose_name="Author name")
    last_name = models.CharField(max_length=100, help_text="Enter author's surname",
                                  verbose_name="Author surname")
    date_of_birth = models.DateField(help_text="Enter date of birth", verbose_name="Date of birth",
                                     null=True, blank=True)
    date_of_death = models.DateField(help_text="Enter date of death", verbose_name="Date of death",
                                     null=True, blank=True)

    def __str__(self):
        return self.last_name

class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Enter book title",
                             verbose_name="Book title")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, help_text="Choose book genre",
                              verbose_name="Book genre", null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE, help_text='Choose book language',
                                 verbose_name='Book language', null=True)
    author = models.ManyToManyField('Author', help_text='Choose book author',
                                    verbose_name='Book author')
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book",
                               verbose_name='Book annotation')
    isbn = models.CharField(max_length=13, help_text='Must contain 13 characters',
                            verbose_name='ISBN of the book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])
    display_author.short_description = "Authors"

class Status(models.Model):
    name = models.CharField(max_length=20, help_text="Enter book status",
                            verbose_name="Book instance status")

    def __str__(self):
        return self.name

class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True, verbose_name="Book title")
    inv_nom = models.CharField(max_length=20, null=True,
                               help_text="Enter book instance inventory number",
                               verbose_name="Inventory number")
    imprint = models.CharField(max_length=200, help_text="Enter publisher and year of publication",
                               verbose_name="Publisher")
    status = models.ForeignKey('Status', on_delete=models.CASCADE,
                               null=True, help_text="Change instance status",
                               verbose_name="Book instance status")
    due_back = models.DateField(null=True, blank=True, help_text="Enter order status term",
                                verbose_name="Status end date")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 blank=True, verbose_name="Customer",
                                 help_text="Choose book customer")

    def __str__(self):
        return '%s %s %s' % (self.inv_nom, self.book, self.status)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False