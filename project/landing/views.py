from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import News

class HomeView(TemplateView):
    template_name = 'landing/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.objects.all().order_by('-created_at')[:3]
        return context

class AboutUsView(TemplateView):
    template_name = 'landing/aboutus.html'

class NewsDetailView(DetailView):
    model = News
    template_name = 'landing/news_detail.html'
    context_object_name = 'news'

class NewsListView(ListView):
    model = News
    template_name = 'landing/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']
    paginate_by = 6
