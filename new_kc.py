import os
import argparse
import shutil
import sys
import subprocess

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
  parser.add_argument("--p", help="path to project's parent directory (error if already exists)", type=str)
  parser.add_argument("--c", help="name of the competition/project", type=str)
  return parser.parse_args()

def build_root(root_name):
  path = os.path.abspath(root_name)
  if os.path.exists(path):
    raise ValueError("directory already exists: {}".format(path))
  os.makedirs(root_name)
  return path

def build_src(proj_path, competition):
  print("building src dirs")
  main_java = os.path.join(proj_path, "src", "main", "java", competition)
  Competition = competition[0].upper() + competition[1:]
  os.makedirs(os.path.join(main_java))
  os.makedirs(os.path.join(proj_path, "src", "main", "java", "water"))
  os.makedirs(os.path.join(proj_path, "src", "test", "java"))
  with open(os.path.join(main_java, "{}.java".format(Competition)), 'w') as f:
    f.write("package {}\n".format(competition))
    f.write("\npublic class {} {{\n".format(Competition))
    f.write("}\n")

def build_lib(proj_path):
  os.makedirs(os.path.join(proj_path, "lib"))
  h2ojar = os.path.join(os.getenv('H2O_HOME'), "build", "h2o.jar")
  path = os.path.join(proj_path, "lib", "h2o.jar")
  print("Copying h2o.jar from {} to {}".format(h2ojar, path))
  shutil.copyfile(h2ojar,path)

def build_dirs(proj_path):
  print("building data, models, submissions, and py_utils")
  os.makedirs(os.path.join(proj_path, "data"))
  os.makedirs(os.path.join(proj_path, "models"))
  os.makedirs(os.path.join(proj_path, "submissions"))
  os.makedirs(os.path.join(proj_path, "py_utils"))

  # file holding previous submission number, useful for automatically
  # increasing submission numbers
  with open( os.path.join(proj_path, "submissions", "next"), 'w') as f:
    f.write("0")

if __name__ == "__main__":
  args = parse_args()
  proj_parent = args.p
  if os.path.exists(proj_parent):
    with chdir(proj_parent) as p:
      proj_path = build_root(args.c)
      try:
        build_src(proj_path, args.c)
        build_lib(proj_path)
        build_dirs(proj_path)
      except Exception as e:
        print e
        print("Exception caught... Undoing project creation")
        shutil.rmtree(proj_path)
        sys.exit(1)
  else:
    raise ValueError("directory does not exist: {}.".format(args.p))
