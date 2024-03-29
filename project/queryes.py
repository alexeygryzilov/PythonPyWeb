import django
import os
import datetime
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from apps.db_train_alternative.models import Blog, Author, AuthorProfile, Entry, Tag

    # obj = Entry.objects.filter(author__name__contains='author')
    # obj = Entry.objects.filter(author__authorprofile__city=None)
    # print(obj)

    # print(Entry.objects.get(id__exact=4))
    # print(Entry.objects.get(id=4))  # Аналогично exact
    # print(Blog.objects.get(name__iexact="Путешествия по миру"))
    # print(Entry.objects.filter(headline__contains='мод'))
    # print(Entry.objects.filter(id__in=[1, 3, 4]))
    # print(Entry.objects.filter(number_of_comments__in='123'))
    # inner_qs = Blog.objects.filter(name__contains='Путешествия')
    # entries = Entry.objects.filter(blog__in=inner_qs)
    # print(entries)
    # print(Entry.objects.filter(number_of_comments__gt=10))
    # print(Entry.objects.filter(pub_date__gte=datetime.date(2023, 6, 1)))
    # print(Entry.objects.filter(number_of_comments__gt=10).filter(rating__lt=4))
    # print(Entry.objects.filter(headline__lte='Зя'))
    # print(Entry.objects.filter(headline__startswith='Как'))
    # print(Entry.objects.filter(headline__endswith='ния'))
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    # print(Entry.objects.filter(pub_date__range=(start_date, end_date)))
    # print(Entry.objects.filter(pub_date__year=2023))
    # print(Entry.objects.filter(pub_date__year__lt=2022))
    # print(Entry.objects.filter(pub_date__month=2).values('blog__name', 'pub_date', 'headline'))
    # print(Entry.objects.filter(pub_date__year=2023).filter(pub_date__day__gte=1).filter(
    # pub_date__day__lte=15).values_list("author__name").distinct())
    # print(Entry.objects.filter(pub_date__week_day=2).values('blog__name', 'pub_date', 'headline'))
    # print(Entry.objects.filter(pub_date__date=datetime.date(2021, 6, 1)))
    # print(Entry.objects.filter(pub_date__date__gt=datetime.date(2024, 1, 1)))
    # print(Entry.objects.filter(pub_date__time=datetime.time(12, 00)))
    # print(Entry.objects.filter(pub_date__time__range=(datetime.time(6), datetime.time(17))))
    # print(AuthorProfile.objects.filter(city__isnull=True))
    # print(Entry.objects.filter(body_text__regex=r'\w*стран\w*'))
    # print(Entry.objects.filter(author__email__iregex=r'\w+(@gmail.com|@mail.ru)'))
    # print(Entry.objects.filter(author__email__iregex=r'\w+(@gmail.com|@mail.ru)').distinct())
    # all_obj = Blog.objects.all()
    # print("Вывод всех значений в таблице Blog\n", all_obj)
    # all_obj = Blog.objects.all()
    # obj_first = all_obj.first()
    # obj_last = all_obj.last()
    # print("Разные запросы на вывод в Blog\n", f"Первое значение таблицы = {obj_first}\n",
    #      f"Все значения = {all_obj}")
    # print(f'{obj_last}')
    # all_obj = Blog.objects.all()
    # for idx, value in enumerate(all_obj):
    #        print(f"idx = {idx}, value = {value}")
    #    print(all_obj[0])  # Получение 0-го элемента
    #    print(all_obj[2:4])  # Получение 2 и 3 элемента
    # print(Blog.objects.exclude(id__gte=2))
    # try:
    #   Blog.objects.get(id=2, name="Путешествия по миру")
    # except Blog.DoesNotExist:
    #   print("Не существует")
    # print(Blog.objects.filter(id=1, name="Путешествия по миру").exists())
    #f_data = Blog.objects.filter(id__gte=2)
    #print(f_data.order_by('-name', '-id'))
    #entry = Blog.objects.annotate(number_of_entries=Count('entries')).values('name', 'number_of_entries')
    #print(entry)
    #blogs = Blog.objects.alias(number_of_entries=Count('entries')).filter(number_of_entries__gt=4)
    #print(blogs)
    #blogs = Blog.objects.alias(number_of_entries_new=Count('entries')).filter(number_of_entries__gt=4).values('blog', 'entries_new')

