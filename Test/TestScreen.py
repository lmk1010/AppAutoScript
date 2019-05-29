# encoding: utf-8

import ADBAction
from PropertiesUtil import Properties
import os

# devices = ADBAction.getDevices()
#
# for device in devices:
#     ADBAction.getSceenSnapshot(device)

configProps = Properties("../Properties/common.properties").getProperties()
twe = configProps.get("qttActs").split(",")
for srt in twe:
    print(srt)


