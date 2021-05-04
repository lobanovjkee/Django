from django.shortcuts import render


def products(request):
    context = {
        'title': 'каталог',
        'links': [
            {'href': 'mainapp:index', 'name': 'все'},
            {'href': 'mainapp:index', 'name': 'дом'},
            {'href': 'mainapp:index', 'name': 'офис'},
            {'href': 'mainapp:index', 'name': 'модерн'},
            {'href': 'mainapp:index', 'name': 'классика'}
        ]}

    return render(request, 'products.html', context=context)
