#!/usr/bin/env python
import os
import sys
import subprocess
import fnmatch
import re
import gzip
import shutil
import requests
import zipfile

v_path_logo = "/tmp"
v_url_logo = "https://codeload.github.com/home-assistant/brands/zip/refs/heads/master"
v_path_js = "/usr/local/lib/python" + "{0[0]}.{0[1]}".format(sys.version_info) + "/site-packages/hass_frontend"

def build_logo(path, url):
    if not os.path.exists(path + "/brands-master"):
        res = requests.get(url, allow_redirects=True)
        open(path + "/brands.zip", 'wb').write(res.content)

        with zipfile.ZipFile(path + "/brands.zip", "r") as zip_ref:
            zip_ref.extractall(path)

        subprocess.run(["apk", "add", "rsync", "librsvg-dev", "optipng"])
        subprocess.run(["chmod", "+x", path + "/brands-master/scripts/build.sh"])
        try:
            subprocess.run(["ln", "-s", "/tmp/brands-master/build", "/config/www/brands"])
        except subprocess.CalledProcessError as e:
            print(e.output)

    print(subprocess.run([path + "/brands-master/scripts/build.sh"], shell=True, cwd=path + "/brands-master"))

def find_js(pattern, path):
    rtn = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                rtn.append(os.path.join(root, name))
    return rtn

def edit_js(files):
    for i in files:
        print("Modify: " + i)
        with open(i, "r") as sources:
            lines = sources.readlines()
        with open(i, "w") as sources:
            for line in lines:
                sources.write(re.sub(r"https://brands.home-assistant.io", "/local/brands/build", line))
        with open(i, 'rb') as f_in:
            with gzip.open(i + ".gz", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

edit_js(find_js("*.js", v_path_js))
build_logo(v_path_logo, v_url_logo)
