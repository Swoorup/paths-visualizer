__author__ = 'Swoorup'
import sapaths
import imp
imp.reload(sapaths)

paths = sapaths.SAPaths()
paths.load_nodes_from_directory(r"E:\paths-visualizer\Vanilla\Compiled\OpenVice")