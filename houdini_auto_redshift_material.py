import hou
import os
import re
import webbrowser
from hutil.Qt import QtCore, QtUiTools, QtWidgets, QtGui


class ShaderCreator(QtWidgets.QWidget):
    def __init__(self):
        super(ShaderCreator, self).__init__()
        ui_file = 'D:/Git/Noel/houdini_redshift_material/ui/createwidget.ui'
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Setup "Create Shader" button
        self.ui.createButton.clicked.connect(self.createButtonClicked)

        # Setup "Browse Textures" button
        self.ui.browseButton.clicked.connect(self.browseButtonClicked)

        # Setup "Browse Asset" button
        self.ui.browseAssetButton.clicked.connect(
            self.browseAssetButtonClicked)

        # Setup "Cancle" button
        self.ui.quitButton.clicked.connect(self.quitButtonClicked)

        # Setup "ckeckBox" clicked event
        self.ui.checkBox.stateChanged.connect(self.checkBoxClicked)

        # Setup "Reload Textures" button
        self.ui.reloadButton.clicked.connect(self.reloadButtonClicked)

        # Setup "Help" button
        self.ui.helpButton.clicked.connect(lambda: webbrowser.open(
            'https://github.com/noelvenus24/houdini_auto_redshift_material/wiki'))

    def createButtonClicked(self):
        self.create_empty_shadernetwork()
        self.createShaders()

    def checkBoxClicked(self):
        if self.ui.checkBox.isChecked():
            self.ui.customNameEdit.setEnabled(True)
            self.ui.reloadButton.setEnabled(True)
        else:
            self.ui.customNameEdit.setEnabled(False)
            self.ui.reloadButton.setEnabled(False)

    def browseButtonClicked(self):
        # Open file dialog to load diffuse texture
        hipPath = os.environ.get('HIP', '')
        collectionFolderPath = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'please select directory.', hipPath)
        if collectionFolderPath:
            self.ui.collectDirLine.setText(collectionFolderPath)
            tex_item = []
            tex_item = self.textureList(collectionFolderPath)
            self.ui.listWidget.clear()
            for i, name in enumerate(tex_item):
                self.ui.listWidget.insertItem(i, name)

    def reloadButtonClicked(self):
        collectionFolderPath = self.ui.collectDirLine.text()
        if collectionFolderPath:
            tex_item = []
            tex_item = self.textureList(collectionFolderPath)
            self.ui.listWidget.clear()
            for i, name in enumerate(tex_item):
                self.ui.listWidget.insertItem(i, name)

    def quitButtonClicked(self):
        win.close()

    def browseAssetButtonClicked(self):
        sel_asset_path = hou.ui.selectNode(node_type_filter=None)
        node = hou.node(sel_asset_path).name()
        self.ui.sel_asset_name.setText(node)

    def textureType(self):
        textype_names = {
            'diffuse': [
                "diffuse",
                "diff",
                "albedo",
                "color",
                "col",
                "alb",
                "dif",
                "basecolor"
            ],
            'ao': [
                "ao",
                "ambientocclusion",
                "ambient_occlusion",
                "cavity"
            ],
            'spec': [
                "specular",
                "spec",
                "s",
                "refl",
                "reflectivity"
            ],
            'rough': [
                "roughness",
                "rough",
                "r"
            ],
            'gloss': [
                "gloss",
                "g",
                "glossiness"
            ],
            'metal': [
                "metal",
                "metalness",
                "m",
                "metallic"
            ],
            'opc': [
                "transparency",
                "t",
                "opacity",
                "o"
            ],
            'emissive': [
                "emission",
                "emissive"
            ],
            'normal': [
                "normal",
                "nrm",
                "nrml",
                "n",
                "norm_ogl",
                "normalbump"
            ],
            'bump': [
                "bump",
                "bmp",
                "height",
                "h"
            ],
            'displ': [
                "displacement",
                "displace",
                "disp"
            ]
        }
        return textype_names

    def tex_input_slot(self):
        INPUT_SLOTS = {
            'diffuse': 0,
            'ao': 1,
            'spec': 5,
            'rough': 7,
            'gloss': 7,
            'metal': 14,
            'opc': 47,
            'emissive': 48,
            'normal': 49,
            'bump': 49
        }
        return INPUT_SLOTS

    def create_empty_shadernetwork(self):
        """Create asset's SOP shader network.

        Example:
            sceneRoot = hou.node('/obj/')
            name = "char_nono"
            create_empty_shadernetwork(name)

        Args:
            asset_name(str): name of the asset

        Returns:
            hou.Nodes

        """
        NODE_COLOR = (0.282353, 0.819608, 0.8)
        NODE_POS = (3, 0)

        custom_name = self.ui.sel_asset_name.text().upper()

        scene_root = hou.node('/obj/')
        shaderpack_name = 'SHADER_' + custom_name
        shaderpack_root = '/obj/' + shaderpack_name
        if hou.node(shaderpack_root):
            hou.node(shaderpack_root).destroy()
        else:
            pass
        shaderpack_node = scene_root.createNode('geo', shaderpack_name)
        shaderpack_node.setColor(hou.Color(*NODE_COLOR))

        shaderpack_node.createNode('shopnet', 'shopnet')
        shaderpack_node.createNode('matnet', 'matnet').setPosition(
            hou.Vector2(*NODE_POS)
        )

    def createShaders(self):
        # get shader builder node name by user
        self.customName = self.ui.sel_asset_name.text().upper()

        # set node's color
        NODE_COLOR = (0.282353, 0.819608, 0.8)
        NODE_SHADER_COLOR = (0.145, 0.667, 0.557)
        NODE_TEX_COLOR = (1, 0.725, 0)

        if self.customName:
            if self.ui.collectDirLine.text():
                path = self.ui.collectDirLine.text()
                tex_items = self.textureList(path)

                # create shader builder and define node name
                shaderpack_name = 'SHADER_' + self.customName
                shaderpack_root = '/obj/' + shaderpack_name
                matpack_root = '/obj/' + shaderpack_name + '/matnet'
                shaderpack_node = hou.node(shaderpack_root)
                matpack_node = hou.node(matpack_root)
                mat_builder_node = matpack_node.createNode(
                    "redshift_vopnet",
                    "MAT_" + self.customName)
                mat_builder_node.setColor(hou.Color(*NODE_COLOR))
                mat_node = mat_builder_node.createNode("redshift::Material")
                mat_node.setColor(hou.Color(*NODE_SHADER_COLOR))
                mat_out_node = hou.node(matpack_root
                                        + "/%s/redshift_material1"
                                        % mat_builder_node.name()
                                        )
                mat_out_node.setInput(0, mat_node)
                mat_out_node.setColor(hou.Color(0, 0, 0))

                for tex in tex_items:
                    image_path = os.path.join(path, tex)
                    image_name = ('.').join(tex.split('.')[:-1])
                    image_type = re.split(r'[ _.]', image_name.lower())[-1]
                    tmp = mat_builder_node.createNode(
                        'redshift::TextureSampler', image_name)
                    tmp.parm('tex0').set(image_path.replace("\\", "/"))
                    tmp.setColor(hou.Color(*NODE_TEX_COLOR))
                    for item in self.textureType():
                        if image_type in self.textureType()[item]:
                            if item == 'opc':
                                opc_node1 = mat_builder_node.createNode(
                                    'redshift::RSMathInvColor')
                                opc_node1.setInput(0, tmp)
                                opc_node2 = mat_builder_node.createNode(
                                    'redshift::RSColorCorrection')
                                opc_node2.setInput(0, tmp)
                                mat_node.setInput(16, opc_node1)
                                mat_node.setInput(self.tex_input_slot()[
                                                  'opc'], opc_node2)
                            elif item == 'bump':
                                bump_node1 = mat_builder_node.createNode(
                                    'redshift::Displacement')
                                bump_node1.setInput(0, tmp)
                                mat_out_node.setInput(1, bump_node1)
                            else:
                                mat_node.setInput(
                                    self.tex_input_slot()[item], tmp)
                mat_builder_node.layoutChildren()
                shaderpack_node.setCurrent(on=True, clear_all_selected=True)
                shaderpack_node.setDisplayFlag(True)

                win.close()
                hou.ui.displayMessage('Done !')
            else:
                hou.ui.displayMessage('Please select "Textures Path" !')
        else:
            hou.ui.displayMessage(
                'Please select asset node in "Asset Model" !')

    def textureList(self, tex_path):
        path = os.path.abspath(tex_path)
        list_name = {}
        types = ["jpg", "exr", "bmp", "tga", "tiff",
                 "jpeg", "hdr", "pic", "png", "UDIM"]

        for file in os.listdir(path):
            if self.ui.checkBox.isChecked():
                asset_name = self.ui.customNameEdit.text()
                asset_type = file.split('.')[-1]
                if asset_name:
                    if asset_name in file:
                        if asset_type in types:
                            if asset_name in list_name:
                                list_name[asset_name].append(file)
                            else:
                                list_name[asset_name] = list()
                                list_name[asset_name].append(file)
                        else:
                            pass
                else:
                    hou.ui.displayMessage(
                        'Please type in "Asset Name and Texture set" !')
                    break
            else:
                if file.count('.') > 1 and file.count('.') < 4:
                    asset_name = ('.').join(file.split('.')[:-2])
                    asset_type = file.split('.')[-1]
                    if asset_type in types:
                        if asset_name in list_name:
                            list_name[asset_name].append(file)
                        else:
                            list_name[asset_name] = list()
                            list_name[asset_name].append(file)
                    else:
                        pass
        return list_name[asset_name]


win = ShaderCreator()
win.show()
