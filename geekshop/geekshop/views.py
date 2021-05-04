from django.shortcuts import render


def main(request):
    context = {
        "title": 'магазин',
        'topic': 'тренды'
    }
    return render(request, 'index.html', context=context)


def contacts(request):
    context = {
        'title': 'контакты',

    }
    return render(request, 'contact.html', context=context)
