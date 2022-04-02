Set ws = CreateObject("Wscript.Shell")
ws.run "cmd /c start.bat",0
ws.run "cmd /c start_celery.bat",0
'ws.run "cmd /c start_celerybeat.bat",0
