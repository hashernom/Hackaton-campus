[ Run in Google Colab ](https://colab.research.google.com/github/voxel51/fiftyone/blob/main/docs/source/getting_started/annotation/05_annotation_3d.ipynb) |  [ View source on GitHub ](https://github.com/voxel51/fiftyone/blob/main/docs/source/getting_started/annotation/05_annotation_3d.ipynb) |  [ Download notebook ](https://raw.githubusercontent.com/voxel51/fiftyone/main/docs/source/getting_started/annotation/05_annotation_3d.ipynb)

# Step 5: 3D Annotation#

Now we annotate 3D cuboids on the point cloud slice. This step covers:

  1. Setting up a 3D annotation schema
  2. Using the 3D annotation tools (cuboids, transform controls)
  3. Understanding the annotation plane concept
  4. Viewing 3D labels projected onto 2D camera images



> **Tip:** Complete Step 4 (2D annotation) first. Having 2D labels as reference helps with 3D annotation consistency.
    
    
    [ ]:
    
    
    
    import fiftyone as fo
    from fiftyone import ViewField as F
    
    dataset = fo.load_dataset("annotation_tutorial")
    batch_v0 = dataset.load_saved_view("batch_v0")
    
    # Get point cloud slice from batch
    batch_v0_pcd = batch_v0.select_group_slices(["pcd"])
    
    print(f"Batch v0: {len(batch_v0.distinct('group.id'))} groups (scenes)")
    print(f"Point cloud samples to annotate: {len(batch_v0_pcd)}")
    

## Define Your 3D Schema#

For 3D cuboids, we use a subset of KITTI classes - focusing on objects that have clear 3D extent in point clouds.
    
    
    [ ]:
    
    
    
    # Define annotation schema for 3D cuboids
    LABEL_FIELD_3D = "human_cuboids"
    
    SCHEMA_3D = {
        "field_name": LABEL_FIELD_3D,
        "classes": [
            "Car",
            "Van",
            "Truck",
            "Pedestrian",
            "Cyclist"
        ]
    }
    
    SCHEMA_CLASSES_3D = set(SCHEMA_3D["classes"])
    
    # Store in dataset
    dataset.info["annotation_schema_3d"] = SCHEMA_3D
    dataset.save()
    
    print(f"3D Schema defined: {len(SCHEMA_3D['classes'])} classes")
    print(f"Target field: {LABEL_FIELD_3D}")
    print(f"\nClasses: {SCHEMA_3D['classes']}")
    print(f"\nWhen you create a field in the App, name it exactly: {LABEL_FIELD_3D}")
    

## 3D Annotation in the App#

### Getting to the 3D View#

  1. Launch the App with your batch
  2. Click a sample to open the modal
  3. **Select the ``pcd`` slice** from the slice dropdown
  4. The 3D visualizer will load the point cloud



### 3D Navigation#

  * **Rotate** : Left-click and drag
  * **Pan** : Right-click and drag (or Shift + left-click)
  * **Zoom** : Scroll wheel
  * **Preset views** : Press `1`, `2`, `3`, `4` for top/right/front/annotation-plane views


    
    
    [ ]:
    
    
    
    # Launch App with point cloud view
    session = fo.launch_app(batch_v0_pcd)
    

## Creating 3D Cuboids#

### Enter Annotate Mode#

  1. Click the **Annotate** tab (pencil icon)
  2. Click **Schema** -> **New Field** -> name it `human_cuboids`
  3. Set type to **Detections** and add the classes above



### Understanding the Annotation Plane#

The **annotation plane** is a virtual surface that determines where your clicks place vertices. By default, itâs the XY plane (ground level).

  * **Moving the plane** : Reposition to place vertices at different heights
  * **Why it matters** : Cuboid corners snap to this plane when you click



### Drawing a Cuboid#

  1. Click the **Cuboid** tool in the left toolbar
  2. Click to place the **first corner** on the annotation plane
  3. Click to place the **opposite corner** (defines the base rectangle)
  4. The cuboid is created with a default height
  5. Select a class from the dropdown



### Transform Controls#

After creating a cuboid, use transform controls to refine it: | Control | What it does  
---|---  
**Translation** | Move along X/Y/Z axes or XY/XZ/YZ planes  
**Rotation** | Rotate around X/Y/Z axes  
**Scaling** | Resize along X/Y/Z axes  
  
Click on a cuboid to select it, then use the transform handles.

## Camera Projections#

One of FiftyOneâs key 3D features is **camera projections** :

### Point Cloud Projections#

  * Flatten the 3D view to 2D planes (top-down, side views)

  * Useful for accurate positioning




### 2D Image Projections#

  * See the camera images in the 3D viewer dropdown

  * Your 3D cuboids are **projected onto the 2D images in real-time**

  * This helps verify that your 3D labels align with the 2D scene




To use camera projections:

  1. Look for the **projection dropdown** in the 3D viewer

  2. Select a camera (e.g., `left`)

  3. See your cuboids rendered on the 2D image




> **Note:** Camera projections require camera intrinsics/extrinsics to be defined in the dataset. The KITTI data in quickstart-groups should have these.

## Annotation Guidelines for 3D#

### Positioning#

  * Center the cuboid on the point cloud cluster representing the object

  * The base should touch the ground plane

  * Include all points belonging to the object




### Orientation#

  * Align the cuboidâs longest axis with the objectâs heading direction

  * For vehicles, the front should point in the driving direction




### Sizing#

  * Tightly fit the cuboid to the point cloud extent

  * Donât include points from other objects or ground




### Consistency with 2D#

  * Objects labeled in 2D should also be labeled in 3D (if visible in point cloud)

  * Use the same class for the same object across both modalities




* * *

## Fast-Forward Option#

If you want to skip manual 3D labeling, set `FAST_FORWARD = True` below.
    
    
    [ ]:
    
    
    
    # Set to True ONLY if you want to skip manual 3D annotation
    FAST_FORWARD = False
    
    if FAST_FORWARD:
        print("Fast-forwarding: copying 3D ground_truth to human_cuboids...")
        print(f"Filtering to schema classes: {SCHEMA_CLASSES_3D}")
    
        copied = 0
        skipped = 0
    
        for sample in batch_v0_pcd:
            if sample.ground_truth:
                human_cuboids = []
                for det in sample.ground_truth.detections:
                    if det.label in SCHEMA_CLASSES_3D:
                        # Copy the 3D detection
                        human_cuboids.append(fo.Detection(
                            label=det.label,
                            location=det.location if hasattr(det, 'location') else None,
                            dimensions=det.dimensions if hasattr(det, 'dimensions') else None,
                            rotation=det.rotation if hasattr(det, 'rotation') else None,
                        ))
                        copied += 1
                    else:
                        skipped += 1
                sample[LABEL_FIELD_3D] = fo.Detections(detections=human_cuboids)
            else:
                sample[LABEL_FIELD_3D] = fo.Detections(detections=[])
            sample.save()
    
        print(f"Copied {copied} cuboids, skipped {skipped} (not in schema)")
    else:
        print("Using your manual 3D annotations.")
        print(f"Make sure you created '{LABEL_FIELD_3D}' and labeled on the PCD slice!")
    
    
    
    [ ]:
    
    
    
    # Reload to see changes
    dataset.reload()
    
    # Check point cloud samples in batch
    batch_pcd = dataset.match_tags("batch:v0").select_group_slices(["pcd"])
    
    if LABEL_FIELD_3D in dataset.get_field_schema():
        has_labels = batch_pcd.match(F(f"{LABEL_FIELD_3D}.detections").length() > 0)
        no_labels = batch_pcd.match(
            (F(LABEL_FIELD_3D) == None) | (F(f"{LABEL_FIELD_3D}.detections").length() == 0)
        )
    
        print(f"Batch v0 (point cloud) status:")
        print(f"  With 3D labels: {len(has_labels)}")
        print(f"  Without labels: {len(no_labels)}")
    
        if len(has_labels) > 0:
            has_labels.tag_samples("annotated_3d:v0")
            print(f"\nTagged {len(has_labels)} point cloud samples as 'annotated_3d:v0'")
    else:
        print(f"Field '{LABEL_FIELD_3D}' not found. Create it in the App first.")
    

## QA Checks for 3D#
    
    
    [ ]:
    
    
    
    # Get annotated point cloud samples
    annotated_3d = dataset.match_tags("annotated_3d:v0")
    
    if len(annotated_3d) == 0:
        print("No 3D annotated samples yet.")
    else:
        print(f"QA Check: 3D Label coverage")
        print(f"  Annotated samples (point cloud): {len(annotated_3d)}")
    
    
    
    [ ]:
    
    
    
    # Class distribution for 3D
    from collections import Counter
    
    if len(annotated_3d) > 0:
        all_labels_3d = []
        for sample in annotated_3d:
            if sample[LABEL_FIELD_3D]:
                all_labels_3d.extend([d.label for d in sample[LABEL_FIELD_3D].detections])
    
        print(f"\n3D Class distribution ({len(all_labels_3d)} total cuboids)")
        for label, count in Counter(all_labels_3d).most_common():
            print(f"  {label}: {count}")
    
    
    
    [ ]:
    
    
    
    # Cross-check: scenes with 2D labels should have 3D labels
    LABEL_FIELD_2D = "human_detections"
    
    if LABEL_FIELD_2D in dataset.get_field_schema() and LABEL_FIELD_3D in dataset.get_field_schema():
        batch_left = dataset.match_tags("batch:v0").select_group_slices(["left"])
        batch_pcd = dataset.match_tags("batch:v0").select_group_slices(["pcd"])
    
        # Groups with 2D labels
        groups_2d = set(
            s.group.id for s in batch_left
            if s[LABEL_FIELD_2D] and len(s[LABEL_FIELD_2D].detections) > 0
        )
    
        # Groups with 3D labels
        groups_3d = set(
            s.group.id for s in batch_pcd
            if s[LABEL_FIELD_3D] and len(s[LABEL_FIELD_3D].detections) > 0
        )
    
        print(f"\nCross-modality check:")
        print(f"  Groups with 2D labels: {len(groups_2d)}")
        print(f"  Groups with 3D labels: {len(groups_3d)}")
        print(f"  Groups with both: {len(groups_2d & groups_3d)}")
    
        missing_3d = groups_2d - groups_3d
        if missing_3d:
            print(f"  >>> {len(missing_3d)} groups have 2D but not 3D labels")
    

## Summary#

You annotated 3D cuboids on the point cloud slice:

  * Defined a 3D schema (subset of KITTI classes)

  * Used the annotation plane and transform controls

  * Verified alignment using camera projections

  * Ran QA checks for coverage and cross-modality consistency




**Artifacts:**

  * `human_cuboids` field with 3D cuboid annotations

  * `annotated_3d:v0` tag on point cloud samples with labels




**Key Concept:** The 3Dâ2D camera projections let you verify that your 3D labels align with the 2D scene. This cross-modal validation is a key differentiator for multimodal annotation workflows.

**Next:** Step 6 - Train + Evaluate

IN THIS ARTICLE 
