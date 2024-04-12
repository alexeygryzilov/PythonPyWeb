from django.shortcuts import render
from django.views import View
from .models import Author, AuthorProfile, Entry, Tag
from django.db.models import Q, Max, Min, Avg, Count


class TrainView(View):
    def get(self, request):
        # Создайте здесь запросы к БД
        max_s_e = Author.objects.aggregate(max_s_e = Max('self_esteem'))
        self.answer1 = Author.objects.filter (self_esteem =max_s_e['max_s_e'])

        self.answer2 = Author.objects.annotate(count = Count('entries')).order_by('-count').values('username')[0]
        inner_qs = Tag.objects.filter(name__in=['Кино', 'Музыка'])
        self.answer3 = Entry.objects.filter(tags__in=inner_qs)
        self.answer4 = Author.objects.filter(gender='ж').count()
        total = Author.objects.count()
        agreed = Author.objects.filter(status_rule=1).count()
        self.answer5 = int(agreed / total * 100)
        inner_qs = AuthorProfile.objects.filter(stage__range=(1, 5))
        self.answer6 = Author.objects.filter(id__in=inner_qs)
        max_age = Author.objects.aggregate(maxim_age=Max('age'))
        self.answer7 = Author.objects.filter(age = max_age['maxim_age'])[0]
        self.answer8 = Author.objects.filter(phone_number__isnull=False).count()
        self.answer9 = Author.objects.filter(age__lt=25)
        self.answer10 = Author.objects.annotate(count = Count('entries')).order_by('-count').values('username', 'count')

        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}

        return render(request, 'train_db/training_db.html', context=context)

