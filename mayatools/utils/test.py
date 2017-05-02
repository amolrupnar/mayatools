from maya import cmds as cmds


def fkchain(sel='joint1'):
    newChain = []
    multiChild = []
    parent = sel
    newChain.append(parent)
    while not multiChild:
        chain = cmds.listRelatives(parent, type='joint')
        if chain:
            if len(chain) == 1:
                newChain.append(chain[0])
                parent = chain[0]
            else:
                multiChild = cmds.listRelatives(parent, c=True, typ='joint')
        else:
            break
    addFk(newChain)
    for each in multiChild:
        fkchain(sel=each)
        # return newChain, multiChild


def addFk(chain):
    controller = []
    for i in range(len(chain)):
        if i != len(chain) - 1:
            cmds.select(cl=True)
            offGrp = cmds.joint(n='FKOffset' + chain[i])
            grp = cmds.group(n='FKExtra' + chain[i], em=True)
            ctrl = cmds.circle(ch=False, n='FK' + chain[i], nr=[1, 0, 0])
            cmds.select(cl=True)
            fkxGrp = cmds.joint(n='FKX' + chain[i])
            cmds.parent(ctrl[0], grp)
            cmds.parent(fkxGrp, ctrl[0])
            cmds.parent(grp, offGrp)
            cmds.delete(cmds.parentConstraint(chain[i], offGrp))
            cmds.makeIdentity(offGrp, a=True, t=1, r=1, s=1, n=0, pn=1)
            cmds.parentConstraint(fkxGrp, chain[i])
            controller.append(fkxGrp)
            if i != 0:
                cmds.parent(offGrp, controller[i - 1])
        else:
            cmds.select(cl=True)
            fkxGrp = cmds.joint(n='FKX' + chain[i])
            cmds.delete(cmds.parentConstraint(chain[i], fkxGrp))
            cmds.parent(fkxGrp, controller[i - 1])
            cmds.parentConstraint(fkxGrp, chain[i])
