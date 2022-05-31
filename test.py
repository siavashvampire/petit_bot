# from anytree import Node, RenderTree
# from anytree.exporter import DotExporter
#
# set_idea = Node("set_idea")
# # upload_pic = Node("upload_pic", parent=set_idea)
# # description = Node("description", parent=upload_pic)
# # same_uploader = Node("same_uploader", parent=description)
# # exist_stl = Node("exist_stl", parent=same_uploader)
# # name_of_innovator = Node("name_of_innovator", parent=same_uploader)
# # stl_link_es = Node("stl_link_es", parent=exist_stl)
# # stl_link_ni = Node("stl_link_ni", parent=name_of_innovator)
# # stl_file_es = Node("stl_file_es", parent=stl_link_es)
# # stl_file_ni = Node("stl_file_ni", parent=stl_link_ni)
# # overview_1 = Node("overview_1", parent=stl_link_ni)
# # overview_2 = Node("overview_2", parent=stl_link_es)
# # overview_3 = Node("overview_3", parent=stl_file_es)
# # upload_file = Node("upload_file", parent=stl_file_es)
# # overview_4 = Node("overview_4", parent=upload_file)
# # print(RenderTree(upload_pic))
# DotExporter(set_idea).to_picture("set_idea.png")

from anytree import Node, RenderTree
from anytree.exporter import DotExporter

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)
DotExporter(udo).to_picture("set_idea.png")
