from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment
from .forms import UserRegisterForm, UserLoginForm, PostForm, CommentForm


class HomePost(ListView):
    model = Post
    template_name = 'my_app/home.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Post.objects.all()


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'my_app/register.html'
    success_url = reverse_lazy('home')
    form_class = UserRegisterForm
    success_message = "Вы успешно зарегистрировались"

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        username, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class SignInView(SuccessMessageMixin, LoginView):
    template_name = 'my_app/login.html'
    form_class = UserLoginForm
    success_message = "Вы успешно вошли в систему"


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'my_app/add_post.html'
    login_url = 'login'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class DeletePost(SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    success_message = "Успешно удалено"

    def get_success_url(self):
        return reverse_lazy('home')

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        if not self.request.user.is_superuser:
            raise Http404
        return obj


class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'my_app/edit_post.html'
    login_url = 'login'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return Post.objects.get(pk=self.kwargs.get("pk"), user=self.request.user)


class Comments(LoginRequiredMixin, FormView):
    model = Comment
    form_class = CommentForm
    login_url = 'login'
    success_url = reverse_lazy('home')
    template_name = 'my_app/comment.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        post_instance = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.post = post_instance
        obj.save()
        return super().form_valid(form)
