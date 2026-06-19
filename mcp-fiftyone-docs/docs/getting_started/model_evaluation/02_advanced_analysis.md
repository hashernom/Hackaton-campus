[ Run in Google Colab ](https://colab.research.google.com/github/voxel51/fiftyone/blob/main/docs/source/getting_started/model_evaluation/02_advanced_analysis.ipynb) |  [ View source on GitHub ](https://github.com/voxel51/fiftyone/blob/main/docs/source/getting_started/model_evaluation/02_advanced_analysis.ipynb) |  [ Download notebook ](https://raw.githubusercontent.com/voxel51/fiftyone/main/docs/source/getting_started/model_evaluation/02_advanced_analysis.ipynb)

# Step 2: Analyzing with Model Evaluation Panel#

In our last step we showed some basic ways on how to evaluate models. In this step, we will show how to take it even further with the [Model Eval](https://docs.voxel51.com/plugins/api/plugins.panels.model_evaluation.html) Panel in the app. With the Model Eval Panel you can:

  * See all evaluation runs on a dataset
  * View summary statistics of each run
  * Filter dataset based on FP, TP, and more
  * Analyze class-wise evaluation metrics and filter based on them
  * View confusion matrices and histograms of evaluation results

Letâs hop into an example to see how to get started!
    
    
    [1]:
    
    
    
    import fiftyone as fo
    import fiftyone.zoo as foz
    
    dataset = foz.load_zoo_dataset("quickstart")
    
    # View summary info about the dataset
    print(dataset)
    
    
    
    Dataset already downloaded
    Loading existing dataset 'quickstart'. To reload from disk, either delete the existing dataset or provide a custom `dataset_name` to use
    Name:        quickstart
    Media type:  image
    Num samples: 200
    Persistent:  False
    Tags:        []
    Sample fields:
        id:                fiftyone.core.fields.ObjectIdField
        filepath:          fiftyone.core.fields.StringField
        tags:              fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
        metadata:          fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.ImageMetadata)
        created_at:        fiftyone.core.fields.DateTimeField
        last_modified_at:  fiftyone.core.fields.DateTimeField
        ground_truth:      fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detections)
        uniqueness:        fiftyone.core.fields.FloatField
        predictions:       fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detections)
        eval_tp:           fiftyone.core.fields.IntField
        eval_fp:           fiftyone.core.fields.IntField
        eval_fn:           fiftyone.core.fields.IntField
        eval_high_conf_tp: fiftyone.core.fields.IntField
        eval_high_conf_fp: fiftyone.core.fields.IntField
        eval_high_conf_fn: fiftyone.core.fields.IntField
    

Letâs quickly rerun evaluation in case we do not have it from the previous step:
    
    
    [2]:
    
    
    
    results = dataset.evaluate_detections(
        "predictions",
        gt_field="ground_truth",
        eval_key="eval",
        compute_mAP=True,
    )
    
    
    
    Evaluating detections...
     100% |âââââââââââââââââ| 200/200 [7.2s elapsed, 0s remaining, 18.5 samples/s]
    Performing IoU sweep...
     100% |âââââââââââââââââ| 200/200 [2.3s elapsed, 0s remaining, 74.4 samples/s]
    
    
    
    [3]:
    
    
    
    from fiftyone import ViewField as F
    
    # Only contains detections with confidence >= 0.75
    high_conf_view = dataset.filter_labels("predictions", F("confidence") > 0.75, only_matches=False)
    
    results = high_conf_view.evaluate_detections(
        "predictions",
        gt_field="ground_truth",
        eval_key="eval_high_conf",
        compute_mAP=True,
    )
      
    
    
    
    Evaluating detections...
     100% |âââââââââââââââââ| 200/200 [1.3s elapsed, 0s remaining, 127.8 samples/s]
    Performing IoU sweep...
     100% |âââââââââââââââââ| 200/200 [924.4ms elapsed, 0s remaining, 216.4 samples/s]
    
    
    
    [11]:
    
    
    
    dataset.load_evaluation_view("eval")
    
    
    
    [11]:
    
    
    
    Name:        quickstart
    Media type:  image
    Num samples: 200
    Persistent:  False
    Tags:        []
    Sample fields:
        id:                fiftyone.core.fields.ObjectIdField
        filepath:          fiftyone.core.fields.StringField
        tags:              fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
        metadata:          fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.ImageMetadata)
        created_at:        fiftyone.core.fields.DateTimeField
        last_modified_at:  fiftyone.core.fields.DateTimeField
        ground_truth:      fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detections)
        uniqueness:        fiftyone.core.fields.FloatField
        predictions:       fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detections)
        eval_tp:           fiftyone.core.fields.IntField
        eval_fp:           fiftyone.core.fields.IntField
        eval_fn:           fiftyone.core.fields.IntField
        eval_high_conf_tp: fiftyone.core.fields.IntField
        eval_high_conf_fp: fiftyone.core.fields.IntField
        eval_high_conf_fn: fiftyone.core.fields.IntField
    

Now we can open up our dataset and view are results in the Model Eval Panel! I recommend opening the app in browser for the best experience at `http://localhost:5151/`!
    
    
    [ ]:
    
    
    
    session = fo.launch_app(dataset)
    

## Explore the Model Evaluation Panel#

Now that you have the Model Evaluation Panel open, you can explore all the powerful features it offers:

  * **Browse evaluation runs** : Switch between different evaluation runs (like `eval` and `eval_high_conf`) to compare model performance
  * **Analyze metrics** : View precision, recall, F1-score, and mAP metrics for your models
  * **Class-wise analysis** : Examine performance metrics for individual classes to identify which objects your model struggles with
  * **Confusion matrices** : Visualize classification errors and understand common misclassifications
  * **Interactive filtering** : Filter your dataset to show only true positives, false positives, false negatives, or specific confidence ranges
  * **Histogram analysis** : Explore distributions of confidence scores, IoU values, and other evaluation metrics
  * **Sample-level insights** : Click on specific samples to understand why certain predictions were classified as TP, FP, or FN

Take some time to explore these features and gain deeper insights into your modelâs performance. The Model Evaluation Panel makes it easy to identify patterns, debug model issues, and make data-driven decisions for model improvement! IN THIS ARTICLE 
