import requests
from bs4 import BeautifulSoup
from time import sleep
import wget
from zipfile import ZipFile
from subprocess import Popen, PIPE
import importlib
import os


class Module:
    def __init__(self):
        self.modules_php = []
        self.modules_js = []
        self.load_modules()

    def _load_module(self, pwd):
        my_path = pwd.replace("/", ".")
        my_path = "modules." + my_path
        module = importlib.import_module(my_path)
        return module.Module()

    def load_modules(self):
        # Save compiled modules in a list (avoid loading them several times)
        for (p, _, files) in os.walk("./modules/php"):
            self.modules_php.extend([self._get_module(f, p) for f in files 
                            if ("_" not in f) and ("_" not in p) and (not f.endswith(".pyc"))])
        while None in self.modules_php:
            self.modules_php.remove(None)

        for (p, _, files) in os.walk("./modules/js"):
            self.modules_js.extend([self._get_module(f, p) for f in files 
                            if ("_" not in f) and ("_" not in p) and (not f.endswith(".pyc"))])
        while None in self.modules_js:
            self.modules_js.remove(None)

    def _get_module(self, module_file, pwd): 
        # Load the module and return it
        try:
            data = self._load_module(os.path.join(pwd.replace("./modules/", ""), module_file.replace(".py", "")))
        except Exception as e:
            print(e)
            data = None
        return data

class Analyze:
    def __init__(self):
        module_generate = Module()
        self.modules_php = module_generate.modules_php
        self.modules_js = module_generate.modules_js

    def remove_empty_result(self, files):
            while "" in files:
                files.remove("")
            return files

    def get_files(self, directory, ext):
        result = Popen(["find",  directory, "-name", ext], stdout=PIPE, stderr=PIPE)
        return self.remove_empty_result(result.stdout.read().decode(errors="ignore").split("\n"))

    def get_download_url(self, plugin):
        req = f"https://api.wordpress.org/plugins/info/1.0/{plugin}.json"
        response = requests.get(req)
        try:
            data = response.json()
            # last_updated = data["last_updated"]
            # Check Update to discard old plugins (if we check early)
            versions = data["versions"]
            last = list(versions.popitem())
            if last[0] == "trunk":
                last = list(versions.popitem())
            return last[1].replace("\\","")
        except:
            return None

    def process_plugin(self, url):
        plugin_name = wget.download(url)
        print("")
        with ZipFile(plugin_name, 'r') as zipObj:
            zipObj.extractall('./plugins')
        # Remove zip
        os.system(f"rm {plugin_name}")
        folder_to_analyze = "plugins/" + plugin_name.replace(".zip", "")
        
        folder_to_analyze = "./" + folder_to_analyze.split(".")[0]
        php_files = self.get_files(folder_to_analyze, "*.php")
        self.process_files(php_files, self.modules_php)

        js_files = self.get_files(folder_to_analyze, "*.js")
        js_files.extend(self.get_files(folder_to_analyze, "*.html"))
        self.process_files(js_files, self.modules_js)

        # Remove final .version
        os.system(f'rm -rf {folder_to_analyze}')

    def process_files(self, files, modules):
        for f in files:
            print(f)
            with open(f) as open_file:
                code = open_file.read()
                for module in modules:
                    data = module.check_code(f, code)
                    if data:
                        self.write_results(f, data)

    def write_results(self, f, vulnerabilities):
        print(f"[+] vulnerabilities found in {f}")
        for vuln in vulnerabilities:
            name = "./results/vulnerabilities.txt"
            with open(name, "a+") as dump_result:
                dump_result.write(f + "\n")
                dump_result.write("-"*len(f) + "\n")
                try:
                    for k, v in vuln.items():
                        dump_result.write(f"{k}: {v}\n")
                    dump_result.write("\n")
                except:
                    pass

    def start_analysis(self):
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
        response = requests.get("http://plugins.svn.wordpress.org/", headers=header)
        code = response.status_code
        if code == 200:
            plugins = response.text
            soup = BeautifulSoup(plugins, 'html.parser')
            refs = soup.find_all('a')
            print(f"[*] Total plugins {len(refs)}")
            print("[*] Starting the analisys")
            for a in refs:
                plugin = a.get("href").strip("/")
                try:
                    download_url = self.get_download_url(plugin)
                    if download_url:
                        ## Download
                        print(download_url)
                        self.process_plugin(download_url)
                except Exception as e:
                    print(e)
                sleep(2)
        else:
            print("[-] Response code: " + str(code))
        

if __name__ == "__main__":
    print("""
 __      ____________  ___ ___               __                
/  \    /  \______   \/   |   \ __ __  _____/  |_  ___________ 
\   \/\/   /|     ___/    ~    \  |  \/    \   __\/ __ \_  __ \\
 \        / |    |   \    Y    /  |  /   |  \  | \  ___/|  | \/
  \__/\  /  |____|____\___|_  /|____/|___|  /__|  \___  >__|   
       \/       /_____/     \/            \/          \/       
       
|__ Author: @JosueEncinar
    
    """)
    print("[*] Starting the process")
    try:
        Analyze().start_analysis()
    except KeyboardInterrupt:
        print("[*] CTRL^C - Bye")
    except Exception as e:
        print("[-] Something was wrong")
        print(e)