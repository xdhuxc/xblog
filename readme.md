# xblog

### 启动程序
```angular2html
python manage.py runserver
```
### 账户
xdhuxc@163.com cat

https://news.cnblogs.com/n/605020/

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
### httpie的使用
1、访问REST API
```angularjs
E:\PycharmProject\xblog>http --auth xdhuxc@163.com:dog --json GET http://127.0.0.1:5000/api/v1/token
HTTP/1.0 200 OK
Content-Length: 170
Content-Type: application/json
Date: Sun, 02 Sep 2018 02:36:48 GMT
Server: Werkzeug/0.14.1 Python/2.7.14

{
    "expiration": 3600,
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUzNTg1OTQwOCwiaWF0IjoxNTM1ODU1ODA4fQ.eyJ1c2VyX2lkIjoyfQ.U4xEpZ35WxYknqJy5rsEo1lywabBnS9F-NXZVNKnJHk"
}
```
### coverage命令的使用
```angularjs
python manage.py test coverage
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

### 在linux下执行pip install -r requirements.txt时，报错如下：
```angular2html
Collecting MySQL-python==1.2.5 (from -r requirements.txt (line 33))
  Using cached https://files.pythonhosted.org/packages/a5/e9/51b544da85a36a68debe7a7091f068d802fc515a3a202652828c73453cad/MySQL-python-1.2.5.zip
    Complete output from command python setup.py egg_info:
    sh: mysql_config: command not found
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-build-4qxBnK/MySQL-python/setup.py", line 17, in <module>
        metadata, options = get_config()
      File "setup_posix.py", line 43, in get_config
        libs = mysql_config("libs_r")
      File "setup_posix.py", line 25, in mysql_config
        raise EnvironmentError("%s not found" % (mysql_config.path,))
    EnvironmentError: mysql_config not found
    
    ----------------------------------------
Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-4qxBnK/MySQL-python/
```
解决：使用如下命令安装mysql-devel
```angular2html
yum -y install mysql-devel
```

报错如下：
```angular2html
Installing collected packages: MySQL-python
  Running setup.py install for MySQL-python ... error
    Complete output from command /usr/bin/python2 -u -c "import setuptools, tokenize;__file__='/tmp/pip-install-YdXPnf/MySQL-python/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-record-XO9KAe/install-record.txt --single-version-externally-managed --compile:
    running install
    running build
    running build_py
    creating build
    creating build/lib.linux-x86_64-2.7
    copying _mysql_exceptions.py -> build/lib.linux-x86_64-2.7
    creating build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/__init__.py -> build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/converters.py -> build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/connections.py -> build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/cursors.py -> build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/release.py -> build/lib.linux-x86_64-2.7/MySQLdb
    copying MySQLdb/times.py -> build/lib.linux-x86_64-2.7/MySQLdb
    creating build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/__init__.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/CR.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/FIELD_TYPE.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/ER.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/FLAG.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/REFRESH.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    copying MySQLdb/constants/CLIENT.py -> build/lib.linux-x86_64-2.7/MySQLdb/constants
    running build_ext
    building '_mysql' extension
    creating build/temp.linux-x86_64-2.7
    gcc -pthread -fno-strict-aliasing -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv -DNDEBUG -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv -fPIC -Dversion_info=(1,2,5,'final',1) -D__version__=1.2.5 -I/usr/include/mysql -I/usr/include/python2.7 -c _mysql.c -o build/temp.linux-x86_64-2.7/_mysql.o
    _mysql.c:29:20: fatal error: Python.h: No such file or directory
     #include "Python.h"
                        ^
    compilation terminated.
    error: command 'gcc' failed with exit status 1
    
    ----------------------------------------
Command "/usr/bin/python2 -u -c "import setuptools, tokenize;__file__='/tmp/pip-install-YdXPnf/MySQL-python/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-record-XO9KAe/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-install-YdXPnf/MySQL-python/
```
解决：使用如下命令安装python-devel
```angular2html
yum install -y python-devel
```
 

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

3、初始化数据库时，报错如下：（mysql版本为：8.0.12）
```angular2html
(venv) D:\PycharmProject\xblog>python manage.py db upgrade
Traceback (most recent call last):
  File "manage.py", line 54, in <module>
    manager.run()
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_script\__init__.py", line 417, in run
    result = self.handle(argv[0], argv[1:])
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_script\__init__.py", line 386, in handle
    res = handle(*args, **config)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_script\commands.py", line 216, in __call__
    return self.run(*args, **kwargs)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_migrate\__init__.py", line 95, in wrapped
    f(*args, **kwargs)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_migrate\__init__.py", line 280, in upgrade
    command.upgrade(config, revision, sql=sql, tag=tag)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\alembic\command.py", line 254, in upgrade
    script.run_env()
  File "D:\PycharmProject\xblog\venv\lib\site-packages\alembic\script\base.py", line 427, in run_env
    util.load_python_file(self.dir, 'env.py')
  File "D:\PycharmProject\xblog\venv\lib\site-packages\alembic\util\pyfiles.py", line 81, in load_python_file
    module = load_module_py(module_id, path)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\alembic\util\compat.py", line 135, in load_module_py
    mod = imp.load_source(module_id, path, fp)
  File "migrations\env.py", line 87, in <module>
    run_migrations_online()
  File "migrations\env.py", line 72, in run_migrations_online
    connection = engine.connect()
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\engine\base.py", line 2102, in connect
    return self._connection_cls(self, **kwargs)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\engine\base.py", line 90, in __init__
    if connection is not None else engine.raw_connection()
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\engine\base.py", line 2188, in raw_connection
    self.pool.unique_connection, _connection)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\engine\base.py", line 2162, in _wrap_pool_connect
    e, dialect, self)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\engine\base.py", line 1476, in _handle_dbapi_exception_noconnection
    exc_info
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\util\compat.py", line 265, in raise_from_cause
    reraise(type(exception), exception, tb=exc_tb, cause=cause)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\engine\base.py", line 2158, in _wrap_pool_connect
    return fn()
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\pool.py", line 345, in unique_connection
    return _ConnectionFairy._checkout(self)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\pool.py", line 791, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\pool.py", line 532, in checkout
    rec = pool._do_get()
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\pool.py", line 1287, in _do_get
    return self._create_connection()
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\pool.py", line 350, in _create_connection
    return _ConnectionRecord(self)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\pool.py", line 477, in __init__
    self.__connect(first_connect_check=True)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\pool.py", line 674, in __connect
    connection = pool._invoke_creator(self)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\engine\strategies.py", line 106, in connect
    return dialect.connect(*cargs, **cparams)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\engine\default.py", line 412, in connect
    return self.dbapi.connect(*cargs, **cparams)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\MySQLdb\__init__.py", line 81, in Connect
    return Connection(*args, **kwargs)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\MySQLdb\connections.py", line 193, in __init__
    super(Connection, self).__init__(*args, **kwargs2)
sqlalchemy.exc.OperationalError: (_mysql_exceptions.OperationalError) (1251, 'Client does not support authentication protocol requested b
y server; consider upgrading MySQL client') (Background on this error at: http://sqlalche.me/e/e3q8)
```
```angular2html
use sys;
alter user 'root'@'localhost' identified with mysql_native_password by '19940423';
```
4、使用中文后，渲染模板时报错：
```angular2html
(venv) D:\PycharmProject\xblog>python manage.py runserver
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 265-864-630
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
D:\PycharmProject\xblog\venv\lib\site-packages\sqlalchemy\engine\default.py:509: Warning: Incorrect string value: '\xD6\xD0\xB9\xFA\xB1\x
EA...' for column 'VARIABLE_VALUE' at row 518
  cursor.execute(statement, parameters)
127.0.0.1 - - [22/Aug/2018 10:51:46] "GET /auth/login HTTP/1.1" 200 -
127.0.0.1 - - [22/Aug/2018 10:51:48] "POST /auth/login HTTP/1.1" 302 -
127.0.0.1 - - [22/Aug/2018 10:51:48] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [22/Aug/2018 10:51:55] "GET /auth/change_password HTTP/1.1" 500 -
Traceback (most recent call last):
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 2309, in __call__
    return self.wsgi_app(environ, start_response)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 2295, in wsgi_app
    response = self.handle_exception(e)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 1741, in handle_exception
    reraise(exc_type, exc_value, tb)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 2292, in wsgi_app
    response = self.full_dispatch_request()
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 1815, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 1718, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 1813, in full_dispatch_request
    rv = self.dispatch_request()
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask\app.py", line 1799, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_login\utils.py", line 261, in decorated_view
    return func(*args, **kwargs)
  File "D:\PycharmProject\xblog\app\auth\views.py", line 141, in change_password
    return render_template('auth/change_password.html', form=form)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask\templating.py", line 135, in render_template
    context, ctx.app)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask\templating.py", line 117, in _render
    rv = template.render(context)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\jinja2\environment.py", line 1008, in render
    return self.environment.handle_exception(exc_info, True)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\jinja2\environment.py", line 780, in handle_exception
    reraise(exc_type, exc_value, tb)
  File "D:\PycharmProject\xblog\app\templates\auth\change_password.html", line 2, in top-level template code
    {% import "bootstrap/wtf.html" as wtf %}
  File "D:\PycharmProject\xblog\app\templates\base.html", line 1, in top-level template code
    {% extends "bootstrap/base.html" %}
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_bootstrap\templates\bootstrap\base.html", line 1, in top-level template code

    {% block doc -%}
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_bootstrap\templates\bootstrap\base.html", line 4, in block "doc"
    {%- block html %}
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_bootstrap\templates\bootstrap\base.html", line 20, in block "html"
    {% block body -%}
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_bootstrap\templates\bootstrap\base.html", line 23, in block "body"
    {% block content -%}
  File "D:\PycharmProject\xblog\app\templates\base.html", line 69, in block "content"
    {% block page_content %}
  File "D:\PycharmProject\xblog\app\templates\auth\change_password.html", line 13, in block "page_content"
    {{ wtf.quick_form(form) }}
  File "D:\PycharmProject\xblog\venv\lib\site-packages\jinja2\runtime.py", line 579, in _invoke
    rv = self._func(*arguments)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_bootstrap\templates\bootstrap\wtf.html", line 205, in template
    {{ form_field(field,
  File "D:\PycharmProject\xblog\venv\lib\site-packages\jinja2\runtime.py", line 579, in _invoke
    rv = self._func(*arguments)
  File "D:\PycharmProject\xblog\venv\lib\site-packages\flask_bootstrap\templates\bootstrap\wtf.html", line 119, in template
    {{field.label(class="control-label")|safe}}
  File "D:\PycharmProject\xblog\venv\lib\site-packages\wtforms\fields\core.py", line 402, in __call__
    return widgets.HTMLString('<label %s>%s</label>' % (attributes, text or self.text))
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128)
```
在 相应的views.py文件中添加如下代码，指定编码方式
```angular2html
charset = 'utf-8'
reload(sys)
sys.setdefaultencoding(charset)
```
