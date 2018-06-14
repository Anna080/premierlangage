#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_parsers.py
#
#  Copyright 2018 Coumes Quentin <qcoumes@etud.u-pem.fr>
#

import os, shutil, sys, json, time

from os.path import join, isdir, isfile

from mock import patch

from django.test import TestCase, Client, override_settings
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.messages import constants as messages

from filebrowser.models import Directory

FAKE_FB_ROOT = join(settings.BASE_DIR, 'filebrowser/tests/ressources')


@override_settings(FILEBROWSER_ROOT=FAKE_FB_ROOT)
class MoveTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='user', password='12345')
        self.c = Client()
        self.c.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        if isdir(join(FAKE_FB_ROOT, 'dir')):
            shutil.rmtree(join(FAKE_FB_ROOT, 'dir'))
        self.folder = Directory.objects.create(name='dir', owner=self.user)
        shutil.copytree(join(FAKE_FB_ROOT, 'fake_filebrowser_data'), self.folder.root)


    def test_move_method_not_allowed(self):
        response = self.c.get(
            '/filebrowser/apply_option/post',
            follow=True
        )
        self.assertEqual(response.status_code, 405)


    def test_move_directory(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'Dir_test',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                    'destination': '..'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            rel = join(settings.FILEBROWSER_ROOT, 'dir/')
            self.assertTrue(isdir(join(rel, 'Dir_test')))
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE')
            self.assertFalse(isdir(join(rel, 'Dir_test')))
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.SUCCESS)

            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'Dir_test',
                    'relative_h': './dir',
                    'type_h': 'entry',
                    'destination': 'TPE'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE')
            self.assertTrue(isdir(join(rel, 'Dir_test')))
            rel = join(settings.FILEBROWSER_ROOT, 'dir')
            self.assertFalse(isdir(join(rel, 'Dir_test')))
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.SUCCESS)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_file(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'function001.pl',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                    'destination': 'Dir_test'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE/Dir_test')
            self.assertTrue(isfile(join(rel, 'function001.pl')))
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE')
            self.assertFalse(isfile(join(rel, 'function001.pl')))
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.SUCCESS)

            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'function001.pl',
                    'relative_h': './dir/TPE/Dir_test',
                    'type_h': 'entry',
                    'destination': '..'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE')
            self.assertTrue(isfile(join(rel, 'function001.pl')))
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE/Dir_test')
            self.assertFalse(isfile(join(rel, 'function001.pl')))
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.SUCCESS)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_directory_no_destination(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'Dir_test',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                },
                follow=True
            )
            self.assertEqual(response.status_code, 400)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_file_no_destination(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'function001.pl',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                },
                follow=True
            )
            self.assertEqual(response.status_code, 400)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_not_existing_directory(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'noDir',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                    'destination': 'Dir_test'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.ERROR)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_not_existing_file(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'nofile',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                    'destination': 'Dir_test'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.ERROR)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_directory_destination_error(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'Dir_test',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                    'destination': 'er&€or'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE')
            self.assertFalse(isdir(join(rel, 'er&€or')))
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE')
            self.assertTrue(isdir(join(rel, 'Dir_test')))
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.ERROR)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_file_destination_error(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'function001.pl',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                    'destination': 'er&€or'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE')
            self.assertFalse(isdir(join(rel, 'er&€or')))
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE')
            self.assertTrue(isfile(join(rel, 'function001.pl')))
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.ERROR)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_directory_not_in_directory(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'Dir_test',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                    'destination': '../..'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE/../..')
            self.assertFalse(isdir(join(rel, 'Dir_test')))
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.ERROR)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_file_not_in_directory(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'function001.pl',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                    'destination': '../..'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE/../..')
            self.assertFalse(isfile(join(rel, 'function001.pl')))
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.ERROR)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_not_existing_directory_not_in_directory(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'noDir',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                    'destination': '../..'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE/../..')
            self.assertFalse(isdir(join(rel, 'noDir')))
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.ERROR)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise


    def test_move_not_existing_file_not_in_directory(self):
        try :
            response = self.c.post(
                '/filebrowser/apply_option/post',
                {
                    'option_h': 'move',
                    'name_h': 'nofile',
                    'relative_h': './dir/TPE',
                    'type_h': 'entry',
                    'destination': '../..'
                },
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            rel = join(settings.FILEBROWSER_ROOT, 'dir/TPE/../..')
            self.assertFalse(isfile(join(rel, 'nofile')))
            m = list(response.context['messages'])
            self.assertEqual(len(m), 1)
            self.assertEqual(m[0].level, messages.ERROR)
        except AssertionError :
            m = list(response.context['messages'])
            if m:
                print("\nFound messages:")
                [print(i.level,':',i.message) for i in m]
            raise