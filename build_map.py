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
import re
import lxml.etree as et


def modify_qgs(template, input_loc):
    sources = {'cold': os.path.join(input_loc, 'PIXELS', 'cold.shp'),
               'hot': os.path.join(input_loc, 'PIXELS', 'hot.shp'),
               'hot_pixel_suggestion': os.path.join(input_loc, 'PIXEL_REGIONS',
                                                    'hot_pixel_suggestion.img'),
               'cold_pixel_suggestion': os.path.join(input_loc, 'PIXEL_REGIONS',
                                                     'cold_pixel_suggestion.img'),
               'region_mask': os.path.join(input_loc, 'PIXEL_REGIONS', 'region_mask.img'),
               'ndvi_toa': os.path.join(input_loc, 'INDICES', 'ndvi_toa.img'),
               'ts': os.path.join(input_loc, 'ts.img'),
               'albedo_at_sur': os.path.join(input_loc, 'albedo_at_sur.img'),
               'et_rf': os.path.join(input_loc, 'ETRF', 'et_rf.img')}

    with open(template) as _file:
        tree = et.parse(_file)
        txt = tree.xpath("//maplayer/datasource[contains(text(), 'albedo_at_sur.img')]")[0].text

        for key, val in sources.items():
            items = tree.xpath("//qgis/layer-tree-group/layer-tree-layer[@name='{}']".format(key))
            for s in items:
                s.attrib['source'] = val

        string = et.tostring(tree)

        string = re.sub(r"{}".format(os.path.dirname(txt)), r"%s" % input_loc, string)

    output = os.path.join(input_loc, '{}_calbration_map.qgs'.format(os.path.basename(input_loc)))
    with open(output, 'w') as out_file:
        for line in string:
            out_file.write(line)


if __name__ == '__main__':
    home = os.path.expanduser('~')
    path = os.path.join(home, 'IrrigationGIS', 'tests', 'qgis')
    t = os.path.join(path, 'qgs_template.qgs')
    targets = []
    for r, d, f in os.walk(path):
        if 'ETRF' in d:
            targets.append(r)
            modify_qgs(t, r)

# ========================= EOF ===================================================
