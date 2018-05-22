import os
import sys
from alfred.feedback import Feedback

def get_devices():
    output = os.popen("/Library/Android/sdk/platform-tools/adb devices -l").read()
    lines = output.split(os.linesep)[1:]
    devices = []
    for line in lines:
        if len(line) == 0:
            continue
        items = line.split(" ")
        deviceId = items[0]
        deviceName = None
        for item in items:
            if item.startswith("model:"):
                deviceName = item.split(":")[1]
                #print deviceName
                break
        if deviceName is not None:
            device = {"id": deviceId, "name": deviceName}
            devices.append(device)
    return devices

def list(devices=None):
    if devices is None:
        devices = get_devices()
    feedback = Feedback()
    if len(devices) == 0:
        feedback.addItem(title = "No device found")
    for device in devices:
        command = device.get("id")
        feedback.addItem(title = device.get("name"), subtitle = command, arg = command)
    feedback.addVariable(name="fromDevices", value="1")
    feedback.addVariable(name="deviceNum", value=str(len(devices)))
    if len(sys.argv) > 1 and len(sys.argv[1].strip()) > 0:
        feedback.addVariable(name="originQuery", value=sys.argv[1].strip())
    print feedback.get(unescape = True)

