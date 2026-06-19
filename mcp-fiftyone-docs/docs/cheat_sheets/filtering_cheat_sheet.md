# Filtering Cheat Sheet#

This cheat sheet shows how to perform common matching and filtering operations in FiftyOne using [dataset views](../user_guide/using_views.html#using-views).

## Strings and pattern matching#

The formulas in this section use the following example data:
    
    
    1import fiftyone.zoo as foz
    2from fiftyone import ViewField as F
    3
    4ds = foz.load_zoo_dataset("quickstart")
    

Operation | Command  
---|---  
Filepath starts with â/Usersâ | 
    
    
    ds.match(F("filepath").starts_with("/Users"))
      
  
Filepath ends with â10.jpgâ or â10.pngâ | 
    
    
    ds.match(F("filepath").ends_with(("10.jpg", "10.png"))
      
  
Label contains string âbeâ | 
    
    
    ds.filter_labels(
        "predictions",
        F("label").contains_str("be"),
    )
      
  
Filepath contains â088â and is JPEG | 
    
    
    ds.match(F("filepath").re_match("088*.jpg"))
      
  
Reference: [`match()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match "fiftyone.core.collections.SampleCollection.match") and [`filter_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_labels "fiftyone.core.collections.SampleCollection.filter_labels").

## Dates and times#

The formulas in this section use the following example data:
    
    
     1from datetime import datetime, timedelta
     2
     3import fiftyone as fo
     4import fiftyone.zoo as foz
     5from fiftyone import ViewField as F
     6
     7filepaths = ["image%d.jpg" % i for i in range(5)]
     8dates = [
     9    datetime(2021, 8, 24, 1, 0, 0),
    10    datetime(2021, 8, 24, 2, 0, 0),
    11    datetime(2021, 8, 25, 3, 11, 12),
    12    datetime(2021, 9, 25, 4, 22, 23),
    13    datetime(2022, 9, 27, 5, 0, 0)
    14]
    15
    16ds = fo.Dataset()
    17ds.add_samples(
    18    [fo.Sample(filepath=f, date=d) for f, d in zip(filepaths, dates)]
    19)
    20
    21# Example data
    22query_date = datetime(2021, 8, 24, 2, 0, 1)
    23query_delta = timedelta(minutes=30)
    

Operation | Command  
---|---  
After 2021-08-24 02:01:00 | 
    
    
    ds.match(F("date") > query_date)
      
  
Within 30 minutes of 2021-08-24 02:01:00 | 
    
    
    ds.match(abs(F("date") - query_date) < query_delta)
      
  
On the 24th of the month | 
    
    
    ds.match(F("date").day_of_month() == 24)
      
  
On even day of the week | 
    
    
    ds.match(F("date").day_of_week() % 2 == 0)
      
  
On the 268th day of the year | 
    
    
    ds.match(F("date").day_of_year() == 268)
      
  
In the 9th month of the year (September) | 
    
    
    ds.match(F("date").month() == 9)
      
  
In the 38th week of the year | 
    
    
    ds.match(F("date").week() == 38)
      
  
In the year 2022 | 
    
    
    ds.match(F("date").year() == 2022)
      
  
With minute not equal to 0 | 
    
    
    ds.match(F("date").minute() != 0)
      
  
Reference: [`match()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match "fiftyone.core.collections.SampleCollection.match").

## Geospatial#

The formulas in this section use the following example data:
    
    
     1import fiftyone.zoo as foz
     2
     3TIMES_SQUARE = [-73.9855, 40.7580]
     4MANHATTAN = [
     5    [
     6        [-73.949701, 40.834487],
     7        [-73.896611, 40.815076],
     8        [-73.998083, 40.696534],
     9        [-74.031751, 40.715273],
    10        [-73.949701, 40.834487],
    11    ]
    12]
    13
    14ds = foz.load_zoo_dataset("quickstart-geo")
    

Operation | Command  
---|---  
Within 5km of Times Square | 
    
    
    ds.geo_near(TIMES_SQUARE, max_distance=5000)
      
  
Within Manhattan | 
    
    
    ds.geo_within(MANHATTAN)
      
  
Reference: [`geo_near()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.geo_near "fiftyone.core.collections.SampleCollection.geo_near") and [`geo_within()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.geo_within "fiftyone.core.collections.SampleCollection.geo_within").

## Detections#

The formulas in this section use the following example data:
    
    
    1import fiftyone.zoo as foz
    2from fiftyone import ViewField as F
    3
    4ds = foz.load_zoo_dataset("quickstart")
    

Operation | Command  
---|---  
Predictions with confidence > 0.95 | 
    
    
    ds.filter_labels("predictions", F("confidence") > 0.95)
      
  
Exactly 10 ground truth detections | 
    
    
    ds.match(F("ground_truth.detections").length() == 10)
      
  
At least one dog | 
    
    
    ds.match(
        F("ground_truth.detections.label").contains("dog")
    )
      
  
Images that do not contain dogs | 
    
    
    ds.match(
        ~F("ground_truth.detections.label").contains("dog")
    )
      
  
Only dog detections | 
    
    
    ds.filter_labels("ground_truth", F("label") == "dog")
      
  
Images that only contain dogs | 
    
    
    ds.match(
        F("ground_truth.detections.label").is_subset(
            ["dog"]
        )
    )
      
  
Contains either a cat or a dog | 
    
    
    ds.match(
         F("predictions.detections.label").contains(
            ["cat","dog"]
         )
    )
      
  
Contains a cat and a dog prediction | 
    
    
    ds.match(
        F("predictions.detections.label").contains(
            ["cat", "dog"], all=True
        )
    )
      
  
Contains a cat or dog but not both | 
    
    
    field = "predictions.detections.label"
    one_expr = F(field).contains(["cat", "dog"])
    both_expr = F(field).contains(["cat", "dog"], all=True)
    ds.match(one_expr & ~both_expr)
      
  
Reference: [`match()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match "fiftyone.core.collections.SampleCollection.match") and [`filter_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_labels "fiftyone.core.collections.SampleCollection.filter_labels").

### Bounding boxes#

The formulas in this section assume the following code has been run:
    
    
     1import fiftyone.zoo as foz
     2from fiftyone import ViewField as F
     3
     4ds = foz.load_zoo_dataset("quickstart")
     5
     6box_width, box_height = F("bounding_box")[2], F("bounding_box")[3]
     7rel_bbox_area = box_width * box_height
     8
     9im_width, im_height = F("$metadata.width"), F("$metadata.height")
    10abs_area = rel_bbox_area * im_width * im_height
    

Bounding box query | Command  
---|---  
Larger than absolute size | 
    
    
    ds.filter_labels("predictions", abs_area > 96**2)
      
  
Between two relative sizes | 
    
    
    good_bboxes = (rel_bbox_area > 0.25) & (rel_bbox_area < 0.75)
    good_expr = rel_bbox_area.let_in(good_bboxes)
    ds.filter_labels("predictions", good_expr)
      
  
Approximately square | 
    
    
    rectangleness = abs(
        box_width * im_width - box_height * im_height
    )
    ds.select_fields("predictions").filter_labels(
        "predictions", rectangleness <= 1
    )
      
  
Aspect ratio > 2 | 
    
    
    aspect_ratio = (
        (box_width * im_width) / (box_height * im_height)
    )
    ds.select_fields("predictions").filter_labels(
        "predictions", aspect_ratio > 2
    )
      
  
Reference: [`filter_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_labels "fiftyone.core.collections.SampleCollection.filter_labels") and [`select_fields()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.select_fields "fiftyone.core.collections.SampleCollection.select_fields").

### Evaluating detections#

The formulas in this section assume the following code has been run on a dataset `ds` with detections in its `predictions` field:
    
    
     1import fiftyone.brain as fob
     2import fiftyone.zoo as foz
     3from fiftyone import ViewField as F
     4
     5ds = foz.load_zoo_dataset("quickstart")
     6
     7ds.evaluate_detections("predictions", eval_key="eval")
     8
     9fob.compute_uniqueness(ds)
    10fob.compute_mistakenness(ds, "predictions", label_field="ground_truth")
    11ep = ds.to_evaluation_patches("eval")
    

Operation | Command  
---|---  
Uniqueness > 0.9 | 
    
    
    ds.match(F("uniqueness") > 0.9)
      
  
10 most unique images | 
    
    
    ds.sort_by("uniqueness", reverse=True)[:10]
      
  
Predictions with confidence > 0.95 | 
    
    
    ds.filter_labels("predictions", F("confidence") > 0.95)
      
  
10 most âwrongâ predictions | 
    
    
    ds.sort_by("mistakenness", reverse=True)[:10]
      
  
Images with more than 10 false positives | 
    
    
    ds.match(F("eval_fp") > 10)
      
  
False positive âdogâ detections | 
    
    
    ep.match_labels(
       filter=(F("eval") == "fp") & (F("label") == "dog"),
       fields="predictions",
    )
      
  
Predictions with IoU > 0.9 | 
    
    
    ep.match(F("iou") > 0.9)
      
  
Reference: [`match()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match "fiftyone.core.collections.SampleCollection.match"), [`sort_by()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.sort_by "fiftyone.core.collections.SampleCollection.sort_by"), [`filter_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_labels "fiftyone.core.collections.SampleCollection.filter_labels"), and [`match_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_labels "fiftyone.core.collections.SampleCollection.match_labels").

## Classifications#

### Evaluating classifications#

The formulas in the following table assumes the following code has been run on a dataset `ds`, where the `predictions` field is populated with classification predictions that have their `logits` attribute set:
    
    
     1import fiftyone.brain as fob
     2import fiftyone.zoo as foz
     3
     4ds = foz.load_zoo_dataset("cifar10", split="test")
     5
     6# TODO: add your own predicted classifications
     7
     8ds.evaluate_classifications("predictions", gt_field="ground_truth")
     9
    10fob.compute_uniqueness(ds)
    11fob.compute_hardness(ds, "predictions")
    12fob.compute_mistakenness(ds, "predictions", label_field="ground_truth")
    

Operation | Command  
---|---  
10 most unique incorrect predictions | 
    
    
    ds.match(
        F("predictions.label") != F("ground_truth.label")
    ).sort_by("uniqueness", reverse=True)[:10]
      
  
10 most âwrongâ predictions | 
    
    
    ds.sort_by("mistakenness", reverse=True)[:10]
      
  
10 most likely annotation mistakes | 
    
    
    ds.match_tags("train").sort_by(
        "mistakenness", reverse=True
    )[:10]
      
  
Reference: [`match()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match "fiftyone.core.collections.SampleCollection.match"), [`sort_by()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.sort_by "fiftyone.core.collections.SampleCollection.sort_by"), and [`match_tags()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_tags "fiftyone.core.collections.SampleCollection.match_tags").

## Built-in filter and match functions#

FiftyOne has special methods for matching and filtering on specific data types. Take a look at the examples in this section to see how various operations can be performed via these special purpose methods, and compare that to the brute force implementation of the same operation that follows.

The tables in this section use the following example data:
    
    
     1from bson import ObjectId
     2
     3import fiftyone as fo
     4import fiftyone.zoo as foz
     5from fiftyone import ViewField as F
     6
     7ds = foz.load_zoo_dataset("quickstart")
     8
     9# Tag a few random samples
    10ds.take(3).tag_labels("potential_mistake", label_fields="predictions")
    11
    12# Grab a few label IDs
    13label_ids = [
    14    dataset.first().ground_truth.detections[0].id,
    15    dataset.last().predictions.detections[0].id,
    16]
    17ds.select_labels(ids=label_ids).tag_labels("error")
    18
    19len_filter = F("label").strlen() < 3
    20id_filter = F("_id").is_in([ObjectId(_id) for _id in label_ids])
    

### Filtering labels#

Operation | Get predicted detections that have confidence > 0.9  
---|---  
Idiomatic | 
    
    
    ds.filter_labels("predictions", F("confidence") > 0.9)
      
  
Brute force | 
    
    
    ds.set_field(
        "predictions.detections",
        F("detections").filter(F("confidence") > 0.9)),
    )
      
  
Reference: [`filter_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_labels "fiftyone.core.collections.SampleCollection.filter_labels").

### Matching labels#

Operation | Samples that have labels with idâs in the list `label_ids`  
---|---  
Idiomatic | 
    
    
    ds.match_labels(ids=label_ids)
      
  
Brute force | 
    
    
    pred_expr = F("predictions.detections").filter(id_filter).length() > 0
    gt_expr = F("ground_truth.detections").filter(id_filter).length() > 0
    ds.match(pred_expr | gt_expr)
      
  
Operation | Samples that have labels satisfying `len_filter` in `predictions` or `ground_truth` field  
---|---  
Idiomatic | 
    
    
    ds.match_labels(
        filter=len_filter,
        fields=["predictions", "ground_truth"],
    )
      
  
Brute force | 
    
    
    pred_expr = F("predictions.detections").filter(len_filter).length() > 0
    gt_expr = F("ground_truth.detections").filter(len_filter).length() > 0
    ds.match(pred_expr | gt_expr)
      
  
Operation | Samples that have labels with tag âerrorâ in `predictions` or `ground_truth` field  
---|---  
Idiomatic | 
    
    
    ds.match_labels(tags="error")
      
  
Brute force | 
    
    
    tag_expr = F("tags").contains("error")
    pred_expr = F("predictions.detections").filter(tag_expr).length() > 0
    gt_expr = F("ground_truth.detections").filter(tag_expr).length() > 0
    ds.match(pred_expr | gt_expr)
      
  
Reference: [`match_labels()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_labels "fiftyone.core.collections.SampleCollection.match_labels").

### Matching tags#

Operation | Samples that have tag `validation`  
---|---  
Idiomatic | 
    
    
    ds.match_tags("validation")
      
  
Brute force | 
    
    
    ds.match(F("tags").contains("validation"))
      
  
Reference: [`match_tags()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_tags "fiftyone.core.collections.SampleCollection.match_tags").

### Matching frames#

The following table uses this example data:
    
    
    1import fiftyone.zoo as foz
    2from fiftyone import ViewField as F
    3
    4ds = foz.load_zoo_dataset("quickstart-video")
    5num_objects = F("detections.detections").length()
    

Operation | Frames with at least 10 detections  
---|---  
Idiomatic | 
    
    
    ds.match_frames(num_objects > 10)
      
  
Brute force | 
    
    
    ds.match(F("frames").filter(num_objects > 10).length() > 0)
      
  
Reference: [`match_frames()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_frames "fiftyone.core.collections.SampleCollection.match_frames").

### Filtering keypoints#

You can use [`filter_keypoints()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.filter_keypoints "fiftyone.core.collections.SampleCollection.filter_keypoints") to retrieve individual keypoints within a [`Keypoint`](../api/fiftyone.core.labels.html#fiftyone.core.labels.Keypoint "fiftyone.core.labels.Keypoint") instance that match a specified condition.

The following table uses this example data:
    
    
     1import fiftyone as fo
     2from fiftyone import ViewField as F
     3
     4ds = fo.Dataset()
     5ds.add_samples(
     6    [
     7        fo.Sample(
     8            filepath="image1.jpg",
     9            predictions=fo.Keypoints(
    10                keypoints=[
    11                    fo.Keypoint(
    12                        label="person",
    13                        points=[(0.1, 0.1), (0.1, 0.9), (0.9, 0.9), (0.9, 0.1)],
    14                        confidence=[0.7, 0.8, 0.95, 0.99],
    15                    )
    16                ]
    17            )
    18        ),
    19        fo.Sample(filepath="image2.jpg"),
    20    ]
    21)
    22
    23ds.default_skeleton = fo.KeypointSkeleton(
    24    labels=["nose", "left eye", "right eye", "left ear", "right ear"],
    25    edges=[[0, 1, 2, 0], [0, 3], [0, 4]],
    26)
    

Operation | Only include predicted keypoints with confidence > 0.9  
---|---  
Idiomatic | 
    
    
    ds.filter_keypoints("predictions", filter=F("confidence") > 0.9)
      
  
Brute force | 
    
    
    tmp = ds.clone()
    for sample in tmp.iter_samples(autosave=True):
        if sample.predictions is None:
            continue
    
        for keypoint in sample.predictions.keypoints:
            for i, confidence in enumerate(keypoint.confidence):
                if confidence <= 0.9:
                    keypoint.points[i] = [None, None]
      
  
Reference: [`match_frames()`](../api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.match_frames "fiftyone.core.collections.SampleCollection.match_frames").

IN THIS ARTICLE 
