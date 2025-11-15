from django.shortcuts import render

from django.shortcuts import render

# View para a página de login
def login_view(request):
    return render(request, 'catalogo/login.html') 


def index(request):
    return render(request, 'catalogo/index.html')

def estoque(request):
    return render(request, 'catalogo/estoque.html')