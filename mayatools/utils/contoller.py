import maya.cmds as cmds


class Control():
    def __init__(self, name='test', parentSnap=False, target=False):
        self.name = name + '_ctl'
        self.parentSnap = parentSnap
        self.target = target

    def circleCnt(self):
        cmds.select(cl=True)
        cnt = cmds.circle(n=self.name, nr=[1, 0, 0], ch=False)
        grp = cmds.createNode('transform', n=self.name + '_grp')
        cmds.parent(cnt[0], grp)
        if self.parentSnap:
            self._snap(self.target, cnt)
        self.C = cnt
        self.O = grp

    def _snap(self, src, trg):
        cmds.delete(cmds.parentConstraint(src, trg))
