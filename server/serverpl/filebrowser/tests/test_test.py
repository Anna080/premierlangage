#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_test.py
#  
#  

import os, shutil, sys, json, time

from os.path import join, isdir, isfile

from mock import patch

from django.test import TestCase, Client, override_settings
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.messages import constants as messages

from filebrowser.models import Directory


FAKE_FB_ROOT = join(settings.BASE_DIR,'filebrowser/tests/ressources')

@override_settings(FILEBROWSER_ROOT=FAKE_FB_ROOT)
class TestTestCase(TestCase):
    
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='user', password='12345')
        self.c = Client()
        self.c.force_login(self.user,backend=settings.AUTHENTICATION_BACKENDS[0])
        if isdir(join(FAKE_FB_ROOT,'dir')):
            shutil.rmtree(join(FAKE_FB_ROOT,'dir'))
        self.folder = Directory.objects.create(name='dir', owner=self.user)
        shutil.copytree(join(FAKE_FB_ROOT, 'fake_filebrowser_data'), self.folder.root)
    
    
    def tearDown(self):
        if isdir(join(FAKE_FB_ROOT,'directory')):
            shutil.rmtree(join(FAKE_FB_ROOT,'directory'))
    
    
    def test_test_method_not_allowed(self):
        response = self.c.get(
            '/filebrowser/apply_option/post',
            follow=True
        )
        self.assertEqual(response.status_code, 405)
    
    
    def test_test_pl(self):
        try:
            response = self.c.get(
                '/filebrowser/apply_option/',
                {
                        'option_h' : 'test',
                        'name_h' : 'function001.pl',
                        'relative_h' : './dir/TPE',
                        'type_h' : 'entry'
                    },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response,"Ecrire une fonction <strong>bob</strong> qui retourne la valeur")
            self.assertContains(response,"<code>&gt;&gt;&gt; bob()\n1238\n</code>",count=1)
            self.assertContains(response,"# Fin du code,")
        except AssertionError:
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise
    
    def test_test_no_pl(self):
        try:
            response = self.c.get(
                '/filebrowser/apply_option/',
                {
                        'option_h' : 'test',
                        'name_h' : 'test.txt',
                        'relative_h' : './dir/TPE/Dir_test',
                        'type_h' : 'entry'
                    },
                follow=True
            )
            m = list(response.context['messages'])
            if m:
                self.assertEqual(len(m), 1)
                self.assertEqual(m[0].level, messages.ERROR)
        except AssertionError:
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise
