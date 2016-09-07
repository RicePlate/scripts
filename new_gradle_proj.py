"""create a empty gradle project with default layout"""


import os
import argparse
import shutil
import sys

class chdir:
  def __init__(self, path):
    self.newpath=os.path.expanduser(path)

  def __enter__(self):
    self.oldpath=os.getcwd()
    os.chdir(self.newpath)
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    os.chdir(self.oldpath)

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--d", help="project name", type=str)
  parser.add_argument("--p", help="path to project home", type=str)
#  parser.add_argument("--g", help="group name (also the package path; e.g. com.rp", type=str)
#  parser.add_argument("--m", help="main class name", type=str)
  return parser.parse_args()

def build_root(root_name):  # assumes cur directory is the project root
  path = os.path.abspath(os.path.join(".", root_name))
  if os.path.exists(path):
    return path
  os.mkdir(root_name)
  return path

def build_src(proj_path):
  os.makedirs(os.path.join(proj_path, "src", "main", "java"))
  os.makedirs(os.path.join(proj_path, "src", "test", "java"))

def copy_gradle_files(proj_path, gsrc):
  gfiles = os.listdir(gsrc)
  for f in gfiles:
    path = os.path.join(gsrc,f)
    if os.path.isfile(path):
      shutil.copy(path, proj_path)
    else:
      shutil.copytree(path, os.path.join(proj_path, f))

if __name__ == "__main__":
  args = parse_args()
  if os.path.exists(args.p):
    with chdir(args.p) as p:
      proj_path = build_root(args.d)
      try:
        build_src(proj_path)
        copy_gradle_files(proj_path, os.path.join(p.oldpath, "newGradleProjectFiles"))
      except Exception as e:
        print e
        print("Exception caught... Undoing project creation")
        shutil.rmtree(proj_path)
        sys.exit(1)
  else:
    raise ValueError("directory does not exist: {}.".format(args.p))
