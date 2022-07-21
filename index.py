#!Python
print("Content-Type: text/html")
print()
import cgi, os  #os모듈을 import한다.
 
files = os.listdir('data') #[CSS,HTML,JavaScript]
listStr = ''
for item in files:
    listStr = listStr + '<li><a href="index.py?id={name}">{name}</a></li>'.format(name=item)
 
form = cgi.FieldStorage()
#a태그 클릭시 id값에 따른 pageId 분기처리
if 'id' in form:
    pageId = form["id"].value
    description = open('data/'+pageId,'r').read() #open함수로 내용 불러오기
else :
    pageId = 'welcome'
    description = 'Welcome!'
 
print('''<!doctype html>
<html>
<head>
  <title>WEB1 - Welcome</title>
  <meta charset="utf-8">
</head>
<body>
  <h1><a href="index.py">WEB</a></h1>
  <ol>
    {listStr}
  </ol>
  <a href="create.py">create</a> #create버튼
  <h2>{title}</h2>
  <p>{desc}
  </p>
</body>
</html>
'''.format(title=pageId, desc=description, listStr=listStr))