# -*- coding: utf-8 -*-
from ui import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtWidgets
import sys
import cv2
import styleChange
import os
import shutil
import subprocess


USER_HOME = os.environ["USERPROFILE"]

class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.cam = True
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.setupUi(mainWindow)
        self.CAM_NUM = 0
        self.train_bool = False
        self.train_convert_bool = False
        self.convert_1_bool = False

    def sh_(self, cmd):
        """ Execute shell commands """
        subprocess.check_call(cmd)

    def current_(self):
        self.open.setVisible(True)
        self.shoot.setVisible(True)
        self.close.setVisible(True)
        self.train_convert.setVisible(True)
        self.train.setVisible(False)
        self.current_ = True
        self.customize_ = False
        self.convert_1.setVisible(False)
        self.choose.setVisible(False)
        self.convert.setVisible(False)
        self.shoot.setText("拍摄")
        self.label_2.setText("Perview:现有模型")
        self.label.clear()

    def customize_(self):
        self.open.setVisible(False)
        self.shoot.setVisible(False)
        self.close.setVisible(False)
        self.train_convert.setVisible(True)
        self.train.setVisible(True)
        self.customize_ = True
        self.current_ = False
        self.shoot.setText("拍摄")
        self.label_2.setText("Perview:自定义训练")
        self.convert_1.setVisible(False)
        self.choose.setVisible(False)
        self.convert.setVisible(False)
        self.label.clear()

    def train_convert_image_choose(self):
        file_path_train,_ =  QFileDialog.getOpenFileName(self,"Dir file", USER_HOME + "/Desktop/", "jpg(*.jpg);;png(*.png);;all files(*.*)")
        try:
            shutil.copyfile(file_path_train, "./images/content.jpg")
        except:
            print("error")
            pass
        self.image = cv2.imread(file_path_train)
        self.label.setPixmap(QtGui.QPixmap(file_path_train).scaled(self.label.width(), self.label.height()))
        self.train_convert_bool = True
        if self.current_:
            self.choose.setVisible(True)
            self.convert.setVisible(True)
    
    def train_image_choose(self):
        file_path,_ =  QFileDialog.getOpenFileName(self,"Dir file", USER_HOME + "/Desktop/", "jpg(*.jpg);;png(*.png);;all files(*.*)")
        self.image_train = cv2.imread(file_path)
        shutil.copyfile(file_path, "./images/style.jpg")
        self.train_bool = True

    def all_(self):
        if self.train_bool and self.train_convert_bool:
            self.convert_1.setText("转化")
            self.convert_1.setVisible(True)

    def convert_1_(self):
        if self.convert_1_bool == False:
            self.sh_("./python3/python.exe train.py")
            self.label.setPixmap(QtGui.QPixmap("./images/train_output.jpg").scaled(self.label.width(), self.label.height()))
            self.convert_1.setText("保存")
            self.convert_1_bool = True
        else:
            file_path =  QFileDialog.getSaveFileName(self,"save file", USER_HOME + "/Desktop/result", "jpg(*.jpg);;png(*.png);;all files(*.*)") 
            image = cv2.imread("./images/train_output.jpg")
            cv2.imwrite(file_path[0], image)
            self.convert_1.setText("转化")
            self.convert_1_bool = False

    def button_open_camera_click(self):
        self.shoot.setText("拍摄")
        self.cam = True
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(
                    self, u"Warning", u"请检测相机与电脑是否连接正确",
                    buttons=QtWidgets.QMessageBox.Ok,
                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)

    def show_camera(self):
        flag, self.image = self.cap.read()
        self.image=cv2.flip(self.image, 1) # 左右翻转
        show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.label.setScaledContents(True)
    
    def takePhoto(self):
        self.cap.release()
        self.timer_camera.stop()
        if not self.cam:
            self.shoot.setText("拍摄")
            file_path =  QFileDialog.getSaveFileName(self,"save file", USER_HOME + "/Desktop/result", "jpg(*.jpg);;png(*.png);;all files(*.*)") 
            try:
                if self.convert__:
                    cv2.imwrite(file_path[0], self.image_)
                else:
                    cv2.imwrite(file_path[0], self.image)
                self.choose.setVisible(False)
                self.convert.setVisible(False)
            except:
                self.shoot.setText("拍摄")
                self.cam = True
            self.label.clear()
        else:
            if self.current_:
                self.choose.setVisible(True)
                self.convert.setVisible(True)
            self.convert__ = False
            self.train_convert_bool = False
            self.convert_1.setVisible(False)
            self.shoot.setText("保存")
            self.cam = False
    
    def closeEvent(self):
        self.shoot.setText("拍摄")
        self.cam = True
        self.cap.release()
        self.timer_camera.stop()
        self.label.clear()
    
    def num(self):
        self.style = self.choose.currentText()
    
    def convert_(self):
        try:    
            self.convert__ = True
            self.image_ = self.image
            self.image_ = styleChange.style_tupian(self.image, self.style)
            cv2.imwrite("./images/output.jpg", self.image_)
            self.label.setPixmap(QtGui.QPixmap("./images/output.jpg").scaled(self.label.width(), self.label.height()))
        except:
            msg = QtWidgets.QMessageBox.warning(
            self, u"Warning", u"请选择一个风格后重新点击转化",
            buttons=QtWidgets.QMessageBox.Ok,
            defaultButton=QtWidgets.QMessageBox.Ok)

    def fullScreenOpen(self):
        mainWindow.showFullScreen()

    def quitScreenStart(self):
        mainWindow.showNormal()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = MainForm()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())