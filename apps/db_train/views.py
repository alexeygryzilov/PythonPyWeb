from django.shortcuts import render
from django.views import View
from django.db.models import Q, Max, Min, Avg, Count
from .models import Author, Entry, Tag, AuthorProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class TrainView(View):
    def get(self, request):
        # Создайте здесь запросы к БД
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem'])
        self.answer2 = Author.objects.annotate(count=Count('entries')).order_by('-count').values()[
            0]  # TODO Какой автор имеет наибольшее количество опубликованных статей?
        inner_qs = Tag.objects.filter(name__in=['Кино', 'Музыка'])
        self.answer3 = Entry.objects.filter(tags__in=inner_qs)  # TODO Какие статьи содержат тег 'Кино' или 'Музыка' ?
        self.answer4 = Author.objects.filter(gender='ж').count()
        total = Author.objects.all().count()
        agree = Author.objects.filter(status_rule__exact=1).count()
        self.answer5 = int(agree / total * 100)  # TODO Какой процент авторов согласился с правилами при регистрации?
        self.answer6 = Author.objects.filter(authorprofile__stage__gte=1).filter(authorprofile__stage__lte=5)
        max_age = Author.objects.aggregate(maxim_age=Max('age'))
        self.answer7 = Author.objects.filter(age=max_age['maxim_age']).values('username', 'age')[0]['username']
        self.answer8 = Author.objects.filter(phone_number__isnull=False).count()
        self.answer9 = Author.objects.filter(age__lt=25)
        self.answer10 = Author.objects.annotate(count=Count('entries')).order_by('-count').values('username',
                                                                                                  'count')  # TODO Сколько статей написано каждым автором?

        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}
        print(context)

        return render(request, 'train_db/training_db.html', context=context)


class TrainViewOld(View):
    def get(self, request):
        context = {}  # Создайте здесь запросы к БД
        return render(request, 'train_db/training_db.html', context=context)


