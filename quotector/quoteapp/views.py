from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


from .forms import AuthorForm, QuoteForm, TagForm
from .models import Author, Quote, Tag
from .scrapy_content import do_scrapy_content


def top_of_tags():
    top_ctag_list = [ (len(tag.quote_set.all()), str(tag)) for tag in Tag.objects.all() ]
    top_ctag_list.sort(reverse=True, key=lambda t: t[0])
    # print(f"[T] Top of Counted Tags: {top_ctag_list[0:10]}")
    return [ ctag[1] for ctag in top_ctag_list[0:10] ]


def main(request, page_num=1, with_tag=''):
    if with_tag:
        # Tags in quotes must be sorted by name
        quotes = Quote.objects.filter(tags__name=with_tag).prefetch_related(
                Prefetch('tags', queryset=Tag.objects.order_by('name')))[(page_num-1)*10:page_num*10]
        # Can be shown anything in the next page?
        quote_next = Quote.objects.filter(tags__name=with_tag)[page_num*10:page_num*10+1]
    else:
        # Tags in quotes must be sorted by name
        quotes = Quote.objects.all().prefetch_related(
                Prefetch('tags', queryset=Tag.objects.order_by('name')))[(page_num-1)*10:page_num*10]
        # Can be shown anything in the next page?
        quote_next = Quote.objects.all()[page_num*10:page_num*10+1]
    if len(quote_next) == 0:
        page_next = 0 # No
    else:
        page_next = page_num + 1 # Yes
    return render(request, 'quoteapp/index.html', {
                "quotes": quotes,
                "page_prev": page_num-1,
                "page_next": page_next,
                "with_tag": with_tag,
                "top_of_tags": top_of_tags()})


def about(request, fullname):
    author = get_object_or_404(Author, fullname=fullname)
    return render(request, 'quoteapp/about.html', {"author": author})


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/quote/{request.POST.getlist("fullname")[0]}/')
        else:
            return render(request, 'quoteapp/author.html', {'form': form})

    return render(request, 'quoteapp/author.html', {'form': AuthorForm()})


@login_required
def quote(request, author=None):
    # Authors must be sorted by fullname to be easy found
    authors = Author.objects.all().order_by('fullname')
    # Tags must be sorted by name to be easy found
    tags = Tag.objects.all().order_by('name')

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.author = Author.objects.filter(
                    fullname=request.POST.getlist("author")[0])[0]
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            last_page = len(Quote.objects.all())
            last_page = last_page // 10 + bool(last_page % 10)

            # return redirect(to=f'quoteapp:page')
            return redirect(f'/page/{last_page}/')
        else:
            return render(request, 'quoteapp/quote.html',
                          {"one_author": author, "authors": authors, "tags": tags, 'form': form})

    return render(request, 'quoteapp/quote.html',
                    {"one_author": author, "authors": authors, "tags": tags, 'form': QuoteForm()})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})
    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


@login_required
def scrapy_content(request):
    print("[#] In views.scrapy_content()")
    do_scrapy_content()
    return redirect(to='admin:quoteapp_author_changelist')
