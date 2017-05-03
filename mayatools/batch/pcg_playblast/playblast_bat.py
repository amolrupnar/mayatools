import pymel.core as pm
import os
import tempfile
from subprocess import Popen, PIPE, STDOUT


def batPlayblast(cam, mayaFilePath, startFrame, endFrame, xRes=1280, yRes=720, imageName=None,
                 renderDirPath=None, mayaVersion='Maya2015', progress=None):
    """
    create pcg_playblast using hardware render.
    :param cam: string
    :param mayaFilePath: string (maya file path)
    :param xRes: int (x resolution)
    :param yRes: int (y resolution)
    :param startFrame: float
    :param endFrame: float
    :param imageName: string
    :param renderDirPath: string (path)
    :param mayaVersion: string
    :param progress: string (progress bar name)
    :return: pcg_playblast
    """
    renderExe = "C:/Program Files/Autodesk/%s/bin/Render.exe" % mayaVersion
    if not imageName:
        imageName = 'test'
    if not renderDirPath:
        renderDirPath = tempfile.mktemp(prefix='test_')
    preCmd = 'startupCmd;'
    render_cmd = '"{0}" -s {7} -e {8} -postRender "{9}" -r "hw2" -of "png" -cam "{1}" -im "{6}" -fnc 3 -x {2} -y {3} -rd "{4}" "{5}"'.format(
        renderExe,
        cam, xRes,
        yRes,
        renderDirPath,
        mayaFilePath,
        imageName,
        startFrame,
        endFrame,
        preCmd
    )
    os.environ['MAYA_SCRIPT_PATH'] = os.path.dirname(__file__)
    os.environ['PYTHONPATH'] = os.path.dirname(__file__)
    os.environ['PROD_SERVER'] = 'P:/badgers_and_foxes'
    total_frames = (endFrame - startFrame)
    percent_increment = 100 / total_frames
    process = Popen(render_cmd, shell=True, stderr=STDOUT, stdout=PIPE)

    i = 0
    while process.poll() is None:
        line = process.stdout.readline()
        if line.find('Rendering frame') != -1:
            frame = line.split(' ')[2]
            percent = percent_increment * i
            if progress:
                print percent
                print frame
                progress.setValue(percent)
            i += 1
    tempdir = tempfile.gettempdir()
    soundFileTextPath = tempdir + '/raw_soundFilePathInText.txt'
    if os.path.isfile(soundFileTextPath):
        with open(soundFileTextPath, 'r') as fi:
            soundFilePath = fi.readline()
        os.remove(soundFileTextPath)
        return renderDirPath, soundFilePath
    else:
        return renderDirPath


def getSoundFilePath():
    """
    get sound file path and export it in your temp directory.
    :param: rawFileName: string (fileNameForExportTxtAsSameNaming)
    :return: soundFileTextPath
    """
    audio = pm.ls(type='audio')[0]
    if audio:
        path = audio.filename.get()
        if path:
            tempDir = tempfile.gettempdir()
            soundFileTextPath = tempDir + '/raw_soundFilePathInText.txt'
            with open(soundFileTextPath, 'w') as fi:
                fi.write(path)
            return soundFileTextPath
        else:
            return False
    else:
        pass
