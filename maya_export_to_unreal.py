"""
# demo version
# export static mesh as fbx file
# custom naming convention for proper workflow
# missing ui file
"""


import pymel.core as pmc
from maya.mel import eval as mevl
from PySide2 import QtCore, QtWidgets
import os
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


if os.name == 'nt':
    ldocscripts = os.environ['HOMEPATH']
elif os.name == 'posix':
    ldocscripts = os.environ['HOME']

os.sys.path.append('C:\\ui')

import export_ue_ui


def mayaMainWin():
    mmw = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mmw), QtWidgets.QWidget)


class ExportUE(export_ue_ui.Ui_export_UE, QtWidgets.QDialog):
    prjctpath = None

    def __init__(self, parent=mayaMainWin()):
        super(WabifaExportUE, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('exportue')

        self.looks()
        self.location_PB.pressed.connect(self.opLocation)
        self.pivot_PB.pressed.connect(lambda:self.opPivApply(tgl=True))
        self.ground_PB.pressed.connect(self.opGround)
        self.sm_add_PB.pressed.connect(self.opSMadd)
        self.sm_rmv_PB.pressed.connect(self.opSMrmv)
        self.sm_sel_PB.pressed.connect(self.opSelect)
        self.export_PB.pressed.connect(self.opExport)

    def looks(self):
        pivots = ['Origin', 'Custom',
                  'Front Top Right', 'Front Top Middle', 'Front Top Left',
                  'Front Middle Right', 'Front Middle Middle', 'Front Middle Left',
                  'Front Bottom Right', 'Front Bottom Middle', 'Front Bottom Left',
                  'Middle Top Right', 'Middle Top Middle', 'Middle Top Left',
                  'Middle Middle Right', 'Middle Middle Middle', 'Middle Middle Left',
                  'Middle Bottom Right', 'Middle Bottom Middle', 'Middle Bottom Left',
                  'Back Top Right', 'Back Top Middle', 'Back Top Left',
                  'Back Middle Right', 'Back Middle Middle', 'Back Middle Left',
                  'Back Bottom Right', 'Back Bottom Middle', 'Back Bottom Left']

        self.setWindowTitle('Unreal Export - Demo Version')
        self.setMinimumSize(400,400)
        self.setMaximumSize(600,900)
        self.resize(500,600)
        self.pivot_CB.addItems(pivots)
        self.pivot_CB.setMaxVisibleItems(11)
        self.pivot_CB.setCurrentIndex(8)
        self.solopiv_ChB.setChecked(0)
        self.solopiv_ChB.setHidden(1)
        self.pivot_PB.setHidden(0)
        self.sm_rnm_PB.setHidden(1)
        self.col_rnm_PB.setHidden(1)
        self.sm_LW.setDisabled(0)
        self.col_L.setHidden(1)
        self.col_add_PB.setHidden(1)
        self.col_rmv_PB.setHidden(1)
        self.col_sel_PB.setHidden(1)
        self.col_LW.setDisabled(1)
        self.col_LW.setHidden(1)
        self.utils_L.setText('Mesh')
        self.utils_L.setHidden(0)
        self.utils_cmbn_RB.setChecked(1)
        self.utils_hrch_RB.setText('Keep')
        self.utils_scl_ChB.setText('cm to m')
        self.utils_scl_ChB.setChecked(0)
        self.utils_scl_ChB.setHidden(1)
        self.combine_PB.setHidden(1)
        self.ground_PB.setHidden(1)
        self.export_PB.setMinimumHeight(30)


    def msg(self,idx):
        msg = ['\nFolder not exist  :(','\nNo Static Mesh found, please add at least one  :(','\nDone  :)']
        pmc.warning(msg[idx])

    def pathExist(self):
        self.prjctpath = self.location_LE.text()
        pathexist = False

        if os.path.isdir(self.prjctpath) and os.path.exists(self.prjctpath):
            pathexist = True
        else:
            pathexist = False

        return pathexist

    def selobjs(self,get):
        objs = pmc.ls(sl=1,o=1,tr=1,v=1)
        rmvs = []

        if objs:
            for obj in objs:
                try:
                    if pmc.nodeType(pmc.listRelatives(obj,s=1)[0]) != 'mesh':
                        rmvs.append(obj)
                except:
                    if len(pmc.listRelatives(obj,s=1)) == 0:
                        rmvs.append(obj)
            for rmv in rmvs:
                objs.remove(rmv)

            if objs:
                if get:
                    objs.reverse()
                    return objs
                else:
                    objsname = []
                    for obj in objs:
                        objsname.append(obj.name())
                    objsname.reverse()
                    return objsname
            else:
                return ['__none_']
        else:
            return None

    def getItems(self,lw,get):
        items = []
        if lw == 'sm':
            for idx in range(self.sm_LW.count()):
                if get:
                    items.append(self.sm_LW.item(idx))
                else:
                    items.append(self.sm_LW.item(idx).text())
        elif lw == 'col':
            for idx in range(self.col_LW.count()):
                if get:
                    items.append(self.col_LW.item(idx))
                else:
                    items.append(self.col_LW.item(idx).text())
        return items

    def movePivot(self,obj,idx):
        pvt = pmc.exactWorldBoundingBox(obj)

        if idx == 0:
            return [0,0,0]
        elif idx == 1:
            return pmc.xform(obj,q=1,rp=1,a=1,ws=1,wd=1)
        elif idx == 2:
            pvt = [pvt[0],pvt[4],pvt[5]]
        elif idx == 3:
            pvt = [(pvt[0]+pvt[3])*0.5,pvt[4],pvt[5]]
        elif idx == 4:
            pvt = [pvt[3],pvt[4],pvt[5]]
        elif idx == 5:
            pvt = [pvt[0],(pvt[1]+pvt[4])*0.5,pvt[5]]
        elif idx == 6:
            pvt = [(pvt[0]+pvt[3])*0.5,(pvt[1]+pvt[4])*0.5,pvt[5]]
        elif idx == 7:
            pvt = [pvt[3],(pvt[1]+pvt[4])*0.5,pvt[5]]
        elif idx == 8:
            pvt = [pvt[0],pvt[1],pvt[5]]
        elif idx == 9:
            pvt = [(pvt[0]+pvt[3])*0.5,pvt[1],pvt[5]]
        elif idx == 10:
            pvt = [pvt[3],pvt[1],pvt[5]]
        elif idx == 11:
            pvt = [pvt[0],pvt[4],(pvt[2]+pvt[5])*0.5]
        elif idx == 12:
            pvt = [(pvt[0]+pvt[3])*0.5,pvt[4],(pvt[2]+pvt[5])*0.5]
        elif idx == 13:
            pvt = [pvt[3],pvt[4],(pvt[2]+pvt[5])*0.5]
        elif idx == 14:
            pvt = [pvt[0],(pvt[1]+pvt[4])*0.5,(pvt[2]+pvt[5])*0.5]
        elif idx == 15:
            pvt = [(pvt[0]+pvt[3])*0.5,(pvt[1]+pvt[4])*0.5,(pvt[2]+pvt[5])*0.5]
        elif idx == 16:
            pvt = [pvt[3],(pvt[1]+pvt[4])*0.5,(pvt[2]+pvt[5])*0.5]
        elif idx == 17:
            pvt = [pvt[0],pvt[1],(pvt[2]+pvt[5])*0.5]
        elif idx == 18:
            pvt = [(pvt[0]+pvt[3])*0.5,pvt[1],(pvt[2]+pvt[5])*0.5]
        elif idx == 19:
            pvt = [pvt[3],pvt[1],(pvt[2]+pvt[5])*0.5]
        elif idx == 20:
            pvt = [pvt[0],pvt[4],pvt[2]]
        elif idx == 21:
            pvt = [(pvt[0]+pvt[3])*0.5,pvt[4],pvt[2]]
        elif idx == 22:
            pvt = [pvt[3],pvt[4],pvt[2]]
        elif idx == 23:
            pvt = [pvt[0],(pvt[1]+pvt[4])*0.5,pvt[2]]
        elif idx == 24:
            pvt = [(pvt[0]+pvt[3])*0.5,(pvt[1]+pvt[4])*0.5,pvt[2]]
        elif idx == 25:
            pvt = [pvt[3],(pvt[1]+pvt[4])*0.5,pvt[2]]
        elif idx == 26:
            pvt = [pvt[0],pvt[1],pvt[2]]
        elif idx == 27:
            pvt = [(pvt[0]+pvt[3])*0.5,pvt[1],pvt[2]]
        elif idx == 28:
            pvt = [pvt[3],pvt[1],pvt[2]]

        return pvt

    def rnmMtls(self,obj):
        mtls = pmc.ls(pmc.listHistory(obj, ac=1), mat=1)
        if not mtls:
            mtls = pmc.ls(pmc.listHistory(pmc.listConnections(pmc.listRelatives(obj,s=1),d=1)),mat=1)

        for mtl in mtls:
            if mtl not in pmc.ls(dn=1,mat=1,set=1):
                if obj.startswith('S_'):
                    obj = obj.split('S_', 1)[1]
                if len(mtls) == 1:
                    pmc.rename(pmc.listConnections(mtls[0],t='shadingEngine')[0],obj+'_SE')
                    pmc.rename(mtls[0], 'M_' + obj)

                elif len(mtls) > 1:
                    for idx in range(len(mtls)):
                        pmc.rename(pmc.listConnections(mtls[idx],t='shadingEngine')[0],obj+'_SE_%02i'%idx)
                        pmc.rename(mtls[idx], 'M_' + obj + '_%02i' % idx)

    def cmbnTyp(self,objs):
        new = []
        if objs:
            for obj in objs:
                if pmc.objExists(obj):
                    if self.utils_cmbn_RB.isChecked():
                        get = True
                        top = None
                        while get:
                            top = obj
                            obj = pmc.listRelatives(obj, p=1)
                            if obj:
                                obj = obj[0]
                            else:
                                get = False
                        try:
                            tmp = pmc.polyUnite(top,ch=0, muv=1, cp=1,)[0]
                            top = pmc.rename(tmp,top).name()
                        except:
                            pass
                        self.opPivApply([top])
                        new.append(self.opSMrename([top])[0])
                        self.rnmMtls(new[-1])
                    elif self.utils_solo_RB.isChecked():
                        if True:
                            objsw = []
                            get = True
                            top = None
                            while get:
                                if pmc.listRelatives(obj, s=1):
                                    top = obj
                                obj = pmc.listRelatives(obj,p=1)
                                if obj:
                                    obj = obj[0]
                                else:
                                    get = False
                            try:
                                hi = pmc.ls(top,tr=1,o=1,v=1,dag=1)
                                hi.remove(top)
                                objsw = pmc.parent(hi,w=1)
                            except:
                                objsw.append(top)
                            if objsw:
                                if top not in objsw:
                                    objsw.insert(0,top)
                                for obj in objsw:
                                    if pmc.objExists(obj):
                                        self.opPivApply([obj])
                                        new.append(self.opSMrename([obj])[0])
                                        self.rnmMtls(new[-1])
                        else:
                            obj = pmc.parent(obj,w=1)[0].name()
                            self.opPivApply([obj])
                            new.append(self.opSMrename([obj])[0])
                            self.rnmMtls(new[-1])
                    elif self.utils_hrch_RB.isChecked():
                        if True:
                            get = True
                            top = None
                            while get:
                                top = obj
                                obj = pmc.listRelatives(obj,p=1)
                                if obj:
                                    obj = obj[0]
                                else:
                                    get = False
                            self.opPivApply([top])
                            new.append(self.opSMrename([top])[0])
                            self.rnmMtls(new[-1])
                        else:
                            get = True
                            while get:
                                self.opPivApply([obj])
                                new.append(self.opSMrename([obj])[0])
                                self.rnmMtls(new[-1])
                                obj = pmc.listRelatives(new[-1],p=1)
                                if obj:
                                    obj = obj[0]
                                else:
                                    get = False
        return new

    @QtCore.Slot()
    def opLocation(self):
        self.location_LE.setText(QtWidgets.QFileDialog.getExistingDirectory())
        if self.pathExist():
            self.location_LE.setText(self.prjctpath)
        else:
            self.msg(0)

        self.location_PB.setDown(False)

    @QtCore.Slot()
    def opPivApply(self,objs=[],tgl=False):
        if not objs:
            objs = self.selobjs(True)
        idx = self.pivot_CB.currentIndex()

        if objs:
            if tgl:
                self.solopiv_ChB.setChecked(1)
            else:
                self.solopiv_ChB.setChecked(0)
            if objs[0] != '__none_':
                for obj in objs:
                    mv = self.movePivot(obj,idx)
                    pmc.delete(obj,ch=1)
                    pmc.makeIdentity(obj,a=1, t=1, r=1, s=1, n=0, pn=1)
                    pmc.xform(obj,piv=mv,a=1,ws=1,wd=1)

                    if not self.solopiv_ChB.isChecked():
                        pmc.move(obj,[-mv[0],-mv[1],-mv[2]],xyz=1,r=1,ws=1,wd=1)
                        pmc.makeIdentity(obj, a=1, t=1, r=1, s=1, n=0, pn=1)

    @QtCore.Slot()
    def opGround(self):
        objs = self.selobjs(True)

        if objs:
            if objs[0] != '__none_':
                for obj in objs:
                    pos = pmc.exactWorldBoundingBox(obj)
                    pos = pmc.objectCenter(obj)[1]-((pos[4]-pos[1])*0.5)

                    pmc.move(obj, -pos, y=1, r=1, ws=1, wd=1)

    @QtCore.Slot()
    def opSMadd(self,objs=[]):
        if not objs:
            objs = self.selobjs(False)
        compare = []

        if objs:
            if objs[0] != '__none_':
                for item in range(self.sm_LW.count()):
                    compare.append(self.sm_LW.item(item).text())
                for obj in objs:
                    if obj not in compare:
                        self.sm_LW.addItem(obj)

    @QtCore.Slot()
    def opSMrmv(self):
        objs = self.selobjs(False)
        compare = []

        if objs:
            if objs[0] != '__none_':
                for item in range(self.sm_LW.count()):
                    compare.append(self.sm_LW.item(item))
                for obj in objs:
                    for i in range(len(compare)):
                        if obj == compare[i].text():
                            self.sm_LW.takeItem(self.sm_LW.row(compare[i]))
        else:
            self.sm_LW.clear()

    @QtCore.Slot()
    def opSMrename(self,objs=[]):
        new = []
        if not objs:
            objs = self.selobjs(True)

        if objs:
            if objs[0] != '__none_':
                for obj in objs:
                    if not obj.startswith('S_'):
                        new.append(pmc.rename(obj,'S_'+obj.split('|',1)[-1].title()).name())
                    else:
                        new.append(pmc.rename(obj,obj.split('|',1)[-1].title()).name())
        return new

    @QtCore.Slot()
    def opSelect(self):
        objs = self.getItems('sm',False)
        pmc.select(cl=1)

        for obj in objs:
            if pmc.objExists(obj):
                pmc.select(obj,add=1)

    @QtCore.Slot()
    def opExport(self):
        itemnames = self.getItems('sm',False)
        count = self.sm_LW.count()
        objs = []
        scl = 1

        if self.utils_scl_ChB.isChecked():
            scl = 10

        if self.pathExist():
            self.location_LE.setText(self.prjctpath)
        else:
            self.opLocation()

        if self.pathExist():
            if count:
                fldr = self.prjctpath.strip()

                pmc.mel.FBXExportSmoothingGroups(v=1)
                pmc.mel.FBXExportHardEdges(v=0)
                pmc.mel.FBXExportSmoothMesh(v=1)
                pmc.mel.FBXExportTangents(v=1)
                pmc.mel.FBXExportInstances(v=0)
                pmc.mel.FBXExportReferencedAssetsContent(v=0)
                pmc.mel.FBXExportTriangulate(v=0)
                pmc.mel.FBXExportAnimationOnly(v=0)

                pmc.mel.FBXExportCameras(v=0)
                pmc.mel.FBXExportLights(v=0)
                pmc.mel.FBXExportAudio(v=0)
                pmc.mel.FBXExportEmbeddedTextures(v=0)
                pmc.mel.FBXExportIncludeChildren(v=1)
                pmc.mel.FBXExportInputConnections(v=1)

                pmc.mel.FBXExportScaleFactor(scl)
                pmc.mel.FBXExportConvertUnitString(v='cm')

                pmc.mel.FBXExportUpAxis('y')
                pmc.mel.FBXExportGenerateLog(v=0)
                pmc.mel.FBXExportInAscii(v=0)
                pmc.mel.FBXExportFileVersion(v='FBX201800')

                for obj in itemnames:
                    if pmc.objExists(obj):
                        objs.append(obj)

                self.sm_LW.clear()
                objs = self.cmbnTyp(objs)
                self.opSMadd(objs)

                for obj in objs:
                    if pmc.objExists(obj):
                        pmc.select(obj, r=1)
                        pmc.mel.FBXExport(obj, f='{}/{}.fbx'.format(fldr, obj), s=1)
                pmc.select(cl=1)
                self.msg(2)
            else:
                self.msg(1)
        else:
            self.msg(0)

        self.export_PB.setDown(False)


def exportue():
    if pmc.window('exportue', ex=1):
        pmc.deleteUI('exportue')
    win = ExportUE()
    win.show()
