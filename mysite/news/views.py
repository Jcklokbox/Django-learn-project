from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewsForm, UserRegisterForm, UserLoginForm, FeedbackForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

from .models import News, Category


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('home')

        else:
            messages.error(request, 'Ошибка')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def send_message(request):
    if request.method == 'POST':
        form = FeedbackForm(data=request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],
                      'sonicogamer@yandex.ru', ('jcklokbox@gmail.com',), fail_silently=True)
            if mail:
                messages.success(request, 'Сообщение успешно отправлено!')
                return redirect('feedback')
            else:
                messages.error(request, 'Ошибка отправки.')
    else:
        form = FeedbackForm()
    return render(request, 'news/send_message.html', {'form': form})


class HomePage(ListView):
    paginate_by = 5
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsCategory(ListView):
    paginate_by = 5
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_cat'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class GetNews(DetailView):
    model = News
    template_name = 'news/current_news.html'
    context_object_name = 'item'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    raise_exception = True
