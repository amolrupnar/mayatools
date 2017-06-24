import os
import sys
import subprocess

app_to_launch = r"C:\Program Files\Autodesk\Maya2015\bin\maya.exe"


def setEnvPaths():
    # set environment variable path.
    os.environ['MAYA_APP_PATH'] = r"C:\Program Files\Autodesk\Maya2015\bin\maya.exe"
    os.environ['XBMLANGPATH'] = r"T:\\amol\bit_bucket\maya_paths\icon"
    os.environ['MAYA_SHELF_PATH'] = r"T:\\amol\bit_bucket\maya_paths\shelf"
    os.environ['PYTHONPATH'] = r"T:\\amol\bit_bucket\mayatools\mayatools\ar_startup"


def launch_app(mayaApp):
    setEnvPaths()
    cmd = [mayaApp, '-noAutoloadPlugins', '-log', 'D:/temp/maya_log.txt']
    subprocess.Popen(cmd)


if __name__ == '__main__':
    launch_app(app_to_launch)
