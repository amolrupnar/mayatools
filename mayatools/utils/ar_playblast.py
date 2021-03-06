import pymel.core as pm
import maya.mel as mel
import tempfile


def ar_playblast(fileName, width, height, startTime=None, endTime=None):
    """
    pcg_playblast using custom setting.
    :param fileName: string (file path)
    :param width: int
    :param height: int
    :param startTime: float
    :param endTime: float
    :return: pcg_playblast
    """
    # cam = pm.ls('*:cameraHD', typ='transform')[0]
    # noinspection PyTypeChecker
    aPlayBackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
    soundFile = pm.windows.timeControl(aPlayBackSlider, q=True, s=True)
    if startTime and endTime:
        pm.playbackOptions(min=startTime)
        pm.playbackOptions(ast=startTime)
        pm.playbackOptions(max=endTime)
        pm.playbackOptions(aet=endTime)
    if soundFile:
        playblast = pm.playblast(f=fileName, format='qt', s=soundFile[0], sqt=0, fo=True, cc=True, p=100,
                                 compression="H.264",
                                 quality=100, height=height, width=width)
    else:
        playblast = pm.playblast(f=fileName, format='qt', sqt=0, fo=True, cc=True, p=100,
                                 compression="H.264",
                                 quality=100, height=height, width=width)
    return playblast


def ar_convertPerspCamToShotCam(cam, perspCam):
    """
    convert perspective cam as shot cam.
    cam transform node as constraint
    cam shape attributes connect.
    :param cam: string
    :param perspCam: string
    :return: perspCam
    """
    cam = pm.PyNode(cam)
    perspCam = pm.PyNode(perspCam)
    camShape = cam.getShape()
    prspShape = perspCam.getShape()

    camShapeAttrs = pm.listAttr(camShape)

    pm.parentConstraint(cam, perspCam)
    for each in camShapeAttrs:
        try:
            pm.connectAttr(camShape + '.' + each, prspShape + '.' + each, f=True)
        except UserWarning:
            pass
    return perspCam


def ar_getSoundFilePath():
    """
    get sound file path and export it in your temp directory.
    :param: rawFileName: string (fileNameForExportTxtAsSameNaming)
    :return: soundFileTextPath
    """
    audio = pm.ls(type='audio')[0]
    path = audio.filename.get()
    if path:
        tempDir = tempfile.gettempdir()
        soundFileTextPath = tempDir + '/raw_soundFilePathInText.txt'
        with open(soundFileTextPath, 'w') as fi:
            fi.write(path)
        return soundFileTextPath
    else:
        return False
