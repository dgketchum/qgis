# ===============================================================================
# Copyright 2018 dgketchum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# PYTHONPATH = / < qgispath > / share / qgis / python
import os

home = os.path.expanduser('~')
path = os.path.join(home, 'miniconda2', 'envs', 'qgis', 'share', 'qgis', 'python')
import sys

sys.path.append(path)

from xml.dom.minidom import Document
import string
import os
import sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import QApplication
from PyQt4.QtXml import *


def make_qgs(template, input):

    QGISAPP = QgsApplication(sys.argv, True)
    QgsApplication.setPrefixPath(os.path.dirname(input), True)
    QgsApplication.initQgis()
    QgsProject.instance().setFileName(template)
    print QgsProject.instance().fileName()

    for file1 in os.listdir(r"C:\myprojects\world"):
        if file1.endswith('.shp'):
            layer = QgsVectorLayer(r"C:\myprojects\world" + r"\\" + file1, file1, "ogr")
            print file1
            print layer.isValid()
            # Add layer to the registry
            QgsMapLayerRegistry.instance().addMapLayer(layer)

    QgsProject.instance().write()
    QgsApplication.exitQgis()

    add_Layers()

    return None


if __name__ == '__main__':
    home = os.path.expanduser('~')
    path = os.path.join(home, 'IrrigationGIS', 'tests', 'qgis')
    folder = os.path.join(path, 'LC08_041027_20150807')
    template = os.path.join(path, 'qgis_template.qgs')
    make_qgs(template, folder)
# ========================= EOF ====================================================================
