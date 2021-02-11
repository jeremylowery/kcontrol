__all__ = ['CompositeControl']

from kcontrol.util import UniqueList
from kcontrol.errors import NotFoundError
from kcontrol.Controls.Control import Control
from kcontrol.Controls.Label import Label

class CompositeControl(Control):
    """Control that contains child controls

    The composite control acts as a container for other controls
    Many times the composite control will map to a larger "element" on the
    page. 

    Composite controls propigate rendering, resources and data sources to
    thier child controls. The resources of all child controls dynamically maps
    to the resources of the composite control.
    """

    _ctrls = []                # Child controls
    _ctrls_built = False
    _ctrls_unique = True
    
    def __init__(self, *a, **k):
        Control.__init__(self, *a, **k)
        self._ctrls = []
    
    def matchUpResource(self, res_pat):
        res = Control.matchUpResource(self, res_pat)
        for ctrl in self._ctrls:
            res = res + ctrl.matchUpResource(res_pat)
        return res
    
    def matchResource(self, res_pat):
        res = Control.matchResource(self, res_pat)
        for ctrl in self._ctrls:
            res = res + ctrl.matchUpResource(res_pat)
        return filter(lambda r: r in self.propResources() or r in self._resources, UniqueList(res))
        
    def getUpResource(self, res_type, idx=1):
        """ Retrieve a resource propigated up to control """
        behavior = self.resourceBehaviors().get(res_type, 'single')
        if behavior == 'single':
            try:
                return self._resourcesUp[res_type], idx
            except KeyError:
                for ctrl in self._ctrls:
                    try:
                        return ctrl.getUpResource(res_type, idx+1)
                    except NotFoundError:
                        pass
                raise NotFoundError("No resource for resource type '%s'" % res_type)
        elif behavior == 'join':
            try:
                res = self._resourcesUp[res_type]
            except KeyError:
                res = []
            pres = []
            for ctrl in self._ctrls:
                try:
                    pres = pres + ctrl.getUpResource(res_type)[0]
                except NotFoundError:
                    pass
            if not pres and not res:
                raise NotFoundError("No resource for resource type '%s'" % res_type)
            return UniqueList(res + pres), idx

    def getResource(self, res_type):
        """ Retrieve a resource
        
        This method takes into consideration resources that have been pushed up
        
        """
        if not self.acceptAllResources and res_type not in self.propResources():
            try:
                return self._resources[res_type]
            except KeyError:
                raise NotFoundError("No resource for resource type '%s'" % res_type)
        
        behavior = self.resourceBehaviors().get(res_type, 'single')
        if behavior == 'single':
            if res_type in self._resources:
                return self._resources[res_type]
            if self._parent:
                try:
                    return self._parent.getDownResource(res_type)[0]
                except NotFoundError:
                    pass
            for ctrl in self._ctrls:
                try:
                    return ctrl.getUpResource(res_type)[0]
                except NotFoundError:
                    pass
            raise NotFoundError("No resource for resource type '%s'" % res_type)
        elif behavior == 'join':
            res = self._resources.get(res_type, [])
            if self._parent:
                try:
                    pres, idx = self._parent.getDownResource(res_type)
                except NotFoundError:
                    pres = []
            else:
                pres = []
            for ctrl in self._ctrls:
                try:
                    pres = pres + ctrl.getUpResource(res_type)[0]
                except NotFoundError:
                    continue
            
            if not res and not pres:
                raise NotFoundError("No resource for resource type '%s'" % res_type)
            else:
                return UniqueList(res + pres)

    def preRender(self):
        Control.preRender(self)
        if not self._ctrls_built:
            self.buildControls()
        for ctrl in self._ctrls:
            ctrl.preRender()

    def buildControls(self):
        self._ctrls_built = True
        
    def addControl(self, ctrl):
        assert self is not ctrl, "Cannot add control to itself"
        assert ctrl.name
        try:
            self.controlByName(ctrl.name)
            if self._ctrls_unique:
                raise DuplicateError("A control with the name '%s' is " + \
                    "already registered with the composite control %s" % (
                    ctrl.name, self.name))
        except IndexError:
            pass
        if ctrl in self._ctrls:
            raise DuplicateError(("A control with the name '%s' is already " +
                "registered with the composite control %s") % (ctrl.name, self.name))
        self._ctrls.append(ctrl)
        ctrl._parent = self

    def addControls(self, ctrls):
        for ctrl in ctrls:
            self.addControl(ctrl)
            
    def controlByName(self, name):
        for ctrl in self._ctrls:
            if ctrl.name == name:
                return ctrl
        raise IndexError("Control with name '%s' not found" % name)
        
    def drawControls(self):
        tar = []
        for ctrl in self._ctrls:
            tar.append(ctrl.draw())
        return '\n\n'.join(tar)
    
    def drawHeader(self):
        return ''
    
    def drawFooter(self):
        return ''
        
    def draw(self):
        return "%s\n%s\n%s" % (
            self.drawHeader(),
            self.drawControls(),
            self.drawFooter()
        )
        
    def awake(self, trans=None):
        Control.awake(self, trans)
        for ctrl in self._ctrls:
            ctrl.awake(trans)
            
    def sleep(self, trans=None):
        Control.sleep(self, trans)
        for ctrl in self._ctrls:
            ctrl.sleep(trans)
        self._ctrls = []
        self._ctrls_built = False

    def __dump__(self):
        buf = Control.__repr__(self)
        buf = buf + 'Child Controls\n' + '-'*80 + '\n'
        for ctrl in self._ctrls:
            buf = buf + '\t' + ctrl.__repr__() + '\n'
        return buf

class DuplicateError(Exception):
    pass
