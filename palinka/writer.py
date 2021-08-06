from __future__ import annotations

import os
import palinka
import re
import shutil

import pkg_resources

import os, shutil

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def rec_copy(src, dest):
    if not pkg_resources.resource_isdir(__name__, src):
        src_stream = pkg_resources.resource_string(__name__, src)
        with open(dest, "wb") as dest_file:
            dest_file.write(src_stream)
    else:
        os.makedirs(dest, exist_ok=True)
        for resource in pkg_resources.resource_listdir(__name__, src):
            rec_copy(src + "/" + resource, os.path.join(dest, resource))

class ProjectGenerator:
    def __init__(self, dir_path: str):
        self.path = os.path.join(dir_path, 'palinka')
        self.libs = []
    
    def add_library(self, dir_path: str, name: str):
        self.libs.append((dir_path, name))
        return self

    def generate(self, raw_code: str, symbol_table: palinka.model.symbol_table.SymbolTable, plant: palinka.model.automation.Plant):
        path = self.path
        
        if os.path.exists(path):
            shutil.rmtree(path)

        try:
            os.makedirs(path, exist_ok=True)
            rec_copy("assets/palinka", os.path.join(path))
            
            for lib, libname in self.libs:
                shutil.copytree(lib, os.path.join(self.path, "libs", libname))

        except Exception as e:
            print(e)
                
            
        CodeWriter(os.path.join(path, 'src/codegen')).write(raw_code)

        with open(os.path.join(path, "symbols.xml"), "wb") as file:
            file.write(palinka.model.symbol_table.serialize(symbol_table))
        
        with open(os.path.join(path, "plant.xml"), "wb") as file:
            file.write(palinka.model.automation.serialize(plant))

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
    
    def write(self, txt):
        for line in txt.split('\n'):
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

def create_project(dest, code: str, symbol_table: palinka.model.symbol_table.SymbolTable):
    ProjectGenerator(dest).generate(code, symbol_table)
    

