#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  filebrowser.py
#  
#  Copyright 2018 Coumes Quentin
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#


import os, copy

from os.path import abspath, join, dirname

from django.conf import settings

from filebrowser.filebrowser_option import ENTRY_OPTIONS, DIRECTORY_OPTIONS, READ, WRITE
from filebrowser.models import Directory



class Filebrowser:
    """Filebrowser allowing to browse through a file tree.
    
    Attributes:
        root (str): Absolute path to the root of the filebrowser.
        relative (str): relative path from self.root of the current position of the filebrowser
        directory (Directory): The current directory, None if current position is self.root
        entry_options (FilebrowserOption): List of every options applicable to entries
        directory_options (FilebrowserOption): List of every options applicable to self.directory
    """
    
    def __init__(self, request, path):
        user_id = str(request.user.id)

        self.root = settings.FILEBROWSER_ROOT
        self.path = abspath(os.path.join(self.root, path))
        self.relative = path
        self.home = self.relative.split('/')[0]
        self.entry_options = copy.deepcopy(ENTRY_OPTIONS)
        self.directory_options = copy.deepcopy(DIRECTORY_OPTIONS)
        self.directory = Directory.objects.get(name=self.home)

    def _filter_category_options(self, category, request):
        
        for group_key, group in category.groups.items():

            filtered_options = {}
            
            for option_key, option in group.options.items():
                if option.right == READ and self.directory.can_read(request.user):
                    filtered_options[option_key] = option
                elif option.right == WRITE and self.directory.can_write(request.user):
                    filtered_options[option_key] = option
            
            category.groups[group_key].options = filtered_options
        
        cleaned = {}
        for group_key, group in category.groups.items():  # removing empty group
            if group.options:
                cleaned[group_key] = group
        category.groups = cleaned
        
        return category
     
    def load_options(self, request):
        self.entry_options = self._filter_category_options(self.entry_options, request)
        self.directory_options = self._filter_category_options(self.directory_options, request)

    def can_read(self, request):
        return self.directory.can_read(request.user)
    
    def can_write(self, request):
        return self.directory.can_read(request.user)

    
    
    
    


