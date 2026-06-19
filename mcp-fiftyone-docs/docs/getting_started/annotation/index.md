# Annotation Guide#

**Multimodal 2D/3D Annotation for Detection Datasets**

FiftyOneâs in-app annotation lets you create and edit labels directly in the Appâincluding 2D bounding boxes on images and 3D cuboids on point clouds. This guide offers two tracks depending on your goals.

## Choose Your Track#

Track | Level | Time | Best For  
---|---|---|---  
**Quickstart** | Beginner | 15-20 min | âDoes this work for me?â Try multimodal annotation immediately.  
**Full Loop** | Intermediate | 90-120 min | Build a complete curate â annotate â train â evaluate pipeline.  
  
Note

**These tracks are independent.** Quickstart uses the zoo dataset directly (ephemeral), Full Loop clones to `annotation_tutorial` (persistent). You can do both without conflict.

## Quickstart Track#

**Level:** Beginner | **Time:** 15-20 minutes

Jump straight to multimodal annotation:

  * [Quickstart: In-App Labeling in 15 Minutes](01_quickstart.html) \- Load grouped data, explore 2D/3D views, draw boxes




If in-app annotation fits your needs, check out the Full Loop for production workflows.

## Full Loop Track#

**Level:** Intermediate | **Time:** 90-120 minutes

A complete data-centric detection workflow with multimodal data. You should be comfortable with:

  * Basic Python and Jupyter notebooks

  * Train/val/test split concepts

  * What embeddings represent (conceptually)

  * Running a training loop (we use YOLOv8)




**Steps:**

  * [Step 2: Setup Data Splits](02_setup_splits.html) \- Clone dataset, create group-level splits (test, val, golden, pool)

  * [Step 3: Smart Sample Selection](03_smart_selection.html) \- Use diversity sampling to pick high-value scenes

  * [Step 4: 2D Annotation + QA](04_annotation_2d.html) \- Annotate 2D detections on camera images with QA discipline

  * [Step 5: 3D Annotation](05_annotation_3d.html) \- Annotate 3D cuboids on point clouds

  * [Step 6: Train + Evaluate](06_train_evaluate.html) \- Train YOLOv8, evaluate, analyze failure modes

  * [Step 7: Iteration Loop](07_iteration.html) \- Hybrid acquisition loop: coverage + targeted failure mining




## What Youâll Learn#

**Quickstart Track:**

  * What grouped datasets are (synchronized multi-sensor data)

  * Switching between 2D images and 3D point clouds

  * Creating detection bounding boxes in Annotate mode

  * Exploring 3D point cloud data




**Full Loop Track (adds):**

  * Group-level split discipline: frozen test set, golden QA, active pool

  * Diversity-based sample selection for efficient labeling

  * 2D annotation on camera images with QA workflows

  * 3D cuboid annotation on point clouds

  * Camera projections: seeing 3D labels on 2D images

  * Failure analysis to drive the next labeling batch

  * Iterative improvement without test set contamination




## When to Use In-App Annotation#

**Ideal for:**

  * Rapid prototyping and schema iteration

  * Model-in-the-loop correction workflows

  * QA passes and targeted refinement

  * Single annotator or small team projects

  * Multimodal data with synchronized 2D/3D views

  * Tight feedback loops between labeling and evaluation




**For large-scale annotation projects** , FiftyOneâs [annotation API](../../integrations/annotation.html#fiftyone-annotation) lets you orchestrate external annotation services while keeping FiftyOne as your central data hub for curation, QA, and model evaluation.

## Dataset#

Both tracks use the `quickstart-groups` datasetâa subset of KITTI with:

  * **Left/right camera images** (2D)

  * **Point cloud data** (3D LiDAR)

  * **200 scenes** with synchronized multi-sensor data




The dataset downloads automatically when you run the notebooks.
    
    
    import fiftyone as fo
    import fiftyone.zoo as foz
    
    dataset = foz.load_zoo_dataset("quickstart-groups")
    session = fo.launch_app(dataset)
    

## Ready to Begin?#

Click **Next** to start with the Quickstart track, or jump directly to [Step 2: Setup Data Splits](02_setup_splits.html) for the Full Loop.

IN THIS ARTICLE 
