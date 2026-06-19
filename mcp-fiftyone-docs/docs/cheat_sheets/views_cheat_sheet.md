# Views Cheat Sheet#

This cheat sheet shows how to use [dataset views](../user_guide/using_views.html#using-views) to retrieve the specific subset of data youâre looking for.

## The six basic operations#

If you run:
    
    
    1import fiftyone as fo
    2
    3dataset = fo.Dataset()
    4print(dataset.list_view_stages())
    

youâll see a list of all [`ViewStage`](../api/fiftyone.core.stages.html#fiftyone.core.stages.ViewStage "fiftyone.core.stages.ViewStage") methods that you can use to construct views into your datasets.

With a few exceptions (which weâll cover later), these methods can be organized into six categories: matching, filtering, selection, exclusion, indexing, and conversion.

### Matching#

These stages select certain subsets of the input collection that match a given condition, without modifying the contents of the samples.

[`match()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match "fiftyone.core.collections.SampleCollection.match")  
---  
[`match_frames()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_frames "fiftyone.core.collections.SampleCollection.match_frames")  
[`match_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_labels "fiftyone.core.collections.SampleCollection.match_labels")  
[`match_tags()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_tags "fiftyone.core.collections.SampleCollection.match_tags")  
  
### Filtering#

These stages filter the contents of the samples in the input collection based on a given condition.

[`filter_field()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_field "fiftyone.core.collections.SampleCollection.filter_field")  
---  
[`filter_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_labels "fiftyone.core.collections.SampleCollection.filter_labels")  
[`filter_keypoints()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_keypoints "fiftyone.core.collections.SampleCollection.filter_keypoints")  
  
### Selection#

These stages select certain subsets of the input collection that contain a given identifier.

Selection is similar to matching/filtering, but with a simpler syntax that supports specific selection criteria (common identifiers like IDs and tags) rather than arbitrary [expressions](../user_guide/using_views.html#querying-samples).

[`select()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select "fiftyone.core.collections.SampleCollection.select")  
---  
[`select_by()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_by "fiftyone.core.collections.SampleCollection.select_by")  
[`select_fields()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_fields "fiftyone.core.collections.SampleCollection.select_fields")  
[`select_frames()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_frames "fiftyone.core.collections.SampleCollection.select_frames")  
[`select_groups()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_groups "fiftyone.core.collections.SampleCollection.select_groups")  
[`select_group_slices()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_group_slices "fiftyone.core.collections.SampleCollection.select_group_slices")  
[`select_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_labels "fiftyone.core.collections.SampleCollection.select_labels")  
  
### Exclusion#

These stages exclude data from the input collection based on the given criteria.

[`exclude()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude "fiftyone.core.collections.SampleCollection.exclude")  
---  
[`exclude_by()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude_by "fiftyone.core.collections.SampleCollection.exclude_by")  
[`exclude_fields()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude_fields "fiftyone.core.collections.SampleCollection.exclude_fields")  
[`exclude_frames()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude_frames "fiftyone.core.collections.SampleCollection.exclude_frames")  
[`exclude_groups()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude_groups "fiftyone.core.collections.SampleCollection.exclude_groups")  
[`exclude_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude_labels "fiftyone.core.collections.SampleCollection.exclude_labels")  
  
### Sorting#

These stages sort the samples in the input collection based on a given condition.

[`sort_by()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.sort_by "fiftyone.core.collections.SampleCollection.sort_by")  
---  
[`sort_by_similarity()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.sort_by_similarity "fiftyone.core.collections.SampleCollection.sort_by_similarity")  
  
### Indexing#

These stages slice and reorder the samples in the input collection.

[`limit()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.limit "fiftyone.core.collections.SampleCollection.limit")  
---  
[`shuffle()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.shuffle "fiftyone.core.collections.SampleCollection.shuffle")  
[`skip()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.skip "fiftyone.core.collections.SampleCollection.skip")  
[`take()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.take "fiftyone.core.collections.SampleCollection.take")  
  
### Conversion#

These stages create views that transform the contents of the input collection into a different shape.

[`to_patches()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.to_patches "fiftyone.core.collections.SampleCollection.to_patches")  
---  
[`to_evaluation_patches()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.to_evaluation_patches "fiftyone.core.collections.SampleCollection.to_evaluation_patches")  
[`to_clips()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.to_clips "fiftyone.core.collections.SampleCollection.to_clips")  
[`to_frames()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.to_frames "fiftyone.core.collections.SampleCollection.to_frames")  
  
### Miscellaneous#

Other stages that do not fit into the six buckets above include:

[`concat()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.concat "fiftyone.core.collections.SampleCollection.concat")  
---  
[`exists()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exists "fiftyone.core.collections.SampleCollection.exists")  
[`geo_near()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.geo_near "fiftyone.core.collections.SampleCollection.geo_near")  
[`geo_within()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.geo_within "fiftyone.core.collections.SampleCollection.geo_within")  
[`group_by()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.group_by "fiftyone.core.collections.SampleCollection.group_by")  
[`map_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.map_labels "fiftyone.core.collections.SampleCollection.map_labels")  
[`mongo()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.mongo "fiftyone.core.collections.SampleCollection.mongo")  
[`set_field()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.set_field "fiftyone.core.collections.SampleCollection.set_field")  
  
## Filtering, matching, selecting, and excluding#

FiftyOneâs goal is to help you perform your computer vision workflows as simply and efficiently as possible, without the need to manually iterate through all the samples in your dataset.

To achieve this, FiftyOne provides builtin view stages tailored for each primitive data type (samples, labels, fields, tags, frames, and groups) that provide concise syntaxes for performing the desired operation against that primitiveâs attributes.

| Match | Filter | Select | Exclude  
---|---|---|---|---  
Samples | [`match()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match "fiftyone.core.collections.SampleCollection.match") |  | [`select()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select "fiftyone.core.collections.SampleCollection.select") | [`exclude()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude "fiftyone.core.collections.SampleCollection.exclude")  
Labels | [`match_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_labels "fiftyone.core.collections.SampleCollection.match_labels") | [`filter_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_labels "fiftyone.core.collections.SampleCollection.filter_labels") | [`select_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_labels "fiftyone.core.collections.SampleCollection.select_labels") | [`exclude_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude_labels "fiftyone.core.collections.SampleCollection.exclude_labels")  
Fields |  | [`filter_field()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_field "fiftyone.core.collections.SampleCollection.filter_field") | [`select_fields()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_fields "fiftyone.core.collections.SampleCollection.select_fields") | [`exclude_fields()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude_fields "fiftyone.core.collections.SampleCollection.exclude_fields")  
Tags | [`match_tags()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_tags "fiftyone.core.collections.SampleCollection.match_tags") |  |  |   
Frames | [`match_frames()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_frames "fiftyone.core.collections.SampleCollection.match_frames") |  | [`select_frames()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_frames "fiftyone.core.collections.SampleCollection.select_frames") | [`exclude_frames()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude_frames "fiftyone.core.collections.SampleCollection.exclude_frames")  
Groups |  |  | [`select_groups()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_groups "fiftyone.core.collections.SampleCollection.select_groups") | [`exclude_groups()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude_groups "fiftyone.core.collections.SampleCollection.exclude_groups")  
  
From the table above, we see that most operations on each primitive type are directly supported via tailored methods. The empty cells in the table fall into two categories:

  * the operation does not make sense on the primitive

  * the operation can easily achieved on the primitive via another base method




In the following sections, weâll fill in the gaps in the table.

### Samples#

The only method missing from the `Samples` row of the table is a âfilterâ method. This is because filtering operations create a view with contents of the primitive to which they are applied. However, as samples are comprised of fields, the [`filter_field()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_field "fiftyone.core.collections.SampleCollection.filter_field") method provides all of the desired functionality.

### Labels#

While all of the methods in the `Labels` row are filled in, there is one subtlety: filtering by `id`.

The [`match_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_labels "fiftyone.core.collections.SampleCollection.match_labels"), [`select_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_labels "fiftyone.core.collections.SampleCollection.select_labels"), and [`exclude_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exclude_labels "fiftyone.core.collections.SampleCollection.exclude_labels") methods all allow you to pass in a list of IDs to define a view. However, in order to filter by ID using [`filter_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_labels "fiftyone.core.collections.SampleCollection.filter_labels"), youâll need to make two changes when creating your filter expression:

  * use `"_id"` rather than `"id"` when referencing ID fields

  * cast ID strings to `ObjectId()`




The following example demonstrates how to correctly filter by label IDs:
    
    
     1from bson import ObjectId
     2
     3import fiftone as fo
     4import fiftyone.zoo as foz
     5from fiftyone import ViewField as F
     6
     7dataset = foz.load_zoo_dataset("quickstart")
     8
     9label_id = dataset.first().predictions.detections[0].id
    10
    11view = dataset.filter_labels("predictions", F("_id") == ObjectId(label_id))
    

### Fields#

The only missing entry in the `Fields` row is a âmatchâ stage. Such a method would absolutely make sense: matches on fields are common. However, a dedicated method is not necessary because you can easily achieve this using the existing [`match()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match "fiftyone.core.collections.SampleCollection.match") method.

A hypothetical match fields method would take as input a `field` and a `filter` to apply to it, but we can achieve this in multiple ways via simple [`match()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match "fiftyone.core.collections.SampleCollection.match") expressions:
    
    
     1import fiftyone as fo
     2import fiftyone.zoo as foz
     3from fiftyone import ViewField as F
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6
     7field = "ground_truth.detections"
     8filter = F().length() > 0
     9
    10# What a `match_fields()` method would look like
    11# view = dataset.match_fields(field, filter)
    12
    13# Option 1: directly apply the filter to the field
    14view = dataset.match(F(field).length() > 0)
    15
    16# Option 2: apply() the filter to the field
    17view = dataset.match(F(field).apply(filter))
    

Note that [`exists()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.exists "fiftyone.core.collections.SampleCollection.exists") is also a special case of field matching:
    
    
    1dataset.take(100).set_field("uniqueness", None).save()
    2
    3# Concise syntax via `exists()`
    4view = dataset.exists("uniqueness")
    5
    6# Equivalent syntax via `match()`
    7view = dataset.match(F("uniqueness") != None)
    

### Tags#

All three of the missing `Tag` methods can be created with relative ease.

Hereâs how selecting tags can be achieved:
    
    
    1from fiftyone import ViewField as F
    2
    3# What a select_tags() method would look like
    4# view = dataset.select_tags(tags)
    5
    6# How to achieve this with existing methods
    7view = dataset.set_field("tags", F("tags").intersection(tags))
    

Hereâs how excluding tags can be achieved:
    
    
    1from fiftyone import ViewField as F
    2
    3# What an exclude_tags() method would look like
    4# view = dataset.exclude_tags(tags)
    5
    6# How to achieve this with existing methods
    7view = dataset.set_field("tags", F("tags").difference(tags))
    

And hereâs how filtering tags can be achieved:
    
    
    1from fiftyone import ViewField as F
    2
    3# What a filter_tags() method would look like
    4# view = dataset.filter_tags(expr)
    5
    6# How to achieve this with existing methods
    7view = dataset.set_field("tags", F("tags").filter(expr))
    

Note

The above examples use the set [`intersection()`](../api/fiftyone.core.expressions.html#fiftyone.core.expressions.ViewExpression.intersection "fiftyone.core.expressions.ViewExpression.intersection") and [`difference()`](../api/fiftyone.core.expressions.html#fiftyone.core.expressions.ViewExpression.difference "fiftyone.core.expressions.ViewExpression.difference") view expressions.

### Frames and groups#

When working with [frame-level](../user_guide/using_views.html#video-views) and [group-level](../user_guide/groups.html#groups-filtering) data in FiftyOne, all applicable view stages naturally support querying against frame- or group-level fields by prepending `"frames."` or `"groups."` to field paths, respectively.

For example, you can retrieve the frame-level object detections in the âdetectionsâ field of the [quickstart-video](../dataset_zoo/datasets/quickstart_video.html#dataset-zoo-quickstart-video) dataset:
    
    
    1import fiftyone as fo
    2import fiftyone.zoo as foz
    3from fiftyone import ViewField as F
    4
    5dataset = foz.load_zoo_dataset("quickstart-video")
    6
    7view = dataset.filter_labels("frames.detections", F("label") == "vehicle")
    

Or when working with grouped datasets, you can match groups based on whether they contain a given group slice:
    
    
     1import fiftyone as fo
     2import fiftyone.zoo as foz
     3from fiftyone import ViewField as F
     4
     5# Load a dataset with 200 groups, each with "left", "right", "pcd" elements
     6dataset = foz.load_zoo_dataset("quickstart-groups")
     7
     8# Add 50 new groups with only "left" slice samples
     9dataset.add_samples(
    10    [
    11        fo.Sample(
    12            filepath="image%d.png" % i,
    13            group=fo.Group().element("left"),
    14        )
    15        for i in range(50)
    16    ]
    17)
    18
    19# Match groups that have "pcd" elements
    20view = dataset.match(F("groups.pcd") != None)
    

## Conversion#

FiftyOne provides a variety of convenient methods for converting your data from one format to another. Some of these conversions are accomplished as view stages that return _generated views_ , which are views that contain a different shape of data than the original [`Dataset`](../api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") or [`DatasetView`](../api/fiftyone.core.view.html#fiftyone.core.view.DatasetView "fiftyone.core.view.DatasetView") to which the view stage was applied.

Letâs briefly cover the transformation that each generated view performs.

### Images to object patches#

If your dataset contains label list fields like [`Detections`](../api/fiftyone.core.labels.html#fiftyone.core.labels.Detections "fiftyone.core.labels.Detections") or [`Polylines`](../api/fiftyone.core.labels.html#fiftyone.core.labels.Polylines "fiftyone.core.labels.Polylines"), then you can use [`to_patches()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.to_patches "fiftyone.core.collections.SampleCollection.to_patches") to create views that contain one sample per object patch in a specified label field of your dataset.

For example, you can extract patches for all ground truth objects in a detection dataset:
    
    
    1import fiftyone as fo
    2import fiftyone.zoo as foz
    3
    4dataset = foz.load_zoo_dataset("quickstart")
    5
    6gt_patches = dataset.to_patches("ground_truth")
    7print(gt_patches)
    
    
    
    Dataset:     quickstart
    Media type:  image
    Num patches: 1232
    Patch fields:
        id:               fiftyone.core.fields.ObjectIdField
        sample_id:        fiftyone.core.fields.ObjectIdField
        filepath:         fiftyone.core.fields.StringField
        tags:             fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
        metadata:         fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.ImageMetadata)
        created_at:       fiftyone.core.fields.DateTimeField
        last_modified_at: fiftyone.core.fields.DateTimeField
        ground_truth:     fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detection)
    View stages:
        1. ToPatches(field='ground_truth', config=None)
    

### Images to evaluation patches#

If you have [run evaluation](../user_guide/evaluation.html#evaluating-detections) on predictions from an object detection model, then you can use [`to_evaluation_patches()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.to_evaluation_patches "fiftyone.core.collections.SampleCollection.to_evaluation_patches") to transform the dataset (or a view into it) into a new view that contains one sample for each true positive, false positive, and false negative example.
    
    
     1import fiftyone as fo
     2import fiftyone.zoo as foz
     3
     4dataset = foz.load_zoo_dataset("quickstart")
     5
     6# Evaluate `predictions` w.r.t. labels in `ground_truth` field
     7dataset.evaluate_detections(
     8 "predictions", gt_field="ground_truth", eval_key="eval"
     9)
    10
    11# Convert to evaluation patches
    12eval_patches = dataset.to_evaluation_patches("eval")
    13print(eval_patches)
    14
    15print(eval_patches.count_values("type"))
    16# {'fn': 246, 'fp': 4131, 'tp': 986}
    
    
    
    Dataset:     quickstart
    Media type:  image
    Num patches: 5363
    Patch fields:
        id:               fiftyone.core.fields.ObjectIdField
        sample_id:        fiftyone.core.fields.ObjectIdField
        filepath:         fiftyone.core.fields.StringField
        tags:             fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
        metadata:         fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.ImageMetadata)
        created_at:       fiftyone.core.fields.DateTimeField
        last_modified_at: fiftyone.core.fields.DateTimeField
        predictions:      fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detections)
        ground_truth:     fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detections)
        type:             fiftyone.core.fields.StringField
        iou:              fiftyone.core.fields.FloatField
        crowd:            fiftyone.core.fields.BooleanField
    View stages:
        1. ToEvaluationPatches(eval_key='eval', config=None)
    

### Videos to clips#

You can use [`to_clips()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.to_clips "fiftyone.core.collections.SampleCollection.to_clips") to create views into your video datasets that contain one sample per clip defined by a specific field or expression in a video collection.
    
    
     1import fiftyone as fo
     2import fiftyone.zoo as foz
     3from fiftyone import ViewField as F
     4
     5dataset = foz.load_zoo_dataset("quickstart-video")
     6
     7# Create a clips view that contains one clip for each contiguous segment
     8# that contains at least one road sign in every frame
     9clips = (
    10    dataset
    11    .filter_labels("frames.detections", F("label") == "road sign")
    12    .to_clips("frames.detections")
    13)
    14print(clips)
    
    
    
    Dataset:    quickstart-video
    Media type: video
    Num clips:  11
    Clip fields:
        id:               fiftyone.core.fields.ObjectIdField
        sample_id:        fiftyone.core.fields.ObjectIdField
        filepath:         fiftyone.core.fields.StringField
        support:          fiftyone.core.fields.FrameSupportField
        tags:             fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
        metadata:         fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.VideoMetadata)
        created_at:       fiftyone.core.fields.DateTimeField
        last_modified_at: fiftyone.core.fields.DateTimeField
    Frame fields:
        id:               fiftyone.core.fields.ObjectIdField
        frame_number:     fiftyone.core.fields.FrameNumberField
        created_at:       fiftyone.core.fields.DateTimeField
        last_modified_at: fiftyone.core.fields.DateTimeField
        detections:       fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detections)
    View stages:
        1. FilterLabels(field='frames.detections', ...)
        2. ToClips(field_or_expr='frames.detections', config=None)
    

### Videos to images#

You can use [`to_frames()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.to_frames "fiftyone.core.collections.SampleCollection.to_frames") to create image views into your video datasets that contain one sample per frame in the input collection.
    
    
    1import fiftyone as fo
    2import fiftyone.zoo as foz
    3
    4dataset = foz.load_zoo_dataset("quickstart-video")
    5
    6# Create a view with one sample per frame
    7frames = dataset.to_frames(sample_frames=True)
    8print(frames)
    
    
    
    Dataset:     quickstart-video
    Media type:  image
    Num samples: 1279
    Sample fields:
       id:               fiftyone.core.fields.ObjectIdField
       sample_id:        fiftyone.core.fields.ObjectIdField
       frame_number:     fiftyone.core.fields.FrameNumberField
       filepath:         fiftyone.core.fields.StringField
       tags:             fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
       metadata:         fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.ImageMetadata)
       created_at:       fiftyone.core.fields.DateTimeField
       last_modified_at: fiftyone.core.fields.DateTimeField
       detections:       fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detections)
    View stages:
      1. ToFrames(config=None)
    

### Grouped to non-grouped#

You can use the [`select_group_slices()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_group_slices "fiftyone.core.collections.SampleCollection.select_group_slices") to generate a [`DatasetView`](../api/fiftyone.core.view.html#fiftyone.core.view.DatasetView "fiftyone.core.view.DatasetView") that contains a flattened collection of samples from specific slice(s) of a grouped dataset.

For example, the following code creates an image collection from the âleftâ and ârightâ group slices of the [quickstart-groups](../dataset_zoo/datasets/quickstart_groups.html#dataset-zoo-quickstart-groups) dataset:
    
    
    1import fiftyone as fo
    2import fiftyone.zoo as foz
    3
    4dataset = foz.load_zoo_dataset("quickstart-groups")
    5
    6image_view = dataset.select_group_slices(["left", "right"])
    7print(image_view)
    
    
    
    Dataset:     groups-overview
    Media type:  image
    Num samples: 400
    Sample fields:
        id:               fiftyone.core.fields.ObjectIdField
        filepath:         fiftyone.core.fields.StringField
        tags:             fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
        metadata:         fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.Metadata)
        created_at:       fiftyone.core.fields.DateTimeField
        last_modified_at: fiftyone.core.fields.DateTimeField
        group:            fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.groups.Group)
        ground_truth:     fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detections)
    View stages:
        1. SelectGroupSlices(slices=['left', 'right'])
    

Note

All group slice(s) you select must have the same media type, since the `media_type` of the returned collection is the media type of the slices you select.

IN THIS ARTICLE 
