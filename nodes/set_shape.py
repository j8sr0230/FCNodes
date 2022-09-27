# -*- coding: utf-8 -*-
###################################################################################
#
#  set_shape.py
#
#  Copyright (c) 2022 Ronny Scharf-Wildenhain <ronny.scharf08@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
###################################################################################
import FreeCAD
import Part

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon


@register_node
class SetShape(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Set Shape"
    op_category = "FreeCAD"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(4, "Obj", 0, 0, True, ("fc_obj", )),
                                           (5, "Shp", 0, "0", False, ("Shape", ))],
                         outputs_init_list=[(4, "Obj", 0, 0, True, ("fc_obj", ))],
                         width=150)

    def eval_operation(self, sockets_input_data: list) -> list:
        obj_list: list = sockets_input_data[0]
        compound = Part.makeCompound(sockets_input_data[1])

        if not (FreeCAD.ActiveDocument is None):
            for obj in obj_list:
                obj.Shape = compound

            FreeCAD.ActiveDocument.recompute()
        else:
            raise Exception('No active document')

        return [obj_list]
