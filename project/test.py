import django
import os
import datetime
import pprint
from django.db.models import Count, Max, Min, Sum, F, Value, Subquery, Window
from django.db.models import Avg, Q, StdDev, Variance
from django.db import connection
from django.db.models import Case, When, BooleanField, CharField

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from apps.db_train.models import Author, AuthorProfile, Entry, Tag


    obj_12 = Author.objects.annotate(entry_count=Count('entries')).order_by('-entry_count').values()[0]['username']
    print(obj_12)


