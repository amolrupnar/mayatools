import maya.OpenMaya as om
import pymel.core as pm


class Actor(object):
    def __init__(self, name, health=100, strength=100):
        self.name = name
        self.health = health
        self.strength = strength


class Warrior(Actor):
    def __init__(self, name):
        super(Warrior, self).__init__(name)


a = Warrior('Amol')
print a.health


def test():
    # arguments
    argData = om.MArgParser(self.syntax(), args)
    index = argData.flagArgumentInt(kFroIndexF, 0)  # currently selected vertex (index)
    range = argData.flagArgumentDouble(kFroRangeF, 0)  # max distance to find a vertex

    # get the active selection
    sel = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(sel)
    list = om.MItSelectionList(sel, om.MFn.kMesh)

    # get mesh
    mesh = None
    dagPath = om.MDagPath()
    list.getDagPath(dagPath)
    mesh = om.MFnMesh(dagPath)

    # define variables to find the vertex
    nb = mesh.numVertices()
    point = om.MPoint()  # target point

    print ("There is " + str(nb) + " vertices in the mesh")

    foundVtx = 0
    closestVert = 0
    minLength = None
    pos = om.MPoint()

    # search for the nearest vertex
    count = 0
    while count < nb:
        # ignore vertex already selected by user
        if count != index:
            # get point by its index
            mesh.getPoint(count, point, om.MSpace.kWorld)
            dist = pos.distanceTo(point)

            # if the vtx is the closest, save it (only if we are under the user range)
            if dist <= range:
                if minLength is None or dist < minLength:
                    foundVtx = 1
                    minLength = dist
                    closestVert = count

        count += 1

    if count:
        print ("Vertex found is " + str(closestVert) + "")

    # send the closest vertex to the user
    resultArray = om.MDoubleArray()
    resultArray.append(foundVtx)
    resultArray.append(closestVert)
    resultArray.append(point.x)
    resultArray.append(point.y)
    resultArray.append(point.z)

    self.clearResult()
    self.setResult(resultArray)


def sphereTest():
    geo = pm.PyNode('pSphere1')
    pos = pm.PyNode('locator1').getRotatePivot(space='world')

    nodeDagPath = om.MObject()
    try:
        selectionList = om.MSelectionList()
        selectionList.add(geo.name())
        nodeDagPath = om.MDagPath()
        selectionList.getDagPath(0, nodeDagPath)
    except:
        pm.warning('om.MDagPath() failed on %s' % geo.name())

    mfnMesh = om.MFnMesh(nodeDagPath)
    pointA = om.MPoint(pos.x, pos.y, pos.z)
    pointB = om.MPoint()
    space = om.MSpace.kWorld

    util = om.MScriptUtil()
    util.createFromInt(0)
    idPointer = util.asIntPtr()

    mfnMesh.getClosestPoint(pointA, pointB, space, idPointer)
    idx = om.MScriptUtil(idPointer).asInt()

    faceVerts = [geo.vtx[i] for i in geo.f[idx].getVertices()]
    closestVertex = None
    minLength = None
    for v in faceVerts:
        thisLength = (pos - v.getPosition(space='world')).length()
        if minLength is None or thisLength < minLength:
            minLength = thisLength
            closestVertex = v
    pm.select(closestVertex)
