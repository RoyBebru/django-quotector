from django.contrib import admin
from .models import Tag, Author, Quote

# Register your models here.
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Quote)

admin.site.site_title="Quotes to Scrape"
admin.site.site_header="Admin Panel for Quotes and Authors"
admin.site.index_title="Quotes and Authors Administration"
