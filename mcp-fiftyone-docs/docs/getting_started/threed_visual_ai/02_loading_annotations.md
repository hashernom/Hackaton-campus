[ Run in Google Colab ](https://colab.research.google.com/github/voxel51/fiftyone/blob/main/docs/source/getting_started/threed_visual_ai/02_loading_annotations.ipynb) |  [ View source on GitHub ](https://github.com/voxel51/fiftyone/blob/main/docs/source/getting_started/threed_visual_ai/02_loading_annotations.ipynb) |  [ Download notebook ](https://raw.githubusercontent.com/voxel51/fiftyone/main/docs/source/getting_started/threed_visual_ai/02_loading_annotations.ipynb)

# Getting Started with Loading 3D Annotations#

3D samples may contain any type and number of custom fields, including 3D detections and 3D polylines, which are natively visualizable by the [Appâs 3D visualizer](https://docs.voxel51.com/user_guide/app.html#using-the-3d-visualizer). Because 3D annotations are stored in dedicated fields of datasets rather than being embedded in FO3D files, they can be queried and filtered via dataset views and in the App just like other primitive/label fields. It looks like this:
    
    
    [ ]:
    
    
    
    import fiftyone as fo
    
    scene = fo.Scene()
    scene.add(fo.GltfMesh("mesh", "mesh.gltf"))
    scene.write("/path/to/scene.fo3d")
    
    detection = fo.Detection(
        label="vehicle",
        location=[0.47, 1.49, 69.44],
        dimensions=[2.85, 2.63, 12.34],
        rotation=[0, -1.56, 0],
    )
    
    sample = fo.Sample(
        filepath="/path/to/scene.fo3d",
        ground_truth=fo.Detections(detections=[detection]),
    )
    

Letâs break down the label a little bit more, diving into just exactly what `location`, `dimensions`, and `rotation` entail:
    
    
    [ ]:
    
    
    
    import fiftyone as fo
    
    # Object label
    label = "vehicle"
    
    # Object center `[x, y, z]` in scene coordinates
    location = [0.47, 1.49, 69.44]
    
    # Object dimensions `[x, y, z]` in scene units
    dimensions = [2.85, 2.63, 12.34]
    
    # Object rotation `[x, y, z]` around its center, in `[-pi, pi]`
    rotation = [0, -1.56, 0]
    
    # A 3D object detection
    detection = fo.Detection(
        label=label,
        location=location,
        dimensions=dimensions,
        rotation=rotation,
    )
    

Note here that scene coordinates are starting from `[0,0,0]` which almost always is the ego, or the location of where the sensor started. It does not map from any known global coordinates.

# 3D Polylines#

3D Polylines work much the same as the detection do! They are stored as a decdicated field on your dataset and needs the arguments `label` and `points3d`:
    
    
    [ ]:
    
    
    
    # Object label
    label = "lane"
    
    # A list of lists of `[x, y, z]` points in scene coordinates describing
    # the vertices of each shape in the polyline
    points3d = [[[-5, -99, -2], [-8, 99, -2]], [[4, -99, -2], [1, 99, -2]]]
    
    # A set of semantically related 3D polylines
    polyline = fo.Polyline(label=label, points3d=points3d)
    

Another note, notice how for 3D you dont use `Detection3D` or `Polyline3D` classes from FiftyOne. The label classes `Detection` and `Polyline` will automatically adjust given 2D or 3D inputs! IN THIS ARTICLE 
