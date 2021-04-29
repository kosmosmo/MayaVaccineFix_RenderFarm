import os
import getpass,socket
from stat import S_IREAD, S_IWRITE
from datetime import date
import maya.cmds as cmds
import os.path
projectDirectory = cmds.workspace(q=True, rd=True)
report_path = projectDirectory.replace('/','\\') + '\\report.txt'
vaccine_file_path = 'C:\\Users\\{}\\Documents\\maya\\scripts'.format(getpass.getuser())
def lock_file(vaccine_py,user_py):
    print('.............................................7')
    if os.path.isfile(vaccine_py):
        os.chmod(vaccine_py, S_IWRITE)
        os.unlink(vaccine_py)
    if os.path.isfile(user_py):
        os.chmod(user_py, S_IWRITE)
        os.unlink(user_py)
    open(vaccine_py, "w")
    open(user_py, 'w')
    os.chmod(vaccine_py, S_IREAD)
    os.chmod(user_py, S_IREAD)

def scan(path):
    vaccine_pyc = path + '\\vaccine.pyc'
    vaccine_py = path + '\\vaccine.py'
    user_py = path + '\\userSetup.py'
    if not os.path.isdir(path):
        os.mkdir(path)
        lock_file(vaccine_py, user_py)
        return "Vaccine files not found. Patch succeeded"
    if not os.path.exists(vaccine_py):
        lock_file(vaccine_py, user_py)
        return "Vaccine files not found. Patch succeeded"
    if os.path.isfile(vaccine_pyc):
        try:
            os.remove(vaccine_pyc)
        except:
            return 'Patch failed'
        lock_file(vaccine_py, user_py)
        return "Inital patch succeeded"
    else:
        lock_file(vaccine_py, user_py)
        return "Repatch succeeded"
report = scan(vaccine_file_path)

print ("report path is ...... " + report_path)
try:
        today = date.today()
        f = open(report_path, "a")
        f.write("{},{},{},{}\n".format(today,socket.gethostname(),getpass.getuser(),report))
        f.close()
except:
        print ('fail to generate report file')


