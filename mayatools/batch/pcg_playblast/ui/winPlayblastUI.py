import sys
import os
from PySide import QtGui, QtCore
from ConfigParser import SafeConfigParser

from mayatools.batch.pcg_playblast.ui import playblastUI
from mayatools.batch.pcg_playblast import playblast_bat
from mayatools.batch.pcg_playblast import mayaSceneParser

reload(playblastUI)
reload(mayaSceneParser)
reload(playblast_bat)
# files.
mayaFilePath = r"D:\temp\BDG105_004_layNew.ma"
configFilePath = os.path.dirname(os.path.dirname(__file__)) + '/setting.config'
# styles.
styles_dir = os.path.join(os.path.dirname(__file__), 'styles')
qt_dark_blue = os.path.join(styles_dir, 'qt_dark_blue.qss')
qt_dark_orange = os.path.join(styles_dir, 'qt_dark_orange.qss')

with open(qt_dark_blue, 'r') as fid:
    QTDark = fid.read()


# Inherit from QThread
class QSignalEmmiter(QtCore.QThread):
    # This is the signal that will be emitted during the processing.
    # By including int as an argument, it lets the signal know to expect
    # an integer argument when emitting.
    updateProgress = QtCore.Signal(int)

    # You can do any extra things in this init you need, but for this example
    # nothing else needs to be done expect call the super's init
    def __init__(self):
        QtCore.QThread.__init__(self)

    # A QThread is run by calling it's start() function, which calls this run()
    # function in it's own "thread".
    def run(self):
        # Notice this is the same thing you were doing in your progress() function
        for i in range(1, 101):
            # Emit the signal so it can be received on the UI side.
            self.updateProgress.emit(i)


class PlayblastUIConn(QtGui.QMainWindow, playblastUI.Ui_MainWindow):
    def __init__(self, maya_file_path, config_file_path):
        super(PlayblastUIConn, self).__init__()
        self.mayaFilePath = maya_file_path
        self.configFilePath = config_file_path
        self.setupUi(self)
        # self.setStyleSheet(QTDark)
        self.playblast_PB.setVisible(False)
        self.fill_ui()
        self.connections()

    def connections(self):
        self.custom_res_CB.stateChanged.connect(self.resOnOff)
        self.create_BTN.clicked.connect(self.test_method)

    def fill_ui(self):
        # add resolution list
        resolution = mayaSceneParser.GetSceneDetails(self.mayaFilePath, self.configFilePath)
        for each in resolution.getResolution():
            self.resolution_LW.addItem(each)
        # add cameras list.
        cameras = mayaSceneParser.GetSceneDetails(self.mayaFilePath, self.configFilePath)
        cameras_list = cameras.get_cams()
        cameras_list.sort()
        for each in cameras_list:
            self.camera_LW.addItem(each)
        # fill start frame and end frame.
        frames = mayaSceneParser.GetSceneDetails(self.mayaFilePath, self.configFilePath)
        startFrame = frames.getFrameRange()[0]
        endFrame = frames.getFrameRange()[1]
        self.startFrame_DSB.setValue(float(startFrame))
        self.endFrame_DSB.setValue(float(endFrame))

    def test_method(self):
        selected_cam = None
        selected_resolution = None
        # get selected camera.
        if self.camera_LW.selectedItems():
            selected_cam = str(self.camera_LW.selectedItems()[0].text())
        # get selected resolution.
        if self.resolution_LW.selectedItems():
            selected_resolution = self.resolution_LW.selectedItems()[0].text()
        # query camera and resolution is selected or not.
        if not selected_resolution or not selected_cam:
            return False
        self.playblast_PB.setVisible(True)
        # query start frame and end frame.
        start_frame = self.startFrame_DSB.value()
        end_frame = self.endFrame_DSB.value()
        parser = SafeConfigParser()
        parser.read(self.configFilePath)
        resolution = parser.get('resolution', selected_resolution)
        res = resolution.split(',')
        playblast_bat.batPlayblast(selected_cam, self.mayaFilePath, start_frame, end_frame, xRes=res[0], yRes=res[1],progress=self.playblast_PB)
        # self.playblast_PB.setVisible(False)

    def resOnOff(self):
        self.custResX_SB.setEnabled(self.custom_res_CB.checkState())
        self.custResY_SB.setEnabled(self.custom_res_CB.checkState())


def main():
    app = QtGui.QApplication(sys.argv)
    window = PlayblastUIConn(mayaFilePath, configFilePath)
    window.show()
    return app.exec_()


if __name__ == '__main__':
    win = main()
