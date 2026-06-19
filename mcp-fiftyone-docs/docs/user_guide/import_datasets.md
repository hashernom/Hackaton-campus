# Importing data into FiftyOne#

The first step to using FiftyOne is to load your data into a [dataset](using_datasets.html#using-datasets). FiftyOne supports automatic loading of datasets stored in various common formats. If your dataset is stored in a custom format, donât worry, FiftyOne also provides support for easily loading datasets in custom formats.

Check out the sections below to see which import pattern is the best fit for your data.

Note

Did you know? You can import media and/or labels from within the FiftyOne App by installing the [@voxel51/io](https://github.com/voxel51/fiftyone-plugins/tree/main/plugins/io) plugin!

Note

When you create a [`Dataset`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset"), its samples and all of their fields (metadata, labels, custom fields, etc.) are written to FiftyOneâs backing database.

**Important:** Samples only store the `filepath` to the media, not the raw media itself. FiftyOne does not create duplicate copies of your data!

## Custom formats#

The simplest and most flexible approach to loading your data into FiftyOne is to iterate over your data in a simple Python loop, create a [`Sample`](../api/fiftyone.utils.data.html#fiftyone.utils.data.Sample "fiftyone.core.sample.Sample") for each data + label(s) pair, and then add those samples to a [`Dataset`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset").

FiftyOne provides [label types](using_datasets.html#using-labels) for common tasks such as classification, detection, segmentation, and many more. The examples below give you a sense of the basic workflow for a few tasks.

Image classificationObject detectionLabeled videos3D scenes
    
    
     1import glob
     2import fiftyone as fo
     3
     4images_patt = "/path/to/images/*"
     5
     6# Ex: your custom label format
     7annotations = {
     8    "/path/to/images/000001.jpg": "dog",
     9    ....,
    10}
    11
    12# Create samples for your data
    13samples = []
    14for filepath in glob.glob(images_patt):
    15    sample = fo.Sample(filepath=filepath)
    16
    17    # Store classification in a field name of your choice
    18    label = annotations[filepath]
    19    sample["ground_truth"] = fo.Classification(label=label)
    20
    21    samples.append(sample)
    22
    23# Create dataset
    24dataset = fo.Dataset("my-classification-dataset")
    25dataset.add_samples(samples)
    
    
    
     1import glob
     2import fiftyone as fo
     3
     4images_patt = "/path/to/images/*"
     5
     6# Ex: your custom label format
     7annotations = {
     8    "/path/to/images/000001.jpg": [
     9        {"bbox": ..., "label": ...},
    10        ...
    11    ],
    12    ...
    13}
    14
    15# Create samples for your data
    16samples = []
    17for filepath in glob.glob(images_patt):
    18    sample = fo.Sample(filepath=filepath)
    19
    20    # Convert detections to FiftyOne format
    21    detections = []
    22    for obj in annotations[filepath]:
    23        label = obj["label"]
    24
    25        # Bounding box coordinates should be relative values
    26        # in [0, 1] in the following format:
    27        # [top-left-x, top-left-y, width, height]
    28        bounding_box = obj["bbox"]
    29
    30        detections.append(
    31            fo.Detection(label=label, bounding_box=bounding_box)
    32        )
    33
    34    # Store detections in a field name of your choice
    35    sample["ground_truth"] = fo.Detections(detections=detections)
    36
    37    samples.append(sample)
    38
    39# Create dataset
    40dataset = fo.Dataset("my-detection-dataset")
    41dataset.add_samples(samples)
    
    
    
     1import fiftyone as fo
     2
     3video_path = "/path/to/video.mp4"
     4
     5# Ex: your custom label format
     6frame_labels = {
     7    1: {
     8        "weather": "sunny",
     9        "objects": [
    10            {
    11                "label": ...
    12                "bbox": ...
    13            },
    14            ...
    15        ]
    16    },
    17    ...
    18}
    19
    20# Create video sample with frame labels
    21sample = fo.Sample(filepath=video_path)
    22for frame_number, labels in frame_labels.items():
    23    frame = fo.Frame()
    24
    25    # Store a frame classification
    26    weather = labels["weather"]
    27    frame["weather"] = fo.Classification(label=weather)
    28
    29    # Convert detections to FiftyOne format
    30    detections = []
    31    for obj in labels["objects"]:
    32        label = obj["label"]
    33
    34        # Bounding box coordinates should be relative values
    35        # in [0, 1] in the following format:
    36        # [top-left-x, top-left-y, width, height]
    37        bounding_box = obj["bbox"]
    38
    39        detections.append(
    40            fo.Detection(label=label, bounding_box=bounding_box)
    41        )
    42
    43    # Store object detections
    44    frame["objects"] = fo.Detections(detections=detections)
    45
    46    # Add frame to sample
    47    sample.frames[frame_number] = frame
    48
    49# Create dataset
    50dataset = fo.Dataset("my-labeled-video-dataset")
    51dataset.add_sample(sample)
    
    
    
     1import fiftyone as fo
     2
     3# Create a 3D scene with a mesh
     4scene = fo.Scene()
     5scene.add(fo.GltfMesh("mesh", "mesh.gltf"))
     6scene.write("/path/to/scene.fo3d")
     7
     8# Define a 3D cuboid
     9detection = fo.Detection(
    10    label="vehicle",
    11    location=[0.47, 1.49, 69.44],
    12    dimensions=[2.85, 2.63, 12.34],
    13    rotation=[0, -1.56, 0],
    14)
    15
    16# Construct a sample representing the scene
    17sample = fo.Sample(
    18    filepath="/path/to/scene.fo3d",
    19    ground_truth=fo.Detections(detections=[detection]),
    20)
    21
    22# Create dataset
    23dataset = fo.Dataset("my-3d-dataset")
    24dataset.add_sample(sample)
    

Note

Using [`Dataset.add_samples()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.add_samples "fiftyone.core.dataset.Dataset.add_samples") to add batches of samples to your datasets can be significantly more efficient than adding samples one-by-one via [`Dataset.add_sample()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.add_sample "fiftyone.core.dataset.Dataset.add_sample").

Note

If you use the same custom data format frequently in your workflows, then writing a custom dataset importer is a great way to abstract and streamline the loading of your data into FiftyOne.

## Common formats#

If your data is stored on disk in one of the many common formats supported natively by FiftyOne, then you can load your data into a [`Dataset`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") via Python or the CLI with the following simple pattern:

PythonCLI

You can import a [`Dataset`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") from disk via the [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") factory method.

If your data is stored in the canonical format of the type youâre importing, then you can load it by providing the `dataset_dir` and `dataset_type` parameters:
    
    
     1import fiftyone as fo
     2
     3# The directory containing the dataset to import
     4dataset_dir = "/path/to/dataset"
     5
     6# The type of the dataset being imported
     7dataset_type = fo.types.COCODetectionDataset  # for example
     8
     9# Import the dataset
    10dataset = fo.Dataset.from_dir(
    11    dataset_dir=dataset_dir,
    12    dataset_type=dataset_type,
    13)
    

Alternatively, when importing labeled datasets in formats such as COCO, you may find it more natural to provide the `data_path` and `labels_path` parameters to independently specify the location of the source media on disk and the annotations file containing the labels to import:
    
    
     1# The directory containing the source images
     2data_path = "/path/to/images"
     3
     4# The path to the COCO labels JSON file
     5labels_path = "/path/to/coco-labels.json"
     6
     7# Import the dataset
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.COCODetectionDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12)
    

Many formats like COCO also support storing absolute filepaths to the source media directly in the labels, in which case you can provide only the `labels_path` parameter:
    
    
    1# The path to a COCO labels JSON file containing absolute image paths
    2labels_path = "/path/to/coco-labels.json"
    3
    4# Import the dataset
    5dataset = fo.Dataset.from_dir(
    6    dataset_type=fo.types.COCODetectionDataset,
    7    labels_path=labels_path,
    8)
    

In general, you can pass any parameter for the [`DatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.DatasetImporter "fiftyone.utils.data.importers.DatasetImporter") of the format youâre importing to [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir"). For example, most builtin importers support optional `max_samples`, `shuffle`, and `seed` parameters, which provide support for importing a small subset of a potentially large dataset:
    
    
    1# Import a random subset of 10 samples from the dataset
    2dataset = fo.Dataset.from_dir(
    3    ...,
    4    max_samples=10,
    5    shuffle=True,
    6    seed=51,
    7)
    

You can import a dataset from disk into FiftyOne [via the CLI](../cli/index.html#cli-fiftyone-datasets-create).

If your data is stored in the canonical format of the type youâre importing, then you can load it by providing the `--dataset-dir` and `--type` options:
    
    
    # A name for the dataset
    NAME=my-dataset
    
    # The directory containing the dataset to import
    DATASET_DIR=/path/to/dataset
    
    # The type of the dataset being imported
    # Any subclass of `fiftyone.types.Dataset` is supported
    TYPE=fiftyone.types.COCODetectionDataset  # for example
    
    # Import the dataset
    fiftyone datasets create --name $NAME --dataset-dir $DATASET_DIR --type $TYPE
    

Alternatively, when importing labeled datasets in formats such as COCO, you may find it more natural to provide the `data_path` and `labels_path` parameters via the [kwargs option](../cli/index.html#cli-fiftyone-datasets-create) to independently specify the location of the source media on disk and the annotations file containing the labels to import:
    
    
    # The directory containing the source images
    DATA_PATH=/path/to/images
    
    # The path to the COCO labels JSON file
    LABELS_PATH=/path/to/coco-labels.json
    
    # Import the dataset
    fiftyone datasets create --name my-dataset \
        --type fiftyone.types.COCODetectionDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Many formats like COCO also support storing absolute filepaths to the source media directly in the labels, in which case you can provide only the `labels_path` parameter:
    
    
    # The path to a COCO labels JSON file containing absolute image paths
    LABELS_PATH=/path/to/coco-labels.json
    
    # Import the dataset
    fiftyone datasets create --name my-dataset \
        --type fiftyone.types.COCODetectionDataset \
        --kwargs labels_path=$LABELS_PATH
    

In general, you can pass any parameter for the [`DatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.DatasetImporter "fiftyone.utils.data.importers.DatasetImporter") of the format youâre importing via the [kwargs option](../cli/index.html#cli-fiftyone-datasets-create). For example, most builtin importers support optional `max_samples`, `shuffle`, and `seed` parameters, which provide support for importing a small subset of a potentially large dataset:
    
    
    # Import a random subset of 10 samples from the dataset
    fiftyone datasets create \
        --name $NAME --dataset-dir $DATASET_DIR --type $TYPE \
        --kwargs \
            max_samples=10 \
            shuffle=True \
            seed=51
    

Note

Jump to this section to see a full list of supported import formats.

Note

Did you know? You can write custom importers to streamline import of data in custom formats.

## Loading media#

If youâre just getting started with a project and all you have is a bunch of media files, you can easily load them into a FiftyOne dataset and start visualizing them [in the App](app.html#fiftyone-app).

ImagesVideos

You can use the [`Dataset.from_images()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_images "fiftyone.core.dataset.Dataset.from_images"), [`Dataset.from_images_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_images_dir "fiftyone.core.dataset.Dataset.from_images_dir"), and [`Dataset.from_images_patt()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_images_patt "fiftyone.core.dataset.Dataset.from_images_patt") factory methods to load your images into FiftyOne:
    
    
     1import fiftyone as fo
     2
     3# Create a dataset from a list of images
     4dataset = fo.Dataset.from_images(
     5    ["/path/to/image1.jpg", "/path/to/image2.jpg", ...]
     6)
     7
     8# Create a dataset from a directory of images
     9dataset = fo.Dataset.from_images_dir("/path/to/images")
    10
    11# Create a dataset from a glob pattern of images
    12dataset = fo.Dataset.from_images_patt("/path/to/images/*.jpg")
    13
    14session = fo.launch_app(dataset)
    

You can also use [`Dataset.add_images()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.add_images "fiftyone.core.dataset.Dataset.add_images"), [`Dataset.add_images_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.add_images_dir "fiftyone.core.dataset.Dataset.add_images_dir"), and [`Dataset.add_images_patt()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.add_images_patt "fiftyone.core.dataset.Dataset.add_images_patt") to add images to an existing dataset.

You can use the [fiftyone app view](../cli/index.html#cli-fiftyone-app-view) command from the CLI to quickly browse images in the App without creating a (persistent) FiftyOne dataset:
    
    
    # View a glob pattern of images in the App
    fiftyone app view --images-patt '/path/to/images/*.jpg'
    
    # View a directory of images in the App
    fiftyone app view --images-dir '/path/to/images'
    

You can use the [`Dataset.from_videos()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_videos "fiftyone.core.dataset.Dataset.from_videos"), [`Dataset.from_videos_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_videos_dir "fiftyone.core.dataset.Dataset.from_videos_dir"), and [`Dataset.from_videos_patt()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_videos_patt "fiftyone.core.dataset.Dataset.from_videos_patt") factory methods to load your videos into FiftyOne:
    
    
     1import fiftyone as fo
     2
     3# Create a dataset from a list of videos
     4dataset = fo.Dataset.from_videos(
     5    ["/path/to/video1.mp4", "/path/to/video2.mp4", ...]
     6)
     7
     8# Create a dataset from a directory of videos
     9dataset = fo.Dataset.from_videos_dir("/path/to/videos")
    10
    11# Create a dataset from a glob pattern of videos
    12dataset = fo.Dataset.from_videos_patt("/path/to/videos/*.mp4")
    13
    14session = fo.launch_app(dataset)
    

You can also use [`Dataset.add_videos()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.add_videos "fiftyone.core.dataset.Dataset.add_videos"), [`Dataset.add_videos_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.add_videos_dir "fiftyone.core.dataset.Dataset.add_videos_dir"), and [`Dataset.add_videos_patt()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.add_videos_patt "fiftyone.core.dataset.Dataset.add_videos_patt") to add videos to an existing dataset.

You can use the [fiftyone app view](../cli/index.html#cli-fiftyone-app-view) command from the CLI to quickly browse videos in the App without creating a (persistent) FiftyOne dataset:
    
    
    # View a glob pattern of videos in the App
    fiftyone app view --videos-patt '/path/to/videos/*.mp4'
    
    # View a directory of videos in the App
    fiftyone app view --videos-dir '/path/to/videos'
    

## Adding model predictions#

Once youâve created a dataset and ground truth labels, you can easily add model predictions to take advantage of FiftyOneâs [evaluation capabilities](evaluation.html#evaluating-models).

COCOYOLOOther formats

If you have model predictions stored in COCO format, then you can use [`add_coco_labels()`](../api/fiftyone.utils.coco.html#fiftyone.utils.coco.add_coco_labels "fiftyone.utils.coco.add_coco_labels") to conveniently add the labels to an existing dataset.

The example below demonstrates a round-trip export and then re-import of both images-and-labels and labels-only data in COCO format:
    
    
     1import fiftyone as fo
     2import fiftyone.zoo as foz
     3import fiftyone.utils.coco as fouc
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6classes = dataset.distinct("predictions.detections.label")
     7
     8# Export images and ground truth labels to disk
     9dataset.export(
    10    export_dir="/tmp/coco",
    11    dataset_type=fo.types.COCODetectionDataset,
    12    label_field="ground_truth",
    13    classes=classes,
    14)
    15
    16# Export predictions
    17dataset.export(
    18    dataset_type=fo.types.COCODetectionDataset,
    19    labels_path="/tmp/coco/predictions.json",
    20    label_field="predictions",
    21    classes=classes,
    22)
    23
    24# Now load ground truth labels into a new dataset
    25dataset2 = fo.Dataset.from_dir(
    26    dataset_dir="/tmp/coco",
    27    dataset_type=fo.types.COCODetectionDataset,
    28    label_field="ground_truth",
    29    label_types="detections",
    30)
    31
    32# And add model predictions
    33fouc.add_coco_labels(
    34    dataset2,
    35    "predictions",
    36    "/tmp/coco/predictions.json",
    37    classes,
    38)
    39
    40# Verify that ground truth and predictions were imported as expected
    41print(dataset.count("ground_truth.detections"))
    42print(dataset2.count("ground_truth.detections"))
    43print(dataset.count("predictions.detections"))
    44print(dataset2.count("predictions.detections"))
    

Note

See [`add_coco_labels()`](../api/fiftyone.utils.coco.html#fiftyone.utils.coco.add_coco_labels "fiftyone.utils.coco.add_coco_labels") for a complete description of the available syntaxes for loading COCO-formatted predictions to an existing dataset.

If you have model predictions stored in YOLO format, then you can use [`add_yolo_labels()`](../api/fiftyone.utils.yolo.html#fiftyone.utils.yolo.add_yolo_labels "fiftyone.utils.yolo.add_yolo_labels") to conveniently add the labels to an existing dataset.

The example below demonstrates a round-trip export and then re-import of both images-and-labels and labels-only data in YOLO format:
    
    
     1import fiftyone as fo
     2import fiftyone.zoo as foz
     3import fiftyone.utils.yolo as fouy
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6classes = dataset.distinct("predictions.detections.label")
     7
     8# Export images and ground truth labels to disk
     9dataset.export(
    10    export_dir="/tmp/yolov4",
    11    dataset_type=fo.types.YOLOv4Dataset,
    12    label_field="ground_truth",
    13    classes=classes,
    14)
    15
    16# Export predictions
    17dataset.export(
    18    dataset_type=fo.types.YOLOv4Dataset,
    19    labels_path="/tmp/yolov4/predictions",
    20    label_field="predictions",
    21    classes=classes,
    22)
    23
    24# Now load ground truth labels into a new dataset
    25dataset2 = fo.Dataset.from_dir(
    26    dataset_dir="/tmp/yolov4",
    27    dataset_type=fo.types.YOLOv4Dataset,
    28    label_field="ground_truth",
    29)
    30
    31# And add model predictions
    32fouy.add_yolo_labels(
    33    dataset2,
    34    "predictions",
    35    "/tmp/yolov4/predictions",
    36    classes,
    37)
    38
    39# Verify that ground truth and predictions were imported as expected
    40print(dataset.count("ground_truth.detections"))
    41print(dataset2.count("ground_truth.detections"))
    42print(dataset.count("predictions.detections"))
    43print(dataset2.count("predictions.detections"))
    

Note

See [`add_yolo_labels()`](../api/fiftyone.utils.yolo.html#fiftyone.utils.yolo.add_yolo_labels "fiftyone.utils.yolo.add_yolo_labels") for a complete description of the available syntaxes for loading YOLO-formatted predictions to an existing dataset.

Model predictions stored in other formats can always be loaded iteratively through a simple Python loop.

The example below shows how to add object detection predictions to a dataset, but many [other label types](using_datasets.html#using-labels) are also supported.
    
    
     1import fiftyone as fo
     2
     3# Ex: your custom predictions format
     4predictions = {
     5    "/path/to/images/000001.jpg": [
     6        {"bbox": ..., "label": ..., "score": ...},
     7        ...
     8    ],
     9    ...
    10}
    11
    12# Add predictions to your samples
    13for sample in dataset:
    14    filepath = sample.filepath
    15
    16    # Convert predictions to FiftyOne format
    17    detections = []
    18    for obj in predictions[filepath]:
    19        label = obj["label"]
    20        confidence = obj["score"]
    21
    22        # Bounding box coordinates should be relative values
    23        # in [0, 1] in the following format:
    24        # [top-left-x, top-left-y, width, height]
    25        bounding_box = obj["bbox"]
    26
    27        detections.append(
    28            fo.Detection(
    29                label=label,
    30                bounding_box=bounding_box,
    31                confidence=confidence,
    32            )
    33        )
    34
    35    # Store detections in a field name of your choice
    36    sample["predictions"] = fo.Detections(detections=detections)
    37
    38    sample.save()
    

Note

If you are in need of a model to run on your dataset, check out the [FiftyOne Model Zoo](../model_zoo/index.html#model-zoo).

## Built-in formats#

FiftyOne provides a variety of built-in importers for common data formats.

Each data format is represented by a subclass of [`fiftyone.types.Dataset`](../api/fiftyone.types.html#fiftyone.types.Dataset "fiftyone.types.Dataset"), which is used by the Python library and CLI to refer to the corresponding dataset format when reading the dataset from disk.

Dataset Type | Description  
---|---  
Image Directory | A directory of images.  
Video Directory | A directory of videos.  
Media Directory | A directory of media files.  
Image Classification Directory Tree | A directory tree whose subfolders define an image classification dataset.  
Video Classification Directory Tree | A directory tree whose subfolders define a video classification dataset.  
FiftyOne Image Classification | A labeled dataset consisting of images and their associated classification labels in a simple JSON format.  
TF Image Classification | A labeled dataset consisting of images and their associated classification labels stored as TFRecords.  
COCO | A labeled dataset consisting of images and their associated object detections saved in [COCO Object Detection Format](https://cocodataset.org/#format-data).  
VOC | A labeled dataset consisting of images and their associated object detections saved in [VOC format](http://host.robots.ox.ac.uk/pascal/VOC).  
KITTI | A labeled dataset consisting of images and their associated object detections saved in [KITTI format](http://www.cvlibs.net/datasets/kitti/eval_object.php).  
YOLOv4 | A labeled dataset consisting of images and their associated object detections saved in [YOLOv4 format](https://github.com/AlexeyAB/darknet).  
YOLOv5 | A labeled dataset consisting of images and their associated object detections saved in [YOLOv5 format](https://github.com/ultralytics/yolov5).  
FiftyOne Object Detection | A labeled dataset consisting of images and their associated object detections stored in a simple JSON format.  
FiftyOne Temporal Detection | A labeled dataset consisting of videos and their associated temporal detections in a simple JSON format.  
TF Object Detection | A labeled dataset consisting of images and their associated object detections stored as TFRecords in [TF Object Detection API format ](https://github.com/tensorflow/models/blob/master/research/object_detection).  
Image Segmentation Directory | A labeled dataset consisting of images and their associated semantic segmentations stored as images on disk.  
CVAT Image | A labeled dataset consisting of images and their associated multitask labels stored in [CVAT image format](https://github.com/opencv/cvat).  
CVAT Video | A labeled dataset consisting of videos and their associated multitask labels stored in [CVAT video format](https://github.com/opencv/cvat).  
OpenLABEL Image | A labeled dataset consisting of images and their associated multitask labels stored in [OpenLABEL format](https://www.asam.net/standards/detail/openlabel/).  
OpenLABEL Video | A labeled dataset consisting of videos and their associated multitask labels stored in [OpenLABEL format](https://www.asam.net/standards/detail/openlabel/).  
BDD | A labeled dataset consisting of images and their associated multitask predictions saved in [Berkeley DeepDrive (BDD) format](http://bdd-data.berkeley.edu).  
CSV | A labeled dataset consisting of images or videos and their associated field values stored as columns of a CSV file.  
DICOM | An image dataset whose image data and optional properties are stored in [DICOM format](https://en.wikipedia.org/wiki/DICOM).  
GeoJSON | An image or video dataset whose location data and labels are stored in [GeoJSON format](https://en.wikipedia.org/wiki/GeoJSON).  
GeoTIFF | An image dataset whose image and geolocation data are stored in [GeoTIFF format](https://en.wikipedia.org/wiki/GeoTIFF).  
FiftyOne Dataset | A dataset consisting of an entire serialized [`Dataset`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") and its associated source media.  
FiftyOne Image Labels | A labeled dataset consisting of images and their associated multitask predictions stored in [ETA ImageLabels format ](https://github.com/voxel51/eta/blob/develop/docs/image_labels_guide.md).  
FiftyOne Video Labels | A labeled dataset consisting of videos and their associated multitask predictions stored in [ETA VideoLabels format ](https://github.com/voxel51/eta/blob/develop/docs/video_labels_guide.md).  
Custom formats | Import datasets in custom formats by defining your own [`Dataset`](../api/fiftyone.types.html#fiftyone.types.Dataset "fiftyone.types.Dataset") or [`DatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.DatasetImporter "fiftyone.utils.data.importers.DatasetImporter") class.  
  
## Image Directory#

The [`fiftyone.types.ImageDirectory`](../api/fiftyone.types.html#fiftyone.types.ImageDirectory "fiftyone.types.ImageDirectory") type represents a directory of images.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        <filename1>.<ext>
        <filename2>.<ext>
    

where files with non-image MIME types are omitted.

By default, the dataset may contain nested subfolders of images, which are recursively listed.

Note

See [`ImageDirectoryImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.ImageDirectoryImporter "fiftyone.utils.data.importers.ImageDirectoryImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a directory of images as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/images-dir"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.ImageDirectory,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/images-dir
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.ImageDirectory
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a directory of images in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/images-dir
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.ImageDirectory
    

## Video Directory#

The [`fiftyone.types.VideoDirectory`](../api/fiftyone.types.html#fiftyone.types.VideoDirectory "fiftyone.types.VideoDirectory") type represents a directory of videos.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        <filename1>.<ext>
        <filename2>.<ext>
    

where files with non-video MIME types are omitted.

By default, the dataset may contain nested subfolders of videos, which are recursively listed.

Note

See [`VideoDirectoryImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.VideoDirectoryImporter "fiftyone.utils.data.importers.VideoDirectoryImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a directory of videos as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/videos-dir"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.VideoDirectory,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/videos-dir
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.VideoDirectory
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a directory of videos in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/videos-dir
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.VideoDirectory
    

## Media Directory#

The [`fiftyone.types.MediaDirectory`](../api/fiftyone.types.html#fiftyone.types.MediaDirectory "fiftyone.types.MediaDirectory") type represents a directory of media files.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        <filename1>.<ext>
        <filename2>.<ext>
    

Note

All files must have the same media type (image, video, point cloud, etc.)

By default, the dataset may contain nested subfolders of media files, which are recursively listed.

Note

See [`MediaDirectoryImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.MediaDirectoryImporter "fiftyone.utils.data.importers.MediaDirectoryImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a directory of media files as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/media-dir"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.MediaDirectory,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/media-dir
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.MediaDirectory
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a directory of media in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/media-dir
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.MediaDirectory
    

## Image Classification Dir Tree#

The [`fiftyone.types.ImageClassificationDirectoryTree`](../api/fiftyone.types.html#fiftyone.types.ImageClassificationDirectoryTree "fiftyone.types.ImageClassificationDirectoryTree") type represents a directory tree whose subfolders define an image classification dataset.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        <classA>/
            <image1>.<ext>
            <image2>.<ext>
            ...
        <classB>/
            <image1>.<ext>
            <image2>.<ext>
            ...
        ...
    

Unlabeled images are stored in a subdirectory named `_unlabeled`.

Each class folder may contain nested subfolders of images.

Note

See [`ImageClassificationDirectoryTreeImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.ImageClassificationDirectoryTreeImporter "fiftyone.utils.data.importers.ImageClassificationDirectoryTreeImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from an image classification directory tree stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/image-classification-dir-tree"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.ImageClassificationDirectoryTree,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/image-classification-dir-tree
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.ImageClassificationDirectoryTree
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view an image classification directory tree in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/image-classification-dir-tree
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.ImageClassificationDirectoryTree
    

## Video Classification Dir Tree#

The [`fiftyone.types.VideoClassificationDirectoryTree`](../api/fiftyone.types.html#fiftyone.types.VideoClassificationDirectoryTree "fiftyone.types.VideoClassificationDirectoryTree") type represents a directory tree whose subfolders define a video classification dataset.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        <classA>/
            <video1>.<ext>
            <video2>.<ext>
            ...
        <classB>/
            <video1>.<ext>
            <video2>.<ext>
            ...
        ...
    

Unlabeled videos are stored in a subdirectory named `_unlabeled`.

Each class folder may contain nested subfolders of videos.

Note

See [`VideoClassificationDirectoryTreeImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.VideoClassificationDirectoryTreeImporter "fiftyone.utils.data.importers.VideoClassificationDirectoryTreeImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a video classification directory tree stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/video-classification-dir-tree"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.VideoClassificationDirectoryTree,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/video-classification-dir-tree
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.VideoClassificationDirectoryTree
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a video classification directory tree in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/video-classification-dir-tree
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.VideoClassificationDirectoryTree
    

## FiftyOne Image Classification#

The [`fiftyone.types.FiftyOneImageClassificationDataset`](../api/fiftyone.types.html#fiftyone.types.FiftyOneImageClassificationDataset "fiftyone.types.FiftyOneImageClassificationDataset") type represents a labeled dataset consisting of images and their associated classification label(s) stored in a simple JSON format.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels.json
    

In the simplest case, `labels.json` can be a JSON file in the following format:
    
    
    {
        "classes": [
            "<labelA>",
            "<labelB>",
            ...
        ],
        "labels": {
            "<uuid1>": <target>,
            "<uuid2>": <target>,
            ...
        }
    }
    

If the `classes` field is provided, the `target` values are class IDs that are mapped to class label strings via `classes[target]`. If no `classes` field is provided, then the `target` values directly store the label strings.

The target value in `labels` for unlabeled images is `None` (or missing).

The UUIDs can also be relative paths like `path/to/uuid`, in which case the images in `data/` should be arranged in nested subfolders with the corresponding names, or they can be absolute paths, in which case the images may or may not be in `data/`.

Alternatively, `labels.json` can contain predictions with associated confidences and additional attributes in the following format:
    
    
    {
        "classes": [
            "<labelA>",
            "<labelB>",
            ...
        ],
        "labels": {
            "<uuid1>": {
                "label": <target>,
                "confidence": <optional-confidence>,
                "attributes": {
                    <optional-name>: <optional-value>,
                    ...
                }
            },
            "<uuid2>": {
                "label": <target>,
                "confidence": <optional-confidence>,
                "attributes": {
                    <optional-name>: <optional-value>,
                    ...
                }
            },
            ...
        }
    }
    

You can also load multilabel classifications in this format by storing lists of targets in `labels.json`:
    
    
    {
        "classes": [
            "<labelA>",
            "<labelB>",
            ...
        ],
        "labels": {
            "<uuid1>": [<target1>, <target2>, ...],
            "<uuid2>": [<target1>, <target2>, ...],
            ...
        }
    }
    

where the target values in `labels` can be class strings, class IDs, or dicts in the format described above defining class labels, confidences, and optional attributes.

Note

See [`FiftyOneImageClassificationDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.FiftyOneImageClassificationDatasetImporter "fiftyone.utils.data.importers.FiftyOneImageClassificationDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from an image classification dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/image-classification-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.FiftyOneImageClassificationDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/image-classification-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneImageClassificationDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view an image classification dataset in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/image-classification-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneImageClassificationDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/labels.json"
     6
     7# Import dataset by explicitly providing paths to the source media and labels
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.FiftyOneImageClassificationDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/labels.json
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.FiftyOneImageClassificationDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Note

If the UUIDs in your labels are absolute paths to the source media, then you can omit the `data_path` parameter from the example above.

## TF Image Classification#

The [`fiftyone.types.TFImageClassificationDataset`](../api/fiftyone.types.html#fiftyone.types.TFImageClassificationDataset "fiftyone.types.TFImageClassificationDataset") type represents a labeled dataset consisting of images and their associated classification labels stored as [TFRecords](https://www.tensorflow.org/tutorials/load_data/tfrecord).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        tf.records-?????-of-?????
    

where the features of the (possibly sharded) TFRecords are stored in the following format:
    
    
    {
        # Image dimensions
        "height": tf.io.FixedLenFeature([], tf.int64),
        "width": tf.io.FixedLenFeature([], tf.int64),
        "depth": tf.io.FixedLenFeature([], tf.int64),
        # Image filename
        "filename": tf.io.FixedLenFeature([], tf.int64),
        # The image extension
        "format": tf.io.FixedLenFeature([], tf.string),
        # Encoded image bytes
        "image_bytes": tf.io.FixedLenFeature([], tf.string),
        # Class label string
        "label": tf.io.FixedLenFeature([], tf.string, default_value=""),
    }
    

For unlabeled samples, the TFRecords do not contain `label` features.

Note

See [`TFImageClassificationDatasetImporter`](../api/fiftyone.utils.tf.html#fiftyone.utils.tf.TFImageClassificationDatasetImporter "fiftyone.utils.tf.TFImageClassificationDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from an image classification dataset stored as a directory of TFRecords in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/tf-image-classification-dataset"
     5images_dir = "/path/for/images"
     6
     7# Create the dataset
     8dataset = fo.Dataset.from_dir(
     9    dataset_dir=dataset_dir,
    10    dataset_type=fo.types.TFImageClassificationDataset,
    11    images_dir=images_dir,
    12    name=name,
    13)
    14
    15# View summary info about the dataset
    16print(dataset)
    17
    18# Print the first few samples in the dataset
    19print(dataset.head())
    

When the above command is executed, the images in the TFRecords will be written to the provided `images_dir`, which is required because FiftyOne datasets must make their images available as individual files on disk.
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/tf-image-classification-dataset
    IMAGES_DIR=/path/for/images
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.TFImageClassificationDataset \
        --kwargs images_dir=$IMAGES_DIR
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

When the above command is executed, the images in the TFRecords will be written to the provided `IMAGES_DIR`, which is required because FiftyOne datasets must make their images available as individual files on disk.

To view an image classification dataset stored as a directory of TFRecords in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/tf-image-classification-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.TFImageClassificationDataset
    

Note

You can provide the `tf_records_path` argument instead of `dataset_dir` in the examples above to directly specify the path to the TFRecord(s) to load. See [`TFImageClassificationDatasetImporter`](../api/fiftyone.utils.tf.html#fiftyone.utils.tf.TFImageClassificationDatasetImporter "fiftyone.utils.tf.TFImageClassificationDatasetImporter") for details.

## COCO#

The [`fiftyone.types.COCODetectionDataset`](../api/fiftyone.types.html#fiftyone.types.COCODetectionDataset "fiftyone.types.COCODetectionDataset") type represents a labeled dataset consisting of images and their associated object detections saved in [COCO Object Detection Format](https://cocodataset.org/#format-data).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <filename0>.<ext>
            <filename1>.<ext>
            ...
        labels.json
    

where `labels.json` is a JSON file in the following format:
    
    
    {
        "info": {...},
        "licenses": [
            {
                "id": 1,
                "name": "Attribution-NonCommercial-ShareAlike License",
                "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
            },
            ...
        ],
        "categories": [
            {
                "id": 1,
                "name": "cat",
                "supercategory": "animal",
                "keypoints": ["nose", "head", ...],
                "skeleton": [[12, 14], [14, 16], ...]
            },
            ...
        ],
        "images": [
            {
                "id": 1,
                "license": 1,
                "file_name": "<filename0>.<ext>",
                "height": 480,
                "width": 640,
                "date_captured": null
            },
            ...
        ],
        "annotations": [
            {
                "id": 1,
                "image_id": 1,
                "category_id": 1,
                "bbox": [260, 177, 231, 199],
                "segmentation": [...],
                "keypoints": [224, 226, 2, ...],
                "num_keypoints": 10,
                "score": 0.95,
                "area": 45969,
                "iscrowd": 0
            },
            ...
        ]
    }
    

See [this page](https://cocodataset.org/#format-data) for a full specification of the `segmentation` field.

For unlabeled datasets, `labels.json` does not contain an `annotations` field.

The `file_name` attribute of the labels file encodes the location of the corresponding images, which can be any of the following:

  * The filename of an image in the `data/` folder

  * A relative path like `data/sub/folder/filename.ext` specifying the relative path to the image in a nested subfolder of `data/`

  * An absolute path to an image, which may or may not be in the `data/` folder




Note

See [`COCODetectionDatasetImporter`](../api/fiftyone.utils.coco.html#fiftyone.utils.coco.COCODetectionDatasetImporter "fiftyone.utils.coco.COCODetectionDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a COCO detection dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/coco-detection-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.COCODetectionDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/coco-detection-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.COCODetectionDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a COCO detection dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/coco-detection-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.COCODetectionDataset
    

Note

By default, all supported label types are loaded (detections, segmentations, and keypoints). However, you can choose specific type(s) to load by passing the optional `label_types` argument to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir"):
    
    
    # Only load bounding boxes
    dataset = fo.Dataset.from_dir(
        dataset_type=fo.types.COCODetectionDataset,
        label_types=["detections"],
        ...
    )
    

See [`COCODetectionDatasetImporter`](../api/fiftyone.utils.coco.html#fiftyone.utils.coco.COCODetectionDatasetImporter "fiftyone.utils.coco.COCODetectionDatasetImporter") for complete documentation of the available COCO import options.

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/coco-labels.json"
     6
     7# Import dataset by explicitly providing paths to the source media and labels
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.COCODetectionDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/coco-labels.json
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.COCODetectionDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Note

If the `file_name` key of your labels contains absolute paths to the source media, then you can omit the `data_path` parameter from the example above.

If you have an existing dataset and corresponding model predictions stored in COCO format, then you can use [`add_coco_labels()`](../api/fiftyone.utils.coco.html#fiftyone.utils.coco.add_coco_labels "fiftyone.utils.coco.add_coco_labels") to conveniently add the labels to the dataset. The example below demonstrates a round-trip export and then re-import of both images-and-labels and labels-only data in COCO format:
    
    
     1import fiftyone as fo
     2import fiftyone.zoo as foz
     3import fiftyone.utils.coco as fouc
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6classes = dataset.distinct("predictions.detections.label")
     7
     8# Export images and ground truth labels to disk
     9dataset.export(
    10    export_dir="/tmp/coco",
    11    dataset_type=fo.types.COCODetectionDataset,
    12    label_field="ground_truth",
    13    classes=classes,
    14)
    15
    16# Export predictions
    17dataset.export(
    18    dataset_type=fo.types.COCODetectionDataset,
    19    labels_path="/tmp/coco/predictions.json",
    20    label_field="predictions",
    21    classes=classes,
    22)
    23
    24# Now load ground truth labels into a new dataset
    25dataset2 = fo.Dataset.from_dir(
    26    dataset_dir="/tmp/coco",
    27    dataset_type=fo.types.COCODetectionDataset,
    28    label_field="ground_truth",
    29)
    30
    31# And add model predictions
    32fouc.add_coco_labels(
    33    dataset2,
    34    "predictions",
    35    "/tmp/coco/predictions.json",
    36    classes,
    37)
    38
    39# Verify that ground truth and predictions were imported as expected
    40print(dataset.count("ground_truth.detections"))
    41print(dataset2.count("ground_truth.detections"))
    42print(dataset.count("predictions.detections"))
    43print(dataset2.count("predictions.detections"))
    

Note

See [`add_coco_labels()`](../api/fiftyone.utils.coco.html#fiftyone.utils.coco.add_coco_labels "fiftyone.utils.coco.add_coco_labels") for a complete description of the available syntaxes for loading COCO-formatted predictions to an existing dataset.

## VOC#

The [`fiftyone.types.VOCDetectionDataset`](../api/fiftyone.types.html#fiftyone.types.VOCDetectionDataset "fiftyone.types.VOCDetectionDataset") type represents a labeled dataset consisting of images and their associated object detections saved in [VOC format](http://host.robots.ox.ac.uk/pascal/VOC).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels/
            <uuid1>.xml
            <uuid2>.xml
            ...
    

where the labels XML files are in the following format:
    
    
    <annotation>
        <folder></folder>
        <filename>image.ext</filename>
        <path>/path/to/dataset-dir/data/image.ext</path>
        <source>
            <database></database>
        </source>
        <size>
            <width>640</width>
            <height>480</height>
            <depth>3</depth>
        </size>
        <segmented></segmented>
        <object>
            <name>cat</name>
            <pose></pose>
            <truncated>0</truncated>
            <difficult>0</difficult>
            <occluded>0</occluded>
            <bndbox>
                <xmin>256</xmin>
                <ymin>200</ymin>
                <xmax>450</xmax>
                <ymax>400</ymax>
            </bndbox>
        </object>
        <object>
            <name>dog</name>
            <pose></pose>
            <truncated>1</truncated>
            <difficult>1</difficult>
            <occluded>1</occluded>
            <bndbox>
                <xmin>128</xmin>
                <ymin>100</ymin>
                <xmax>350</xmax>
                <ymax>300</ymax>
            </bndbox>
        </object>
        ...
    </annotation>
    

where either the `<filename>` and/or `<path>` field of the annotations may be populated to specify the corresponding source image.

Unlabeled images have no corresponding file in `labels/`.

The `data/` and `labels/` files may contain nested subfolders of parallelly organized images and masks.

Note

See [`VOCDetectionDatasetImporter`](../api/fiftyone.utils.voc.html#fiftyone.utils.voc.VOCDetectionDatasetImporter "fiftyone.utils.voc.VOCDetectionDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a VOC detection dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/voc-detection-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.VOCDetectionDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/voc-detection-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.VOCDetectionDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a VOC detection dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/voc-detection-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.VOCDetectionDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/voc-labels"
     6
     7# Import dataset by explicitly providing paths to the source media and labels
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.VOCDetectionDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/voc-labels
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.VOCDetectionDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Note

If the `<path>` field of your labels are populated with the absolute paths to the source media, then you can omit the `data_path` parameter from the example above.

## KITTI#

The [`fiftyone.types.KITTIDetectionDataset`](../api/fiftyone.types.html#fiftyone.types.KITTIDetectionDataset "fiftyone.types.KITTIDetectionDataset") type represents a labeled dataset consisting of images and their associated object detections saved in [KITTI format](http://www.cvlibs.net/datasets/kitti/eval_object.php).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels/
            <uuid1>.txt
            <uuid2>.txt
            ...
    

where the labels TXT files are space-delimited files where each row corresponds to an object and the 15 (and optional 16th score) columns have the following meanings:

# of columns | Name | Description | Default  
---|---|---|---  
1 | type | The object label |   
1 | truncated | A float in `[0, 1]`, where 0 is non-truncated and 1 is fully truncated. Here, truncation refers to the object leaving image boundaries | 0  
1 | occluded | An int in `(0, 1, 2, 3)` indicating occlusion state, where:- 0 = fully visible- 1 = partly occluded- 2 = largely occluded- 3 = unknown | 0  
1 | alpha | Observation angle of the object, in `[-pi, pi]` | 0  
4 | bbox | 2D bounding box of object in the image in pixels, in the format `[xtl, ytl, xbr, ybr]` |   
1 | dimensions | 3D object dimensions, in meters, in the format `[height, width, length]` | 0  
1 | location | 3D object location `(x, y, z)` in camera coordinates (in meters) | 0  
1 | rotation_y | Rotation around the y-axis in camera coordinates, in `[-pi, pi]` | 0  
1 | score | `(optional)` A float confidence for the detection |   
  
When reading datasets of this type, all columns after the four `bbox` columns are optional.

Unlabeled images have no corresponding file in `labels/`.

The `data/` and `labels/` files may contain nested subfolders of parallelly organized images and masks.

Note

See [`KITTIDetectionDatasetImporter`](../api/fiftyone.utils.kitti.html#fiftyone.utils.kitti.KITTIDetectionDatasetImporter "fiftyone.utils.kitti.KITTIDetectionDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a KITTI detection dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/kitti-detection-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.KITTIDetectionDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/kitti-detection-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.KITTIDetectionDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a KITTI detection dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/kitti-detection-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.KITTIDetectionDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/kitti-labels"
     6
     7# Import dataset by explicitly providing paths to the source media and labels
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.KITTIDetectionDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/kitti-labels
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.KITTIDetectionDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

## YOLOv4#

The [`fiftyone.types.YOLOv4Dataset`](../api/fiftyone.types.html#fiftyone.types.YOLOv4Dataset "fiftyone.types.YOLOv4Dataset") type represents a labeled dataset consisting of images and their associated object detections saved in [YOLOv4 format](https://github.com/AlexeyAB/darknet).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        obj.names
        images.txt
        data/
            <uuid1>.<ext>
            <uuid1>.txt
            <uuid2>.<ext>
            <uuid2>.txt
            ...
    

where `obj.names` contains the object class labels:
    
    
    <label-0>
    <label-1>
    ...
    

and `images.txt` contains the list of images in `data/`:
    
    
    data/<uuid1>.<ext>
    data/<uuid2>.<ext>
    ...
    

The image paths in `images.txt` can be specified as either relative (to the location of file) or as absolute paths. Alternatively, this file can be omitted, in which case the `data/` directory is listed to determine the available images.

The TXT files in `data/` are space-delimited files where each row corresponds to an object in the image of the same name, in one of the following formats:
    
    
    # Detections
    <target> <x-center> <y-center> <width> <height>
    <target> <x-center> <y-center> <width> <height> <confidence>
    
    # Instance segmentations or polygons
    <target> <x1> <y1> <x2> <y2> <x3> <y3> ...
    

where `<target>` is the zero-based integer index of the object class label from `obj.names`, all coordinates are expressed as relative values in `[0, 1] x [0, 1]`, and `<confidence>` is an optional confidence in `[0, 1]`.

Unlabeled images have no corresponding TXT file in `data/`.

The `data/` folder may contain nested subfolders.

Note

By default, all annotations are loaded as [`Detections`](../api/fiftyone.core.labels.html#fiftyone.core.labels.Detections "fiftyone.core.labels.Detections"), converting any polylines to tight bounding boxes if necessary. However, you can choose to load YOLO annotations as instance segmentations or polygons by passing the optional `label_type` argument to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir"):
    
    
    # Load annotations as instance segmentations
    dataset = fo.Dataset.from_dir(
        dataset_type=fo.types.YOLOv4Dataset,
        label_type="instances",
        mask_size=(width, height),  # optional size for each dense mask
        ...
    )
    
    # Load annotations as polygons
    dataset = fo.Dataset.from_dir(
        dataset_type=fo.types.YOLOv4Dataset,
        label_type="polylines",
        ...
    )
    

See [`YOLOv4DatasetImporter`](../api/fiftyone.utils.yolo.html#fiftyone.utils.yolo.YOLOv4DatasetImporter "fiftyone.utils.yolo.YOLOv4DatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a YOLOv4 dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/yolov4-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.YOLOv4Dataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/yolov4-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.YOLOv4Dataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a YOLOv4 dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/yolov4-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.YOLOv4Dataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/yolo-labels"
     6classes = ["list", "of", "classes"]
     7
     8# Import dataset by explicitly providing paths to the source media and labels
     9dataset = fo.Dataset.from_dir(
    10    dataset_type=fo.types.YOLOv4Dataset,
    11    data_path=data_path,
    12    labels_path=labels_path,
    13    classes=classes,
    14    name=name,
    15)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/yolo-labels
    OBJECTS_PATH=/path/to/obj.names
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.YOLOv4Dataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH \
            objects_path=$OBJECTS_PATH
    

If you have an existing dataset and corresponding model predictions stored in YOLO format, then you can use [`add_yolo_labels()`](../api/fiftyone.utils.yolo.html#fiftyone.utils.yolo.add_yolo_labels "fiftyone.utils.yolo.add_yolo_labels") to conveniently add the labels to the dataset.

The example below demonstrates a round-trip export and then re-import of both images-and-labels and labels-only data in YOLO format:
    
    
     1import fiftyone as fo
     2import fiftyone.zoo as foz
     3import fiftyone.utils.yolo as fouy
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6classes = dataset.distinct("predictions.detections.label")
     7
     8# Export images and ground truth labels to disk
     9dataset.export(
    10    export_dir="/tmp/yolov4",
    11    dataset_type=fo.types.YOLOv4Dataset,
    12    label_field="ground_truth",
    13    classes=classes,
    14)
    15
    16# Export predictions
    17dataset.export(
    18    dataset_type=fo.types.YOLOv4Dataset,
    19    labels_path="/tmp/yolov4/predictions",
    20    label_field="predictions",
    21    classes=classes,
    22)
    23
    24# Now load ground truth labels into a new dataset
    25dataset2 = fo.Dataset.from_dir(
    26    dataset_dir="/tmp/yolov4",
    27    dataset_type=fo.types.YOLOv4Dataset,
    28    label_field="ground_truth",
    29)
    30
    31# And add model predictions
    32fouy.add_yolo_labels(
    33    dataset2,
    34    "predictions",
    35    "/tmp/yolov4/predictions",
    36    classes,
    37)
    38
    39# Verify that ground truth and predictions were imported as expected
    40print(dataset.count("ground_truth.detections"))
    41print(dataset2.count("ground_truth.detections"))
    42print(dataset.count("predictions.detections"))
    43print(dataset2.count("predictions.detections"))
    

Note

See [`add_yolo_labels()`](../api/fiftyone.utils.yolo.html#fiftyone.utils.yolo.add_yolo_labels "fiftyone.utils.yolo.add_yolo_labels") for a complete description of the available syntaxes for loading YOLO-formatted predictions to an existing dataset.

## YOLOv5#

The [`fiftyone.types.YOLOv5Dataset`](../api/fiftyone.types.html#fiftyone.types.YOLOv5Dataset "fiftyone.types.YOLOv5Dataset") type represents a labeled dataset consisting of images and their associated object detections saved in [YOLOv5 format](https://github.com/ultralytics/yolov5).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        dataset.yaml
        images/
            train/
                <uuid1>.<ext>
                <uuid2>.<ext>
                ...
            val/
                <uuid3>.<ext>
                <uuid4>.<ext>
                ...
        labels/
            train/
                <uuid1>.txt
                <uuid2>.txt
                ...
            val/
                <uuid3>.txt
                <uuid4>.txt
                ...
    

where `dataset.yaml` contains the following information:
    
    
    path: <dataset_dir>  # optional
    train: ./images/train/
    val: ./images/val/
    
    names:
      0: list
      1: of
      2: classes
      ...
    

See [this page](https://docs.ultralytics.com/datasets/detect) for a full description of the possible format of `dataset.yaml`. In particular, the dataset may contain one or more splits with arbitrary names, as the specific split being imported or exported is specified by the `split` argument to [`fiftyone.utils.yolo.YOLOv5DatasetImporter`](../api/fiftyone.utils.yolo.html#fiftyone.utils.yolo.YOLOv5DatasetImporter "fiftyone.utils.yolo.YOLOv5DatasetImporter"). Also, `dataset.yaml` can be located outside of `<dataset_dir>` as long as the optional `path` is provided.

Note

Any relative paths in `dataset.yaml` or per-split TXT files are interpreted relative to the directory containing these files, not your current working directory.

The TXT files in `labels/` are space-delimited files where each row corresponds to an object in the image of the same name, in one of the following formats:
    
    
    # Detections
    <target> <x-center> <y-center> <width> <height>
    <target> <x-center> <y-center> <width> <height> <confidence>
    
    # Instance segmentations or polygons
    <target> <x1> <y1> <x2> <y2> <x3> <y3> ...
    

where `<target>` is the zero-based integer index of the object class label from `names`, all coordinates are expressed as relative values in `[0, 1] x [0, 1]`, and `<confidence>` is an optional confidence in `[0, 1]`.

Unlabeled images have no corresponding TXT file in `labels/`. The label file path for each image is obtained by replacing `images/` with `labels/` in the respective image path.

The image and labels directories for a given split may contain nested subfolders of parallelly organized images and labels.

Note

By default, all annotations are loaded as [`Detections`](../api/fiftyone.core.labels.html#fiftyone.core.labels.Detections "fiftyone.core.labels.Detections"), converting any polylines to tight bounding boxes if necessary. However, you can choose to load YOLO annotations as instance segmentations or polygons by passing the optional `label_type` argument to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir"):
    
    
    # Load annotations as instance segmentations
    dataset = fo.Dataset.from_dir(
        dataset_type=fo.types.YOLOv5Dataset,
        label_type="instances",
        mask_size=(width, height),  # optional size for each dense mask
        ...
    )
    
    # Load annotations as polygons
    dataset = fo.Dataset.from_dir(
        dataset_type=fo.types.YOLOv5Dataset,
        label_type="polylines",
        ...
    )
    

See [`YOLOv5DatasetImporter`](../api/fiftyone.utils.yolo.html#fiftyone.utils.yolo.YOLOv5DatasetImporter "fiftyone.utils.yolo.YOLOv5DatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a YOLOv5 dataset stored in the above format as follows:
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/yolov5-dataset"
     5
     6# The splits to load
     7splits = ["train", "val"]
     8
     9# Load the dataset, using tags to mark the samples in each split
    10dataset = fo.Dataset(name)
    11for split in splits:
    12    dataset.add_dir(
    13        dataset_dir=dataset_dir,
    14        dataset_type=fo.types.YOLOv5Dataset,
    15        split=split,
    16        tags=split,
    17)
    18
    19# View summary info about the dataset
    20print(dataset)
    21
    22# Print the first few samples in the dataset
    23print(dataset.head())
    

If you have an existing dataset and corresponding model predictions stored in YOLO format, then you can use [`add_yolo_labels()`](../api/fiftyone.utils.yolo.html#fiftyone.utils.yolo.add_yolo_labels "fiftyone.utils.yolo.add_yolo_labels") to conveniently add the labels to the dataset.

The example below demonstrates a round-trip export and then re-import of both images-and-labels and labels-only data in YOLO format:
    
    
     1import fiftyone as fo
     2import fiftyone.zoo as foz
     3import fiftyone.utils.yolo as fouy
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6classes = dataset.distinct("predictions.detections.label")
     7
     8# YOLOv5 format supports splits, so let's grab only the `validation` split
     9view = dataset.match_tags("validation")
    10
    11# Export images and ground truth labels to disk
    12view.export(
    13    export_dir="/tmp/yolov5",
    14    dataset_type=fo.types.YOLOv5Dataset,
    15    split="validation",
    16    label_field="ground_truth",
    17    classes=classes,
    18)
    19
    20# Export predictions
    21view.export(
    22    dataset_type=fo.types.YOLOv5Dataset,
    23    labels_path="/tmp/yolov5/predictions/validation",
    24    label_field="predictions",
    25    classes=classes,
    26)
    27
    28# Now load ground truth labels into a new dataset
    29dataset2 = fo.Dataset.from_dir(
    30    dataset_dir="/tmp/yolov5",
    31    dataset_type=fo.types.YOLOv5Dataset,
    32    split="validation",
    33    label_field="ground_truth",
    34)
    35
    36# And add model predictions
    37fouy.add_yolo_labels(
    38    dataset2,
    39    "predictions",
    40    "/tmp/yolov5/predictions/validation",
    41    classes,
    42)
    43
    44# Verify that ground truth and predictions were imported as expected
    45print(view.count("ground_truth.detections"))
    46print(dataset2.count("ground_truth.detections"))
    47print(view.count("predictions.detections"))
    48print(dataset2.count("predictions.detections"))
    

Note

See [`add_yolo_labels()`](../api/fiftyone.utils.yolo.html#fiftyone.utils.yolo.add_yolo_labels "fiftyone.utils.yolo.add_yolo_labels") for a complete description of the available syntaxes for loading YOLO-formatted predictions to an existing dataset.

## FiftyOne Object Detection#

The [`fiftyone.types.FiftyOneImageDetectionDataset`](../api/fiftyone.types.html#fiftyone.types.FiftyOneImageDetectionDataset "fiftyone.types.FiftyOneImageDetectionDataset") type represents a labeled dataset consisting of images and their associated object detections stored in a simple JSON format.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels.json
    

where `labels.json` is a JSON file in the following format:
    
    
    {
        "classes": [
            <labelA>,
            <labelB>,
            ...
        ],
        "labels": {
            <uuid1>: [
                {
                    "label": <target>,
                    "bounding_box": [
                        <top-left-x>, <top-left-y>, <width>, <height>
                    ],
                    "confidence": <optional-confidence>,
                    "attributes": {
                        <optional-name>: <optional-value>,
                        ...
                    }
                },
                ...
            ],
            <uuid2>: [
                ...
            ],
            ...
        }
    }
    

and where the bounding box coordinates are expressed as relative values in `[0, 1] x [0, 1]`.

If the `classes` field is provided, the `target` values are class IDs that are mapped to class label strings via `classes[target]`. If no `classes` field is provided, then the `target` values directly store the label strings.

The target value in `labels` for unlabeled images is `None` (or missing).

The UUIDs can also be relative paths like `path/to/uuid`, in which case the images in `data/` should be arranged in nested subfolders with the corresponding names, or they can be absolute paths, in which case the images may or may not be in `data/`.

Note

See [`FiftyOneImageDetectionDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.FiftyOneImageDetectionDatasetImporter "fiftyone.utils.data.importers.FiftyOneImageDetectionDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from an image detection dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/image-detection-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.FiftyOneImageDetectionDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/image-detection-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneImageDetectionDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view an image detection dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/image-detection-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneImageDetectionDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/labels.json"
     6
     7# Import dataset by explicitly providing paths to the source media and labels
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.FiftyOneImageDetectionDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/labels.json
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.FiftyOneImageDetectionDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Note

If the UUIDs in your labels are absolute paths to the source media, then you can omit the `data_path` parameter from the example above.

## FiftyOne Temporal Detection#

The [`fiftyone.types.FiftyOneTemporalDetectionDataset`](../api/fiftyone.types.html#fiftyone.types.FiftyOneTemporalDetectionDataset "fiftyone.types.FiftyOneTemporalDetectionDataset") type represents a labeled dataset consisting of videos and their associated temporal detections stored in a simple JSON format.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels.json
    

where `labels.json` is a JSON file in the following format:
    
    
    {
        "classes": [
            "<labelA>",
            "<labelB>",
            ...
        ],
        "labels": {
            "<uuid1>": [
                {
                    "label": <target>,
                    "support": [<first-frame>, <last-frame>],
                    "confidence": <optional-confidence>,
                    "attributes": {
                        <optional-name>: <optional-value>,
                        ...
                    }
                },
                {
                    "label": <target>,
                    "support": [<first-frame>, <last-frame>],
                    "confidence": <optional-confidence>,
                    "attributes": {
                        <optional-name>: <optional-value>,
                        ...
                    }
                },
                ...
            ],
            "<uuid2>": [
                {
                    "label": <target>,
                    "timestamps": [<start-timestamp>, <stop-timestamp>],
                    "confidence": <optional-confidence>,
                    "attributes": {
                        <optional-name>: <optional-value>,
                        ...
                    }
                },
                {
                    "label": <target>,
                    "timestamps": [<start-timestamp>, <stop-timestamp>],
                    "confidence": <optional-confidence>,
                    "attributes": {
                        <optional-name>: <optional-value>,
                        ...
                    }
                },
            ],
            ...
        }
    }
    

The temporal range of each detection can be specified either via the `support` key, which should contain the `[first, last]` frame numbers of the detection, or the `timestamps` key, which should contain the `[start, stop]` timestamps of the detection in seconds.

If the `classes` field is provided, the `target` values are class IDs that are mapped to class label strings via `classes[target]`. If no `classes` field is provided, then the `target` values directly store the label strings.

Unlabeled videos can have a `None` (or missing) key in `labels`.

The UUIDs can also be relative paths like `path/to/uuid`, in which case the images in `data/` should be arranged in nested subfolders with the corresponding names, or they can be absolute paths, in which case the images may or may not be in `data/`.

Note

See [`FiftyOneTemporalDetectionDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.FiftyOneTemporalDetectionDatasetImporter "fiftyone.utils.data.importers.FiftyOneTemporalDetectionDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a temporal detection dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/temporal-detection-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.FiftyOneTemporalDetectionDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/temporal-detection-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneTemporalDetectionDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a temporal detection dataset in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/temporal-detection-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneTemporalDetectionDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/labels.json"
     6
     7# Import dataset by explicitly providing paths to the source media and labels
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.FiftyOneTemporalDetectionDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/labels.json
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.FiftyOneTemporalDetectionDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Note

If the UUIDs in your labels are absolute paths to the source media, then you can omit the `data_path` parameter from the example above.

## TF Object Detection#

The [`fiftyone.types.TFObjectDetectionDataset`](../api/fiftyone.types.html#fiftyone.types.TFObjectDetectionDataset "fiftyone.types.TFObjectDetectionDataset") type represents a labeled dataset consisting of images and their associated object detections stored as [TFRecords](https://www.tensorflow.org/tutorials/load_data/tfrecord) in [TF Object Detection API format](https://github.com/tensorflow/models/blob/master/research/object_detection).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        tf.records-?????-of-?????
    

where the features of the (possibly sharded) TFRecords are stored in the following format:
    
    
    {
        # Image dimensions
        "image/height": tf.io.FixedLenFeature([], tf.int64),
        "image/width": tf.io.FixedLenFeature([], tf.int64),
    
        # Image filename is used for both of these when writing
        "image/filename": tf.io.FixedLenFeature([], tf.string),
        "image/source_id": tf.io.FixedLenFeature([], tf.string),
    
        # Encoded image bytes
        "image/encoded": tf.io.FixedLenFeature([], tf.string),
    
        # Image format, either `jpeg` or `png`
        "image/format": tf.io.FixedLenFeature([], tf.string),
    
        # Normalized bounding box coordinates in `[0, 1]`
        "image/object/bbox/xmin": tf.io.FixedLenSequenceFeature(
            [], tf.float32, allow_missing=True
        ),
        "image/object/bbox/xmax": tf.io.FixedLenSequenceFeature(
            [], tf.float32, allow_missing=True
        ),
        "image/object/bbox/ymin": tf.io.FixedLenSequenceFeature(
            [], tf.float32, allow_missing=True
        ),
        "image/object/bbox/ymax": tf.io.FixedLenSequenceFeature(
            [], tf.float32, allow_missing=True
        ),
    
        # Class label string
        "image/object/class/text": tf.io.FixedLenSequenceFeature(
            [], tf.string, allow_missing=True
        ),
    
        # Integer class ID
        "image/object/class/label": tf.io.FixedLenSequenceFeature(
            [], tf.int64, allow_missing=True
        ),
    }
    

The TFRecords for unlabeled samples do not contain `image/object/*` features.

Note

See [`TFObjectDetectionDatasetImporter`](../api/fiftyone.utils.tf.html#fiftyone.utils.tf.TFObjectDetectionDatasetImporter "fiftyone.utils.tf.TFObjectDetectionDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from an object detection dataset stored as a directory of TFRecords in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/tf-object-detection-dataset"
     5images_dir = "/path/for/images"
     6
     7# Create the dataset
     8dataset = fo.Dataset.from_dir(
     9    dataset_dir=dataset_dir,
    10    dataset_type=fo.types.TFObjectDetectionDataset,
    11    images_dir=images_dir,
    12    name=name,
    13)
    14
    15# View summary info about the dataset
    16print(dataset)
    17
    18# Print the first few samples in the dataset
    19print(dataset.head())
    

When the above command is executed, the images in the TFRecords will be written to the provided `images_dir`, which is required because FiftyOne datasets must make their images available as individual files on disk.
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/tf-object-detection-dataset
    IMAGES_DIR=/path/for/images
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.TFObjectDetectionDataset \
        --kwargs images_dir=$IMAGES_DIR
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

When the above command is executed, the images in the TFRecords will be written to the provided `IMAGES_DIR`, which is required because FiftyOne datasets must make their images available as individual files on disk.

To view an object detection dataset stored as a directory of TFRecords in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/tf-object-detection-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.TFObjectDetectionDataset
    

Note

You can provide the `tf_records_path` argument instead of `dataset_dir` in the examples above to directly specify the path to the TFRecord(s) to load. See [`TFObjectDetectionDatasetImporter`](../api/fiftyone.utils.tf.html#fiftyone.utils.tf.TFObjectDetectionDatasetImporter "fiftyone.utils.tf.TFObjectDetectionDatasetImporter") for details.

## Image Segmentation Directory#

The [`fiftyone.types.ImageSegmentationDirectory`](../api/fiftyone.types.html#fiftyone.types.ImageSegmentationDirectory "fiftyone.types.ImageSegmentationDirectory") type represents a labeled dataset consisting of images and their associated semantic segmentations stored as images on disk.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <filename1>.<ext>
            <filename2>.<ext>
            ...
        labels/
            <filename1>.<ext>
            <filename2>.<ext>
            ...
    

where `labels/` contains the semantic segmentations stored as images.

Unlabeled images have no corresponding file in `labels/`.

The `data/` and `labels/` files may contain nested subfolders of parallelly organized images and masks.

Note

See [`ImageSegmentationDirectoryImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.ImageSegmentationDirectoryImporter "fiftyone.utils.data.importers.ImageSegmentationDirectoryImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from an image segmentation dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/image-segmentation-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.ImageSegmentationDirectory,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/image-segmentation-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.ImageSegmentationDirectory
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view an image segmentation dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/image-segmentation-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.ImageSegmentationDirectory
    

You can also independently specify the locations of the masks and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/masks"
     6
     7# Import dataset by explicitly providing paths to the source media and masks
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.ImageSegmentationDirectory,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/masks
    
    # Import dataset by explicitly providing paths to the source media and masks
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.ImageSegmentationDirectory \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

## CVAT Image#

The [`fiftyone.types.CVATImageDataset`](../api/fiftyone.types.html#fiftyone.types.CVATImageDataset "fiftyone.types.CVATImageDataset") type represents a labeled dataset consisting of images and their associated tags and object detections stored in [CVAT image format](https://github.com/opencv/cvat).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels.xml
    

where `labels.xml` is an XML file in the following format:
    
    
    <?xml version="1.0" encoding="utf-8"?>
    <annotations>
        <version>1.1</version>
        <meta>
            <task>
                <id>0</id>
                <name>task-name</name>
                <size>51</size>
                <mode>annotation</mode>
                <overlap></overlap>
                <bugtracker></bugtracker>
                <flipped>False</flipped>
                <created>2017-11-20 11:51:51.000000+00:00</created>
                <updated>2017-11-20 11:51:51.000000+00:00</updated>
                <labels>
                    <label>
                        <name>car</name>
                        <attributes>
                            <attribute>
                                <name>type</name>
                                <values>coupe\\nsedan\\ntruck</values>
                            </attribute>
                            ...
                        </attributes>
                    </label>
                    <label>
                        <name>traffic_line</name>
                        <attributes>
                            <attribute>
                                <name>color</name>
                                <values>white\\nyellow</values>
                            </attribute>
                            ...
                        </attributes>
                    </label>
                    ...
                </labels>
            </task>
            <segments>
                <segment>
                    <id>0</id>
                    <start>0</start>
                    <stop>50</stop>
                    <url></url>
                </segment>
            </segments>
            <owner>
                <username></username>
                <email></email>
            </owner>
            <dumped>2017-11-20 11:51:51.000000+00:00</dumped>
        </meta>
        <image id="0" name="<uuid1>.<ext>" width="640" height="480">
            <tag label="urban"></tag>
            ...
            <box label="car" xtl="100" ytl="50" xbr="325" ybr="190" occluded="0">
                <attribute name="type">sedan</attribute>
                ...
            </box>
            ...
            <polygon label="car" points="561.30,916.23;561.30,842.77;...;560.20,966.67" occluded="0">
                <attribute name="make">Honda</attribute>
                ...
            </polygon>
            ...
            <polyline label="traffic_line" points="462.10,0.00;126.80,1200.00" occluded="0">
                <attribute name="color">yellow</attribute>
                ...
            </polyline>
            ...
            <points label="wheel" points="574.90,939.48;1170.16,907.90;...;600.16,459.48" occluded="0">
                <attribute name="location">front_driver_side</attribute>
                ...
            </points>
            ...
        </image>
        ...
        <image id="50" name="<uuid51>.<ext>" width="640" height="480">
            ...
        </image>
    </annotations>
    

Unlabeled images have no corresponding `image` tag in `labels.xml`.

The `name` field of the `<image>` tags in the labels file encodes the location of the corresponding images, which can be any of the following:

  * The filename of an image in the `data/` folder

  * A relative path like `data/sub/folder/filename.ext` specifying the relative path to the image in a nested subfolder of `data/`

  * An absolute path to an image, which may or may not be in the `data/` folder




Note

See [`CVATImageDatasetImporter`](../api/fiftyone.utils.cvat.html#fiftyone.utils.cvat.CVATImageDatasetImporter "fiftyone.utils.cvat.CVATImageDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a CVAT image dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/cvat-image-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.CVATImageDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/cvat-image-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.CVATImageDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a CVAT image dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/cvat-image-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.CVATImageDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/cvat-labels.xml"
     6
     7# Import dataset by explicitly providing paths to the source media and labels
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.CVATImageDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/cvat-labels.xml
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.CVATImageDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Note

If the `name` key of your labels contains absolute paths to the source media, then you can omit the `data_path` parameter from the example above.

## CVAT Video#

The [`fiftyone.types.CVATVideoDataset`](../api/fiftyone.types.html#fiftyone.types.CVATVideoDataset "fiftyone.types.CVATVideoDataset") type represents a labeled dataset consisting of videos and their associated object detections stored in [CVAT video format](https://github.com/opencv/cvat).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels/
            <uuid1>.xml
            <uuid2>.xml
            ...
    

where the labels XML files are stored in the following format:
    
    
    <?xml version="1.0" encoding="utf-8"?>
    <annotations>
        <version>1.1</version>
        <meta>
            <task>
                <id>task-id</id>
                <name>task-name</name>
                <size>51</size>
                <mode>interpolation</mode>
                <overlap></overlap>
                <bugtracker></bugtracker>
                <flipped>False</flipped>
                <created>2017-11-20 11:51:51.000000+00:00</created>
                <updated>2017-11-20 11:51:51.000000+00:00</updated>
                <labels>
                    <label>
                        <name>car</name>
                        <attributes>
                            <attribute>
                                <name>type</name>
                                <values>coupe\\nsedan\\ntruck</values>
                            </attribute>
                            ...
                        </attributes>
                    </label>
                    <label>
                        <name>traffic_line</name>
                        <attributes>
                            <attribute>
                                <name>color</name>
                                <values>white\\nyellow</values>
                            </attribute>
                            ...
                        </attributes>
                    </label>
                    ...
                </labels>
            </task>
            <segments>
                <segment>
                    <id>0</id>
                    <start>0</start>
                    <stop>50</stop>
                    <url></url>
                </segment>
            </segments>
            <owner>
                <username></username>
                <email></email>
            </owner>
            <original_size>
                <width>640</width>
                <height>480</height>
            </original_size>
            <dumped>2017-11-20 11:51:51.000000+00:00</dumped>
        </meta>
        <track id="0" label="car">
            <box frame="0" xtl="100" ytl="50" xbr="325" ybr="190" outside="0" occluded="0" keyframe="1">
                <attribute name="type">sedan</attribute>
                ...
            </box>
            ...
        </track>
        <track id="1" label="car">
            <polygon frame="0" points="561.30,916.23;561.30,842.77;...;560.20,966.67" outside="0" occluded="0" keyframe="1">
                <attribute name="make">Honda</attribute>
                ...
            </polygon>
            ...
        </track>
        ...
        <track id="10" label="traffic_line">
            <polyline frame="10" points="462.10,0.00;126.80,1200.00" outside="0" occluded="0" keyframe="1">
                <attribute name="color">yellow</attribute>
                ...
            </polyline>
            ...
        </track>
        ...
        <track id="88" label="wheel">
            <points frame="176" points="574.90,939.48;1170.16,907.90;...;600.16,459.48" outside="0" occluded="0" keyframe="1">
                <attribute name="location">front_driver_side</attribute>
                ...
            </points>
            ...
        </track>
    </annotations>
    

Unlabeled videos have no corresponding file in `labels/`.

The `data/` and `labels/` files may contain nested subfolders of parallelly organized images and labels.

Note

See [`CVATVideoDatasetImporter`](../api/fiftyone.utils.cvat.html#fiftyone.utils.cvat.CVATVideoDatasetImporter "fiftyone.utils.cvat.CVATVideoDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a CVAT video dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/cvat-video-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.CVATVideoDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/cvat-video-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.CVATVideoDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a CVAT video dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/cvat-video-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.CVATVideoDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/cvat-labels"
     6
     7# Import dataset by explicitly providing paths to the source media and labels
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.CVATVideoDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/cvat-labels
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.CVATVideoDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

## OpenLABEL Image#

The [`fiftyone.types.OpenLABELImageDataset`](../api/fiftyone.types.html#fiftyone.types.OpenLABELImageDataset "fiftyone.types.OpenLABELImageDataset") type represents a labeled dataset consisting of images and their associated multitask predictions stored = in [OpenLABEL format](https://www.asam.net/index.php?eID=dumpFile&t=f&f=3876&token=413e8c85031ae64cc35cf42d0768627514868b2f).

OpenLABEL is a flexible format which allows labels to be stored in a variety of different ways with respect to the corresponding media files. The following enumerates the possible structures in which media data and OpenLABEL formatted label files can be stored in ways that is understood by FiftyOne:

  1. One label file per image. Each label contains only the metadata and labels associated with the image of the same name. In this case, the `labels_path` argument is expected to be a directory, if provided:



    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels/
            <uuid1>.json
            <uuid2>.json
            ...
    

  2. One label file for all images. The label file contains all of the metadata and labels associated with every image. In this case, there needs to be additional information provided in the label file to match labels to images. Specifically, the image filepath corresponding to a label must be stored as a stream:



    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels.json
    

  3. Multiple label files, each corresponding to one or more images. This case is similar to when there is a single label file, except that the label information may be spread out over multiple files. Since the filenames cannot be used to match labels to images, the image filepaths must again be stored as streams in the labels files:



    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels/
            <labels-filename1>.json
            <labels-filename2>.json
            ...
    

As for the actual structure of the labels files themselves, labels are stored in one or more JSON files and can follow a variety of formats. In general following this format:

Note

All object information stored in the `frames` key is applied to the corresponding image.
    
    
    {
        "openlabel": {
            "metadata": {
                "schema_version": "1.0.0",
                "uri": "/path/to/<uuid>.<ext>",
            },
            "objects": {
                "object_uuid1": {
                    "name": "instance1",
                    "type": "label1",
                    "object_data": {
                        "bbox": [
                            {
                                "name": "shape",
                                "val": [
                                    center-x,
                                    center-y,
                                    width,
                                    height
                                ]
                            }
                        ]
                    }
                },
                "object_uuid2": {
                    "name": "instance1",
                    "type": "label2",
                    "object_data": {},  # DEFINED IN FRAMES
                }
            },
            "frames": {
                "0": {
                   "frame_properties": {
                      "streams": {
                         "Camera1": {
                            "uri": "<uuid>.<ext>"
                         }
                      }
                   },
                   "objects": {
                      "object_uuid2": {
                         "object_data": {
                            "poly2d": [
                               {
                                  "attributes": {
                                     "boolean": [
                                        {
                                           "name": "is_hole",
                                           "val": false
                                        }
                                     ],
                                     "text": [
                                        {  # IF NOT PROVIDED OTHERWISE
                                           "name": "stream",
                                           "val": "Camera1"
                                        }
                                     ]
                                  },
                                  "closed": true,
                                  "mode": "MODE_POLY2D_ABSOLUTE",
                                  "name": "polygon_name",
                                  "stream": "Camera1",  # IF NOT IN ATTRIBUTES
                                  "val": [
                                     point1-x,
                                     point1-y,
                                     point2-x,
                                     point2-y,
                                     ...
                                  ]
                               }
                            ]
                         }
                      }
                  }
               }
            },
            "streams": {
               "Camera1": {
                  "description": "",
                  "stream_properties": {
                     "height": 480,
                     "width": 640
                  },
                  "type": "camera"
               }
            },
            "ontologies": ... # NOT PARSED
            "relations": ... # NOT PARSED
            "resources": ... # NOT PARSED
            "tags": ... # NOT PARSED
        }
    }
    

Note

See [`OpenLABELImageDatasetImporter`](../api/fiftyone.utils.openlabel.html#fiftyone.utils.openlabel.OpenLABELImageDatasetImporter "fiftyone.utils.openlabel.OpenLABELImageDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

If loading [`Keypoints`](../api/fiftyone.core.labels.html#fiftyone.core.labels.Keypoints "fiftyone.core.labels.Keypoints") related to a given [`KeypointSkeleton`](../api/fiftyone.core.odm.dataset.html#fiftyone.core.odm.dataset.KeypointSkeleton "fiftyone.core.odm.dataset.KeypointSkeleton"), then you can provide a `skeleton` and `skeleton_key` argument to the [`OpenLABELImageDatasetImporter`](../api/fiftyone.utils.openlabel.html#fiftyone.utils.openlabel.OpenLABELImageDatasetImporter "fiftyone.utils.openlabel.OpenLABELImageDatasetImporter") allowing you to match points in your annotations file to labels in the [`KeypointSkeleton`](../api/fiftyone.core.odm.dataset.html#fiftyone.core.odm.dataset.KeypointSkeleton "fiftyone.core.odm.dataset.KeypointSkeleton") and load the points and their attributes in the correct order.

You can create a FiftyOne dataset from a OpenLABEL image dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/openlabel-image-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.OpenLABELImageDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/openlabel-image-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.OpenLABELImageDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a OpenLABEL image dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/openlabel-image-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.OpenLABELImageDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5
     6labels_path = "/path/to/openlabel-labels.json"
     7# labels_path = "/path/to/openlabel-labels"
     8
     9# Import dataset by explicitly providing paths to the source media and labels
    10dataset = fo.Dataset.from_dir(
    11    dataset_type=fo.types.OpenLABELImageDataset,
    12    data_path=data_path,
    13    labels_path=labels_path,
    14    name=name,
    15)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    
    LABELS_PATH=/path/to/openlabel-labels.json
    # LABELS_PATH=/path/to/openlabel-labels
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.OpenLABELImageDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Note

OpenLABEL is a flexible format that allows for many user-specific decisions about how to represent labels and metadata. If you have OpenLABEL-compliant data in a format not understood by the current importers, please make an issue or contribute a pull request!

## OpenLABEL Video#

The [`fiftyone.types.OpenLABELVideoDataset`](../api/fiftyone.types.html#fiftyone.types.OpenLABELVideoDataset "fiftyone.types.OpenLABELVideoDataset") type represents a labeled dataset consisting of videos and their associated multitask predictions stored in [OpenLABEL format](https://www.asam.net/index.php?eID=dumpFile&t=f&f=3876&token=413e8c85031ae64cc35cf42d0768627514868b2f).

OpenLABEL is a flexible format which allows labels to be stored in a variety of different ways with respect to the corresponding media files. The following enumerates the possible structures in which media data and OpenLABEL formatted label files can be stored in ways that is understood by FiftyOne:

  1. One label file per video. Each label contains only the metadata and labels associated with the video of the same name. In this case, the `labels_path` argument is expected to be a directory, if provided:



    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels/
            <uuid1>.json
            <uuid2>.json
            ...
    

  2. One label file for all videos. The label file contains all of the metadata and labels associated with every video. In this case, there needs to be additional information provided in the label file to match labels to videos. Specifically, the video filepath corresponding to a label must be stored as a stream:



    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels.json
    

  3. Multiple label files, each corresponding to one or more videos. This case is similar to when there is a single label file, except that the label information may be spread out over multiple files. Since the filenames cannot be used to match labels to videos, the video filepaths must again be stored as streams in the labels files:



    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels/
            <labaels-filename1>.json
            <labaels-filename2>.json
            ...
    

As for the actual structure of the labels files themselves, labels are stored in one or more JSON files and can follow a variety of formats. In general following this format:
    
    
    {
        "openlabel": {
            "metadata": {
                "schema_version": "1.0.0",
                "uri": "/path/to/<uuid>.<ext>",
            },
            "objects": {
                "object_uuid1": {
                    "name": "instance1",
                    "type": "label1",
                    "object_data": {
                        "bbox": [
                            {
                                "name": "shape",
                                "val": [
                                    center-x,
                                    center-y,
                                    width,
                                    height
                                ]
                            }
                        ]
                    }
                    "frame_intervals": [{"frame_start": 0, "frame_end": 10}],
                },
                "object_uuid2": {
                    "name": "instance1",
                    "type": "label2",
                    "object_data": {},  # DEFINED IN FRAMES
                }
            },
            "frames": {
                "0": {
                   "frame_properties": {
                      "streams": {
                         "Camera1": {
                            "uri":"<uuid>.<ext>"
                         }
                      }
                   },
                   "objects": {
                      "object_uuid2": {
                         "object_data": {
                            "poly2d": [
                               {
                                  "attributes": {
                                     "boolean": [
                                        {
                                           "name": "is_hole",
                                           "val": false
                                        }
                                     ],
                                     "text": [
                                        {  # IF NOT PROVIDED OTHERWISE
                                           "name": "stream",
                                           "val": "Camera1"
                                        }
                                     ]
                                  },
                                  "closed": true,
                                  "mode": "MODE_POLY2D_ABSOLUTE",
                                  "name": "polygon_name",
                                  "stream": "Camera1",  # IF NOT IN ATTRIBUTES
                                  "val": [
                                     point1-x,
                                     point1-y,
                                     point2-x,
                                     point2-y,
                                     ...
                                  ]
                               }
                            ]
                         }
                      }
                  },
                  ...
               }
            },
            "streams": {
               "Camera1": {
                  "description": "",
                  "stream_properties": {
                     "height": 480,
                     "width": 640
                  },
                  "type": "camera"
               }
            },
            "ontologies": ...  # NOT PARSED
            "relations" ...  # NOT PARSED
            "resources" ...  # NOT PARSED
            "tags": ...  # NOT PARSED
        }
    }
    

Note

See [`OpenLABELVideoDatasetImporter`](../api/fiftyone.utils.openlabel.html#fiftyone.utils.openlabel.OpenLABELVideoDatasetImporter "fiftyone.utils.openlabel.OpenLABELVideoDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

If loading [`Keypoints`](../api/fiftyone.core.labels.html#fiftyone.core.labels.Keypoints "fiftyone.core.labels.Keypoints") related to a given [`KeypointSkeleton`](../api/fiftyone.core.odm.dataset.html#fiftyone.core.odm.dataset.KeypointSkeleton "fiftyone.core.odm.dataset.KeypointSkeleton"), then you can provide a `skeleton` and `skeleton_key` argument to the [`OpenLABELVideoDatasetImporter`](../api/fiftyone.utils.openlabel.html#fiftyone.utils.openlabel.OpenLABELVideoDatasetImporter "fiftyone.utils.openlabel.OpenLABELVideoDatasetImporter") allowing you to match points in your annotations file to labels in the [`KeypointSkeleton`](../api/fiftyone.core.odm.dataset.html#fiftyone.core.odm.dataset.KeypointSkeleton "fiftyone.core.odm.dataset.KeypointSkeleton") and load the points and their attributes in the correct order.

You can create a FiftyOne dataset from a OpenLABEL video dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/openlabel-video-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.OpenLABELVideoDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/openlabel-video-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.OpenLABELVideoDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a OpenLABEL video dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/openlabel-video-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.OpenLABELVideoDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/videos"
     5
     6labels_path = "/path/to/openlabel-labels.json"
     7# labels_path = "/path/to/openlabel-labels"
     8
     9# Import dataset by explicitly providing paths to the source media and labels
    10dataset = fo.Dataset.from_dir(
    11    dataset_type=fo.types.OpenLABELVideoDataset,
    12    data_path=data_path,
    13    labels_path=labels_path,
    14    name=name,
    15)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/videos
    
    LABELS_PATH=/path/to/openlabel-labels.json
    # LABELS_PATH=/path/to/openlabel-labels
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.OpenLABELVideoDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Note

OpenLABEL is a flexible format that allows for many user-specific decisions about how to represent labels and metadata. If you have OpenLABEL-compliant data in a format not understood by the current importers, please make an issue or contribute a pull request!

## BDD#

The [`fiftyone.types.BDDDataset`](../api/fiftyone.types.html#fiftyone.types.BDDDataset "fiftyone.types.BDDDataset") type represents a labeled dataset consisting of images and their associated multitask predictions saved in [Berkeley DeepDrive (BDD) format](http://bdd-data.berkeley.edu).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <filename0>.<ext>
            <filename1>.<ext>
            ...
        labels.json
    

where `labels.json` is a JSON file in the following format:
    
    
    [
        {
            "name": "<filename0>.<ext>",
            "attributes": {
                "scene": "city street",
                "timeofday": "daytime",
                "weather": "overcast"
            },
            "labels": [
                {
                    "id": 0,
                    "category": "traffic sign",
                    "manualAttributes": true,
                    "manualShape": true,
                    "attributes": {
                        "occluded": false,
                        "trafficLightColor": "none",
                        "truncated": false
                    },
                    "box2d": {
                        "x1": 1000.698742,
                        "x2": 1040.626872,
                        "y1": 281.992415,
                        "y2": 326.91156
                    },
                    "score": 0.95
                },
                ...
                {
                    "id": 34,
                    "category": "drivable area",
                    "manualAttributes": true,
                    "manualShape": true,
                    "attributes": {
                        "areaType": "direct"
                    },
                    "poly2d": [
                        {
                            "types": "LLLLCCC",
                            "closed": true,
                            "vertices": [
                                [241.143645, 697.923453],
                                [541.525255, 380.564983],
                                ...
                            ]
                        }
                    ],
                    "score": 0.87
                },
                ...
                {
                    "id": 109356,
                    "category": "lane",
                    "attributes": {
                        "laneDirection": "parallel",
                        "laneStyle": "dashed",
                        "laneType": "single white"
                    },
                    "manualShape": true,
                    "manualAttributes": true,
                    "poly2d": [
                        {
                            "types": "LL",
                            "closed": false,
                            "vertices": [
                                [492.879546, 331.939543],
                                [0, 471.076658],
                                ...
                            ]
                        }
                    ],
                    "score": 0.98
                },
                ...
            }
        }
        ...
    ]
    

Unlabeled images have no corresponding entry in `labels.json`.

The `name` attribute of the labels file encodes the location of the corresponding images, which can be any of the following:

  * The filename of an image in the `data/` folder

  * A relative path like `data/sub/folder/filename.ext` specifying the relative path to the image in a nested subfolder of `data/`

  * An absolute path to an image, which may or may not be in the `data/` folder




Note

See [`BDDDatasetImporter`](../api/fiftyone.utils.bdd.html#fiftyone.utils.bdd.BDDDatasetImporter "fiftyone.utils.bdd.BDDDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a BDD dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/bdd-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.BDDDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/bdd-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.BDDDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a BDD dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/bdd-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.BDDDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/bdd-labels.json"
     6
     7# Import dataset by explicitly providing paths to the source media and labels
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.BDDDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/bdd-labels.json
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.BDDDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Note

If the `name` key of your labels contains absolute paths to the source media, then you can omit the `data_path` parameter from the example above.

## CSV#

The [`fiftyone.types.CSVDataset`](../api/fiftyone.types.html#fiftyone.types.CSVDataset "fiftyone.types.CSVDataset") type represents a dataset consisting of images or videos and their associated field values stored as columns of a CSV file.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <filename1>.<ext>
            <filename2>.<ext>
            ...
        labels.csv
    

where `labels.csv` is a CSV file in the following format:
    
    
    field1,field2,field3,...
    value1,value2,value3,...
    value1,value2,value3,...
    ...
    

One sample will be generated per row in the CSV file (excluding the header row).

One column of the CSV file must contain media paths, which may be either:

  * filenames or relative paths to media files in `data/`

  * absolute paths to media files




By default it is assumed that a `filepath` column exists and contains the media paths, but you can customize this via the optional `media_field` parameter.

By default all columns are loaded as string fields, but you can provide the optional `fields` parameter to select a subset of columns to load or provide custom parsing functions for each field, as demonstrated below.

Note

See [`CSVDatasetImporter`](../api/fiftyone.utils.csv.html#fiftyone.utils.csv.CSVDatasetImporter "fiftyone.utils.csv.CSVDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a CSV dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/csv-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.CSVDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/csv-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.CSVDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a CSV dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/csv-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.CSVDataset
    

If your CSV file contains absolute media paths, then you can directly specify the path to the CSV file itself by providing the `labels_path` parameter.

Additionally, you can use the `fields` parameter to customize how each field is parsed, as demonstrated below:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4labels_path = "/path/to/labels.csv"
     5
     6fields = {
     7    "filepath": None,  # load as strings
     8    "tags": lambda v: v.strip("").split(","),
     9    "float_field": lambda v: float(v),
    10    "weather": lambda v: fo.Classification(label=v) if v else None,
    11}
    12
    13# Import CSV file with absolute media paths and custom field parsers
    14dataset = fo.Dataset.from_dir(
    15    dataset_type=fo.types.CSVDataset,
    16    labels_path=labels_path,
    17    fields=fields,
    18    name=name,
    19)
    
    
    
    NAME=my-dataset
    LABELS_PATH=/path/to/labels.csv
    
    # Import CSV file with absolute media paths
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.CSVDataset \
        --kwargs labels_path=$LABELS_PATH
    

## DICOM#

The [`fiftyone.types.DICOMDataset`](../api/fiftyone.types.html#fiftyone.types.DICOMDataset "fiftyone.types.DICOMDataset") type represents a dataset consisting of images and their associated properties stored in [DICOM format](https://en.wikipedia.org/wiki/DICOM).

Note

You must have [pydicom<3](https://github.com/pydicom/pydicom) installed in order to load DICOM datasets.

The standard format for datasets of this type is the following:
    
    
    <dataset_dir>/
        <filename1>.dcm
        <filename2>.dcm
    

where each `.dcm` file is a DICOM file that can be read via [`pydicom.dcmread`](https://pydicom.github.io/pydicom/stable/reference/generated/pydicom.filereader.dcmread.html#pydicom.filereader.dcmread "\(in pydicom v3.0.2\)").

Alternatively, rather than providing a `dataset_dir`, you can provide the `dicom_path` argument, which can directly specify a glob pattern of DICOM files or the path to a [DICOMDIR](https://pydicom.github.io/pydicom/stable/tutorials/filesets.html) file.

By default, all attributes in the DICOM files discoverable via [`pydicom.dataset.Dataset.dir()`](https://pydicom.github.io/pydicom/stable/reference/generated/pydicom.dataset.Dataset.html#pydicom.dataset.Dataset.dir "\(in pydicom v3.0.2\)") with supported types are loaded into sample-level fields, but you can select only specific attributes by passing the optional `keywords` argument.

Note

When importing DICOM datasets, the pixel data are converted to 8-bit images, using the `SmallestImagePixelValue` and `LargestImagePixelValue` attributes (if present), to inform the conversion.

The images are written to a backing directory that you can configure by passing the `images_dir` argument. By default, the images are written to `dataset_dir`.

Currently, only single frame images are supported, but a community contribution to support 3D or 4D image types (e.g., CT scans) is welcomed!

Note

See `DICOMDatasetImporter` for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a DICOM dataset stored in standard format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/dicom-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.DICOMDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/dicom-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.DICOMDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

You can create a FiftyOne dataset from a glob pattern of DICOM files or the path to a DICOMDIR file as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4
     5dicom_path = "/path/to/*.dcm"  # glob pattern of DICOM files
     6# dicom_path = "/path/to/DICOMDIR"  # DICOMDIR file
     7
     8# Create the dataset
     9dataset = fo.Dataset.from_dir(
    10    dicom_path=dicom_path,
    11    dataset_type=fo.types.DICOMDataset,
    12    keywords=["PatientName", "StudyID"],  # load specific attributes
    13    name=name,
    14)
    15
    16# View summary info about the dataset
    17print(dataset)
    18
    19# Print the first few samples in the dataset
    20print(dataset.head())
    
    
    
    NAME=my-dataset
    
    DICOM_PATH='/path/to/*.dcm'  # glob pattern of DICOM files
    # DICOM_PATH='/path/to/DICOMDIR'  # DICOMDIR file
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.DICOMDataset \
        --kwargs \
            dicom_path=$DICOM_PATH \
            keywords=PatientName,StudyID  # load specific attributes
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

## GeoJSON#

The [`fiftyone.types.GeoJSONDataset`](../api/fiftyone.types.html#fiftyone.types.GeoJSONDataset "fiftyone.types.GeoJSONDataset") type represents a dataset consisting of images or videos and their associated geolocation data and optional properties stored in [GeoJSON format](https://en.wikipedia.org/wiki/GeoJSON).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <filename1>.<ext>
            <filename2>.<ext>
            ...
        labels.json
    

where `labels.json` is a GeoJSON file containing a `FeatureCollection` in the following format:
    
    
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        -73.99496451958454,
                        40.66338032487842
                    ]
                },
                "properties": {
                    "filename": <filename1>.<ext>,
                    ...
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        -73.80992143421788,
                        40.65611832778962
                    ]
                },
                "properties": {
                    "filename": <filename2>.<ext>,
                    ...
                }
            },
            ...
        ]
    }
    

where the `geometry` field may contain any valid GeoJSON geometry object, and the `filename` property encodes the name of the corresponding media in the `data/` folder. The `filename` property can also be an absolute path, which may or may not be in the `data/` folder.

Samples with no location data will have a null `geometry` field.

The `properties` field of each feature can contain additional labels that can be imported.

Note

See [`GeoJSONDatasetImporter`](../api/fiftyone.utils.geojson.html#fiftyone.utils.geojson.GeoJSONDatasetImporter "fiftyone.utils.geojson.GeoJSONDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a GeoJSON dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/geojson-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.GeoJSONDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/geojson-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.GeoJSONDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a GeoJSON dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/geojson-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.GeoJSONDataset
    

You can also independently specify the locations of the labels and the root directory containing the corresponding media files by providing the `labels_path` and `data_path` parameters rather than `dataset_dir`:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4data_path = "/path/to/images"
     5labels_path = "/path/to/geo-labels.json"
     6
     7# Import dataset by explicitly providing paths to the source media and labels
     8dataset = fo.Dataset.from_dir(
     9    dataset_type=fo.types.GeoJSONDataset,
    10    data_path=data_path,
    11    labels_path=labels_path,
    12    name=name,
    13)
    
    
    
    NAME=my-dataset
    DATA_PATH=/path/to/images
    LABELS_PATH=/path/to/geo-labels.json
    
    # Import dataset by explicitly providing paths to the source media and labels
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.GeoJSONDataset \
        --kwargs \
            data_path=$DATA_PATH \
            labels_path=$LABELS_PATH
    

Note

If the `filename` key of your labels contains absolute paths to the source media, then you can omit the `data_path` parameter from the example above.

## GeoTIFF#

The [`fiftyone.types.GeoTIFFDataset`](../api/fiftyone.types.html#fiftyone.types.GeoTIFFDataset "fiftyone.types.GeoTIFFDataset") type represents a dataset consisting of images and their associated geolocation data stored in [GeoTIFF format](https://en.wikipedia.org/wiki/GeoTIFF).

Note

You must have [rasterio](https://github.com/mapbox/rasterio) installed in order to load GeoTIFF datasets.

The standard format for datasets of this type is the following:
    
    
    <dataset_dir>/
        <filename1>.tif
        <filename2>.tif
    

where each `.tif` file is a GeoTIFF image that can be read via [`rasterio.open`](https://rasterio.readthedocs.io/en/latest/api/rasterio.html#rasterio.open "\(in rasterio\)").

Alternatively, rather than providing a `dataset_dir`, you can provide the `image_path` argument, which can directly specify a list or glob pattern of GeoTIFF images to load.

The dataset will contain a [`GeoLocation`](../api/fiftyone.core.labels.html#fiftyone.core.labels.GeoLocation "fiftyone.core.labels.GeoLocation") field whose [`point`](../api/fiftyone.core.labels.html#fiftyone.core.labels.GeoLocation.point "fiftyone.core.labels.GeoLocation.point") attribute contains the `(longitude, latitude)` coordinates of each image center and whose [`polygon`](../api/fiftyone.core.labels.html#fiftyone.core.labels.GeoLocation.polygon "fiftyone.core.labels.GeoLocation.polygon") attribute contains the `(longitude, latitude)` coordinates of the corners of the image (clockwise, starting from the top-left corner).

Note

See [`GeoTIFFDatasetImporter`](../api/fiftyone.utils.geotiff.html#fiftyone.utils.geotiff.GeoTIFFDatasetImporter "fiftyone.utils.geotiff.GeoTIFFDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a GeoTIFF dataset stored in standard format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/geotiff-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.GeoTIFFDataset,
    10    label_field="location",
    11    name=name,
    12)
    13
    14# View summary info about the dataset
    15print(dataset)
    16
    17# Print the first few samples in the dataset
    18print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/geotiff-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.GeoTIFFDataset \
        --kwargs label_field=location
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

You can create a FiftyOne dataset from a list or glob pattern of GeoTIFF images as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4image_path = "/path/to/*.tif"  # glob pattern of GeoTIFF images
     5# image_path = ["/path/to/image1.tif", ...]  # list of GeoTIFF images
     6
     7# Create the dataset
     8dataset = fo.Dataset.from_dir(
     9    image_path=image_path,
    10    dataset_type=fo.types.GeoTIFFDataset,
    11    label_field="location",
    12    name=name,
    13)
    14
    15# View summary info about the dataset
    16print(dataset)
    17
    18# Print the first few samples in the dataset
    19print(dataset.head())
    
    
    
    NAME=my-dataset
    IMAGE_PATH='/path/to/*.tif'  # glob pattern of GeoTIFF images
    # IMAGE_PATH='/path/to/image1.tif,...'  # list of GeoTIFF images
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --type fiftyone.types.GeoTIFFDataset \
        --kwargs \
            image_path=$IMAGE_PATH \
            label_field=location
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

## FiftyOne Dataset#

The [`fiftyone.types.FiftyOneDataset`](../api/fiftyone.types.html#fiftyone.types.FiftyOneDataset "fiftyone.types.FiftyOneDataset") provides a disk representation of an entire [`Dataset`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") in a serialized JSON format along with its source media.

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        metadata.json
        samples.json
        data/
            <filename1>.<ext>
            <filename2>.<ext>
            ...
        annotations/
            <anno_key1>.json
            <anno_key2>.json
            ...
        brain/
            <brain_key1>.json
            <brain_key2>.json
            ...
        evaluations/
            <eval_key1>.json
            <eval_key2>.json
            ...
    

where `metadata.json` is a JSON file containing metadata associated with the dataset, `samples.json` is a JSON file containing a serialized representation of the samples in the dataset, `annotations/` contains any serialized [`AnnotationResults`](../api/fiftyone.core.annotation.html#fiftyone.core.annotation.AnnotationResults "fiftyone.core.annotation.AnnotationResults"), `brain/` contains any serialized [`BrainResults`](../api/fiftyone.core.brain.html#fiftyone.core.brain.BrainResults "fiftyone.core.brain.BrainResults"), and `evaluations/` contains any serialized [`EvaluationResults`](../api/fiftyone.core.evaluation.html#fiftyone.core.evaluation.EvaluationResults "fiftyone.core.evaluation.EvaluationResults").

The contents of the `data/` directory may also be organized in nested subfolders, depending on how the dataset was exported, in which case the filepaths in `samples.json` should contain correspondingly nested paths.

Video datasets have an additional `frames.json` file that contains a serialized representation of the frame labels for each video in the dataset.

Note

See [`FiftyOneDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.FiftyOneDatasetImporter "fiftyone.utils.data.importers.FiftyOneDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a directory in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/fiftyone-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.FiftyOneDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/fiftyone-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a dataset stored on disk in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/fiftyone-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneDataset
    

If you performed a [FiftyOneDataset export](export_datasets.html#fiftyonedataset-export) using the `rel_dir` parameter to strip a common prefix from the media filepaths in the dataset, then simply include the `rel_dir` parameter when importing back into FiftyOne to prepend the appropriate prefix to each media path:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/fiftyone-dataset"
     5
     6# Import dataset, prepending `rel_dir` to each media path
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.FiftyOneDataset,
    10    rel_dir="/common/images/dir",
    11    name=name,
    12)
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/fiftyone-dataset
    
    # Import dataset, prepending `rel_dir` to each media path
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneDataset \
        --kwargs rel_dir=/common/images/dir
    

Note

Exporting in [FiftyOneDataset format](export_datasets.html#fiftyonedataset-export) using the `export_media=False` and `rel_dir` parameters is a convenient way to transfer datasets between work environments, since this enables you to store the media files wherever you wish in each environment and then simply provide the appropriate `rel_dir` value as shown above when importing the dataset into FiftyOne in a new environment.

## FiftyOne Image Labels#

The [`fiftyone.types.FiftyOneImageLabelsDataset`](../api/fiftyone.types.html#fiftyone.types.FiftyOneImageLabelsDataset "fiftyone.types.FiftyOneImageLabelsDataset") type represents a labeled dataset consisting of images and their associated multitask predictions stored in [ETA ImageLabels format](https://github.com/voxel51/eta/blob/develop/docs/image_labels_guide.md).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels/
            <uuid1>.json
            <uuid2>.json
            ...
        manifest.json
    

where `manifest.json` is a JSON file in the following format:
    
    
    {
        "type": "eta.core.datasets.LabeledImageDataset",
        "description": "",
        "index": [
            {
                "data": "data/<uuid1>.<ext>",
                "labels": "labels/<uuid1>.json"
            },
            {
                "data": "data/<uuid2>.<ext>",
                "labels": "labels/<uuid2>.json"
            },
            ...
        ]
    }
    

and where each labels JSON file is stored in [ETA ImageLabels format](https://github.com/voxel51/eta/blob/develop/docs/image_labels_guide.md).

For unlabeled images, an empty `eta.core.image.ImageLabels` file is stored.

Note

See [`FiftyOneImageLabelsDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.FiftyOneImageLabelsDatasetImporter "fiftyone.utils.data.importers.FiftyOneImageLabelsDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from an image labels dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/image-labels-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.FiftyOneImageLabelsDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/image-labels-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneImageLabelsDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view an image labels dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/image-labels-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneImageLabelsDataset
    

## FiftyOne Video Labels#

The [`fiftyone.types.FiftyOneVideoLabelsDataset`](../api/fiftyone.types.html#fiftyone.types.FiftyOneVideoLabelsDataset "fiftyone.types.FiftyOneVideoLabelsDataset") type represents a labeled dataset consisting of videos and their associated labels stored in [ETA VideoLabels format](https://github.com/voxel51/eta/blob/develop/docs/video_labels_guide.md).

Datasets of this type are read in the following format:
    
    
    <dataset_dir>/
        data/
            <uuid1>.<ext>
            <uuid2>.<ext>
            ...
        labels/
            <uuid1>.json
            <uuid2>.json
            ...
        manifest.json
    

where `manifest.json` is a JSON file in the following format:
    
    
    {
        "type": "eta.core.datasets.LabeledVideoDataset",
        "description": "",
        "index": [
            {
                "data": "data/<uuid1>.<ext>",
                "labels": "labels/<uuid1>.json"
            },
            {
                "data": "data/<uuid2>.<ext>",
                "labels": "labels/<uuid2>.json"
            },
            ...
        ]
    }
    

and where each labels JSON file is stored in [ETA VideoLabels format](https://github.com/voxel51/eta/blob/develop/docs/video_labels_guide.md).

For unlabeled videos, an empty `eta.core.video.VideoLabels` file is written.

Note

See [`FiftyOneVideoLabelsDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.FiftyOneVideoLabelsDatasetImporter "fiftyone.utils.data.importers.FiftyOneVideoLabelsDatasetImporter") for parameters that can be passed to methods like [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") to customize the import of datasets of this type.

You can create a FiftyOne dataset from a video labels dataset stored in the above format as follows:

PythonCLI
    
    
     1import fiftyone as fo
     2
     3name = "my-dataset"
     4dataset_dir = "/path/to/video-labels-dataset"
     5
     6# Create the dataset
     7dataset = fo.Dataset.from_dir(
     8    dataset_dir=dataset_dir,
     9    dataset_type=fo.types.FiftyOneVideoLabelsDataset,
    10    name=name,
    11)
    12
    13# View summary info about the dataset
    14print(dataset)
    15
    16# Print the first few samples in the dataset
    17print(dataset.head())
    
    
    
    NAME=my-dataset
    DATASET_DIR=/path/to/video-labels-dataset
    
    # Create the dataset
    fiftyone datasets create \
        --name $NAME \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneVideoLabelsDataset
    
    # View summary info about the dataset
    fiftyone datasets info $NAME
    
    # Print the first few samples in the dataset
    fiftyone datasets head $NAME
    

To view a video labels dataset stored in the above format in the FiftyOne App without creating a persistent FiftyOne dataset, you can execute:
    
    
    DATASET_DIR=/path/to/video-labels-dataset
    
    # View the dataset in the App
    fiftyone app view \
        --dataset-dir $DATASET_DIR \
        --type fiftyone.types.FiftyOneVideoLabelsDataset
    

## Custom formats#

If your data does not follow one of the previous formats, then the simplest and most flexible approach to loading your data into FiftyOne is to iterate over your data in a loop and add it to a [`Dataset`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset").

Alternatively, the [`Dataset`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") class provides a [`Dataset.from_importer()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_importer "fiftyone.core.dataset.Dataset.from_importer") factory method that can be used to import a dataset using any [`DatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.DatasetImporter "fiftyone.utils.data.importers.DatasetImporter") instance.

This means that you can define your own [`DatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.DatasetImporter "fiftyone.utils.data.importers.DatasetImporter") class and then import a dataset from disk in your custom format using the following recipe:
    
    
    1import fiftyone as fo
    2
    3# Create an instance of your custom dataset importer
    4importer = CustomDatasetImporter(...)
    5
    6# Import the dataset
    7dataset = fo.Dataset.from_importer(importer)
    

You can also define a custom [`Dataset`](../api/fiftyone.types.html#fiftyone.types.Dataset "fiftyone.types.Dataset") type, which enables you to import datasets in your custom format using the [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") factory method:
    
    
    1import fiftyone as fo
    2
    3# The `fiftyone.types.Dataset` subclass for your custom dataset
    4dataset_type = CustomDataset
    5
    6# Import the dataset
    7dataset = fo.Dataset.from_dir(dataset_type=dataset_type, ...)
    

### Writing a custom DatasetImporter#

[`DatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.DatasetImporter "fiftyone.utils.data.importers.DatasetImporter") is an abstract interface; the concrete interface that you should implement is determined by the type of dataset that you are importing.

Generic datasetsBatch importsUnlabeled image datasetsLabeled image datasetsUnlabeled video datasetsLabeled video datasetsGrouped datasets

The [`GenericSampleDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GenericSampleDatasetImporter "fiftyone.utils.data.importers.GenericSampleDatasetImporter") interface allows you to define importers that emit a sequence of arbitrary [`Sample`](../api/fiftyone.utils.data.html#fiftyone.utils.data.Sample "fiftyone.core.sample.Sample") objects.

The pseudocode below provides a template for a custom [`GenericSampleDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GenericSampleDatasetImporter "fiftyone.utils.data.importers.GenericSampleDatasetImporter"):
    
    
      1import fiftyone.utils.data as foud
      2
      3class CustomGenericSampleDatasetImporter(foud.GenericSampleDatasetImporter):
      4    """Custom importer for generic sample datasets.
      5
      6    Args:
      7        dataset_dir (None): the dataset directory. This may be optional for
      8            some importers
      9        shuffle (False): whether to randomly shuffle the order in which the
     10            samples are imported
     11        seed (None): a random seed to use when shuffling
     12        max_samples (None): a maximum number of samples to import. By default,
     13            all samples are imported
     14        **kwargs: additional keyword arguments for your importer
     15    """
     16
     17    def __init__(
     18        self,
     19        dataset_dir=None,
     20        shuffle=False,
     21        seed=None,
     22        max_samples=None,
     23        **kwargs,
     24    ):
     25        super().__init__(
     26            dataset_dir=dataset_dir,
     27            shuffle=shuffle,
     28            seed=seed,
     29            max_samples=max_samples
     30        )
     31        # Your initialization here
     32
     33    def __len__(self):
     34        """The total number of samples that will be imported.
     35
     36        Raises:
     37            TypeError: if the total number is not known
     38        """
     39        # Return the total number of samples in the dataset (if known)
     40        pass
     41
     42    def __next__(self):
     43        """Returns information about the next sample in the dataset.
     44
     45        Returns:
     46            a :class:`fiftyone.core.sample.Sample` instance
     47
     48        Raises:
     49            StopIteration: if there are no more samples to import
     50        """
     51        # Implement loading the next sample in your dataset here
     52        pass
     53
     54    @property
     55    def has_dataset_info(self):
     56        """Whether this importer produces a dataset info dictionary."""
     57        # Return True or False here
     58        pass
     59
     60    @property
     61    def has_sample_field_schema(self):
     62        """Whether this importer produces a sample field schema."""
     63        # Return True or False here
     64        pass
     65
     66    def setup(self):
     67        """Performs any necessary setup before importing the first sample in
     68        the dataset.
     69
     70        This method is called when the importer's context manager interface is
     71        entered, :func:`DatasetImporter.__enter__`.
     72        """
     73        # Your custom setup here
     74        pass
     75
     76    def get_dataset_info(self):
     77        """Returns the dataset info for the dataset.
     78
     79        By convention, this method should be called after all samples in the
     80        dataset have been imported.
     81
     82        Returns:
     83            a dict of dataset info
     84        """
     85        # Return a dict of dataset info, if supported by your importer
     86        pass
     87
     88    def get_sample_field_schema(self):
     89        """Returns a dictionary describing the field schema of the samples
     90        loaded by this importer.
     91
     92        Returns:
     93            a dict mapping field names to :class:`fiftyone.core.fields.Field`
     94            instances or ``str(field)`` representations of them
     95        """
     96        # Return the sample schema here, if known
     97        pass
     98
     99    def close(self, *args):
    100        """Performs any necessary actions after the last sample has been
    101        imported.
    102
    103        This method is called when the importer's context manager interface is
    104        exited, :func:`DatasetImporter.__exit__`.
    105
    106        Args:
    107            *args: the arguments to :func:`DatasetImporter.__exit__`
    108        """
    109        # Your custom code here to complete the import
    110        pass
    

When [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") is called with a custom [`GenericSampleDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GenericSampleDatasetImporter "fiftyone.utils.data.importers.GenericSampleDatasetImporter"), the import is effectively performed via the pseudocode below:
    
    
    import fiftyone as fo
    
    dataset = fo.Dataset(...)
    importer = CustomGenericSampleDatasetImporter(...)
    
    with importer:
        for sample in importer:
            dataset.add_sample(sample)
    
        if importer.has_dataset_info:
            info = importer.get_dataset_info()
            parse_info(dataset, info)
    

Note that the importer is invoked via its context manager interface, which automatically calls the [`setup()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GenericSampleDatasetImporter.setup "fiftyone.utils.data.importers.GenericSampleDatasetImporter.setup") and [`close()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GenericSampleDatasetImporter.close "fiftyone.utils.data.importers.GenericSampleDatasetImporter.close") methods of the importer to handle setup/completion of the import.

The samples in the dataset are iteratively loaded by invoking the [`__next__()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GenericSampleDatasetImporter.__next__ "fiftyone.utils.data.importers.GenericSampleDatasetImporter.__next__") method of the importer.

The [`has_dataset_info`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GenericSampleDatasetImporter.has_dataset_info "fiftyone.utils.data.importers.GenericSampleDatasetImporter.has_dataset_info") property of the importer allows it to declare whether its [`get_dataset_info()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GenericSampleDatasetImporter.get_dataset_info "fiftyone.utils.data.importers.GenericSampleDatasetImporter.get_dataset_info") method should be called after all samples have been imported to retrieve dataset-level information to store on the FiftyOne dataset. See this section for more information.

The [`BatchDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.BatchDatasetImporter "fiftyone.utils.data.importers.BatchDatasetImporter") interface allows you to define importers that load all of their [`Sample`](../api/fiftyone.utils.data.html#fiftyone.utils.data.Sample "fiftyone.core.sample.Sample") objects onto a dataset via a single custom method. This interface allows for greater efficiency for import formats that handle aggregating over the samples themselves.

The pseudocode below provides a template for a custom [`BatchDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.BatchDatasetImporter "fiftyone.utils.data.importers.BatchDatasetImporter"):
    
    
      1import fiftyone.utils.data as foud
      2
      3class CustomBatchDatasetImporter(foud.BatchDatasetImporter):
      4    """Custom batch importer for datasets.
      5
      6    Args:
      7        dataset_dir (None): the dataset directory. This may be optional for
      8            some importers
      9        shuffle (False): whether to randomly shuffle the order in which the
     10            samples are imported
     11        seed (None): a random seed to use when shuffling
     12        max_samples (None): a maximum number of samples to import. By default,
     13            all samples are imported
     14        **kwargs: additional keyword arguments for your importer
     15    """
     16
     17    def __init__(
     18        self,
     19        dataset_dir=None,
     20        shuffle=False,
     21        seed=None,
     22        max_samples=None,
     23        **kwargs,
     24    ):
     25        super().__init__(
     26            dataset_dir=dataset_dir,
     27            shuffle=shuffle,
     28            seed=seed,
     29            max_samples=max_samples
     30        )
     31        # Your initialization here
     32
     33    def __len__(self):
     34        """The total number of samples that will be imported.
     35
     36        Raises:
     37            TypeError: if the total number is not known
     38        """
     39        # Return the total number of samples in the dataset (if known)
     40        pass
     41
     42    def import_samples(self, dataset, tags=None, progress=None):
     43        """Imports the samples into the given dataset.
     44
     45        Args:
     46            dataset: a :class:`fiftyone.core.dataset.Dataset`
     47            tags (None): an optional list of tags to attach to each sample
     48            progress (None): whether to render a progress bar (True/False), use
     49                the default value ``fiftyone.config.show_progress_bars``
     50                (None), or a progress callback function to invoke instead
     51
     52        Returns:
     53            a list of IDs of the samples that were added to the dataset
     54        """
     55        # Implement adding the samples to the dataset here
     56        pass
     57
     58    @property
     59    def has_dataset_info(self):
     60        """Whether this importer produces a dataset info dictionary."""
     61        # Return True or False here
     62        pass
     63
     64    @property
     65    def has_sample_field_schema(self):
     66        """Whether this importer produces a sample field schema."""
     67        # Return True or False here
     68        pass
     69
     70    def setup(self):
     71        """Performs any necessary setup before importing the first sample in
     72        the dataset.
     73
     74        This method is called when the importer's context manager interface is
     75        entered, :func:`DatasetImporter.__enter__`.
     76        """
     77        # Your custom setup here
     78        pass
     79
     80    def get_dataset_info(self):
     81        """Returns the dataset info for the dataset.
     82
     83        By convention, this method should be called after all samples in the
     84        dataset have been imported.
     85
     86        Returns:
     87            a dict of dataset info
     88        """
     89        # Return a dict of dataset info, if supported by your importer
     90        pass
     91
     92    def get_sample_field_schema(self):
     93        """Returns a dictionary describing the field schema of the samples
     94        loaded by this importer.
     95
     96        Returns:
     97            a dict mapping field names to :class:`fiftyone.core.fields.Field`
     98            instances or ``str(field)`` representations of them
     99        """
    100        # Return the sample schema here, if known
    101        pass
    102
    103    def close(self, *args):
    104        """Performs any necessary actions after the last sample has been
    105        imported.
    106
    107        This method is called when the importer's context manager interface is
    108        exited, :func:`DatasetImporter.__exit__`.
    109
    110        Args:
    111            *args: the arguments to :func:`DatasetImporter.__exit__`
    112        """
    113        # Your custom code here to complete the import
    114        pass
    

When [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") is called with a custom [`BatchDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.BatchDatasetImporter "fiftyone.utils.data.importers.BatchDatasetImporter"), the import is effectively performed via the pseudocode below:
    
    
    import fiftyone as fo
    
    dataset = fo.Dataset(...)
    importer = CustomBatchDatasetImporter(...)
    
    with importer:
        impoter.import_samples(dataset, ...)
    
        if importer.has_dataset_info:
            info = importer.get_dataset_info()
            parse_info(dataset, info)
    

Note that the importer is invoked via its context manager interface, which automatically calls the [`setup()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.BatchDatasetImporter.setup "fiftyone.utils.data.importers.BatchDatasetImporter.setup") and [`close()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.BatchDatasetImporter.close "fiftyone.utils.data.importers.BatchDatasetImporter.close") methods of the importer to handle setup/completion of the import.

The samples are then imported via a single call to the [`import_samples()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.BatchDatasetImporter.import_samples "fiftyone.utils.data.importers.BatchDatasetImporter.import_samples") method of the importer.

The [`has_dataset_info`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.BatchDatasetImporter.has_dataset_info "fiftyone.utils.data.importers.BatchDatasetImporter.has_dataset_info") property of the importer allows it to declare whether its [`get_dataset_info()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.BatchDatasetImporter.get_dataset_info "fiftyone.utils.data.importers.BatchDatasetImporter.get_dataset_info") method should be called after all samples have been imported to retrieve dataset-level information to store on the FiftyOne dataset. See this section for more information.

To define a custom importer for unlabeled image datasets, implement the [`UnlabeledImageDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter") interface.

The pseudocode below provides a template for a custom [`UnlabeledImageDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter"):
    
    
      1import fiftyone.utils.data as foud
      2
      3class CustomUnlabeledImageDatasetImporter(foud.UnlabeledImageDatasetImporter):
      4    """Custom importer for unlabeled image datasets.
      5
      6    Args:
      7        dataset_dir (None): the dataset directory. This may be optional for
      8            some importers
      9        shuffle (False): whether to randomly shuffle the order in which the
     10            samples are imported
     11        seed (None): a random seed to use when shuffling
     12        max_samples (None): a maximum number of samples to import. By default,
     13            all samples are imported
     14        **kwargs: additional keyword arguments for your importer
     15    """
     16
     17    def __init__(
     18        self,
     19        dataset_dir=None,
     20        shuffle=False,
     21        seed=None,
     22        max_samples=None,
     23        **kwargs,
     24    ):
     25        super().__init__(
     26            dataset_dir=dataset_dir,
     27            shuffle=shuffle,
     28            seed=seed,
     29            max_samples=max_samples
     30        )
     31        # Your initialization here
     32
     33    def __len__(self):
     34        """The total number of samples that will be imported.
     35
     36        Raises:
     37            TypeError: if the total number is not known
     38        """
     39        # Return the total number of samples in the dataset (if known)
     40        pass
     41
     42    def __next__(self):
     43        """Returns information about the next sample in the dataset.
     44
     45        Returns:
     46            an ``(image_path, image_metadata)`` tuple, where:
     47            -   ``image_path`` is the path to the image on disk
     48            -   ``image_metadata`` is an
     49                :class:`fiftyone.core.metadata.ImageMetadata` instances for the
     50                image, or ``None`` if :meth:`has_image_metadata` is ``False``
     51
     52        Raises:
     53            StopIteration: if there are no more samples to import
     54        """
     55        # Implement loading the next sample in your dataset here
     56        pass
     57
     58    @property
     59    def has_dataset_info(self):
     60        """Whether this importer produces a dataset info dictionary."""
     61        # Return True or False here
     62        pass
     63
     64    @property
     65    def has_image_metadata(self):
     66        """Whether this importer produces
     67        :class:`fiftyone.core.metadata.ImageMetadata` instances for each image.
     68        """
     69        # Return True or False here
     70        pass
     71
     72    def setup(self):
     73        """Performs any necessary setup before importing the first sample in
     74        the dataset.
     75
     76        This method is called when the importer's context manager interface is
     77        entered, :func:`DatasetImporter.__enter__`.
     78        """
     79        # Your custom setup here
     80        pass
     81
     82    def get_dataset_info(self):
     83        """Returns the dataset info for the dataset.
     84
     85        By convention, this method should be called after all samples in the
     86        dataset have been imported.
     87
     88        Returns:
     89            a dict of dataset info
     90        """
     91        # Return a dict of dataset info, if supported by your importer
     92        pass
     93
     94    def close(self, *args):
     95        """Performs any necessary actions after the last sample has been
     96        imported.
     97
     98        This method is called when the importer's context manager interface is
     99        exited, :func:`DatasetImporter.__exit__`.
    100
    101        Args:
    102            *args: the arguments to :func:`DatasetImporter.__exit__`
    103        """
    104        # Your custom code here to complete the import
    105        pass
    

When [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") is called with a custom [`UnlabeledImageDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter"), the import is effectively performed via the pseudocode below:
    
    
    import fiftyone as fo
    
    dataset = fo.Dataset(...)
    importer = CustomUnlabeledImageDatasetImporter(...)
    
    with importer:
        for image_path, image_metadata in importer:
            dataset.add_sample(
                fo.Sample(filepath=image_path, metadata=image_metadata)
            )
    
        if importer.has_dataset_info:
            info = importer.get_dataset_info()
            parse_info(dataset, info)
    

Note that the importer is invoked via its context manager interface, which automatically calls the [`setup()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.setup "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.setup") and [`close()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.close "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.close") methods of the importer to handle setup/completion of the import.

The images in the dataset are iteratively loaded by invoking the [`__next__()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.__next__ "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.__next__") method of the importer.

The [`has_dataset_info`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.has_dataset_info "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.has_dataset_info") property of the importer allows it to declare whether its [`get_dataset_info()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.get_dataset_info "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.get_dataset_info") method should be called after all samples have been imported to retrieve dataset-level information to store on the FiftyOne dataset. See this section for more information.

The [`has_image_metadata`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.has_image_metadata "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.has_image_metadata") property of the importer allows it to declare whether it returns [`ImageMetadata`](../api/fiftyone.core.metadata.html#fiftyone.core.metadata.ImageMetadata "fiftyone.core.metadata.ImageMetadata") instances for each image that it loads when [`__next__()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.__next__ "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter.__next__") is called.

To define a custom importer for labeled image datasets, implement the [`LabeledImageDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter "fiftyone.utils.data.importers.LabeledImageDatasetImporter") interface.

The pseudocode below provides a template for a custom [`LabeledImageDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter "fiftyone.utils.data.importers.LabeledImageDatasetImporter"):
    
    
      1import fiftyone.utils.data as foud
      2
      3class CustomLabeledImageDatasetImporter(foud.LabeledImageDatasetImporter):
      4    """Custom importer for labeled image datasets.
      5
      6    Args:
      7        dataset_dir (None): the dataset directory. This may be optional for
      8            some importers
      9        shuffle (False): whether to randomly shuffle the order in which the
     10            samples are imported
     11        seed (None): a random seed to use when shuffling
     12        max_samples (None): a maximum number of samples to import. By default,
     13            all samples are imported
     14        **kwargs: additional keyword arguments for your importer
     15    """
     16
     17    def __init__(
     18        self,
     19        dataset_dir=None,
     20        shuffle=False,
     21        seed=None,
     22        max_samples=None,
     23        **kwargs,
     24    ):
     25        super().__init__(
     26            dataset_dir=dataset_dir,
     27            shuffle=shuffle,
     28            seed=seed,
     29            max_samples=max_samples,
     30        )
     31        # Your initialization here
     32
     33    def __len__(self):
     34        """The total number of samples that will be imported.
     35
     36        Raises:
     37            TypeError: if the total number is not known
     38        """
     39        # Return the total number of samples in the dataset (if known)
     40        pass
     41
     42    def __next__(self):
     43        """Returns information about the next sample in the dataset.
     44
     45        Returns:
     46            an  ``(image_path, image_metadata, label)`` tuple, where
     47
     48            -   ``image_path``: the path to the image on disk
     49            -   ``image_metadata``: an
     50                :class:`fiftyone.core.metadata.ImageMetadata` instances for the
     51                image, or ``None`` if :meth:`has_image_metadata` is ``False``
     52            -   ``label``: an instance of :meth:`label_cls`, or a dictionary
     53                mapping field names to :class:`fiftyone.core.labels.Label`
     54                instances, or ``None`` if the sample is unlabeled
     55
     56        Raises:
     57            StopIteration: if there are no more samples to import
     58        """
     59        # Implement loading the next sample in your dataset here
     60        pass
     61
     62    @property
     63    def has_dataset_info(self):
     64        """Whether this importer produces a dataset info dictionary."""
     65        # Return True or False here
     66        pass
     67
     68    @property
     69    def has_image_metadata(self):
     70        """Whether this importer produces
     71        :class:`fiftyone.core.metadata.ImageMetadata` instances for each image.
     72        """
     73        # Return True or False here
     74        pass
     75
     76    @property
     77    def label_cls(self):
     78        """The :class:`fiftyone.core.labels.Label` class(es) returned by this
     79        importer.
     80
     81        This can be any of the following:
     82
     83        -   a :class:`fiftyone.core.labels.Label` class. In this case, the
     84            importer is guaranteed to return labels of this type
     85        -   a list or tuple of :class:`fiftyone.core.labels.Label` classes. In
     86            this case, the importer can produce a single label field of any of
     87            these types
     88        -   a dict mapping keys to :class:`fiftyone.core.labels.Label` classes.
     89            In this case, the importer will return label dictionaries with keys
     90            and value-types specified by this dictionary. Not all keys need be
     91            present in the imported labels
     92        -   ``None``. In this case, the importer makes no guarantees about the
     93            labels that it may return
     94        """
     95        # Return the appropriate value here
     96        pass
     97
     98    def setup(self):
     99        """Performs any necessary setup before importing the first sample in
    100        the dataset.
    101
    102        This method is called when the importer's context manager interface is
    103        entered, :func:`DatasetImporter.__enter__`.
    104        """
    105        # Your custom setup here
    106        pass
    107
    108    def get_dataset_info(self):
    109        """Returns the dataset info for the dataset.
    110
    111        By convention, this method should be called after all samples in the
    112        dataset have been imported.
    113
    114        Returns:
    115            a dict of dataset info
    116        """
    117        # Return a dict of dataset info, if supported by your importer
    118        pass
    119
    120    def close(self, *args):
    121        """Performs any necessary actions after the last sample has been
    122        imported.
    123
    124        This method is called when the importer's context manager interface is
    125        exited, :func:`DatasetImporter.__exit__`.
    126
    127        Args:
    128            *args: the arguments to :func:`DatasetImporter.__exit__`
    129        """
    130        # Your custom code here to complete the import
    131        pass
    

When [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") is called with a custom [`LabeledImageDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter "fiftyone.utils.data.importers.LabeledImageDatasetImporter"), the import is effectively performed via the pseudocode below:
    
    
    import fiftyone as fo
    
    dataset = fo.Dataset(...)
    importer = CustomLabeledImageDatasetImporter(...)
    label_field = ...
    
    if isinstance(label_field, dict):
        label_key = lambda k: label_field.get(k, k)
    elif label_field is not None:
        label_key = lambda k: label_field + "_" + k
    else:
        label_field = "ground_truth"
        label_key = lambda k: k
    
    with importer:
        for image_path, image_metadata, label in importer:
            sample = fo.Sample(filepath=image_path, metadata=image_metadata)
    
            if isinstance(label, dict):
                sample.update_fields({label_key(k): v for k, v in label.items()})
            elif label is not None:
                sample[label_field] = label
    
            dataset.add_sample(sample)
    
        if importer.has_dataset_info:
            info = importer.get_dataset_info()
            parse_info(dataset, info)
    

Note that the importer is invoked via its context manager interface, which automatically calls the [`setup()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter.setup "fiftyone.utils.data.importers.LabeledImageDatasetImporter.setup") and [`close()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter.close "fiftyone.utils.data.importers.LabeledImageDatasetImporter.close") methods of the importer to handle setup/completion of the import.

The images and their corresponding [`Label`](../api/fiftyone.core.labels.html#fiftyone.core.labels.Label "fiftyone.core.labels.Label") instances in the dataset are iteratively loaded by invoking the [`__next__()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter.__next__ "fiftyone.utils.data.importers.LabeledImageDatasetImporter.__next__") method of the importer.

The [`has_dataset_info`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter.has_dataset_info "fiftyone.utils.data.importers.LabeledImageDatasetImporter.has_dataset_info") property of the importer allows it to declare whether its [`get_dataset_info()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter.get_dataset_info "fiftyone.utils.data.importers.LabeledImageDatasetImporter.get_dataset_info") method should be called after all samples have been imported to retrieve dataset-level information to store on the FiftyOne dataset. See this section for more information.

The [`label_cls`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter.label_cls "fiftyone.utils.data.importers.LabeledImageDatasetImporter.label_cls") property of the importer declares the type of label(s) that the importer will produce.

The [`has_image_metadata`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter.has_image_metadata "fiftyone.utils.data.importers.LabeledImageDatasetImporter.has_image_metadata") property of the importer allows it to declare whether it returns [`ImageMetadata`](../api/fiftyone.core.metadata.html#fiftyone.core.metadata.ImageMetadata "fiftyone.core.metadata.ImageMetadata") instances for each image that it loads when [`__next__()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter.__next__ "fiftyone.utils.data.importers.LabeledImageDatasetImporter.__next__") is called.

To define a custom importer for unlabeled video datasets, implement the [`UnlabeledVideoDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter") interface.

The pseudocode below provides a template for a custom [`UnlabeledVideoDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter"):
    
    
      1import fiftyone.utils.data as foud
      2
      3class CustomUnlabeledVideoDatasetImporter(foud.UnlabeledVideoDatasetImporter):
      4    """Custom importer for unlabeled video datasets.
      5
      6    Args:
      7        dataset_dir (None): the dataset directory. This may be optional for
      8            some importers
      9        shuffle (False): whether to randomly shuffle the order in which the
     10            samples are imported
     11        seed (None): a random seed to use when shuffling
     12        max_samples (None): a maximum number of samples to import. By default,
     13            all samples are imported
     14        **kwargs: additional keyword arguments for your importer
     15    """
     16
     17    def __init__(
     18        self,
     19        dataset_dir=None,
     20        shuffle=False,
     21        seed=None,
     22        max_samples=None,
     23        **kwargs,
     24    ):
     25        super().__init__(
     26            dataset_dir=dataset_dir,
     27            shuffle=shuffle,
     28            seed=seed,
     29            max_samples=max_samples,
     30        )
     31        # Your initialization here
     32
     33    def __len__(self):
     34        """The total number of samples that will be imported.
     35
     36        Raises:
     37            TypeError: if the total number is not known
     38        """
     39        # Return the total number of samples in the dataset (if known)
     40        pass
     41
     42    def __next__(self):
     43        """Returns information about the next sample in the dataset.
     44
     45        Returns:
     46            an ``(video_path, video_metadata)`` tuple, where:
     47            -   ``video_path`` is the path to the video on disk
     48            -   ``video_metadata`` is an
     49                :class:`fiftyone.core.metadata.VideoMetadata` instances for the
     50                video, or ``None`` if :meth:`has_video_metadata` is ``False``
     51
     52        Raises:
     53            StopIteration: if there are no more samples to import
     54        """
     55        # Implement loading the next sample in your dataset here
     56        pass
     57
     58    @property
     59    def has_dataset_info(self):
     60        """Whether this importer produces a dataset info dictionary."""
     61        # Return True or False here
     62        pass
     63
     64    @property
     65    def has_video_metadata(self):
     66        """Whether this importer produces
     67        :class:`fiftyone.core.metadata.VideoMetadata` instances for each video.
     68        """
     69        # Return True or False here
     70        pass
     71
     72    def setup(self):
     73        """Performs any necessary setup before importing the first sample in
     74        the dataset.
     75
     76        This method is called when the importer's context manager interface is
     77        entered, :func:`DatasetImporter.__enter__`.
     78        """
     79        # Your custom setup here
     80        pass
     81
     82    def get_dataset_info(self):
     83        """Returns the dataset info for the dataset.
     84
     85        By convention, this method should be called after all samples in the
     86        dataset have been imported.
     87
     88        Returns:
     89            a dict of dataset info
     90        """
     91        # Return a dict of dataset info, if supported by your importer
     92        pass
     93
     94    def close(self, *args):
     95        """Performs any necessary actions after the last sample has been
     96        imported.
     97
     98        This method is called when the importer's context manager interface is
     99        exited, :func:`DatasetImporter.__exit__`.
    100
    101        Args:
    102            *args: the arguments to :func:`DatasetImporter.__exit__`
    103        """
    104        # Your custom code here to complete the import
    105        pass
    

When [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") is called with a custom [`UnlabeledVideoDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter"), the import is effectively performed via the pseudocode below:
    
    
    import fiftyone as fo
    
    dataset = fo.Dataset(...)
    importer = CustomUnlabeledVideoDatasetImporter(...)
    
    with importer:
        for video_path, video_metadata in importer:
            dataset.add_sample(
                fo.Sample(filepath=video_path, metadata=video_metadata)
            )
    
        if importer.has_dataset_info:
            info = importer.get_dataset_info()
            parse_info(dataset, info)
    

Note that the importer is invoked via its context manager interface, which automatically calls the [`setup()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.setup "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.setup") and [`close()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.close "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.close") methods of the importer to handle setup/completion of the import.

The videos in the dataset are iteratively loaded by invoking the [`__next__()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.__next__ "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.__next__") method of the importer.

The [`has_dataset_info`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.has_dataset_info "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.has_dataset_info") property of the importer allows it to declare whether its [`get_dataset_info()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.get_dataset_info "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.get_dataset_info") method should be called after all samples have been imported to retrieve dataset-level information to store on the FiftyOne dataset. See this section for more information.

The [`has_video_metadata`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.has_video_metadata "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.has_video_metadata") property of the importer allows it to declare whether it returns [`VideoMetadata`](../api/fiftyone.core.metadata.html#fiftyone.core.metadata.VideoMetadata "fiftyone.core.metadata.VideoMetadata") instances for each video that it loads when [`__next__()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.__next__ "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter.__next__") is called.

To define a custom importer for labeled video datasets, implement the [`LabeledVideoDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter "fiftyone.utils.data.importers.LabeledVideoDatasetImporter") interface.

The pseudocode below provides a template for a custom [`LabeledVideoDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter "fiftyone.utils.data.importers.LabeledVideoDatasetImporter"):
    
    
      1import fiftyone.utils.data as foud
      2
      3class CustomLabeledVideoDatasetImporter(foud.LabeledVideoDatasetImporter):
      4    """Custom importer for labeled video datasets.
      5
      6    Args:
      7        dataset_dir (None): the dataset directory. This may be optional for
      8            some importers
      9        shuffle (False): whether to randomly shuffle the order in which the
     10            samples are imported
     11        seed (None): a random seed to use when shuffling
     12        max_samples (None): a maximum number of samples to import. By default,
     13            all samples are imported
     14        **kwargs: additional keyword arguments for your importer
     15    """
     16
     17    def __init__(
     18        self,
     19        dataset_dir=None,
     20        shuffle=False,
     21        seed=None,
     22        max_samples=None,
     23        **kwargs,
     24    ):
     25        super().__init__(
     26            dataset_dir=dataset_dir,
     27            shuffle=shuffle,
     28            seed=seed,
     29            max_samples=max_samples,
     30        )
     31        # Your initialization here
     32
     33    def __len__(self):
     34        """The total number of samples that will be imported.
     35
     36        Raises:
     37            TypeError: if the total number is not known
     38        """
     39        # Return the total number of samples in the dataset (if known)
     40        pass
     41
     42    def __next__(self):
     43    """Returns information about the next sample in the dataset.
     44
     45        Returns:
     46            an  ``(video_path, video_metadata, labels, frames)`` tuple, where
     47
     48            -   ``video_path``: the path to the video on disk
     49            -   ``video_metadata``: an
     50                :class:`fiftyone.core.metadata.VideoMetadata` instances for the
     51                video, or ``None`` if :meth:`has_video_metadata` is ``False``
     52            -   ``labels``: sample-level labels for the video, which can be any
     53                of the following::
     54
     55                -   a :class:`fiftyone.core.labels.Label` instance
     56                -   a dictionary mapping label fields to
     57                    :class:`fiftyone.core.labels.Label` instances
     58                -   ``None`` if the sample has no sample-level labels
     59
     60            -   ``frames``: frame-level labels for the video, which can
     61                be any of the following::
     62
     63                -   a dictionary mapping frame numbers to dictionaries that
     64                    map label fields to :class:`fiftyone.core.labels.Label`
     65                    instances for each video frame
     66                -   ``None`` if the sample has no frame-level labels
     67
     68        Raises:
     69            StopIteration: if there are no more samples to import
     70        """
     71        # Implement loading the next sample in your dataset here
     72        pass
     73
     74    @property
     75    def has_dataset_info(self):
     76        """Whether this importer produces a dataset info dictionary."""
     77        # Return True or False here
     78        pass
     79
     80    @property
     81    def has_video_metadata(self):
     82        """Whether this importer produces
     83        :class:`fiftyone.core.metadata.VideoMetadata` instances for each video.
     84        """
     85        # Return True or False here
     86        pass
     87
     88    @property
     89    def label_cls(self):
     90        """The :class:`fiftyone.core.labels.Label` class(es) returned by this
     91        importer within the sample-level labels that it produces.
     92
     93        This can be any of the following:
     94
     95        -   a :class:`fiftyone.core.labels.Label` class. In this case, the
     96            importer is guaranteed to return sample-level labels of this type
     97        -   a list or tuple of :class:`fiftyone.core.labels.Label` classes. In
     98            this case, the importer can produce a single sample-level label
     99            field of any of these types
    100        -   a dict mapping keys to :class:`fiftyone.core.labels.Label` classes.
    101            In this case, the importer will return sample-level label
    102            dictionaries with keys and value-types specified by this
    103            dictionary. Not all keys need be present in the imported labels
    104        -   ``None``. In this case, the importer makes no guarantees about the
    105            sample-level labels that it may return
    106        """
    107        # Return the appropriate value here
    108        pass
    109
    110    @property
    111    def frame_label_cls(self):
    112        """The :class:`fiftyone.core.labels.Label` class(es) returned by this
    113        importer within the frame labels that it produces.
    114
    115        This can be any of the following:
    116
    117        -   a :class:`fiftyone.core.labels.Label` class. In this case, the
    118            importer is guaranteed to return frame labels of this type
    119        -   a list or tuple of :class:`fiftyone.core.labels.Label` classes. In
    120            this case, the importer can produce a single frame label field of
    121            any of these types
    122        -   a dict mapping keys to :class:`fiftyone.core.labels.Label` classes.
    123            In this case, the importer will return frame label dictionaries
    124            with keys and value-types specified by this dictionary. Not all
    125            keys need be present in each frame
    126        -   ``None``. In this case, the importer makes no guarantees about the
    127            frame labels that it may return
    128        """
    129        # Return the appropriate value here
    130        pass
    131
    132    def setup(self):
    133        """Performs any necessary setup before importing the first sample in
    134        the dataset.
    135
    136        This method is called when the importer's context manager interface is
    137        entered, :func:`DatasetImporter.__enter__`.
    138        """
    139        # Your custom setup here
    140        pass
    141
    142    def get_dataset_info(self):
    143        """Returns the dataset info for the dataset.
    144
    145        By convention, this method should be called after all samples in the
    146        dataset have been imported.
    147
    148        Returns:
    149            a dict of dataset info
    150        """
    151        # Return a dict of dataset info, if supported by your importer
    152        pass
    153
    154    def close(self, *args):
    155        """Performs any necessary actions after the last sample has been
    156        imported.
    157
    158        This method is called when the importer's context manager interface is
    159        exited, :func:`DatasetImporter.__exit__`.
    160
    161        Args:
    162            *args: the arguments to :func:`DatasetImporter.__exit__`
    163        """
    164        # Your custom code here to complete the import
    165        pass
    

When [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") is called with a custom [`LabeledVideoDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter "fiftyone.utils.data.importers.LabeledVideoDatasetImporter"), the import is effectively performed via the pseudocode below:
    
    
    import fiftyone as fo
    
    dataset = fo.Dataset(...)
    importer = CustomLabeledVideoDatasetImporter(...)
    label_field = ...
    
    if isinstance(label_field, dict):
        label_key = lambda k: label_field.get(k, k)
    elif label_field is not None:
        label_key = lambda k: label_field + "_" + k
    else:
        label_field = "ground_truth"
        label_key = lambda k: k
    
    with importer:
        for video_path, video_metadata, label, frames in importer:
            sample = fo.Sample(filepath=video_path, metadata=video_metadata)
    
            if isinstance(label, dict):
                sample.update_fields({label_key(k): v for k, v in label.items()})
            elif label is not None:
                sample[label_field] = label
    
            if frames is not None:
                frame_labels = {}
    
                for frame_number, _label in frames.items():
                    if isinstance(_label, dict):
                        frame_labels[frame_number] = {
                            label_key(k): v for k, v in _label.items()
                        }
                    elif _label is not None:
                        frame_labels[frame_number] = {label_field: _label}
    
                sample.frames.merge(frame_labels)
    
            dataset.add_sample(sample)
    
        if importer.has_dataset_info:
            info = importer.get_dataset_info()
            parse_info(dataset, info)
    

Note that the importer is invoked via its context manager interface, which automatically calls the [`setup()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter.setup "fiftyone.utils.data.importers.LabeledVideoDatasetImporter.setup") and [`close()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter.close "fiftyone.utils.data.importers.LabeledVideoDatasetImporter.close") methods of the importer to handle setup/completion of the import.

The videos and their corresponding labels in the dataset are iteratively loaded by invoking the [`__next__()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter.__next__ "fiftyone.utils.data.importers.LabeledVideoDatasetImporter.__next__") method of the importer. In particular, sample-level labels for the video may be returned in a `label` value (which may contain a single [`Label`](../api/fiftyone.core.labels.html#fiftyone.core.labels.Label "fiftyone.core.labels.Label") value or a dictionary that maps field names to labels), and frame-level labels may be returned in a `frames` dictionary that maps frame numbers to dictionaries of field names and labels.

The [`has_dataset_info`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter.has_dataset_info "fiftyone.utils.data.importers.LabeledVideoDatasetImporter.has_dataset_info") property of the importer allows it to declare whether its [`get_dataset_info()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter.get_dataset_info "fiftyone.utils.data.importers.LabeledVideoDatasetImporter.get_dataset_info") method should be called after all samples have been imported to retrieve dataset-level information to store on the FiftyOne dataset. See this section for more information.

The [`label_cls`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter.label_cls "fiftyone.utils.data.importers.LabeledVideoDatasetImporter.label_cls") property of the importer declares the type of sample-level label(s) that the importer will produce (if any), and the [`frame_labels_cls`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter.frame_labels_cls "fiftyone.utils.data.importers.LabeledVideoDatasetImporter.frame_labels_cls") property of the importer declares the type of frame-level label(s) that the importer will produce (if any).

The [`has_video_metadata`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter.has_video_metadata "fiftyone.utils.data.importers.LabeledVideoDatasetImporter.has_video_metadata") property of the importer allows it to declare whether it returns [`VideoMetadata`](../api/fiftyone.core.metadata.html#fiftyone.core.metadata.VideoMetadata "fiftyone.core.metadata.VideoMetadata") instances for each video that it loads when [`__next__()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter.__next__ "fiftyone.utils.data.importers.LabeledVideoDatasetImporter.__next__") is called.

To define a custom importer for grouped datasets, implement the [`GroupDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GroupDatasetImporter "fiftyone.utils.data.importers.GroupDatasetImporter") interface.

The pseudocode below provides a template for a custom [`GroupDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GroupDatasetImporter "fiftyone.utils.data.importers.GroupDatasetImporter"):
    
    
      1import fiftyone.utils.data as foud
      2
      3class CustomGroupDatasetImporter(foud.GroupDatasetImporter):
      4    """Custom importer for grouped datasets.
      5
      6    Args:
      7        dataset_dir (None): the dataset directory. This may be optional for
      8            some importers
      9        shuffle (False): whether to randomly shuffle the order in which the
     10            samples are imported
     11        seed (None): a random seed to use when shuffling
     12        max_samples (None): a maximum number of samples to import. By default,
     13            all samples are imported
     14        **kwargs: additional keyword arguments for your importer
     15    """
     16
     17    def __init__(
     18        self,
     19        dataset_dir=None,
     20        shuffle=False,
     21        seed=None,
     22        max_samples=None,
     23        **kwargs,
     24    ):
     25        super().__init__(
     26            dataset_dir=dataset_dir,
     27            shuffle=shuffle,
     28            seed=seed,
     29            max_samples=max_samples
     30        )
     31        # Your initialization here
     32
     33    def __len__(self):
     34        """The total number of samples that will be imported across all group
     35        slices.
     36
     37        Raises:
     38            TypeError: if the total number is not known
     39        """
     40        # Return the total number of samples in the dataset (if known)
     41        pass
     42
     43    def __next__(self):
     44        """Returns information about the next group in the dataset.
     45
     46        Returns:
     47            a dict mapping slice names to :class:`fiftyone.core.sample.Sample`
     48            instances
     49
     50        Raises:
     51            StopIteration: if there are no more groups to import
     52        """
     53        # Implement loading the next group in your dataset here
     54        pass
     55
     56    @property
     57    def has_dataset_info(self):
     58        """Whether this importer produces a dataset info dictionary."""
     59        # Return True or False here
     60        pass
     61
     62    @property
     63    def has_sample_field_schema(self):
     64        """Whether this importer produces a sample field schema."""
     65        # Return True or False here
     66        pass
     67
     68    @property
     69    def group_field(self):
     70        """The name of the group field to populate on each sample."""
     71        # This is the default, but you can customize if desired
     72        return "group"
     73
     74    def setup(self):
     75        """Performs any necessary setup before importing the first sample in
     76        the dataset.
     77
     78        This method is called when the importer's context manager interface is
     79        entered, :func:`DatasetImporter.__enter__`.
     80        """
     81        # Your custom setup here
     82        pass
     83
     84    def get_dataset_info(self):
     85        """Returns the dataset info for the dataset.
     86
     87        By convention, this method should be called after all samples in the
     88        dataset have been imported.
     89
     90        Returns:
     91            a dict of dataset info
     92        """
     93        # Return a dict of dataset info, if supported by your importer
     94        pass
     95
     96    def get_sample_field_schema(self):
     97        """Returns a dictionary describing the field schema of the samples
     98        loaded by this importer.
     99
    100        Returns:
    101            a dict mapping field names to :class:`fiftyone.core.fields.Field`
    102            instances or ``str(field)`` representations of them
    103        """
    104        # Return the sample schema here, if known
    105        pass
    106
    107    def get_group_media_types(self):
    108        """Returns a dictionary describing the group slices of the samples
    109        loaded by this importer.
    110
    111        Returns:
    112            a dict mapping slice names to media types
    113        """
    114        # Return the group media types here, if known
    115        pass
    116
    117    def close(self, *args):
    118        """Performs any necessary actions after the last sample has been
    119        imported.
    120
    121        This method is called when the importer's context manager interface is
    122        exited, :func:`DatasetImporter.__exit__`.
    123
    124        Args:
    125            *args: the arguments to :func:`DatasetImporter.__exit__`
    126        """
    127        # Your custom code here to complete the import
    128        pass
    

When [`Dataset.from_dir()`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.from_dir "fiftyone.core.dataset.Dataset.from_dir") is called with a custom [`GroupDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GroupDatasetImporter "fiftyone.utils.data.importers.GroupDatasetImporter"), the import is effectively performed via the pseudocode below:
    
    
    import fiftyone as fo
    
    dataset = fo.Dataset(...)
    importer = CustomGroupDatasetImporter(...)
    group_field = importer.group_field
    
    with importer:
        for group in importer:
            _group = fo.Group()
            for name, sample in group.items():
                sample[group_field] = _group.element(name)
                dataset.add_sample(sample)
    
        if importer.has_dataset_info:
            info = importer.get_dataset_info()
            parse_info(dataset, info)
    

Note that the importer is invoked via its context manager interface, which automatically calls the [`setup()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GroupDatasetImporter.setup "fiftyone.utils.data.importers.GroupDatasetImporter.setup") and [`close()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GroupDatasetImporter.close "fiftyone.utils.data.importers.GroupDatasetImporter.close") methods of the importer to handle setup/completion of the import.

The groups in the dataset are iteratively loaded by invoking the [`__next__()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GroupDatasetImporter.__next__ "fiftyone.utils.data.importers.GroupDatasetImporter.__next__") method of the importer.

The [`has_dataset_info`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GroupDatasetImporter.has_dataset_info "fiftyone.utils.data.importers.GroupDatasetImporter.has_dataset_info") property of the importer allows it to declare whether its [`get_dataset_info()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GroupDatasetImporter.get_dataset_info "fiftyone.utils.data.importers.GroupDatasetImporter.get_dataset_info") method should be called after all samples have been imported to retrieve dataset-level information to store on the FiftyOne dataset. See this section for more information.

The [`group_field`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GroupDatasetImporter.group_field "fiftyone.utils.data.importers.GroupDatasetImporter.group_field") property of the importer allows it to declare the name of the field in which to store the [`Group`](../api/fiftyone.core.groups.html#fiftyone.core.groups.Group "fiftyone.core.groups.Group") information for each sample.

### Importing dataset-level information#

The [`has_dataset_info`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.DatasetImporter.has_dataset_info "fiftyone.utils.data.importers.DatasetImporter.has_dataset_info") property of the importer allows it to declare whether its [`get_dataset_info()`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.DatasetImporter.get_dataset_info "fiftyone.utils.data.importers.DatasetImporter.get_dataset_info") method should be called after all samples have been imported to retrieve a dict of dataset-level information to store in the [`info`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.info "fiftyone.core.dataset.Dataset.info") property of the dataset.

As a special case, if the `info` dict contains any of the keys listed below, these items are popped and stored in the corresponding dedicated dataset field:

  * `"classes"` key: [`Dataset.classes`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.classes "fiftyone.core.dataset.Dataset.classes")

  * `"default_classes"` key: [`Dataset.default_classes`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.default_classes "fiftyone.core.dataset.Dataset.default_classes")

  * `"mask_targets"` key: [`Dataset.mask_targets`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.mask_targets "fiftyone.core.dataset.Dataset.mask_targets")

  * `"default_mask_targets"` key: [`Dataset.default_mask_targets`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.default_mask_targets "fiftyone.core.dataset.Dataset.default_mask_targets")

  * `"skeletons"` key: [`Dataset.skeletons`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.skeletons "fiftyone.core.dataset.Dataset.skeletons")

  * `"default_skeleton"` key: [`Dataset.default_skeleton`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.default_skeleton "fiftyone.core.dataset.Dataset.default_skeleton")

  * `"app_config"` key: [`Dataset.app_config`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset.app_config "fiftyone.core.dataset.Dataset.app_config")




### Writing a custom Dataset type#

FiftyOne provides the [`Dataset`](../api/fiftyone.types.html#fiftyone.types.Dataset "fiftyone.types.Dataset") type system so that dataset formats can be conveniently referenced by their type when reading/writing datasets on disk.

The primary function of the [`Dataset`](../api/fiftyone.types.html#fiftyone.types.Dataset "fiftyone.types.Dataset") subclasses is to define the [`DatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.DatasetImporter "fiftyone.utils.data.importers.DatasetImporter") that should be used to read instances of the dataset from disk and the [`DatasetExporter`](../api/fiftyone.utils.data.exporters.html#fiftyone.utils.data.exporters.DatasetExporter "fiftyone.utils.data.exporters.DatasetExporter") that should be used to write instances of the dataset to disk.

See [this page](export_datasets.html#writing-a-custom-dataset-exporter) for more information about defining custom [`DatasetExporter`](../api/fiftyone.utils.data.exporters.html#fiftyone.utils.data.exporters.DatasetExporter "fiftyone.utils.data.exporters.DatasetExporter") classes.

Custom dataset types can be declared by implementing the [`Dataset`](../api/fiftyone.types.html#fiftyone.types.Dataset "fiftyone.types.Dataset") subclass corresponding to the type of dataset that you are working with.

Generic datasetsUnlabeled image datasetsLabeled image datasetsUnlabeled video datasetsLabeled video datasetsGrouped datasets

The pseudocode below provides a template for a custom [`Dataset`](../api/fiftyone.types.html#fiftyone.types.Dataset "fiftyone.types.Dataset") subclass that represents a collection of arbitrary content:
    
    
     1import fiftyone.types as fot
     2
     3class CustomDataset(fot.Dataset):
     4    """Custom dataset type."""
     5
     6    def get_dataset_importer_cls(self):
     7        """Returns the
     8        :class:`fiftyone.utils.data.importers.DatasetImporter`
     9        class for importing datasets of this type from disk.
    10
    11        Returns:
    12            a :class:`fiftyone.utils.data.importers.DatasetImporter`
    13            class
    14        """
    15        # Return your custom DatasetImporter class here
    16        pass
    17
    18    def get_dataset_exporter_cls(self):
    19        """Returns the
    20        :class:`fiftyone.utils.data.exporters.DatasetExporter`
    21        class for exporting datasets of this type to disk.
    22
    23        Returns:
    24            a :class:`fiftyone.utils.data.exporters.DatasetExporter`
    25            class
    26        """
    27        # Return your custom DatasetExporter class here
    28        pass
    

Note that, as this type represents a dataset of arbitrary content, its importer should subclass from the base [`DatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.DatasetImporter "fiftyone.utils.data.importers.DatasetImporter"), and its exporter should subclass from the base [`DatasetExporter`](../api/fiftyone.utils.data.exporters.html#fiftyone.utils.data.exporters.DatasetExporter "fiftyone.utils.data.exporters.DatasetExporter").

The pseudocode below provides a template for a custom [`UnlabeledImageDataset`](../api/fiftyone.types.html#fiftyone.types.UnlabeledImageDataset "fiftyone.types.UnlabeledImageDataset") subclass:
    
    
     1import fiftyone.types as fot
     2
     3class CustomUnlabeledImageDataset(fot.UnlabeledImageDataset):
     4    """Custom unlabeled image dataset type."""
     5
     6    def get_dataset_importer_cls(self):
     7        """Returns the
     8        :class:`fiftyone.utils.data.importers.UnlabeledImageDatasetImporter`
     9        class for importing datasets of this type from disk.
    10
    11        Returns:
    12            a :class:`fiftyone.utils.data.importers.UnlabeledImageDatasetImporter`
    13            class
    14        """
    15        # Return your custom UnlabeledImageDatasetImporter class here
    16        pass
    17
    18    def get_dataset_exporter_cls(self):
    19        """Returns the
    20        :class:`fiftyone.utils.data.exporters.UnlabeledImageDatasetExporter`
    21        class for exporting datasets of this type to disk.
    22
    23        Returns:
    24            a :class:`fiftyone.utils.data.exporters.UnlabeledImageDatasetExporter`
    25            class
    26        """
    27        # Return your custom UnlabeledImageDatasetExporter class here
    28        pass
    

Note that, as this type represents an unlabeled image dataset, its importer must be a subclass of [`UnlabeledImageDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledImageDatasetImporter "fiftyone.utils.data.importers.UnlabeledImageDatasetImporter"), and its exporter must be a subclass of [`UnlabeledImageDatasetExporter`](../api/fiftyone.utils.data.exporters.html#fiftyone.utils.data.exporters.UnlabeledImageDatasetExporter "fiftyone.utils.data.exporters.UnlabeledImageDatasetExporter").

The pseudocode below provides a template for a custom [`LabeledImageDataset`](../api/fiftyone.types.html#fiftyone.types.LabeledImageDataset "fiftyone.types.LabeledImageDataset") subclass:
    
    
     1import fiftyone.types as fot
     2
     3class CustomLabeledImageDataset(fot.LabeledImageDataset):
     4    """Custom labeled image dataset type."""
     5
     6    def get_dataset_importer_cls(self):
     7        """Returns the
     8        :class:`fiftyone.utils.data.importers.LabeledImageDatasetImporter`
     9        class for importing datasets of this type from disk.
    10
    11        Returns:
    12            a :class:`fiftyone.utils.data.importers.LabeledImageDatasetImporter`
    13            class
    14        """
    15        # Return your custom LabeledImageDatasetImporter class here
    16        pass
    17
    18    def get_dataset_exporter_cls(self):
    19        """Returns the
    20        :class:`fiftyone.utils.data.exporters.LabeledImageDatasetExporter`
    21        class for exporting datasets of this type to disk.
    22
    23        Returns:
    24            a :class:`fiftyone.utils.data.exporters.LabeledImageDatasetExporter`
    25            class
    26        """
    27        # Return your custom LabeledImageDatasetExporter class here
    28        pass
    

Note that, as this type represents a labeled image dataset, its importer must be a subclass of [`LabeledImageDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledImageDatasetImporter "fiftyone.utils.data.importers.LabeledImageDatasetImporter"), and its exporter must be a subclass of [`LabeledImageDatasetExporter`](../api/fiftyone.utils.data.exporters.html#fiftyone.utils.data.exporters.LabeledImageDatasetExporter "fiftyone.utils.data.exporters.LabeledImageDatasetExporter").

The pseudocode below provides a template for a custom [`UnlabeledVideoDataset`](../api/fiftyone.types.html#fiftyone.types.UnlabeledVideoDataset "fiftyone.types.UnlabeledVideoDataset") subclass:
    
    
     1import fiftyone.types as fot
     2
     3class CustomUnlabeledVideoDataset(fot.UnlabeledVideoDataset):
     4    """Custom unlabeled video dataset type."""
     5
     6    def get_dataset_importer_cls(self):
     7        """Returns the
     8        :class:`fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter`
     9        class for importing datasets of this type from disk.
    10
    11        Returns:
    12            a :class:`fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter`
    13            class
    14        """
    15        # Return your custom UnlabeledVideoDatasetImporter class here
    16        pass
    17
    18    def get_dataset_exporter_cls(self):
    19        """Returns the
    20        :class:`fiftyone.utils.data.exporters.UnlabeledVideoDatasetExporter`
    21        class for exporting datasets of this type to disk.
    22
    23        Returns:
    24            a :class:`fiftyone.utils.data.exporters.UnlabeledVideoDatasetExporter`
    25            class
    26        """
    27        # Return your custom UnlabeledVideoDatasetExporter class here
    28        pass
    

Note that, as this type represents an unlabeled video dataset, its importer must be a subclass of [`UnlabeledVideoDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter "fiftyone.utils.data.importers.UnlabeledVideoDatasetImporter"), and its exporter must be a subclass of [`UnlabeledVideoDatasetExporter`](../api/fiftyone.utils.data.exporters.html#fiftyone.utils.data.exporters.UnlabeledVideoDatasetExporter "fiftyone.utils.data.exporters.UnlabeledVideoDatasetExporter").

The pseudocode below provides a template for a custom [`LabeledVideoDataset`](../api/fiftyone.types.html#fiftyone.types.LabeledVideoDataset "fiftyone.types.LabeledVideoDataset") subclass:
    
    
     1import fiftyone.types as fot
     2
     3class CustomLabeledVideoDataset(fot.LabeledVideoDataset):
     4    """Custom labeled video dataset type."""
     5
     6    def get_dataset_importer_cls(self):
     7        """Returns the
     8        :class:`fiftyone.utils.data.importers.LabeledVideoDatasetImporter`
     9        class for importing datasets of this type from disk.
    10
    11        Returns:
    12            a :class:`fiftyone.utils.data.importers.LabeledVideoDatasetImporter`
    13            class
    14        """
    15        # Return your custom LabeledVideoDatasetImporter class here
    16        pass
    17
    18    def get_dataset_exporter_cls(self):
    19        """Returns the
    20        :class:`fiftyone.utils.data.exporters.LabeledVideoDatasetExporter`
    21        class for exporting datasets of this type to disk.
    22
    23        Returns:
    24            a :class:`fiftyone.utils.data.exporters.LabeledVideoDatasetExporter`
    25            class
    26        """
    27        # Return your custom LabeledVideoDatasetExporter class here
    28        pass
    

Note that, as this type represents a labeled video dataset, its importer must be a subclass of [`LabeledVideoDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.LabeledVideoDatasetImporter "fiftyone.utils.data.importers.LabeledVideoDatasetImporter"), and its exporter must be a subclass of [`LabeledVideoDatasetExporter`](../api/fiftyone.utils.data.exporters.html#fiftyone.utils.data.exporters.LabeledVideoDatasetExporter "fiftyone.utils.data.exporters.LabeledVideoDatasetExporter").

The pseudocode below provides a template for a custom [`GroupDataset`](../api/fiftyone.types.html#fiftyone.types.GroupDataset "fiftyone.types.GroupDataset") subclass:
    
    
     1import fiftyone.types as fot
     2
     3class CustomGroupDataset(fot.GroupDataset):
     4    """Custom grouped dataset type."""
     5
     6    def get_dataset_importer_cls(self):
     7        """Returns the
     8        :class:`fiftyone.utils.data.importers.GroupDatasetImporter`
     9        class for importing datasets of this type from disk.
    10
    11        Returns:
    12            a :class:`fiftyone.utils.data.importers.GroupDatasetImporter`
    13            class
    14        """
    15        # Return your custom GroupDatasetImporter class here
    16        pass
    17
    18    def get_dataset_exporter_cls(self):
    19        """Returns the
    20        :class:`fiftyone.utils.data.exporters.GroupDatasetExporter`
    21        class for exporting datasets of this type to disk.
    22
    23        Returns:
    24            a :class:`fiftyone.utils.data.exporters.GroupDatasetExporter`
    25            class
    26        """
    27        # Return your custom GroupDatasetExporter class here
    28        pass
    

Note that, as this type represents a grouped dataset, its importer must be a subclass of [`GroupDatasetImporter`](../api/fiftyone.utils.data.importers.html#fiftyone.utils.data.importers.GroupDatasetImporter "fiftyone.utils.data.importers.GroupDatasetImporter"), and its exporter must be a subclass of [`GroupDatasetExporter`](../api/fiftyone.utils.data.exporters.html#fiftyone.utils.data.exporters.GroupDatasetExporter "fiftyone.utils.data.exporters.GroupDatasetExporter").

IN THIS ARTICLE 
