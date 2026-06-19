[ Run in Google Colab ](https://colab.research.google.com/github/voxel51/fiftyone/blob/main/docs/source/getting_started/object_detection/03_finding_mistakes.ipynb) |  [ View source on GitHub ](https://github.com/voxel51/fiftyone/blob/main/docs/source/getting_started/object_detection/03_finding_mistakes.ipynb) |  [ Download notebook ](https://raw.githubusercontent.com/voxel51/fiftyone/main/docs/source/getting_started/object_detection/03_finding_mistakes.ipynb)

# Step 3: Find Detection Mistakes#

Annotations mistakes create an artificial ceiling on the performance of your models. However, finding these mistakes by hand is at least as arduous as the original annotation work! Enter FiftyOne. In this tutorial, we explore how FiftyOne can be used to help you find mistakes in your object detection annotations. To detect mistakes in classification datasets, check out the recipe in the Classification task. Weâll cover the following concepts:

  * Computing insights into your dataset relating to possible label mistakes
  * Visualizing mistakes in the FiftyOne App

In order to compute mistakenness, your dataset needs to have [two detections](https://docs.voxel51.com/user_guide/using_datasets.html#object-detection) fields, one with your ground truth annotations and one with your model predictions. In this example, weâll load the [quickstart](https://docs.voxel51.com/user_guide/dataset_zoo/datasets.html#dataset-zoo-quickstart) dataset from the FiftyOne Dataset Zoo, which has ground truth annotations and predictions from a PyTorch Faster-RCNN model for a few samples from the COCO dataset.
    
    
    [ ]:
    
    
    
    import fiftyone as fo
    import fiftyone.zoo as foz
    
    dataset = foz.load_zoo_dataset("quickstart")
    
    session = fo.launch_app(dataset)
    

## Compute Mistakeness#

Now weâre ready to assess the mistakenness of the ground truth detections. Mistakeness We can do so by running the [compute_mistakenness()](https://docs.voxel51.com/api/fiftyone.brain.html#fiftyone.brain.compute_mistakenness) method from the FiftyOne Brain:
    
    
    [ ]:
    
    
    
    import fiftyone.brain as fob
    
    # Compute mistakenness of annotations in `ground_truth` field using
    # predictions from `predictions` field as point of reference
    fob.compute_mistakenness(dataset, "predictions", label_field="ground_truth")
    

The above method populates a number of fields on the samples of our dataset as well as the ground truth and predicted objects: New ground truth object attributes (in ground_truth field):

  * mistakenness (float): A measure of the likelihood that a ground truth objectâs label is incorrect
  * mistakenness_loc: A measure of the likelihood that a ground truth objectâs localization (bounding box) is inaccurate
  * possible_spurious: Ground truth objects that were not matched with a predicted object and are deemed to be likely spurious annotations will have this attribute set to True

New predicted object attributes (in predictions field):

  * possible_missing: If a highly confident prediction with no matching ground truth object is encountered, this attribute is set to True to indicate that it is a likely missing ground truth annotation

Sample-level fields:

  * mistakenness: The maximum mistakenness of the ground truth objects in each sample
  * possible_spurious: The number of possible spurious ground truth objects in each sample
  * possible_missing: The number of possible missing ground truth objects in each sample



## Analyzing Results#

Letâs use FiftyOne to investigate the results. First, letâs show the samples with the most likely annotation mistakes:
    
    
    [ ]:
    
    
    
    from fiftyone import ViewField as F
    
    # Sort by likelihood of mistake (most likely first)
    mistake_view = dataset.sort_by("mistakenness", reverse=True)
    
    # Print some information about the view
    print(mistake_view)
    
    # Show the samples we processed in rank order by the mistakenness
    session.view = mistake_view
    

Another useful query is to find all objects that have a high mistakenness, letâs say > 0.95:
    
    
    [ ]:
    
    
    
    from fiftyone import ViewField as F
    
    session.view = dataset.filter_labels("ground_truth", F("mistakenness") > 0.95)
    

Looking through the results, we can see that many of these images have a bunch of predictions which actually look like they are correct, but no ground truth annotations. This is a common mistake in object detection datasets, where the annotator may have missed some objects in the image. On the other hand, there are some detections which are mislabeled and are just wrong. In the example we can see two potential issues. One is the person on the TV is unlabeled. Two is the books on the bookcase are ambiguously labeled. Is one book a book, or is a group of books âbookâ. FiftyOne helps you sort out issues exactly like this. We can use a similar workflow to look at objects that may be localized poorly:
    
    
    [ ]:
    
    
    
    session.view = dataset.filter_labels("ground_truth", F("mistakenness_loc") > 0.85)
    

In some of these examples, there is not necessarily highly mistaken localization, there are just a bunch of small, relatively overlapping objects. In other examples, such as above, the localization is clearly off. The possible_missing field can also be useful to sort by to find instances of incorrect annotations. Similarly, possible_spurious can be used to find objects that the model detected that may have been missed by annotators.
    
    
    [ ]:
    
    
    
    session.view = dataset.match(F("possible_missing") > 0)
    

Once again, we can find more of those pesky mistakes! Look at all the missing person annotations here!  In FiftyOne, we can tag our samples and export them for an annotation job with one of our labeling integrations: [CVAT](https://docs.voxel51.com/integrations/cvat.html), [Label Studio](https://docs.voxel51.com/integrations/labelstudio.html), [V7](https://docs.voxel51.com/integrations/v7.html), or [LabelBox](https://docs.voxel51.com/integrations/labelbox.html)! This can get our dataset back into tip-top shape to train again!

## Summary#

Youâve learned to find annotation mistakes using `fob.compute_mistakenness()` and analyze results with mistakenness scores, localization errors, and missing/spurious detection fields. Next up: **Step 4: Use labeling integrations to fix mistakes and improve your dataset quality** IN THIS ARTICLE 
