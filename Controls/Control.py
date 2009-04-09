# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

__all__ = ["Control", "ResWatcher"]

import os
import logging
import string
import fnmatch
import urllib

import kcontrol.ds
from kcontrol.util import UniqueList
from kcontrol.errors import NotFoundError
from kcontrol.res import ResWatcher

import kcontrol.config as cfg

log = logging.getLogger("kcontrol")


class Control(object):
    """

    This is a GOD OBJECT!!! RUN AWAY!!!!

    The Control class is the base class for all of the other controls in the
    system. Every control has a concept of a 'name' and a caption. A caption
    is akin to a label while a name is akin to a unique identifier. These
    two attributes are nearly always assigned upon the creation of a control
    in the control's constructor.

    Controls also have the concept of a "data source." The data source, which
    is stored in the "ds" property of the control, Is used to assign a value
    to the control. The Data Source (which much derive from the abstract
    DataSource class. See the Documentation on the DataSource class for more
    information about data sources.

    Because Control's are used in the stateless model that is the web. A
    control really doesn't have a "value." However, a value property exists
    which internally queries the data source for a value associated with the
    name of the control.

    Control's also have the concept of a default value. A control's default
    value is used if the data source raises a KeyError when the value is
    searched for.

    Each control can be 'rendered' which means that a Html string is generated
    to represent the control. The render() method is called on the control.
    A 'value' for the control can be assigned to the control by passing it
    as a parameter to the render method. the value can also be assigned using
    the assign() method.

    To implement a new control, override the draw() method, which actually
    creates the Html output.

    It is legal for controls to take different numbers of parameters for their
    constructor (although all controls should accept a 'name' and 'caption' as
    the first two parameters). Override preRender is also useful for doing
    calculations before an actual render occurs. This is preferred to putting
    logic inside the draw method, which should only be used for Html output.

    Controls also support resource information. To declare that a control
    requires a resource, override the buildDeps() method and use the global
    add_res function. Currently, only js and css resources are widely used,
    though other uses are available for those that need it.

    Controls may also specify resources that the control depends on. These
    resources propigate up the control hierarchy and are used at the top
    control.  Currently css and javascript resources are used.

    Generic Resource/Event Propigation
    ----------------------------
    Many times, controls need to pass values and references to each other. Due
    to the complex nature of HTML, managing html attributes and properties on
    a case by case basis can be error prone and time consuming.

    Some resources propigate up, while others propigate down. Below are some
    common examples:

    - Javascript file references propigate up (A DatePicker's javascript
      dependancies are handled by the page control)
    - CSS file references propigate up
    - CSS classes propigate down (A table class will propigate down to the
      table rows)
    - select javascript events propigate up (onload on a control should go in
      the body's on load)
    - other javascript events propigate down (a form that forces validation
      should propigate onblur events down to the form controls).

    The    mechanism works the following way.

    - A control declares what resource types it handles by using the getResource
      method
    - A control can propigate a resource up or down, using the pushResourceUp
      and pushResourceDown methods

    Resource declarations and propigation should be done in the buildResources()
    method.

    Mechanisms are provided to automatically handle html attributes and
    javascript events that propigate up and down. The htmlAttrs attribute of a
    control dynamically includes attributes that come from up or down.

    Resource Conflicts
    ==================

    Sometimes a resource may be defined by different controls in a control
    chain.  The control that is closest to the consumer control wins. Resources
    defined by the consumer control always win. In some cases, like Javascript
    events different resources should be merged together. These are presented
    as lists of javascript events.
    """

    showCaption = False             # Should the caption of the control be shown?
                                            # Control Containers should honor this attribute
                                            # when rendering.

    visible = True                        # Is the Control "visible?" This mainly applies
                                            # to control containers that render rows or other
                                            # Html framework for controls. If the control is
                                            # not visible, control container should just output
                                            # the control and not bother with 'framework' for
                                            # appearances sake. Examples of controls that are
                                            # not visible include hidden form elements and
                                            # Html elements with a hidden css property

    useValue = True

    acceptAllResources = False        # Should this control accept all resources
                                                # that are propigated to it? The default
                                                # is no and this should stay false except
                                                # in very specific circumstances

    # HTML Attributes that should not be quoted for special characters. These
    # are mainly Javascript event handlers
    quoteExceptions = [
        "onblur",
        "onclick",
        "onfocus",
        "onchange",
        "onsubmit",
        "onload",
        "onunload",
        "href",
        "onkeydown",
        "onkeypress",
        "onkeyup"
    ]

    _name = ""
    _caption = ""
    _ds = None
    _parent = None
    _ctrlCount = 0
    _defaultValue = ""
    _defaultDS = None
    _relpath = ""

    _mode = None
    _default_mode = "form"

    _resource_watchers = [ResWatcher]

    def __init__(self, name=None, caption="", pos=None, **kwd):
        """ Construct a control

        All arguments are optional and need not be defined. If no name is given
        then a generic ControlClass# name is assigned to the control
        (i.e. ListBox2). Captions are supported by many controls but not
        neccessarily required.

        env is used to lookup path information for generating links and references
        to other files on the server.

        As a convinence, an arbitrary number of keyword arguments can be given,
        which assign the values to attributes on the control. This is very
        useful for mechanisms like PSP.
        """
        if not name:
            self.__class__._ctrlCount = self.__class__._ctrlCount + 1
            name = "%s%s" % (self.__class__.__name__, self.__class__._ctrlCount)

        self.name = name
        if caption:
            self.caption = caption

        self.pos = pos
        self._jsEvents = {}
        self._resources = {}        # Resources on self, overriding all others
        self._resourcesUp = {}        # Resources that propigate up the chain
        self._resourcesDown = {}    # Resources that propigate down the chain
        for k, v in kwd.items():
            if k in ("onchange", "onfocus",
                     "onblur", "onkeydown", "onkeyup", "onclick"):
                self.addJSEvent(k, v)
            elif k in ("id", "class_", "title", 
                       "style", "disabled", "autocomplete"):
                self.addHtmlAttr(k, v)
            else:
                setattr(self, k, v)

    ## Class Methods ##
    def setDefaultDS(cls, ds):
        """ The Default data source is useful for python server pages where
            adding child control's to a parent control is cumbersome.
            the default data source mechanism can be substituted for simple
            pages but lacks all of the flexibility and power of the control
            hierarchy approach
        """
        Control._defaultDS = ds
    setDefaultDS = classmethod(setDefaultDS)

    ## Generic Attributes ##
    _doc_name = """
        The name of the control. This should usually
        be global inside of a single page though
        no explicit provisions exist to insure this.
        The name can be meaningless for some controls
        like certain composite controls.
    """
    def _get_name(self):
        return self._name
    def _set_name(self, name):
        self._name = name
    name = property(_get_name, _set_name, doc=_doc_name)

    _doc_caption = """
        A Textual caption associated with a control
        The caption is usually used as an external
        textual reference to the control. Many times,
    """
    def _get_caption(self):
        if hasattr(self, 'getCaption'):
            return self.getCaption()
        return self._caption
    def _set_caption(self, caption):
        self._caption = caption
    caption = property(_get_caption, _set_caption, doc=_doc_caption)

    _doc_value = """
        Retrieves the value of the control. This actually queries the data
        source of the control, based off the name of the control.

        If the data source is a list, a pos can also be given to the
        constructor to specify which element.
    """
    def _get_value(self):
        if not self.useValue or self.ds is None:
            return ""
        try:
            value = self.ds[self.name]
        except KeyError:
            value = self.defaultValue
        if isinstance(value, (list, tuple)) and self.pos is not None:
            if self.pos >= len(value):
                return None
            else:
                return value[self.pos]
        else:
            return value
            

    def _set_value(self, value):
        log.debug("Setting value %s for %s", value, self.name)
        self._ds = kcontrol.ds.SingleValueDS(value)
    value = property(_get_value, _set_value, doc=_doc_value)

    _doc_ds = """
        The data source that the control is associated with
        The data source is used to query for the "value"
        that a control recieves.
    """
    def _get_ds(self):
        if self._ds is not None:
            log.debug("Giving assigned DS %s for %s", self._ds, self.name)
            return self._ds
        elif self._parent:
            return self._parent.ds
        elif self._defaultDS:
            return self._defaultDS
        else:
            try:
                return kcontrol.ds.store
            except:
                raise ValueError, dir(kcontrol.ds)

    def _set_ds(self, ds):
        log.debug("setting DS for %s to %s", self.name, ds)
        if type(ds) is str:
            ds = kcontrol.ds.SingleValueDS(ds)

        self._ds = ds
    ds = property(_get_ds, _set_ds, doc=_doc_ds)

    _doc_defaultValue = """
        The default value is a value to assign to the control
        if the data source does not provide  a value
    """
    def _get_defaultValue(self):
        return self._defaultValue
    def _set_defaultValue(self, value):
        self._defaultValue = value
    defaultValue = property(_get_defaultValue, _set_defaultValue, doc=_doc_defaultValue)

    def _get_parent(self):
        return self._parent
    def _set_parent(self, parent):
        self._parent = parent
    parent = property(_get_parent, _set_parent)

    ## Resource Management ##
    def resourceBehaviors(self):
        """ Resource behaviors are dictionaries that define how resource
        conflicts should be handled. The following behaviors are available:
         - join (the Resources will be defined as a list)
         - single ( a single value )

        The default is 'single' so those do not have to be explicitly given
        unless overridden.
        """
        return {
            "inline_js" : "join",
            "js" : "join",
            "inline_css" : "join",
            "css" : "join",
            "js_onload" : "join",
            "js_onblur" : "join",
            "js_onchange" : "join",
            "js_onfocus" : "join",
            "js_onsubmit" : "join",
            "js_onclick" : "join",
            "js_onkeypress" : "join",
            "js_onkeyup" : "join",
            "js_onkeydown" : "join",
            "js_onclose" : "join"
        }

    def _addResourceToChain(self, chain, res_type, res):
        """ Adds the resource to the chain taking into account the
            resource behavior.
        """
        behavior = self.resourceBehaviors().get(res_type, 'single')
        if behavior == "join":
            try:
                chain[res_type].append(res)
            except KeyError:
                chain[res_type] = [res]
        elif behavior == "single":
                chain[res_type] = res
        else:
            raise ValueError, "Invalid resource behavior %r" % behavior

        for c in self._resource_watchers:
            c(res_type, self.relurl(res))

    def pushResourceUp(self, res_type, res):
        """ Push the given resource up the resource chain """
        self._addResourceToChain(self._resourcesUp, res_type, res)

    def pushResourceDown(self, res_type, res):
        """ Push the given resource down the resource chain """
        self._addResourceToChain(self._resourcesDown, res_type, res)

    def matchUpResource(self, res_pat):
        return fnmatch.filter(self._resourcesUp, res_pat)

    def matchDownResource(self, res_pat):
        res = fnmatch.filter(self._resourcesDown, res_pat)
        if self._parent:
            res = res + self._parent.matchDownResource(res_pat)
        return res

    def matchResource(self, res_pat):
        """ Find matches for a given resource pattern. Current fnmatch
        (glob-style) matching is supported.
        """
        res = fnmatch.filter(self._resources.keys(), res_pat)

        if self._parent:
            res = res + self._parent.matchDownResource(res_pat)
        return filter(lambda r: r in self.propResources() or r in self._resources, UniqueList(res))

    def getDownResource(self, res_type, idx=1):
        """ Retrieve a resource propigated down to  control """
        behavior = self.resourceBehaviors().get(res_type, 'single')
        if behavior == 'single':
            try:
                return self._resourcesDown[res_type], idx
            except KeyError:
                if self._parent:
                    return self._parent.getDownResource(res_type, idx+1)
                raise NotFoundError, "No resource for resource type '%s'" % res_type
        elif behavior == 'join':
            try:
                res = self._resourcesDown[res_type]
            except KeyError:
                res = []
            if self._parent:
                try:
                    pres = self._parent.getDownResource(res_type)[0]
                except NotFoundError:
                    pres = []
            else:
                pres = []
            if not pres and not res:
                raise NotFoundError, "No resource for resource type '%s'" % res_type
            try:
                return UniqueList(res + pres), idx
            except TypeError:
                raise str(res) + str(pres)

    def getUpResource(self, res_type, idx=1):
        try:
            return self._resourcesUp[res_type], idx
        except KeyError:
            raise NotFoundError, "No resource for resource type '%s'" % res_type

    def propResources(self):
        """ These are resources that the control will accept from other
        controls as being propigated. If the control should accept all
        controls, set the acceptAllResources attribute to True
        """
        return [
            'inline_js',
            'js',
            'inline_css',
            'css',
            'js_onblur',
            'js_onchange',
            'js_onfocus',
            'html_class'
        ]

    def getResource(self, res_type):
        """ Retrieve a resource

        This method takes into consideration resources that have been pushed up

        """
        if not self.acceptAllResources and res_type not in self.propResources():
            try:
                return self._resources[res_type]
            except KeyError:
                raise NotFoundError, "No resource for resource type '%s'" % res_type
        behavior = self.resourceBehaviors().get(res_type, 'single')
        if behavior == 'single':
            if res_type in self._resources:
                return self._resources[res_type]
            if self._parent:
                try:
                    return self._parent.getDownResource(res_type)[0]
                except NotFoundError:
                    pass
            raise NotFoundError, "No resource for resource type '%s'" % res_type
        elif behavior == 'join':
            res = self._resources.get(res_type, [])
            if self._parent:
                try:
                    pres, idx = self._parent.getDownResource(res_type)
                except NotFoundError:
                    pres = []
            else:
                pres = []
            if not res and not pres:
                raise NotFoundError, "No resource for resource type '%s'" % res_type
            else:
                return UniqueList(res + pres)

    _doc_resources = """
        Resources are javascript and css files that propigate up the control
        chain.  If a control has no parent, then the resources are assigned to
        it.
    """
    def _get_resources(self):
        nres = {}
        for k in self.matchResource('*'):
            nres[k] = self.getResource(k)
        return nres
    resources = property(_get_resources, doc=_doc_resources)

    _doc_htmlAttrs = """
        Html Attributes that are assigned to 'this' element. This may not be
        used for complex composite controls, and if so then the attributes
        should be assigned to the logical Html element.
    """
    def _get_htmlAttrs(self):
        res = self.matchResource("html_*")
        d = {}
        for r in res:
            d[r[5:]] = self.getResource(r)
        return d
    htmlAttrs = property(_get_htmlAttrs, doc=_doc_htmlAttrs)

    _doc_jsEvents = """
        Javascript events that occur on the element.
    """
    def _get_jsEvents(self):
        res = self.matchResource("js_*")
        d = {}
        for r in res:
            d[r] = self.getResource(r)
        return d
    jsEvents = property(_get_jsEvents, doc=_doc_jsEvents)

    def buildResources(self):
        """Override this method and place addResource method calls to add
           resources to the given control. """
        self.addResource('js', "js/kcontrol.js")

    def addResource(self, res_type, path):
        """Add a resource to the control

        Duplicate resources are ok beacuse they are filtered out. The most
        commonly used resource types now are js and css. """
        behavior = self.resourceBehaviors().get(res_type, 'single')
        if behavior == 'single':
            self._resources[res_type] = path
        elif behavior == 'join':
            try:
                self._resources[res_type].append(path)
            except KeyError:
                self._resources[res_type] = [path]

    def addResources(self, reses):
        map(lambda res: self.addResource(*res), reses)

    ## HTML Attribute Handling ##

    def addJSEvent(self, event, value):
        self.addResource("js_%s" % event, value)

    def addHtmlAttr(self, attr, value, push=None):
        self.addResource("html_%s" % attr, value)
        if push == 'up':
            self.pushResourceUp("html_%s" % attr, value)
        elif push == 'down':
            self.pushResourceDown("html_%s" % attr, value)

    def drawJSEvents(self):
        events = {}
        for n, v in self.jsEvents.items():
            if len(v) == 1:
                events[n[3:]] = v[0]
            else:
                events[n[3:]] = "{%s}" % ";".join(v)
        return self.joinHtmlAttrs(events)

    def drawHtmlAttrs(self):
        return self.joinHtmlAttrs(self.htmlAttrs)

    def joinHtmlAttrs(self, attrs):
        """Returns a string containing the the Html attributes given in the
        attrs parameter. If certain entries in attrs are javascript event
        handlers then the contents are not html encoded.
        """
        tar = []
        for k, v in attrs.items():
            if k not in self.quoteExceptions:
                v = self.htmlEncode(v)
            if k[-1] == '_':
                k = k[:-1]
            tar.append('%s="%s"' % (k, v))
        return "\n ".join(tar)

    ## Rendering Methods ##
    def preRender(self):
        """The pre-rendering step is executed right before the control is
        drawn.  In cases where certain calcuations must occur before a control
        is invoked, and after the control is created, those calculations should
        be placed in this method.
        """
        self.buildResources()

    def render(self, ds=None):
        """Rendering a control generates the output of the control. Inherited
        controls should not override this method unless the way the control
        functions is dramatically changed. Use draw() and preRender()
        """
        if ds is not None:
            self.ds = ds
        self.preRender()
        return self.draw()

    def draw(self):
        """Override this method to control how the control is drawn in Html.
        Nearly all controls will override this method, either directly or by
        the overriding of parent controls.
        """
        return self.value

    ## WebKit awake/sleep cycle helpers ##
    def awake(self, trans=None):
        return

    def sleep(self, trans=None):
        self._defaultDS = None
        self._resources = {}

    _doc_mode = """ Sets the default property to be used when overiding
        the __str__ method (representing the instance as a str)
        mode may be set to: base, form, html, view
        """
    def _get_mode(self):
        if not self._mode:
            try:
                self._mode = kcontrol.store['mode']
            except KeyError:
                return self._default_mode
        return self._mode
    
    def _set_mode(self, mode):
        try:
            getattr(self, mode)
        except AttributeError:
            raise AttributeError, "Control has no such mode: %s" % mode
        else:
            self._mode = mode
    mode = property(_get_mode, _set_mode, doc=_doc_mode)

    @property
    def HTML_ENCODE(self):
        """ Returns html encoded value
        """
        return self.htmlEncode(self.value)

    @property
    def HTML(self):
        """ Returns the html element as it would be displayed on a form.
        """
        return self.render()

    @property
    def VIEW(self):
        """ Returns the str rep of the value.
        This may be overriden to do formatting for print views of the data.
        """
        if not self.value:
            return ''
        return str(self.value)
    
    @property
    def _BASE(self):
        """ Returns the html view of the base rep of the value, used for 
            the kcontrol server examples of these controls
        """
        import cgi
        return cgi.escape('%s %s' % (type(self.BASE), self.value))

    @property
    def _HTML_SHOW(self):
        """ Returns the html to be displayed in a browser, used for 
            the kcontrol server examples of these controls
        """
        import cgi
        return cgi.escape(self.render())

        
    @property
    def BASE(self):
        """ Returns the cononicle base representation of the value.

            i.e. would return a datetime.datetime for a DateControl
        """
        return self.value
    
    ## Behavioral Overrides ##
    def __str__(self):
        try:
            attr = getattr(self, self.mode)
        except AttributeError:
            return self.render()
        return attr

    def __dump__(self):
        return """
Control: %s
Type: %s
Caption: %s
Value: "%s"
DataSource: %s (%s)
    """ % (self.name, self.__class__.__name__, self.caption, self.value, self.ds, self._ds)

    ## Convinence Methods ##
    def htmlEncode(self, s):
        if not s:
            return ''
        s = str(s)
        codes = [
            ['&', '&amp;'],
            ['<', '&lt;'],
            ['>', '&gt;'],
            ['"', '&quot;']
        ]
        for code in codes:
            s = string.replace(s, code[0], code[1])
        return s

    def htmlDecode(self, s):
        s = str(s)
        codes = [
            ['&', '&amp;'],
            ['<', '&lt;'],
            ['>', '&gt;'],
            ['"', '&quot;']
        ]
        for code in codes:
            s = string.replace(s, code[1], code[0])
        return s

    def urlEncode(self, s):
        return urllib.urlencode(str(s))

    def urlDecode(self, s):
        return Funcs.urlDecode(str(s))

    def relurl(self, path=''):
        return os.path.join(cfg.get('kcontrol_url', ''), self._relpath, path)

    def contextUrl(self, path=''):
        return os.path.join(cfg.get('kcontrol_url', ''), path)
