from django.shortcuts import render


def home(request):
    context = {
        'mensagem': 'Petshop',
        'usuario': request.user.username
        }
    return render(request, 'index.html', context)

