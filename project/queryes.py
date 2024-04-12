import django
import datetime
import os
from django.db.models import Q, Max, Min, Avg, Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from apps.db_train_alternative.models import Blog, Author, AuthorProfile, Entry, Tag

    # TODO Сделайте здесь запросы

    # obj = Entry.objects.filter(author__name__contains='author')
    # obj = Entry.objects.filter(author__authorprofile__city=None)
    # print(Entry.objects.get(id__exact=4))
    # print(Entry.objects.get(id=4))  # Аналогично exact
    # print(Blog.objects.get(name__iexact="Путешествия по миру"))
    # print(Entry.objects.filter(headline__contains='мод'))
    # print(Entry.objects.filter(id__in=[1,3,4]))
    # print(Entry.objects.filter(number_of_comments__in='123'))
    # inner_qs = Blog.objects.filter(name__contains='Путешествия')
    # entries = Entry.objects.filter(blog__in=inner_qs)
    # print(entries)
    # print(Entry.objects.filter(number_of_comments__gt=10))
    # print(Entry.objects.filter(pub_date__gte=datetime.date(2023, 6, 1)))
    # print(Entry.objects.filter(number_of_comments__gt=10))
    #print(Entry.objects.filter(headline__endswith='ния'))
    #start_date = datetime.date(2023, 1, 1)
    #end_date = datetime.date(2023, 12, 31)
    #print(Entry.objects.filter(pub_date__year=2023))
    answer10 = Entry.objects.annotate(number_of_entries=Count('author_id')). \
        values('author', 'number_of_entries').order_by('-number_of_entries')
    print(answer10)
