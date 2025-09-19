import os
from app.functions.tools.resourcePath import resourcePath

def getIcon(name):
    resources_path = resourcePath()
    icon = os.path.join(resources_path, "../", "assets", "icons", name)
    return icon
