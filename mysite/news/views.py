from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, UserRegisterFrom, UserLoginFrom
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)

        if form.is_valid():
            messages.success(request, 'Вы успешно заригестрированы!')
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterFrom()

    return render(request, 'news/register.html', {'form': form })

def user_login(request):
    if request.method == "POST":
        form = UserLoginFrom(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginFrom()
    return render(request, 'news/login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('login')

class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'Hello World'
    paginate_by = 2
    #extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False# Не разрешаем показ пустых списков
    paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(category_id = self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'# Можно использовать без context_object_name, к данным можно обращаться через Objects
    #template_name = 'news/news_detail.html'
    #pk_url_kwarg = 'news_id'

class CreateNews(LoginRequiredMixin, CreateView):
    # Если у класса  News есть get_absolute_url то он делает ссылку на которую делает редирект
    # Если нет то получим ошибку

    form_class = NewsForm
    template_name = 'news/add_news.html'
    # Можно переопределить редирект функцией reverse она занимается построением ссылки
    # На основе именногованого адреса. Она строит ссылку передавая туда аргументы
    # Это синоним тега URL(в html) который используется в шаблонах
    # Только URL используется в шаблонах а reverse в коде(py)


    #login_url = '/admin/'

    raise_exception = True

    #Функцию reverse нельзя использовать №
    #success_url = reverse('home')

    #success_url = reverse_lazy('home')

def test(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7', 'ringo8']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)# Если параметра page нет, то будет присвоена 1
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category})

"""
def index(request):
    news = News.objects.all()
    context = {'news': news,
               'title': 'Список Новостей',
               }
    return render(request, 'news/index.html', context=context)
"""

# def view_news(request, news_id):
#     #news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {"news_item": news_item})




# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#
#         if form.is_valid():
#             #print(form.cleaned_data)
#             #news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})