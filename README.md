# paths-visualizer
A toolkit/add-on for designing paths seamlessly and accurately by using a mesh-based path network, instead of traditional spline ones. 
 
I have seen many total conversion mods usually the map overhaul ones with totally empty paths. I hope those mods can get some lively feeling through this. Even though we have 3ds max plugins for creating paths, i have found it un-intuitive and hard to actually use. It might be because we lacked documentation at that time. Also the tools represented the paths as splines which are actually difficult to get it right. I am talking about deniska or steve-m's scripts.

So I have been developing an add-on for modeling toolkit for creating paths. While R* probably actually used splines to represent paths judging from their paths.ipl its much easier to create them as a vertex-edge only mesh. To represent things like junction you can just easily extrude vertices, instead of adding intersected splines. If you are familiar with polygon modelling, pushing/pulling vertex there there isn't much to really know on using it.

This toolkit actually introduces a new common waypoint format in which games/3D modelling tools can import/export from/to respectively. However it only supports waypoint based paths at the moment. I am looking at the possibility of other games too such as manhunt.

Primarily GTA Vice City (paths.ipl) and GTA San Andreas (nodesXX.dat) will have full functionality that includes import/export functionality. You can even combine paths from one game to other and export to any of these games (useful for mods like GTA: State of Liberty or Platinum Serbs GTA LCxVCxSA).

However, at the moment you can only import vehicle paths from GTA IV and V (Need help on researching these format, especially flags). Navigational Meshes are also not supported, so you cant do pedestrian paths for rage engine. 
 
It is currently realized as a blender plugin. I have had a few requests for 3Ds max version too. There is no ETA yet, as I have got a bit more work to do.
 
## Currently Supported Features:
* Import/Export all paths from GTA VC
* All flags from VC have been discovered and you can edit them to through node or link attributes panel
* Visualize some attributes such as left or right lane into the modelling toolkit
* Edit Car, Boat and Ped path meshes seperately

# Installation
1. Download the repository as a folder.
2. Copy the folder to your scripts\addons folder.
3. Activate the addon from blender.

# Note
This is currently a WIP. Please report any bugs or issues.
