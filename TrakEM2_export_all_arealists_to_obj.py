"""
Script to extract all arealists in trakem2 project to .obj

author: Ben Mulcahy

Modified from https://imagej.net/plugins/trakem2/scripting
"""
from ini.trakem2.display import Display
from org.scijava.vecmath import Color3f
from customnode import WavefrontExporter, CustomTriangleMesh
from java.io import StringWriter
from ij.text import TextWindow

out_path = "/Users/benmulcahy/Desktop/test/" # Change me

for seg in Display.getFront().getLayerSet().getZDisplayables():
# Get the selected AreaList
	arealist = seg

# Create the triangle mesh with resample of 1 (no resampling)
# CAUTION: may take a long time. Try first with a resampling of at least 10.
	resample = 2
	triangles = arealist.generateTriangles(1, resample)

# Prepare a 3D Viewer object to provide interpretation
	color = Color3f(1.0, 1.0, 0.0)
	transparency = 0.0
	mesh = CustomTriangleMesh(triangles, color, transparency)

# Write the mesh as Wavefront
	name = str(arealist)
	m = {name : mesh}
	meshData = StringWriter()
	materialData = StringWriter()
	materialFileName = name + ".mtl"
	WavefrontExporter.save(m, materialFileName, meshData, materialData)

# Save the files in selected folder
	obj_data = meshData.toString()
	mtl_data = materialData.toString()

# Save the files
	obj_out = out_path + str(name) + ".obj"
	mtl_out = out_path + str(name) + ".mtl"
	with open(obj_out, "w") as output:
	    output.write(obj_data)
	with open(mtl_out, "w") as output:
	    output.write(mtl_data)
