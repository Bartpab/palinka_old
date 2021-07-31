from __future__ import annotations

import os
import re
import shutil

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

class ProjectGenerator:
    def __init__(self, dir_path: str):
        self.path = os.path.join(dir_path, 'framework')
    
    def generate(self, raw_code: str):
        path = self.path
        if os.path.exists(path):
            shutil.rmtree(path)

        try:
            framework = pkg_resources.resource_filename("palinka", "assets/framework")
            shutil.copytree(framework, os.path.join(path))
        except Exception as e:
            print(e)
        finally:
            pass
            #pkg_resources.cleanup_resources()
        
        write(os.path.join(path, 'codegen'), raw_code)

class CodeWriter:
    BEGIN_RE = r"\/\/\/ BEGIN (FILE|DIRECTORY) (\S+([.]\s)?) \/\/\/"
    END_RE = r"\/\/\/ END (FILE|DIRECTORY) \/\/\/"

    def __init__(self, root_dir):
        self.path = [root_dir]
        self.files = []
        self.acc = []

        if os.path.exists(os.path.join(*self.path)):
            shutil.rmtree(os.path.join(*self.path))
        os.makedirs(os.path.join(*self.path))
    
    def begin_dir(self, dir):
        self.path.append(dir)
    
    def end_dir(self):
        self.path.pop(-1)
    
    def write(self, line):
        m_begin = re.search(CodeWriter.BEGIN_RE, line)
        m_end = re.search(CodeWriter.END_RE, line)

        if m_begin:
            t_file_or_dir = m_begin.group(1)
            arg = m_begin.group(2)
            if t_file_or_dir == "FILE":
                self.begin_file(arg)
            else:
                self.begin_dir(arg)
        elif m_end:
            t_file_or_dir = m_end.group(1)
            if t_file_or_dir == "FILE":
                self.end_file()
            else:
                self.end_dir()
        else:
            self.acc.append(line)

    def begin_file(self, file):
        self.files.append(file)
        
    def end_file(self):
        file = self.files.pop(-1)
        path = os.path.join(*self.path, file)
        
        # Make directry if not
        os.makedirs(os.path.join(*self.path), exist_ok=True)

        with open(path, "w") as file:
            file.write("\n".join(self.acc))

        self.acc = []

def write(root_dir: str, code: str):
    w = CodeWriter(root_dir)
    
    for line in code.split('\n'):
        w.write(line)

def create_project(dest, code: str):
    ProjectGenerator(dest).generate(code)
    

