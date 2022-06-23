#!/usr/bin/env python
""" Server startup routine
Example ./sa_server.py -a cps_ar/

"""
import os
import html
import optparse
import decimal
import datetime
import logging
import cherrypy
import kg.procutils
import kg.web_dispatch
import kg.static_dispatch
import kg.template
import kcontrol
from .url import res
mount = kg.web_dispatch.Mounter()

# Mako Template interface
from mako.template import Template

config = {
    'global' : {
        'server.shutdown_timeout' : 0,    # See http://www.cherrypy.org/ticket/691
        'server.pid_file' : '/tmp/cps.pid',
        'engine.autoreload_on' : True,
        'server.socket_port' : 8011,
        'log.error_file' : 'error.log'
         },
    '/': {
        'request.dispatch' : kg.web_dispatch.Dispatcher(),
        'tools.sessions.on' : True,
        'kg.auto_template.on' : True,
        'kg.auto_template.compile_tmpl_dir' : '/tmp/_tc',
        'kg.unrepr_params.on' : True,
        'kg.auto_decode.on'   : True,
        # kcontrol config
        'kcontrol.time.format' : 'standard', 
        'kcontrol.date.format' : 'american',
        'kcontrol.name.format' : '%T %F %M %L %S'
        }
}

def mytype(kcon):
    return html.escape(str(type(kcon.BASE)))

def code(s):
    return html.escape(str(s))

tmpl = Template("""
<% import kcontrol %>
<% kcontrol.store.update(ctx) %>
<% kcontrol.store['mode'] = 'HTML' %>
<html>
<head>
    <title>kcontrol demo</title>

    <script language='javascript' type='text/javascript' src='/kcontrol/js/zcom.js'></script>
    <link rel='stylesheet' type='text/css' href='/kcontrol/DatePicker/css/calendar.css' />
    <script language='JavaScript' type='text/javascript' src='/kcontrol/DatePicker/js/calendar.js'></script>
    <script language='JavaScript' type='text/javascript' src='/kcontrol/DatePicker/js/lang/calendar-en.js'></script>
    <script language='JavaScript' type='text/javascript' src='/kcontrol/DatePicker/js/calendar-setup.js'></script>
    <script language='JavaScript' type='text/javascript' src='/kcontrol/Currency/js/currency_control.js'></script>
    <script language='JavaScript' type='text/javascript' src='/kcontrol/Number/js/number_control.js'></script>
    <script language='JavaScript' type='text/javascript' src='/kcontrol/Phone/js/phone_control.js'></script>

    <script language='JavaScript' type='text/javascript' src='/kcontrol/SSN/js/ssn_control.js'></script>
    <script language='JavaScript' type='text/javascript' src='/kcontrol/NameTextBox/js/name_ctrl.js'></script>
    <script language='javascript' type='text/javascript' src='/kcontrol/TimePicker/js/timepicker.js'></script>
<style type='text/css'>
BODY {
    background-color:#e9e3de;
    margin: 20px;
}
INPUT:focus, INPUT.sffocus,
TEXTAREA:focus, TEXTAREA.sffocus,
SELECT:focus, SELECT.sffocus {
	background-color: #FFFFCC;
    border: 1px solid #CCC;
}
INPUT[type=text], TEXTAREA {
    border: 1px solid #CCC;
}
H1 {
    text-align:center;
    color: #333;
}   
DIV.kcontrol {
    border-top: 1px solid #AAA;
    border-left: 1px solid #AAA;
    border-right: 1px solid #AAA;
    border-bottom: 1px solid #AAA;
    width: 100%;
}
DIV.kcontrol-s {
    border-top: 1px solid #000;
    border-left: 1px solid #000;
    border-right: 1px solid #000;
    border-bottom: 1px solid #000;
    background: #FFF;
    width: 100%;
}
TABLE.kcontrol {
    border: 1px solid #000;
}
TABLE.kcontrol TH {
    background-color: #2e2f2e;
    color: #02c0fa;
    padding: 4px;
}
TABLE.kcontrol TD {
    padding: 4px;
    border-left: 1px solid #DDD;
    border-bottom: 1px solid #CCC;
    font-family: verdana;
}
TABLE.kcontrol TD.mako_rep {
    background: #CCEEFF;
    padding: 4px;
    border-left: 1px solid #DDD;
    border-bottom: 1px solid #CCC;
    font-size: 12px;
    font-family: arial;
    margin-bottom: 20px;
}
TABLE.kcontrol TD.example {
    background: #FFFFE9;
    padding: 4px;
    border-left: 1px solid #DDD;
    border-bottom: 1px solid #444;
    font-size: 12px;
    font-family: arial;
    margin-bottom: 20px;
}
</style>
</head>
<body>

<div class='kcontrol' align='center'>
<div class='kcontrol-s'>
<h1>kcontrol</h1>
<form method='get'>
<table class='kcontrol' cellspacing='0' cellpadding='0'>
<tr>
    <th>Control</th>
    <th>BASE</th>
    <th>VIEW</th>
    <th>HTML</th>
</tr>

<!-- kcontrol/Controls/Button.py -->
<tr>
    <td>${kcontrol.Button('button_name').__class__.__name__}</td>
    <td>${kcontrol.Button('button_name')._BASE}</td>
    <td>${kcontrol.Button('button_name').VIEW}&nbsp;</td>
    <td>${kcontrol.Button('button_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Button('button_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.Button('button_name')._HTML_SHOW}</pre>
    </td>
</tr>


<!-- kcontrol/Controls/CheckBox.py -->
<tr>
    <td>${kcontrol.CheckBox('checkbox_name').__class__.__name__}</td>
    <td>${kcontrol.CheckBox('checkbox_name')._BASE}</td>
    <td>${kcontrol.CheckBox('checkbox_name').VIEW} ( or <span style='color: #990000; font-weight: bold;'>No</span> )</td>
    <td>${kcontrol.CheckBox('checkbox_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.CheckBox('checkbox_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.CheckBox('checkbox_name')._HTML_SHOW}</pre>
    </td>
</tr>

<!-- kcontrol/Controls/Currency.py -->
<tr>
    <td>${kcontrol.Currency('currency_name').__class__.__name__}</td>
    <td>${kcontrol.Currency('currency_name')._BASE}</td>
    <td>${kcontrol.Currency('currency_name').VIEW}&nbsp;</td>
    <td>${kcontrol.Currency('currency_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Currency('currency_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.Currency('currency_name')._HTML_SHOW}</pre>
    </td>
</tr>


<!-- kcontrol/Controls/DatePicker.py -->
<tr>
    <td>${kcontrol.DatePicker('datepicker_name').__class__.__name__}</td>
    <td>${kcontrol.DatePicker('datepicker_name')._BASE}</td>
    <td>${kcontrol.DatePicker('datepicker_name').VIEW}&nbsp;</td>
    <td>${kcontrol.DatePicker('datepicker_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.DatePicker('datepicker_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.DatePicker('datepicker_name')._HTML_SHOW}</pre>
    </td>
</tr>



<!-- kcontrol/Controls/FilePicker.py -->
<tr>
    <td>${kcontrol.FilePicker('filepicker_name').__class__.__name__}</td>
    <td>${kcontrol.FilePicker('filepicker_name')._BASE}</td>
    <td>${kcontrol.FilePicker('filepicker_name').VIEW}&nbsp;</td>
    <td>${kcontrol.FilePicker('filepicker_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.FilePicker('filepicker_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.FilePicker('filepicker_name')._HTML_SHOW}</pre>
    </td>
</tr>


<!-- kcontrol/Controls/Hidden.py -->
<tr>
    <td>${kcontrol.Hidden('hidden_name').__class__.__name__}</td>
    <td>${kcontrol.Hidden('hidden_name')._BASE}</td>
    <td>${kcontrol.Hidden('hidden_name').VIEW}&nbsp;</td>
    <td>${kcontrol.Hidden('hidden_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Hidden('hidden_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
        ${kcontrol.Hidden('hidden_name')._HTML_SHOW}
    </td>
</tr>


<!-- kcontrol/Controls/Icon.py -->
<tr>
    <td>${kcontrol.Icon('icon_name').__class__.__name__}</td>
    <td>${kcontrol.Icon('icon_name')._BASE}</td>
    <td>${kcontrol.Icon('icon_name').VIEW}&nbsp;</td>
    <td>${kcontrol.Icon('icon_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Icon('icon_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
        ${kcontrol.Icon('icon_name')._HTML_SHOW}
    </td>
</tr>


<!-- kcontrol/Controls/Info.py -->
<tr>
    <td>${kcontrol.Info('info_name').__class__.__name__}</td>
    <td>${kcontrol.Info('info_name')._BASE}</td>
    <td>${kcontrol.Info('info_name').VIEW}&nbsp;</td>
    <td>${kcontrol.Info('info_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Info('info_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.Info('info_name')._HTML_SHOW}</pre>
    </td>
</tr>



<!-- kcontrol/Controls/Label.py -->
<tr>
    <td>${kcontrol.Label('label_name').__class__.__name__}</td>
    <td>${kcontrol.Label('label_name')._BASE}</td>
    <td>${kcontrol.Label('label_name').VIEW}&nbsp;</td>
    <td>${kcontrol.Label('label_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Label('label_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.Label('label_name')._HTML_SHOW}</pre>
    </td>
</tr>



<!-- kcontrol/Controls/Link.py -->
    <% 
       link_ctrl = kcontrol.Link('link_name')
       link_ctrl.target = '_blank'
       link_ctrl.link = 'http://www.google.com' %>
<tr>
    <td>${kcontrol.Link('link_name').__class__.__name__}</td>
    <td>${kcontrol.Link('link_name')._BASE}</td>
    <td>${kcontrol.Link('link_name').VIEW}&nbsp;</td>
    <td>${link_ctrl}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Link('link_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.Link('link_name')._HTML_SHOW}</pre>
    </td>
</tr>



<!-- kcontrol/Controls/ListBox.py -->
    <%
        _list_box = kcontrol.ListBox('listbox_name')
        _list_box.values = {'a' : 'a', 'b' : 'b', 'c' : 'c'} %>
<tr>
    <td>${kcontrol.ListBox('listbox_name').__class__.__name__}</td>
    <td>${kcontrol.ListBox('listbox_name')._BASE}</td>
    <td>${kcontrol.ListBox('listbox_name').VIEW}&nbsp;</td>
    <td>${_list_box}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.ListBox('listbox_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.ListBox('listbox_name')._HTML_SHOW}</pre>
    </td>
</tr>


<!-- kcontrol/Controls/Meter.py -->
<tr>
    <td>${kcontrol.Meter('meter_name').__class__.__name__}</td>
    <td>${kcontrol.Meter('meter_name')._BASE}</td>
    <td>${kcontrol.Meter('meter_name').VIEW}&nbsp;</td>
    <td>
        
        ${kcontrol.Meter('meter_name')}
        ${kcontrol.Meter('meter_name75')}
        ${kcontrol.Meter('meter_name50')}
        ${kcontrol.Meter('meter_name25')}
        ${kcontrol.Meter('meter_name0')}
        (several meters)
    </td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Meter('meter_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.Meter('meter_name')._HTML_SHOW}</pre>
    </td>
</tr>

<!-- kcontrol/Controls/Month.py -->
<tr>
    <td>${kcontrol.Month('month_name').__class__.__name__}</td>
    <td>${kcontrol.Month('month_name')._BASE}</td>
    <td>${kcontrol.Month('month_name').VIEW}&nbsp;</td>
    <td>${kcontrol.Month('month_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Month('month_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.Month('month_name')._HTML_SHOW}</pre>
    </td>
</tr>



<!-- kcontrol/Controls/NameTextBox.py -->
<tr>
    <td>${kcontrol.NameTextBox('nametextbox_name').__class__.__name__}<br />
        <span style='font-size: 10pt'>
            (format:<br /> <span style='font-size: 8pt'>%T %F %M %L %S</span>) 
        </span>    
    </td>
    <td>${kcontrol.NameTextBox('nametextbox_name')._BASE}</td>
    <td>${kcontrol.NameTextBox('nametextbox_name').VIEW}&nbsp;</td>
    <td>${kcontrol.NameTextBox('nametextbox_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.NameTextBox('nametextbox_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.NameTextBox('nametextbox_name')._HTML_SHOW}</pre>
    </td>
</tr>



<!-- kcontrol/Controls/Number.py -->
<tr>
    <td>${kcontrol.Number('number_name').__class__.__name__}</td>
    <td>${kcontrol.Number('number_name')._BASE}</td>
    <td>${kcontrol.Number('number_name').VIEW}&nbsp;</td>
    <td>${kcontrol.Number('number_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Number('number_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.Number('number_name')._HTML_SHOW}</pre>
    </td>
</tr>


<!-- kcontrol/Controls/Phone.py -->
<tr>
    <td>${kcontrol.Phone('phone_name').__class__.__name__}</td>
    <td>${kcontrol.Phone('phone_name')._BASE}</td>
    <td>${kcontrol.Phone('phone_name').VIEW}&nbsp;</td>
    <td>${kcontrol.Phone('phone_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Phone('phone_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.Phone('phone_name')._HTML_SHOW}</pre>
    </td>
</tr>


<!-- kcontrol/Controls/SSN.py -->
<tr>
    <td>${kcontrol.SSN('ssn_name').__class__.__name__}</td>
    <td>${kcontrol.SSN('ssn_name')._BASE}</td>
    <td>${kcontrol.SSN('ssn_name').VIEW}&nbsp;</td>
    <td>${kcontrol.SSN('ssn_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.SSN('ssn_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.SSN('ssn_name')._HTML_SHOW}</pre>
    </td>
</tr>


<!-- kcontrol/Controls/TextArea.py -->
<tr>
    <td>${kcontrol.TextArea('textarea_name').__class__.__name__}</td>
    <td>${kcontrol.TextArea('textarea_name')._BASE}</td>
    <td>${kcontrol.TextArea('textarea_name').VIEW}&nbsp;</td>
    <td>${kcontrol.TextArea('textarea_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.TextArea('textarea_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.TextArea('textarea_name')._HTML_SHOW}</pre>
    </td>
</tr>


<!-- kcontrol/Controls/TextBox.py -->
<tr>
    <td>${kcontrol.TextBox('textbox_name').__class__.__name__}</td>
    <td>${kcontrol.TextBox('textbox_name')._BASE}</td>
    <td>${kcontrol.TextBox('textbox_name').VIEW}&nbsp;</td>
    <td>${kcontrol.TextBox('textbox_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.TextBox('textbox_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.TextBox('textbox_name')._HTML_SHOW}</pre>
    </td>
</tr>


<!-- kcontrol/Controls/TimePicker.py -->
<tr>
    <td>${kcontrol.TimePicker('timepicker_name').__class__.__name__}</td>
    <td>${kcontrol.TimePicker('timepicker_name')._BASE}</td>
    <td>${kcontrol.TimePicker('timepicker_name').VIEW}&nbsp;</td>
    <td>${kcontrol.TimePicker('timepicker_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.TimePicker('timepicker_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.TimePicker('timepicker_name')._HTML_SHOW}</pre>
    </td>
</tr>



<!-- kcontrol/Controls/Year.py -->
<tr>
    <td>${kcontrol.Year('year_name').__class__.__name__}</td>
    <td>${kcontrol.Year('year_name')._BASE}</td>
    <td>${kcontrol.Year('year_name').VIEW}&nbsp;</td>
    <td>${kcontrol.Year('year_name')}&nbsp;</td>
</tr>
<tr>
    <td colspan='5' class='mako_rep'>
        ${code("${kcontrol.Year('year_name')}")}
    </td>
</tr>
<tr>
    <td colspan='5' class='example'>
<pre>${kcontrol.Year('year_name')._HTML_SHOW}</pre>
    </td>
</tr>

</table>
</form>
</div>
</div>
</body>
</html>
""")

@mount.get('/')
def index(ctx):
    ctx = {
        'button_name' : 'Click ME',
        'checkbox_name' : True,
        'currency_name' : decimal.Decimal('100.98899'),
        'datepicker_name' : datetime.date(1980, 12, 13),
        'filepicker_name' : None,
        'hidden_name' : 1,
        'icon_name' : 'kcontrol/img/test.jpg',
        'info_name' : 'Peter Pan',
        'label_name' : "Hit Me",
        'link_name' : 'Google.com',
        'listbox_name' : 'b',
        'meter_name' : 100,
        'meter_name75' : 75,
        'meter_name50' : 50,
        'meter_name25' : 25,
        'meter_name0' : 3,
        'nametextbox_name' : 'Lee, Josh',
            'first_name' : 'Josh',
            'last_name' : 'Lee',
        'number_name' : 25.0,
        'phone_name' : '8005551212',
        'ssn_name' : '123456789',
        'textarea_name' : """Noodle Salad,
and corn bread.""",
        'textbox_name' : 'John Jones',
        'timepicker_name' : datetime.time(12, 45),
        'year_name' : 2007,
    }
    return tmpl.render(**dict(ctx=ctx, code=code))

kg.static_dispatch.cp_update('res/kcontrol.resources', config)

def main():
    log = logging.getLogger('')
    parser = optparse.OptionParser(description=__doc__)
    parser.formatter.format_description = lambda s:s
    parser.add_option('-D', '--debug', action='store_true',
                      default=False,
                      help='run in debug mode')

    opts, cmds = parser.parse_args()

    # Determine Paths
    app_dir = os.path.dirname(__file__)

    os.environ['MAKO_APP_DIR'] = app_dir

    
    # Load Configuration

    pid_file = config['global']['server.pid_file']
    daemon = kg.procutils.Daemon(pid_file, app_dir)

    # Logging Configuration
    log.setLevel(0)
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    if opts.debug:
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.INFO)

    log.addHandler(console)

    if 'stop' in cmds:
        return daemon.stop()
    elif 'start' in cmds:
        daemon.start()
    elif 'restart' in cmds:
        daemon.restart()
    else:
        daemon.write_pid()

    # import our components after we have set up logging
    # and configuration


    app = cherrypy.Application(mount, '')
    kg.cptools.register(app)
    cherrypy.quickstart(app, config=config)

if __name__ == '__main__':
    main() 

