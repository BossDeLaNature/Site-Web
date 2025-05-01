# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 15:36:03 2025

@author: moito
"""

from pdf2image import convert_from_path
pages = convert_from_path('Physiopath-Endocrino.pdf', 500)

for count, page in enumerate(pages):
    page.save(f'pdf/out{count}.jpg', 'JPEG')