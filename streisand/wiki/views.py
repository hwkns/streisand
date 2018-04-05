# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.response import Response

from rest_framework import mixins
from .forms import WikiArticleForm
from .models import WikiArticle
from www.pagination import WikiPageNumberPagination

from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
from .serializers import WikiCreateUpdateDestroySerializer, WikiBodySerializer, WikiViewListOnlySerializer


class WikiArticleCreateUpdateDestroyViewSet(mixins.CreateModelMixin,
                                            mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                            mixins.DestroyModelMixin,
                                            GenericViewSet):
    """
    API endpoint that allows Wikis to be created, edited, or deleted only. Options are HEAD, POST, PATCH, DELETE.
    """
    serializer_class = WikiCreateUpdateDestroySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAdminUser]
    search_fields = ['title', 'created_by__username', 'read_access_minimum_user_class__username__userclass']
    pagination_class = WikiPageNumberPagination  # PageNumberPagination

    def partial_update(self, request, pk=None):
        serializer = WikiCreateUpdateDestroySerializer(request.user, data=request.data, partial=True)
        serializer.save()
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        queryset_list = WikiArticle.objects.all()  # filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(created_by__username__icontains=query) |
                Q(read_access_minimum_user_class__username__userclass__icontains=query)
            ).distinct()
        return queryset_list


class WikiArticleBodyViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    API endpoint that allows Wiki Body and body ID to be viewed, or Patched only.
    """
    permission_classes = [IsAdminUser]
    serializer_class = WikiBodySerializer
    search_fields = ['body', 'id']
    pagination_class = WikiPageNumberPagination  # PageNumberPagination

    def partial_update(self, request, pk=None):
        serializer = WikiBodySerializer(request.user, data=request.data, partial=True)
        serializer.save()
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        queryset_list = WikiArticle.objects.all()  # filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(body__icontains=query) | Q(id__icontains=query)).distinct()
        return queryset_list


class WikiArticleViewListOnlyViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    API endpoint that allows Wikis to be viewed only. Note: Body and Body_html is not shown.
    This Endpoint includes Searching for Title or users.
    """
    serializer_class = WikiViewListOnlySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAdminUser]
    search_fields = ['title', 'created_by__username']
    pagination_class = WikiPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = WikiArticle.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(created_by__username__icontains=query)
            ).distinct()
        return queryset_list


def wiki_index(request):
    wiki_articles = WikiArticle.objects.all()

    return render(
        request=request,
        template_name='wiki_index.html',
        context={
            'wiki_articles': wiki_articles,
        },
    )


def wiki_article_details(request, wiki_article_id):
    article = get_object_or_404(
        WikiArticle.objects.accessible_to_user(request.user),
        id=wiki_article_id,
    )

    return render(
        request=request,
        template_name='wiki_article_details.html',
        context={
            'article': article,
        }
    )


class WikiArticleEditView(View):

    def dispatch(self, request, *args, **kwargs):

        self.article = get_object_or_404(
            WikiArticle.objects.editable_by_user(request.user),
            id=kwargs.pop('wiki_article_id'),
        )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        form = WikiArticleForm(instance=self.article, author=request.user)

        return self._render(
            context={
                'new': False,
                'form': form,
            },
        )

    def post(self, request):

        form = WikiArticleForm(instance=self.article, data=request.POST, author=request.user)

        if form.is_valid():

            article = form.save()
            return redirect(article)

        else:

            return self._render(
                context={
                    'new': False,
                    'form': form,
                }
            )

    def _render(self, context):

        return render(
            request=self.request,
            template_name='wiki_article_edit.html',
            context=context,
        )


class WikiArticleCreationView(View):

    def get(self, request):

        form = WikiArticleForm(author=request.user)

        return render(
            request=request,
            template_name='wiki_article_edit.html',
            context={
                'new': True,
                'form': form,
            }
        )

    def post(self, request):

        form = WikiArticleForm(request.POST, author=request.user)

        if form.is_valid():

            article = form.save()
            return redirect(article)

        else:

            return render(
                request=request,
                template_name='wiki_article_edit.html',
                context={
                    'new': True,
                    'form': form,
                }
            )


def wiki_article_delete(request, wiki_article_id):
    article = get_object_or_404(
        WikiArticle,
        id=wiki_article_id,
    )

    article.delete()

    return redirect('wiki_index')
