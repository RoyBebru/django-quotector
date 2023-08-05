from datetime import datetime, date
from django.forms import ModelForm, CharField, TextInput, Textarea, DateField
from .models import Author, Quote, Tag


class AuthorForm(ModelForm):
    fullname = CharField(min_length=2, required=True, widget=TextInput())
    description = CharField(min_length=10, required=True, widget=Textarea())
    born_location = CharField(min_length=2, required=True, widget=TextInput())
    born_date = DateField(initial=date.today())

    class Meta:
        model = Author
        fields = ['fullname', 'description', 'born_location', 'born_date']


class QuoteForm(ModelForm):

    quote = CharField(min_length=10, required=True, widget=Textarea())

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['author', 'tags']


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


