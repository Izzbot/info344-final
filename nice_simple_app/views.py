from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.utils import timezone
from django.conf import settings

# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework.reverse import reverse

from ratelimit.decorators import ratelimit
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from nice_simple_app.serializers import ProfileSerializer
from nice_simple_app.serializers import UserSerializer
from django.contrib.auth.models import User
from nice_simple_app.permissions import IsOwnerOrReadOnly
from django.http import Http404
from ratelimit.mixins import RatelimitMixin

from .models import Profile, Comparison
from .serializers import ProfileSerializer, UserSerializer
from .forms import ComparisonForm
from ratelimit.decorators import ratelimit
# from nice_simple_app_site.settings import LOGIN_URL
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from allauth.socialaccount.helpers import complete_social_login
import allauth.account

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from bs4 import BeautifulSoup
from selenium import webdriver
from nice_simple_app_site.settings import STATIC_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import os, requests


class ApiList(RatelimitMixin, generics.ListCreateAPIView):
    ratelimit_key = 'ip'
    ratelimit_rate = '10/m'
    ratelimit_block = True
    ratelimit_method = 'GET', 'POST'

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ApiDetail(RatelimitMixin, generics.RetrieveUpdateDestroyAPIView):
    ratelimit_key = 'ip'
    ratelimit_rate = '10/m'
    ratelimit_block = True
    ratelimit_method = 'GET', 'PUT', 'DELETE'

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)



# @login_required(login_url='accounts/login/')
# @api_view(['GET', 'POST'])
# def api_list(request, format=None):
#     if request.method == 'GET':
#         profile = Profile.objects.all()
#         serializer = ProfileSerializer(profile, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

# @login_required(login_url='accounts/login/')
def home_page(request):
    # if not request.user.is_authenticated():
    #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # else:
    comparisons = Comparison.objects.all()
    profiles = Profile.objects.all()

    # tack on the name for each of the comparisons
    for comparison in comparisons:
        profile = profiles.get(pk=comparison.l_profile.id)
        comparison.name = profile.p_name

    return render(request, 'nice_simple_app/home_page.html', {'comparisons': comparisons})

@login_required(login_url='accounts/login/')
def comparison_page(request, pk):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        comparison = get_object_or_404(Comparison, pk=pk)
        l_profile = get_object_or_404(Profile, pk=comparison.l_profile.id)
        r_profile = get_object_or_404(Profile, pk=comparison.r_profile.id)
        return render(request, 'nice_simple_app/comparison_page.html', {
            'comparison':comparison,
            'l_profile':l_profile,
            'r_profile':r_profile,
        })


def about_page(request):
    return render(request, 'nice_simple_app/about_page.html', {})

@login_required(login_url='accounts/login/')
def new_comparison_page(request):

    # if not request.user.is_authenticated():
    #     return redirect('%s?next=%s' %(settings.LOGIN_URL, request.path))
    # else:
    if request.method == 'POST':

        # add in logic to create a new comparison
        form = ComparisonForm(request.POST)
        if form.is_valid():
            comparison = form.save(commit=False)
            comparison.owner = request.user



            # # connect up and fetch the website
            # req = requests.request('GET', comparison.profile_url)
            # comparison.profile_url = req.url

            # collect initial data
            comparison.collected_date = timezone.now()
            creator = request.user
            access_token = SocialToken.objects.get(account__user=creator,account__provider='facebook')
            comparison.collected_by = creator
            user_json = requests.request('GET', 'https://graph.facebook.com/me?access_token='+access_token.token+'&fields=id,name,email')

#            return render(request, 'nice_simple_app/new_comparison_page.html', {'form': form, 'errors': (user_json,)})

            # create the related profile instances
            pub_profile = Profile()
            priv_profile = Profile()

            # # public page view
            # set defaults
            pub_profile.p_name = ''
            pub_profile.p_phone = ''
            pub_profile.p_city = ''
            pub_profile.p_region = ''
            pub_profile.p_country = ''
            pub_profile.p_birthday = ''
            pub_profile.p_birthyear = ''
            pub_profile.p_relationship = ''
            pub_profile.p_relationship_with = ''
            pub_profile.p_job_title = ''
            pub_profile.p_job_employer = ''
            pub_profile.p_studying = ''
            pub_profile.p_school = ''
            pub_profile.p_friends = 0
            pub_profile.p_likes = 0
            pub_profile.p_groups = 0
            pub_profile.p_information = ''
            pub_profile.p_quotes = ''
            pub_profile.p_nickname = ''

            # try:
            #     pub_req = requests.request('GET', comparison.profile_url)
            # except:
            #     return redirect('nice_simple_app.views.new_comparison_page', {})
            #
            # pub_soup = BeautifulSoup(pub_req.text, 'html.parser')
            # if pub_soup.title.string is not None:
            #     split_title = soup.title.string.split('|')
            #     pub_profile.p_name = split_title[0]

            # try:
            #     pub_about_req = requests.request('GET', comparison.profile_url + '/about')
            # except:
            #     return redirect('nice_simple_app.views.new_comparison_page')
            #
            # # Use beautiful Soup to traverse and assign about data
            # pub_about_soup = BeautifulSoup(pub_about_req.text, 'html.parser')
            # if pub_about_soup.phone.string is not None:
            #   pub_profile.p_phone = pub_about_soup.phone.string
            # if pub_about_soup.city.string is not None:
            #   pub_profile.p_city = pub_about_soup.city.string
            # if pub_about_soup.region.string is not None:
            #   pub_profile.p_region = pub_about_soup.region.string

            # initial save so we can get an ID
            pub_profile.save()

            # fetch a "screenshot"
            driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
            driver.set_window_size(1024, 768)
            driver.get('http://google.com')
            nameFile = str(pub_profile.id) + '.png'
            driver.save_screenshot('/tmp/' + nameFile)
            conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
            k = Key(bucket)
            k.key = 'screenshot/' + nameFile
            k.set_contents_from_filename('/tmp/' + nameFile)
            k.make_public()
            os.remove('/tmp/' + nameFile)
            pub_profile.img_url = STATIC_URL + "screenshot/" + nameFile

            # save our public profile
            pub_profile.save()

            # private profile view
            # set defaults
            priv_profile.p_name = ''
            priv_profile.p_phone = ''
            priv_profile.p_city = ''
            priv_profile.p_region = ''
            priv_profile.p_country = ''
            priv_profile.p_birthday = ''
            priv_profile.p_birthyear = ''
            priv_profile.p_relationship = ''
            priv_profile.p_relationship_with = ''
            priv_profile.p_job_title = ''
            priv_profile.p_job_employer = ''
            priv_profile.p_studying = ''
            priv_profile.p_school = ''
            priv_profile.p_friends = 0
            priv_profile.p_likes = 0
            priv_profile.p_groups = 0
            priv_profile.p_information = ''
            priv_profile.p_quotes = ''
            priv_profile.p_nickname = ''

            # try:
            #     priv_req = requests.request('GET', comparison.profile_url)
            # except:
            #     return redirect('nice_simple_app.views.new_comparison_page')
            #
            # priv_soup = BeautifulSoup(Priv_req.text, 'html.parser')
            # if priv_soup.title.string is not None:
            #     split_title = soup.title.string.split('|')
            #     priv_profile.p_name = split_title[0]

            # # Use beautiful Soup to traverse and assign about data
            # priv_about_soup = BeautifulSoup(priv_about_req.text, 'html.parser')
            # if priv_about_soup.phone.string is not None:
            #   priv_profile.p_phone = priv_about_soup.phone.string
            # if priv_about_soup.city.string is not None:
            #   priv_profile.p_city = priv_about_soup.city.string
            # if priv_about_soup.region.string is not None:
            #   priv_profile.p_region = priv_about_soup.region.string

            # initial save so we can get an ID
            priv_profile.save()

            # fetch a "screenshot"
            driver.get('http://bing.com')
            conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
            k = Key(bucket)
            nameFile = str(priv_profile.id) + '.png'
            k.key = 'screenshot/' + nameFile
            driver.save_screenshot('/tmp/' + nameFile)
            k.set_contents_from_filename('/tmp/' + nameFile)
            k.make_public()
            os.remove('/tmp/' + nameFile)
            priv_profile.img_url = STATIC_URL + "screenshot/" + nameFile

            # save our public profile
            priv_profile.save()

            # close out the webdriver
            driver.quit()

            comparison.l_profile = pub_profile
            comparison.r_profile = priv_profile
            comparison.save()
            return render(request, 'nice_simple_app/comparison_page.html', {
            'comparison':comparison,
            'l_profile':pub_profile,
            'r_profile':priv_profile,
        })
    else:
        form = ComparisonForm()
        return render(request, 'nice_simple_app/new_comparison_page.html', {'form': form})