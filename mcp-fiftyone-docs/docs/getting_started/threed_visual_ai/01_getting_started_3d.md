[ Run in Google Colab ](https://colab.research.google.com/github/voxel51/fiftyone/blob/main/docs/source/getting_started/threed_visual_ai/01_getting_started_3d.ipynb) |  [ View source on GitHub ](https://github.com/voxel51/fiftyone/blob/main/docs/source/getting_started/threed_visual_ai/01_getting_started_3d.ipynb) |  [ Download notebook ](https://raw.githubusercontent.com/voxel51/fiftyone/main/docs/source/getting_started/threed_visual_ai/01_getting_started_3d.ipynb)

# Getting Started with 3D Datasets#

There are many different types of 3D datasets and ways to work with them. In this first tutorial, we will cover the very basics of loading and visualizing 3D datasets in FiftyOne.

## FiftyOne Scenes#

FiftyOne helps you manage your 3D samples with [fo.Scene()](https://docs.voxel51.com/api/fiftyone.core.threed.scene_3d.html#fiftyone.core.threed.scene_3d.Scene) otherwise known as FO3D files. An FO3D file encapsulates a 3D scene constructed using the [Scene](https://docs.voxel51.com/api/fiftyone.core.threed.scene_3d.html#fiftyone.core.threed.scene_3d.Scene) class, which provides methods to add, remove, and manipulate 3D objects in the scene. A scene is internally represented as a n-ary tree of 3D objects, where each object is a node in the tree. A 3D object is either a [3D mesh](https://docs.voxel51.com/api/fiftyone.core.threed.mesh.html), [point cloud](https://docs.voxel51.com/api/fiftyone.core.threed.pointcloud.html), or a [3D shape geometry](https://docs.voxel51.com/api/fiftyone.core.threed.shape_3d.html). A scene may be explicitly initialized with additional attributes, such as `camera`, `lights`, and `background`. By default, a scene is created with neutral lighting, and a perspective camera whose up is set to Y axis in a right-handed coordinate system. After a scene is constructed, it should be written to the disk using the scene.write() method, which serializes the scene into a lightweight FO3D file.

## How to Load a Sample#

Any Sample whose filepath is a file with extension `.fo3d` is recognized as a 3D sample, and datasets composed of 3D samples have media type 3d. You can store multiple 3D objects inside your `.fo3d` scene to create a single sample that encapsulates the scenario you are trying to cover. Letâs look at a basic example first:
    
    
    [ ]:
    
    
    
    import fiftyone as fo
    
    scene = fo.Scene()
    scene.camera = fo.PerspectiveCamera(up="Z")
    
    mesh = fo.GltfMesh("mesh", "mesh.glb")
    mesh.rotation = fo.Euler(90, 0, 0, degrees=True)
    
    sphere1 = fo.SphereGeometry("sphere1", radius=2.0)
    sphere1.position = [-1, 0, 0]
    sphere1.default_material.color = "red"
    
    sphere2 = fo.SphereGeometry("sphere2", radius=2.0)
    sphere2.position = [1, 0, 0]
    sphere2.default_material.color = "blue"
    
    scene.add(mesh, sphere1, sphere2)
    
    scene.write("/path/to/scene.fo3d")
    
    sample = fo.Sample(filepath="/path/to/scene.fo3d")
    
    dataset = fo.Dataset()
    dataset.add_sample(sample)
    
    print(dataset.media_type)  # 3d
    

In the above scene, we add my custom 3D object `mesh.glb` as well as 2 additional spheres into the scene. We make sure the positions are correct as well as customize the color. Afterwards we write the scene to its file. To modify an exising scene, load it via `Scene.from_fo3d()`, perform any necessary updates, and then re-write it to disk:
    
    
    [ ]:
    
    
    
    scene = fo.Scene.from_fo3d("/path/to/scene.fo3d")
    
    for node in scene.traverse():
        if isinstance(node, fo.SphereGeometry):
            node.visible = False
    
    scene.write("/path/to/scene.fo3d")
    

That covers the basics of `fo.Scene()` and `.fo3d` files. Now we will jump into specific file formats and how to load them.

## 3D Meshes#

A 3D mesh is a collection of vertices, edges, and faces that define the shape of a 3D object. Whereas some mesh formats store only the geometry of the mesh, others also store the material properties and textures of the mesh. If a mesh file contains material properties and textures, FiftyOne will automatically load and display them. You may also assign default material for your meshes by setting the default_material attribute of the mesh. In the absence of any material information, meshes are assigned a [MeshStandardMaterial](https://docs.voxel51.com/api/fiftyone.core.threed.html#fiftyone.core.threed.MeshStandardMaterial) with reasonable defaults that can also be dynamically configured from the app. Please refer to [material_3d](https://docs.voxel51.com/api/fiftyone.core.threed.material_3d.html) for more details. FiftyOne currently supports `GLTF`, `OBJ`, `PLY`, `STL`, and `FBX 7.x+` [mesh formats](https://docs.voxel51.com/api/fiftyone.core.threed.mesh.html).
    
    
    [ ]:
    
    
    
    import fiftyone as fo
    
    scene = fo.Scene()
    
    mesh1 = fo.GltfMesh("mesh1", "mesh.glb")
    mesh1.rotation = fo.Euler(90, 0, 0, degrees=True)
    
    mesh2 = fo.ObjMesh("mesh2", "mesh.obj")
    mesh3 = fo.PlyMesh("mesh3", "mesh.ply")
    mesh4 = fo.StlMesh("mesh4", "mesh.stl")
    mesh5 = fo.FbxMesh("mesh5", "mesh.fbx")
    
    scene.add(mesh1, mesh2, mesh3, mesh4, mesh5)
    
    scene.write("/path/to/scene.fo3d")
    

## 3D Point Clouds#

FiftyOne supports the PCD point cloud format. A code snippet to create a PCD object that can be added to a FiftyOne 3D scene is shown below:
    
    
    [ ]:
    
    
    
    import fiftyone as fo
    
    pcd = fo.PointCloud("my-pcd", "point-cloud.pcd")
    pcd.default_material.shading_mode = "custom"
    pcd.default_material.custom_color = "red"
    pcd.default_material.point_size = 2
    
    scene = fo.Scene()
    scene.add(pcd)
    
    scene.write("/path/to/scene.fo3d")
    

What is awesome about 3D Scenes and point clouds is that you can stack multiple in the same scene to mirror the different sensor outputs. You might have something like a LIDAR sensor paired with multiple RADAR sensors that all fire at the same interval. With FiftyOne, you visualize them all at once, or turn on and off point clouds as you prefer! IN THIS ARTICLE 
