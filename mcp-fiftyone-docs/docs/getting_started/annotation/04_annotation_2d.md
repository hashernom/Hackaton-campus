[ Run in Google Colab ](https://colab.research.google.com/github/voxel51/fiftyone/blob/main/docs/source/getting_started/annotation/04_annotation_2d.ipynb) |  [ View source on GitHub ](https://github.com/voxel51/fiftyone/blob/main/docs/source/getting_started/annotation/04_annotation_2d.ipynb) |  [ Download notebook ](https://raw.githubusercontent.com/voxel51/fiftyone/main/docs/source/getting_started/annotation/04_annotation_2d.ipynb)

# Step 4: 2D Annotation + QA#

Now we annotate the selected batch. This step covers:

  1. Setting up a consistent annotation schema (KITTI classes)
  2. Annotating 2D detections on the **left camera slice**
  3. QA checks before moving to 3D annotation



> **Time commitment:** Plan 1-2 minutes per scene for careful annotation. Start with 10-20 scenes to get the workflow, then continue or use the fast-forward option.
    
    
    [ ]:
    
    
    
    import fiftyone as fo
    from fiftyone import ViewField as F
    
    dataset = fo.load_dataset("annotation_tutorial")
    batch_v0 = dataset.load_saved_view("batch_v0")
    
    # Get left camera slice from batch
    batch_v0_left = batch_v0.select_group_slices(["left"])
    
    print(f"Batch v0: {len(batch_v0.distinct('group.id'))} groups (scenes)")
    print(f"Left camera samples to annotate: {len(batch_v0_left)}")
    

## Define Your Schema (KITTI Classes)#

Before labeling, define the rules. This prevents class drift and maintains consistency. We use the standard KITTI classes for autonomous driving.
    
    
    [ ]:
    
    
    
    # Define annotation schema for 2D detections
    LABEL_FIELD_2D = "human_detections"
    
    SCHEMA_2D = {
        "field_name": LABEL_FIELD_2D,
        "classes": [
            "Car",
            "Van",
            "Truck",
            "Pedestrian",
            "Person_sitting",
            "Cyclist",
            "Tram",
            "Misc"  # catch-all for edge cases
        ]
    }
    
    SCHEMA_CLASSES_2D = set(SCHEMA_2D["classes"])
    
    # Store in dataset for reference
    dataset.info["annotation_schema_2d"] = SCHEMA_2D
    dataset.save()
    
    print(f"2D Schema defined: {len(SCHEMA_2D['classes'])} classes")
    print(f"Target field: {LABEL_FIELD_2D}")
    print(f"\nClasses: {SCHEMA_2D['classes']}")
    print(f"\nWhen you create a field in the App, name it exactly: {LABEL_FIELD_2D}")
    

## Annotate 2D Detections in the App#

**This is the real labeling step.** Open the App and annotate the left camera images.

### Setup (one time)#

  1. Launch the App with your batch
  2. Click a sample to open the modal
  3. **Select the ``left`` slice** from the slice dropdown
  4. Click the **Annotate** tab (pencil icon)
  5. Click **Schema** -> **New Field** -> name it `human_detections`
  6. Set type to **Detections** and add the KITTI classes above



### For each scene#

  1. Ensure youâre on the **left** slice
  2. Review the image
  3. Click **Detection** button (square icon)
  4. Draw boxes around all vehicles, pedestrians, cyclists
  5. Assign the correct KITTI class
  6. Move to the next scene



### Labeling Guidelines#

  * **Car** : Sedans, SUVs, hatchbacks
  * **Van** : Minivans, cargo vans
  * **Truck** : Pickup trucks, semi-trucks
  * **Pedestrian** : Standing or walking people
  * **Person_sitting** : Seated people (benches, ground)
  * **Cyclist** : Person on bicycle
  * **Tram** : Streetcars, light rail
  * **Misc** : Ambiguous or other vehicles


    
    
    [ ]:
    
    
    
    # Launch App with batch view (left camera slice)
    session = fo.launch_app(batch_v0_left)
    

### Stop here and annotate samples#

Take 15-30 minutes to label some scenes. This is the core skill. When youâre done (or want to fast-forward), continue below.

* * *

## Fast-Forward Option#

If you want to proceed without labeling everything manually, set `FAST_FORWARD = True` below. This copies `ground_truth` labels to `human_detections` to simulate completed annotation.

> **Note:** In real projects, thereâs no shortcut. Label quality determines model quality.
    
    
    [ ]:
    
    
    
    # Set to True ONLY if you want to skip manual annotation
    FAST_FORWARD = False
    
    if FAST_FORWARD:
        print("Fast-forwarding: copying ground_truth to human_detections...")
        print(f"Filtering to schema classes: {SCHEMA_CLASSES_2D}")
    
        copied = 0
        skipped = 0
    
        # Only copy to left camera samples
        for sample in batch_v0_left:
            if sample.ground_truth:
                human_dets = []
                for det in sample.ground_truth.detections:
                    if det.label in SCHEMA_CLASSES_2D:
                        human_dets.append(fo.Detection(
                            label=det.label,
                            bounding_box=det.bounding_box,
                        ))
                        copied += 1
                    else:
                        skipped += 1
                sample[LABEL_FIELD_2D] = fo.Detections(detections=human_dets)
            else:
                sample[LABEL_FIELD_2D] = fo.Detections(detections=[])
            sample.save()
    
        print(f"Copied {copied} detections, skipped {skipped} (not in schema)")
    else:
        print("Using your manual annotations.")
        print(f"Make sure you created '{LABEL_FIELD_2D}' and labeled on the LEFT slice!")
    

## Mark Annotated Samples#

**Important:** We only mark samples as âannotatedâ if they actually have labels.
    
    
    [ ]:
    
    
    
    # Reload to see changes
    dataset.reload()
    
    # Check left camera samples in batch
    batch_left = dataset.match_tags("batch:v0").select_group_slices(["left"])
    
    if LABEL_FIELD_2D in dataset.get_field_schema():
        has_labels = batch_left.match(F(f"{LABEL_FIELD_2D}.detections").length() > 0)
        no_labels = batch_left.match(
            (F(LABEL_FIELD_2D) == None) | (F(f"{LABEL_FIELD_2D}.detections").length() == 0)
        )
    
        print(f"Batch v0 (left camera) status:")
        print(f"  With 2D labels: {len(has_labels)}")
        print(f"  Without labels: {len(no_labels)}")
    
        if len(has_labels) == 0:
            print(f"\n>>> No samples have labels in {LABEL_FIELD_2D}.")
            print(">>> Either label some samples in the App, or set FAST_FORWARD = True.")
        else:
            # Tag samples with labels as annotated_2d
            has_labels.tag_samples("annotated_2d:v0")
    
            # Tag all slices of annotated groups
            # Must iterate explicitly since F("group.id").is_in() does not work on grouped datasets
            annotated_group_ids = set(has_labels.distinct("group.id"))
    
            for slice_name in dataset.group_slices:
                view = dataset.select_group_slices([slice_name])
                for sample in view.iter_samples(autosave=True):
                    if sample.group.id in annotated_group_ids:
                        if "annotated:v0" not in sample.tags:
                            sample.tags.append("annotated:v0")
    
            print(f"\nTagged {len(has_labels)} left camera samples as annotated_2d:v0")
            print(f"Tagged all slices of {len(annotated_group_ids)} groups as annotated:v0")
    else:
        print(f"Field {LABEL_FIELD_2D} not found. Create it in the App first.")
    

## QA Checks#

Before moving to 3D annotation, verify 2D label quality.
    
    
    [ ]:
    
    
    
    # Get annotated left camera samples
    annotated_2d = dataset.match_tags("annotated_2d:v0")
    
    if len(annotated_2d) == 0:
        print("No 2D annotated samples yet. Complete the annotation step above.")
    else:
        print(f"QA Check 1: Label coverage")
        print(f"  Annotated samples (left camera): {len(annotated_2d)}")
    
    
    
    [ ]:
    
    
    
    # Check 2: Class distribution
    from collections import Counter
    
    if len(annotated_2d) > 0:
        all_labels = []
        for sample in annotated_2d:
            if sample[LABEL_FIELD_2D]:
                all_labels.extend([d.label for d in sample[LABEL_FIELD_2D].detections])
    
        print(f"\nQA Check 2: Class distribution ({len(all_labels)} total detections)")
        for label, count in Counter(all_labels).most_common():
            print(f"  {label}: {count}")
    
    
    
    [ ]:
    
    
    
    # Check 3: Unexpected classes
    if len(annotated_2d) > 0 and len(all_labels) > 0:
        actual = set(all_labels)
        unexpected = actual - SCHEMA_CLASSES_2D
    
        if unexpected:
            print(f"\nQA Check 3: Unexpected classes found: {unexpected}")
            print("   These don't match your schema. Review before training.")
        else:
            print(f"\nQA Check 3: All classes match schema")
    
    
    
    [ ]:
    
    
    
    # Check 4: Detection count per scene
    if len(annotated_2d) > 0:
        det_counts = [
            len(s[LABEL_FIELD_2D].detections)
            for s in annotated_2d
            if s[LABEL_FIELD_2D]
        ]
    
        print(f"\nQA Check 4: Detections per scene")
        print(f"  Min: {min(det_counts)}")
        print(f"  Max: {max(det_counts)}")
        print(f"  Mean: {sum(det_counts)/len(det_counts):.1f}")
    
        # Flag scenes with very few or very many detections
        low_det = [s for s in annotated_2d if s[LABEL_FIELD_2D] and len(s[LABEL_FIELD_2D].detections) < 2]
        if low_det:
            print(f"  \n  >>> {len(low_det)} scenes have <2 detections. Review for missed objects.")
    

## Summary#

You annotated 2D detections on the left camera slice:

  * Defined KITTI schema for consistency
  * Labeled samples in the App (or fast-forwarded)
  * **Only samples with actual labels** were marked as annotated
  * Ran QA checks: coverage, class distribution, schema compliance

**Artifacts:**

  * `human_detections` field with 2D bounding boxes
  * `annotated_2d:v0` tag on left camera samples with labels
  * `annotated:v0` tag on all slices of annotated groups

**Next:** Step 5 - 3D Annotation (cuboids on point clouds) IN THIS ARTICLE 
