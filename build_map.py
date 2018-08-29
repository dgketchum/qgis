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

import os
import lxml.etree as et


def modify_qgs(template, input):
    with open(template) as f:
        tree = et.parse(f)
        root = tree.getroot()

        for elem in root.getiterator():
            try:
                elem.text = elem.text.replace(
                    '/home/dgketchum/IrrigationGIS/tests/qgis/LC08_041027_20150807/ts.img',
                    '/home/dgketchum/IrrigationGIS/tests/qgis/LC08_041027_20160825/ts.img')

            except AttributeError:
                pass

    output = os.path.join(input, '{}_calbration_map.qgs'.format(os.path.basename(input)))

    tree.write(output, xml_declaration=True, method='xml', encoding="utf8")


if __name__ == '__main__':
    home = os.path.expanduser('~')
    path = os.path.join(home, 'IrrigationGIS', 'tests', 'qgis')
    t = os.path.join(path, 'qgs_template.qgs')
    targets = []
    for r, d, f in os.walk(path):
        if 'ETRF' in d:
            targets.append(r)
            print(r, d, f)
            modify_qgs(t, r)

# ========================= EOF ====================================================================
