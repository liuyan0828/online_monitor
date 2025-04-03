"""
-*- coding: utf-8 -*-
@Time : 4/2/25 
@Author : liuyan
@function : 
"""
import os
from datetime import datetime

def create_dirs():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dirs = {
        "report": f"reports/report_{timestamp}.html",
        "screenshot": f"screenshots/screenshot_{timestamp}.png",
        "log": f"logs/log_{timestamp}.txt",
        "timestamp": timestamp
    }
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    return dirs
