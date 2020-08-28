from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Post, Document
from .forms import DocumentForm
from . import pdf_jp2en
from django.shortcuts import render, redirect
from django.urls import reverse
import os
from config.settings import BASE_DIR
from django.http import FileResponse, Http404
import urllib.parse

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['date_posted']


class PartTimerView(ListView):
    model = Post
    template_name = 'blog/parttimer.html'
    context_object_name = 'posts'
    ordering = ['date_posted']


class ManagerView(ListView):
    model = Post
    template_name = 'blog/manager.html'
    context_object_name = 'posts'
    ordering = ['date_posted']


class PostAdmin(ListView):
    model = Post
    template_name = 'blog/admin.html'
    context_object_name = 'posts'
    ordering = ['date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'answer']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'answer']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def model_form_upload(request):
    if request.method == 'POST':
        path = os.path.join(BASE_DIR,'documents/manual.pdf')
        if os.path.exists(path):
            os.remove(path)
        request.FILES['document'].name = 'manual.pdf'
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            redirect_url = reverse('blog-home')
            pdf_jp2en.main_()
            return redirect(pdf_view)
    else:
        form = DocumentForm()
    return render(request, 'blog/model_form_upload.html', {
        'form': form,
    })

def pdf_view(request):
    try:
        response = FileResponse(open(os.path.join(BASE_DIR,'documents/manual_eng.pdf'), 'rb'), content_type='application/pdf')
        response ['Content-Disposition'] = "filename={}".format(urllib.parse.quote('manual_eng.pdf'))
        return response
    except FileNotFoundError:
        raise Http404()