# xblog

### 启动程序
```angular2html
python manage.py runserver
```

### 运行测试命令
```angular2html
python manage.py test
```
### 数据库迁移
第一次，初始化，创建migrations迁移目录
```angularjs
python manage.py db init 
```
#### 数据库迁移一般分为两步
1、生成迁移的脚本
```angularjs
python manage.py db migrate
```
2、运行脚本，更改数据库
```angular2html
python manage.py db upgrade
```
### 增加记录
```angularjs
(venv) E:\PycharmProject\xblog>python manage.py shell
DEV_DATABASE_URL: mysql://root:19940423@localhost/xblog

>>> u = User(user_email='xdhuxc@163.com', user_name='xdhuxc', password='cat')
>>> db.session.add(u)
>>> db.session.commit()
E:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\engine\default.py:509: Warning: Incorrect string value: '\xD6\xD0\xB9\xFA\xB1\xEA...' for column 'VARIABLE_
VALUE' at row 496
  cursor.execute(statement, parameters)
>>> exit()

(venv) E:\PycharmProject\xblog>
```

### 常见问题及解决
1、安装 mysql-python 时，报错如下：
```angularjs
(venv) E:\PycharmProject\xblog>pip install mysql-python
Collecting mysql-python
  Using cached https://files.pythonhosted.org/packages/a5/e9/51b544da85a36a68debe7a7091f068d802fc515a3a202652828c73453cad/MySQL-python-1.2.5.zip
Building wheels for collected packages: mysql-python
  Running setup.py bdist_wheel for mysql-python ... error
  Complete output from command e:\pycharmproject\xblog\venv\scripts\python.exe -u -c "import setuptools, tokenize;__file__='c:\\users\\wanghuan\\appdata\\local\\temp
\\pip-install-eatlgd\\mysql-python\\setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__,
'exec'))" bdist_wheel -d c:\users\wanghuan\appdata\local\temp\pip-wheel-nsdlm3 --python-tag cp27:
  running bdist_wheel
  running build
  running build_py
  creating build
  creating build\lib.win-amd64-2.7
  copying _mysql_exceptions.py -> build\lib.win-amd64-2.7
  creating build\lib.win-amd64-2.7\MySQLdb
  copying MySQLdb\__init__.py -> build\lib.win-amd64-2.7\MySQLdb
  copying MySQLdb\converters.py -> build\lib.win-amd64-2.7\MySQLdb
  copying MySQLdb\connections.py -> build\lib.win-amd64-2.7\MySQLdb
  copying MySQLdb\cursors.py -> build\lib.win-amd64-2.7\MySQLdb
  copying MySQLdb\release.py -> build\lib.win-amd64-2.7\MySQLdb
  copying MySQLdb\times.py -> build\lib.win-amd64-2.7\MySQLdb
  creating build\lib.win-amd64-2.7\MySQLdb\constants
  copying MySQLdb\constants\__init__.py -> build\lib.win-amd64-2.7\MySQLdb\constants
  copying MySQLdb\constants\CR.py -> build\lib.win-amd64-2.7\MySQLdb\constants
  copying MySQLdb\constants\FIELD_TYPE.py -> build\lib.win-amd64-2.7\MySQLdb\constants
  copying MySQLdb\constants\ER.py -> build\lib.win-amd64-2.7\MySQLdb\constants
  copying MySQLdb\constants\FLAG.py -> build\lib.win-amd64-2.7\MySQLdb\constants
  copying MySQLdb\constants\REFRESH.py -> build\lib.win-amd64-2.7\MySQLdb\constants
  copying MySQLdb\constants\CLIENT.py -> build\lib.win-amd64-2.7\MySQLdb\constants
  running build_ext
  building '_mysql' extension
  creating build\temp.win-amd64-2.7
  creating build\temp.win-amd64-2.7\Release
  C:\Users\wanghuan\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0\VC\Bin\amd64\cl.exe /c /nologo /Ox /MD /W3 /GS- /DNDEBUG -Dversion_info=(1,2,5,
'final',1) -D__version__=1.2.5 "-IC:\Program Files (x86)\MySQL\MySQL Connector C 6.0.2\include" -Ic:\xdhuxc\python\include -Ie:\pycharmproject\xblog\venv\PC /Tc_mysq
l.c /Fobuild\temp.win-amd64-2.7\Release\_mysql.obj /Zl
  _mysql.c
  _mysql.c(42) : fatal error C1083: Cannot open include file: 'config-win.h': No such file or directory
  error: command 'C:\\Users\\wanghuan\\AppData\\Local\\Programs\\Common\\Microsoft\\Visual C++ for Python\\9.0\\VC\\Bin\\amd64\\cl.exe' failed with exit status 2

  ----------------------------------------
  Failed building wheel for mysql-python
  Running setup.py clean for mysql-python
Failed to build mysql-python
Installing collected packages: mysql-python
  Running setup.py install for mysql-python ... error
    Complete output from command e:\pycharmproject\xblog\venv\scripts\python.exe -u -c "import setuptools, tokenize;__file__='c:\\users\\wanghuan\\appdata\\local\\te
mp\\pip-install-eatlgd\\mysql-python\\setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__
, 'exec'))" install --record c:\users\wanghuan\appdata\local\temp\pip-record-yixxxl\install-record.txt --single-version-externally-managed --compile --install-header
s e:\pycharmproject\xblog\venv\include\site\python2.7\mysql-python:
    running install
    running build
    running build_py
    creating build
    creating build\lib.win-amd64-2.7
    copying _mysql_exceptions.py -> build\lib.win-amd64-2.7
    creating build\lib.win-amd64-2.7\MySQLdb
    copying MySQLdb\__init__.py -> build\lib.win-amd64-2.7\MySQLdb
    copying MySQLdb\converters.py -> build\lib.win-amd64-2.7\MySQLdb
    copying MySQLdb\connections.py -> build\lib.win-amd64-2.7\MySQLdb
    copying MySQLdb\cursors.py -> build\lib.win-amd64-2.7\MySQLdb
    copying MySQLdb\release.py -> build\lib.win-amd64-2.7\MySQLdb
    copying MySQLdb\times.py -> build\lib.win-amd64-2.7\MySQLdb
    creating build\lib.win-amd64-2.7\MySQLdb\constants
    copying MySQLdb\constants\__init__.py -> build\lib.win-amd64-2.7\MySQLdb\constants
    copying MySQLdb\constants\CR.py -> build\lib.win-amd64-2.7\MySQLdb\constants
    copying MySQLdb\constants\FIELD_TYPE.py -> build\lib.win-amd64-2.7\MySQLdb\constants
    copying MySQLdb\constants\ER.py -> build\lib.win-amd64-2.7\MySQLdb\constants
    copying MySQLdb\constants\FLAG.py -> build\lib.win-amd64-2.7\MySQLdb\constants
    copying MySQLdb\constants\REFRESH.py -> build\lib.win-amd64-2.7\MySQLdb\constants
    copying MySQLdb\constants\CLIENT.py -> build\lib.win-amd64-2.7\MySQLdb\constants
    running build_ext
    building '_mysql' extension
    creating build\temp.win-amd64-2.7
    creating build\temp.win-amd64-2.7\Release
    C:\Users\wanghuan\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0\VC\Bin\amd64\cl.exe /c /nologo /Ox /MD /W3 /GS- /DNDEBUG -Dversion_info=(1,2,
5,'final',1) -D__version__=1.2.5 "-IC:\Program Files (x86)\MySQL\MySQL Connector C 6.0.2\include" -Ic:\xdhuxc\python\include -Ie:\pycharmproject\xblog\venv\PC /Tc_my
sql.c /Fobuild\temp.win-amd64-2.7\Release\_mysql.obj /Zl
    _mysql.c
    _mysql.c(42) : fatal error C1083: Cannot open include file: 'config-win.h': No such file or directory
    error: command 'C:\\Users\\wanghuan\\AppData\\Local\\Programs\\Common\\Microsoft\\Visual C++ for Python\\9.0\\VC\\Bin\\amd64\\cl.exe' failed with exit status 2

    ----------------------------------------
Command "e:\pycharmproject\xblog\venv\scripts\python.exe -u -c "import setuptools, tokenize;__file__='c:\\users\\wanghuan\\appdata\\local\\temp\\pip-install-eatlgd\\
mysql-python\\setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --re
cord c:\users\wanghuan\appdata\local\temp\pip-record-yixxxl\install-record.txt --single-version-externally-managed --compile --install-headers e:\pycharmproject\xblo
g\venv\include\site\python2.7\mysql-python" failed with error code 1 in c:\users\wanghuan\appdata\local\temp\pip-install-eatlgd\mysql-python\
```
解决：到 https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python 下载相应的包，例如，MySQL_python‑1.2.5‑cp27‑none‑win_amd64.whl，使用pip安装之，然后继续安装即可。

2、运行程序时，报错如下：
```angularjs
Traceback (most recent call last):
  File "E:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 2309, in __call__
    return self.wsgi_app(environ, start_response)
  File "E:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 2295, in wsgi_app
    response = self.handle_exception(e)
  File "E:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 1741, in handle_exception
    reraise(exc_type, exc_value, tb)
  File "E:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 2292, in wsgi_app
    response = self.full_dispatch_request()
  File "E:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 1815, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "E:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 1718, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "E:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 1813, in full_dispatch_request
    rv = self.dispatch_request()
  File "E:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 1799, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "E:\PycharmProject\xblog\app\auth\views.py", line 28, in login
    login_user(user, form.remember_me.data)
  File "E:\PycharmProject\xblog\venv\lib\site-packages\flask_login\utils.py", line 161, in login_user
    user_id = getattr(user, current_app.login_manager.id_attribute)()
  File "E:\PycharmProject\xblog\venv\lib\site-packages\flask_login\mixins.py", line 39, in get_id
    raise NotImplementedError('No `id` attribute - override `get_id`')
NotImplementedError: No `id` attribute - override `get_id`
```

在 models.py 中添加如下代码：
```angularjs
def get_id(self):
    # 返回一个能唯一识别用户的，并能用于从 user_loader 回调中 加载用户的 unicode 。注意着 必须 是一个 unicode ——如果 ID 原本是 一个 int 或其它类型，你需要把它转换为 unicode。
    return unicode(self.user_id)
```
