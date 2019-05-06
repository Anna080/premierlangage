import os
import shutil
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from splinter import Browser

from filebrowser.models import Directory


FAKE_FB_ROOT = os.path.join(settings.APPS_DIR, 'tests/tmp')

HOME_DIR = os.path.join(settings.APPS_DIR, "misc_tests/resources/fake_filebrowser_data/")
LIB_DIR = os.path.join(settings.APPS_DIR, "misc_tests/resources/lib/")



@override_settings(FILEBROWSER_ROOT=FAKE_FB_ROOT)
class SplinterTestCase(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.b = Browser()
    
    
    @classmethod
    def tearDownClass(cls):
        cls.b.quit()
        shutil.rmtree(FAKE_FB_ROOT)
        super().tearDownClass()
    
    
    def setUp(self):
        super().setUp()
        self.u = User.objects.create_superuser("login", password="secret", email="test@test.test")
        self.dir = Directory.objects.create(name='Yggdrasil', owner=self.u).root
        self.lib = Directory.objects.create(name='lib', owner=self.u).root
        shutil.rmtree(os.path.join(self.dir))
        shutil.copytree(HOME_DIR, self.dir)
        shutil.rmtree(os.path.join(self.lib))
        shutil.copytree(LIB_DIR, self.lib)
    
    
    def connect_to_filebrowser(self):
        self.b.reload()
        self.visit("filebrowser")
        if not self.b.is_text_present("login"):
            self.b.fill("username", "login")
            self.b.fill("password", "secret")
            self.b.find_by_text("Log-in").click()
    
    
    def visit(self, url):
        self.b.visit(os.path.join(self.live_server_url, url))
    
    
    def answer_preview(self, web_driver, answer):
        self.assertTrue(web_driver.is_element_present_by_name("answer", wait_time=10))
        web_driver.fill("answer", answer)
        self.assertTrue(web_driver.is_element_present_by_text("Valider", wait_time=10))
        web_driver.find_by_text("Valider").click()
        time.sleep(0.5)
    
    
    def answer_pl(self, answer):
        self.assertTrue(self.b.is_element_present_by_id("form_answer", wait_time=50))
        self.b.fill("answer", answer)
        self.assertTrue(self.b.is_element_present_by_text("Valider", wait_time=10))
        self.b.find_by_text("Valider").click()
        time.sleep(1)
    
    
    def test_file_browser_preview(self):
        self.connect_to_filebrowser()
        self.assertTrue(self.b.is_text_present("home", wait_time=10))
        self.b.find_by_text("home").click()
        self.assertTrue(self.b.is_text_present("lib", wait_time=10))
        self.b.find_by_text("lib").click()
        self.assertTrue(self.b.is_text_present("demo", wait_time=10))
        self.b.find_by_text("demo").click()
        self.assertTrue(self.b.is_text_present("static_add.pl", wait_time=10))
        self.b.find_by_text("static_add.pl").click()
        self.assertTrue(self.b.is_element_present_by_css('div[class="tab-item ng-star-inserted"]',
                                                         wait_time=10))
        self.b.find_by_css('div[class="tab-item ng-star-inserted"]').click()
        
        self.assertTrue(self.b.is_element_present_by_tag("iframe", wait_time=10))
        self.b.is_element_present_by_text("Valider", wait_time=2)
        with self.b.get_iframe(0) as iframe:
            self.answer_preview(iframe, "1")
            self.assertTrue(iframe.is_text_present("Mauvaise réponse"))
            self.answer_preview(iframe, "2")
            self.assertTrue(iframe.is_text_present("Mauvaise réponse"))
            self.answer_preview(iframe, "7")
            self.assertTrue(iframe.is_text_present("Bonne réponse"))
            self.answer_preview(iframe, "3")
            self.assertTrue(iframe.is_text_present("Mauvaise réponse"))
            self.answer_preview(iframe, "4")
            self.assertTrue(iframe.is_text_present("Mauvaise réponse"))
            self.answer_preview(iframe, "7")
            self.assertTrue(iframe.is_text_present("Bonne réponse"))
            self.answer_preview(iframe, "5")
            self.assertTrue(iframe.is_text_present("Mauvaise réponse"))
    
    
    def test_filebrowser_pl(self):
        self.connect_to_filebrowser()
        self.assertTrue(self.b.is_text_present("lib", wait_time=10))
        self.b.find_by_text("lib").click()
        self.assertTrue(self.b.is_text_present("demo", wait_time=10))
        self.b.find_by_text("demo").click()
        self.assertTrue(self.b.is_text_present("static_add.pl", wait_time=10))
        self.b.find_by_text("static_add.pl").first.mouse_over()
        self.assertTrue(
                self.b.is_element_present_by_id("op-0-lib/demo/static_add.pl", wait_time=10))
        self.b.find_by_id("op-0-lib/demo/static_add.pl").first.click()
        self.b.windows[0].close()
        
        self.answer_pl("1")
        self.assertTrue(self.b.is_text_present("Mauvaise réponse"))
        self.answer_pl("2")
        self.assertTrue(self.b.is_text_present("Mauvaise réponse"))
        self.answer_pl("7")
        self.assertTrue(self.b.is_text_present("Bonne réponse"))
        self.answer_pl("3")
        self.assertTrue(self.b.is_text_present("Mauvaise réponse"))
        self.answer_pl("4")
        self.assertTrue(self.b.is_text_present("Mauvaise réponse"))
        self.answer_pl("7")
        self.assertTrue(self.b.is_text_present("Bonne réponse"))
        self.answer_pl("5")
        self.assertTrue(self.b.is_text_present("Mauvaise réponse"))
    
    
    def test_filebrowser_activity(self):
        self.connect_to_filebrowser()
        self.assertTrue(self.b.is_text_present("lib", wait_time=10))
        self.b.find_by_text("lib").click()
        self.assertTrue(self.b.is_text_present("demo", wait_time=10))
        self.b.find_by_text("demo").click()
        self.assertTrue(self.b.is_text_present("static_add.pl", wait_time=10))
        self.b.find_by_text("random_all.pltp").first.mouse_over()
        self.assertTrue(
                self.b.is_element_present_by_id("op-1-lib/demo/random_all.pltp", wait_time=10))
        self.b.find_by_id("op-1-lib/demo/random_all.pltp").first.click()
        
        self.assertTrue(
                self.b.is_element_present_by_text(
                        " a bien été créée et a pour URL LTI:                     ", wait_time=10))
        self.assertTrue(
                self.b.is_element_present_by_text(" OPEN                    ", wait_time=10))
        self.b.find_by_text(" OPEN                    ").click()
        time.sleep(1)
        self.b.windows[0].close()
        
        self.b.click_link_by_partial_text("Commencer")
        self.b.fill("answer", "7")
        self.assertTrue(self.b.is_element_present_by_text("Valider", wait_time=10))
        self.b.find_by_text("Valider").click()
        self.assertTrue(self.b.is_element_present_by_text("Bonne réponse", wait_time=50))
        self.b.click_link_by_partial_text("Suivant")
        
        self.assertTrue(self.b.is_element_present_by_css(
                'a[class="btn btn-secondary btn-type state-succeded btn-lg"]', wait_time=10))
        self.assertTrue(self.b.is_element_present_by_css(
                'a[class="btn btn-secondary btn-type state-started btn-lg active"]', wait_time=10))
        
        self.assertTrue(self.b.is_element_present_by_css(
                'a[class="btn btn-secondary btn-type state-unstarted btn-lg"]', wait_time=10))
        self.b.click_link_by_partial_text("Addition Aléatoire (using eval_func)")
        time.sleep(1)
        self.b.fill("answer", "-1")
        self.assertTrue(self.b.is_element_present_by_text("Valider", wait_time=10))
        self.b.find_by_text("Valider").click()
        time.sleep(1)
        self.b.find_by_text("Random add").click()
        self.assertTrue(self.b.is_element_present_by_css(
                'a[class="btn btn-secondary btn-type state-failed btn-lg"]', wait_time=10))
    
    
    def test_filebrowser_markdown_mathjax(self):
        self.connect_to_filebrowser()
        self.assertTrue(self.b.is_text_present("home", wait_time=10))
        self.b.find_by_text("home").click()
        self.assertTrue(self.b.is_text_present("cbank", wait_time=10))
        self.b.find_by_text("cbank").click()
