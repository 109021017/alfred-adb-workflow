import os
import subprocess
import sys
import devices
from alfred import Feedback


feedback = Feedback()
adb = "/Library/Android/sdk/platform-tools/adb"
device = ""
if len(sys.argv) > 1 and len(sys.argv[1].strip()) > 0:
    device = " -s "+sys.argv[1]
cmd = adb + device + " shell dumpsys window windows | grep -E 'mCurrentFocus'"
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()
if error is not None and "more than one" in error:
    devices.list()
    exit(0)
if error is not None and "no devices" in error:
    devices.list()
    exit(0)
result = os.popen(cmd).read().strip()
displayName = result.split(' ')[-1][0:-1]
parts = displayName.split("/")
packageName = None
className = None
simpleName = None
if len(parts) > 1:
    packageName = parts[0]
    className = parts[1]
    simpleName = className.split(".")[-1]

if simpleName is not None:
    feedback.addItem(arg=simpleName, title=simpleName, subtitle="Simple Name")
if className is not None:
    feedback.addItem(arg=className, title=className, subtitle="Class Name")
if packageName is not None:
    feedback.addItem(arg=packageName, title=packageName, subtitle="Package Name")
if displayName is not None:
    feedback.addItem(arg=displayName, title=displayName, subtitle="Full String")

print feedback.get()
