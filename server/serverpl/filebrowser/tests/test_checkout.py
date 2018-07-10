#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_parsers.py
#  
#  Copyright 2018 Coumes Quentin <qcoumes@etud.u-pem.fr>
#  

import shutil

from os.path import join, isdir

from django.test import TestCase, Client, override_settings
from django.conf import settings
from django.contrib.auth.models import User

from filebrowser.models import Directory


FAKE_FB_ROOT = join(settings.BASE_DIR,'filebrowser/tests/ressources')

@override_settings(FILEBROWSER_ROOT=FAKE_FB_ROOT)
class CheckoutTestCase(TestCase):
    
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='user', password='12345', id=100)
        self.c = Client()
        self.c.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        rel = join(settings.FILEBROWSER_ROOT, '100/')
        if isdir(rel):
            shutil.rmtree(join(rel))
        self.folder = Directory.objects.get(name='100', owner=self.user)
        shutil.copytree(join(FAKE_FB_ROOT, 'fake_filebrowser_data'), self.folder.root)

    
    def tearDown(self):
        if isdir(join(FAKE_FB_ROOT,'directory')):
            shutil.rmtree(join(FAKE_FB_ROOT,'directory'))
    
    
    def test_checkout_method_not_allowed(self):
        response = self.c.post(
                '/filebrowser/home/opt/',
                {
                    'option': 'entry-git-checkout',
                    'target':'.plconception',
                },
                follow=True
            )
        self.assertEqual(response.status_code, 405)
    
