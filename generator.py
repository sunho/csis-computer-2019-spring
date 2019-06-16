from os import walk
import re
from shutil import copyfile
from jinja2 import Template

tmpl = Template("""
<html>
    <head>
        <title>
            {{grade}}-{{name}}
        </title>
    </head>
    <body>
        <div style="display: flex; justify-content: center; align-items: center">
            <div style="padding: 10px; margin-right: 10px; font-size: 30px; background: gray; color: white">
                {{grade}}
            </div>
            <div style="padding: 10px; font-size: 25px;">
                {{name}}
            </div>
        </div>
        <div style = "text-align: center">
            <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" width="550" height="400" id="project" align="middle">
                <param name="movie" value="{{file}}"/>
                <!--[if !IE]>-->
                <object type="application/x-shockwave-flash" data="{{file}}" width="550" height="400">
                <param name="movie" value="{{file}}"/>
                <!--<![endif]-->
                <a href="http://www.adobe.com/go/getflash">
                    <img src="http://www.adobe.com/images/shared/download_buttons/get_flash_player.gif" alt="Get Adobe Flash player"/>
                </a>
                <!--[if !IE]>-->
                </object>
                <!--<![endif]-->
            </object>
        </div>
    </body>
</html>
""")

tmpl2 =  Template("""
<!doctype html>
<html>
    <head>
        <title>
            CSIS COMPUTER 2019 SPRING projects
        </title>
    </head>
    <body>
        {% for grade, students in grades.items() %}
          <div>
            <div>
                {{ grade }}
            </div>
            <ul>
            {% for student in students %}
                <li>
                    <a href="{{student.link}}">{{student.name}}</a>
                </li>
            {% endfor %}
            </ul>
          </div>  
        {% endfor %}
    </body>
</html>
""")

projects = []
for _, _, files in walk('./swfs'):
    for file in files:
        projects.append(re.findall(r'(.+)\-(.+)\-(.+).swf', file)[0])

grades = dict()
for p in projects:
    with open('{}/{}.html'.format(p[0],p[1]), 'w') as file:
        swf = '{}-{}-{}.swf'.format(p[0], p[1], p[2])
        copyfile('./swfs/' + swf, './{}/{}'.format(p[0],swf))
        file.write(tmpl.render(grade=p[0], name=p[1], file=swf))
    if p[0] not in grades:
        grades[p[0]] = []
    grades[p[0]].append({'name': p[1], 'link': '{}/{}.html'.format(p[0],p[1])})

with open('index.html'.format(p[0],p[1]), 'w') as file:
    file.write(tmpl2.render(grades=grades))