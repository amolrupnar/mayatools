import sys
import os
from PySide import QtGui
from ConfigParser import SafeConfigParser

from mayatools.ui import playblastUI
from mayatools.batch.pcg_playblast import playblast_bat
from mayatools.batch.pcg_playblast import mayaSceneParser

reload(playblastUI)
reload(mayaSceneParser)

# files.
mayaFilePath = r"D:\temp\BDG105_004_lay.ma"
# configFilePath = os.path.dirname(__file__) + '/setting.config'
configFilePath = r"C:\Users\amol\PycharmProjects\mayatools\batch\pcg_playblast\setting.config"
# styles.
styles_dir = os.path.join(os.path.dirname(__file__), 'styles')
qt_dark_blue = os.path.join(styles_dir, 'qt_dark_blue.qss')
qt_dark_orange = os.path.join(styles_dir, 'qt_dark_orange.qss')

with open(qt_dark_blue, 'r') as fid:
    QTDark = fid.read()


class PlayblastUIConn(QtGui.QMainWindow, playblastUI.Ui_MainWindow):
    def __init__(self, maya_file_path, config_file_path):
        super(PlayblastUIConn, self).__init__()
        self.mayaFilePath = maya_file_path
        self.configFilePath = config_file_path
        self.setupUi(self)
        self.setStyleSheet(QTDark)
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
        print start_frame
        print end_frame
        print selected_cam
        print selected_resolution
        parser = SafeConfigParser()
        parser.read(self.configFilePath)
        resolution = parser.get('resolution', selected_resolution)
        res = resolution.split(',')
        playblast_bat.batPlayblast(selected_cam, self.mayaFilePath, start_frame, end_frame, xRes=res[0], yRes=res[1])
        self.playblast_PB.setVisible(False)

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
