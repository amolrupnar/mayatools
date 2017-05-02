import pymel.core as pm
import maya.mel as mel


class LipSetup(object):
    def __init__(self, face_geo, face_geo_top_node, namespaceName='XXX'):
        """
        export and import only Lip rig part from asp face rig.
        :param face_geo: string (face geometry)
        :param face_geo_top_node: string (top group of your face geometry.)
        :param namespaceName: string (namespace like 'XYZ')
        """
        self.face_geo = pm.PyNode(face_geo)
        self.face_geo_top_node = face_geo_top_node
        self.namespaceName = namespaceName
        self.lipCtrlGrps = ['upperLip3Attach_L', 'upperLip3Attach_R', 'lowerLip3Attach_L', 'lowerLip3Attach_R',
                            'upperLip5Attach_R', 'lowerLip5Attach_R', 'upperLip5Attach_L', 'lowerLip5Attach_L',
                            'Lip6Attach_L', 'Lip6Attach_R', 'lowerLip0Attach_M', 'upperLip0Attach_M']
        self.deleteObjArray = ['FaceGroup', 'Head_M', 'Main', 'faceLid', 'Jaw_M', 'FaceUpperRegion_M',
                               'FaceLowerRegion_M']
        self.controllers = ['upperLip3_L', 'upperLip3_R', 'lowerLip3_L', 'lowerLip3_R', 'Lip6_L', 'Lip6_R',
                            'lowerLip0_M', 'upperLip0_M', 'FKLips_M']
        self.lip_geos = ['LipRegion', 'LipsRegion']

    def exportLipSetup(self):
        # create groups.
        lipControllersGrp = pm.createNode('transform', n='Lip_Controllers')
        clusterSetup = pm.createNode('transform', n='NewClusterSetup')
        pm.parent('LipRegion', 'LipsRegion', 'FKOffsetLips_M', 'LipSetup', 'Brs', 'faceHeadJoint', self.lipCtrlGrps,
                  w=True)
        pm.parent(self.lipCtrlGrps, lipControllersGrp)
        # get all rivets and connect with "lipRegion" geometry.
        # all connected with "curveFromMeshEdge" node type.
        for each in self.lipCtrlGrps:
            allHist = pm.listHistory(each, pdo=True)
            for hist in allHist:
                if hist.nodeType() == 'pointOnCurveInfo':
                    clusterCurve = hist.inputCurve.connections()[0]
                    pm.parent(clusterCurve, clusterSetup)
                    crvFrmMshEdg = hist.inputCurve.connections()[0].create.connections()[0]
                    pm.connectAttr('LipRegionShape.worldMesh[0]', crvFrmMshEdg + '.inputMesh', f=True)

        # create dummy head and main.
        pm.delete('Brs_orientConstraint1', 'FaceAllSet', 'FaceControlSet', 'MainAndHeadScaleMultiplyDivide',
                  self.deleteObjArray, self.face_geo_top_node)
        # Brs scale set to 1.
        pm.setAttr('Brs.sx', 1)
        pm.setAttr('Brs.sy', 1)
        pm.setAttr('Brs.sz', 1)
        # create Hierarchy.
        faceGroup = pm.createNode('transform', n='FaceGroup')
        faceMotionSystem = pm.createNode('transform', n='FaceMotionSystem')
        faceMotionFollowHead = pm.createNode('transform', n='FaceMotionFollowHead')
        controlsSetup = pm.createNode('transform', n='ControlsSetup')
        faceDeformationSystem = pm.createNode('transform', n='FaceDeformationSystem')
        regionDeformation = pm.createNode('transform', n='RegionDeformations')
        pm.parent(faceMotionSystem, faceDeformationSystem, faceGroup)
        pm.parent(faceMotionFollowHead, controlsSetup, clusterSetup, 'LipSetup', faceMotionSystem)
        pm.parent(regionDeformation, 'faceHeadJoint', faceDeformationSystem)
        pm.parent('Brs', lipControllersGrp, controlsSetup)
        pm.parent('FKOffsetLips_M', faceMotionFollowHead)
        pm.parent('LipRegion', 'LipsRegion', regionDeformation)
        clusterSetup.rename('ClusterSetup')
        mel.eval("MLdeleteUnused")

    def importLipSetup(self):
        self._hierarchyChecker()
        # connect all rivet to "self.face_geo" geometry.
        for each in self.lipCtrlGrps:
            allHist = pm.listHistory(each, pdo=True)
            for hist in allHist:
                if hist.nodeType() == 'pointOnCurveInfo':
                    crvFrmMshEdg = hist.inputCurve.connections()[0].create.connections()[0]
                    self.face_geo.worldMesh[0].connect(crvFrmMshEdg.inputMesh, f=True)
        # get existing blendshape if exist.
        blendshapes = []
        allHist = self.face_geo.history(pdo=True)
        for each in allHist:
            if each.nodeType() == 'blendShape':
                blendshapes.append(each)
        # add blendshape.
        if not blendshapes:
            blendNode = pm.blendShape(self.lip_geos, self.face_geo, foc=True, n='BS_' + self.face_geo)[0]
            weightCount = blendNode.listAttr(m=True, k=True)
            for each in weightCount:
                pm.setAttr(each, 1)
        elif len(blendshapes) == 1:
            face_blend = blendshapes[0]
            for each in self.lip_geos:
                weightCount = face_blend.getWeightCount()
                pm.blendShape(face_blend, edit=True, t=(self.face_geo, weightCount + 1, each, 1.0))
                face_blend.setAttr(each, 1)
        else:
            pm.warning('geometry have more than one blenshapes found...')

    def _hierarchyChecker(self):
        groups = ['FaceGroup', 'FaceMotionSystem', 'FaceDeformationSystem', 'FaceMotionFollowHead', 'ControlsSetup',
                  'RegionDeformations']
        existed = []
        notExisted = []
        for each in groups:
            if pm.objExists(each):
                existed.append(each)
            else:
                notExisted.append(each)

        if not notExisted:
            if len(existed) == len(groups):
                # parent all objects in groups.
                pm.parent(self.namespaceName + ':FKOffsetLips_M', 'FaceMotionFollowHead')
                pm.parent(self.namespaceName + ':Brs', self.namespaceName + ':Lip_Controllers', 'ControlsSetup')
                pm.parent(self.namespaceName + ':ClusterSetup', self.namespaceName + ':LipSetup', 'FaceMotionSystem')
                pm.parent(self.namespaceName + ':LipRegion', self.namespaceName + ':LipsRegion', 'RegionDeformations')
                pm.parent(self.namespaceName + ':faceHeadJoint', 'FaceDeformationSystem')
                pm.delete(self.namespaceName + ':FaceGroup')
                self._removeNamespace()
                pm.orientConstraint('Head_M', 'Brs', mo=True)
                ret = True
            else:
                pm.warning('default hierarchy is exist but not proper, please undo step and match hierarchy...'),
                ret = False
        else:
            if len(notExisted) == len(groups):
                pm.parent(self.namespaceName + ':FaceGroup', 'Rig')
                self._removeNamespace()
                pm.orientConstraint('Head_M', 'Brs', mo=True)
                pm.orientConstraint('Head_M', 'FaceMotionFollowHead', mo=True)
                ret = True
            else:
                pm.warning('default hierarchy is exist but not proper, please undo step and match hierarchy...'),
                ret = False
        if ret:
            if pm.objExists('Main'):
                pm.connectAttr('Main.s', 'Brs.s', f=True)
            else:
                pm.connectAttr('Main_CTRL.s', 'Brs.s', f=True)
            for each in self.controllers:
                pm.rename(each, each + '_CTRL')
            pm.setAttr('FaceDeformationSystem.v', 0)
            pm.setAttr('FaceDeformationSystem.v', l=True)
            return True
        else:
            return False

    def _removeNamespace(self):
        allNameSpaces = pm.listNamespaces()
        for each in allNameSpaces:
            if each == ':' + self.namespaceName:
                pm.namespace(rm=each[1:], mnr=True)
