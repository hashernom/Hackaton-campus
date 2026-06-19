# FiftyOne Brain#

The [FiftyOne Brain](https://github.com/voxel51/fiftyone-brain) provides powerful machine learning techniques that are designed to transform how you curate your data from an art into a measurable science.

Note

Did you know? You can execute Brain methods from the FiftyOne App by installing the [@voxel51/brain](https://github.com/voxel51/fiftyone-plugins/tree/main/plugins/brain) plugin!

[ Try experimental Brain features in FiftyOne Labs ](labs/index.html)

The FiftyOne Brain methods are useful across the stages of the machine learning workflow:

  * Visualizing embeddings: Tired of combing through individual images/videos and staring at aggregate performance metrics trying to figure out how to improve the performance of your model? Using FiftyOne to visualize your dataset in a _low-dimensional embedding space_ can reveal patterns and clusters in your data that can help you answer many important questions about your data, from identifying the most critical failure modes of your model, to isolating examples of critical scenarios, to recommending new samples to add to your training dataset, and more!

  * Similarity: When constructing a dataset or training a model, have you ever wanted to find similar examples to an image or object of interest? For example, you may have found a failure case of your model and now want to search for similar scenarios in your evaluation set to diagnose the issue, or you want to mine your data lake to augment your training set to fix the issue. Use the FiftyOne Brain to index your data by _similarity_ and you can easily query and sort your datasets to find similar examples, both programmatically and via point-and-click in the App.

  * Leaky splits: Often when sourcing data en masse, duplicates and near duplicates can slip through the cracks. The FiftyOne Brain offers a _leaky splits analysis_ that can be used to find potential leaks between dataset splits. Such leaks can be misleading when evaluating a model, giving an overly optimistic measure for the quality of training.

  * Near duplicates: When curating massive datasets, you may inadvertently add near duplicate data to your datasets, which can bias or otherwise confuse your models. The FiftyOne Brain offers a _near duplicate detection_ algorithm that automatically surfaces such data quality issues and prompts you to take action to resolve them.

  * Exact duplicates: Despite your best efforts, you may accidentally add duplicate data to a dataset. The FiftyOne Brain provides an _exact duplicate detection_ method that scans your data and alerts you if a dataset contains duplicate samples, either under the same or different filenames.

  * Uniqueness: During the training loop for a model, the best results will be seen when training on unique data. The FiftyOne Brain provides a _uniqueness measure_ for images that compare the content of every image in a dataset with all other images. Uniqueness operates on raw images and does not require any prior annotation on the data. It is hence very useful in the early stages of the machine learning workflow when you are likely asking âWhat data should I select to annotate?â

  * Mistakenness: Annotations mistakes create an artificial ceiling on the performance of your models. However, finding these mistakes by hand is at least as arduous as the original annotation was, especially in cases of larger datasets. The FiftyOne Brain provides a quantitative _mistakenness measure_ to identify possible label mistakes. Mistakenness operates on labeled images and requires the logit-output of your model predictions in order to provide maximum efficacy. It also works on detection datasets to find missed objects, incorrect annotations, and localization issues.

  * Hardness: While a model is training, it will learn to understand attributes of certain samples faster than others. The FiftyOne Brain provides a _hardness measure_ that calculates how easy or difficult it is for your model to understand any given sample. Mining hard samples is a tried and true measure of mature machine learning processes. Use your current model instance to compute predictions on unlabeled samples to determine which are the most valuable to have annotated and fed back into the system as training samples, for example.

  * Representativeness: When working with large datasets, it can be hard to determine what samples within it are outliers and which are more typical. The FiftyOne Brain offers a _representativeness measure_ that can be used to find the most common types of images in your dataset. This is especially helpful to find easy examples to train on in your data and for visualizing common modes of the data.




Note

Check out the [tutorials page](tutorials/index.html#tutorials) for detailed examples demonstrating the use of many Brain capabilities.

## Visualizing embeddings#

The FiftyOne Brain provides a powerful [`compute_visualization()`](api/fiftyone.brain.html#fiftyone.brain.compute_visualization "fiftyone.brain.compute_visualization") method that you can use to generate low-dimensional representations of the samples and/or individual objects in your datasets.

These representations can be visualized natively in the Appâs [Embeddings panel](user_guide/app.html#app-embeddings-panel), where you can interactively select points of interest and view the corresponding samples/labels of interest in the [Samples panel](user_guide/app.html#app-samples-panel), and vice versa.

There are two primary components to an embedding visualization: the method used to generate the embeddings, and the dimensionality reduction method used to compute a low-dimensional representation of the embeddings.

### Embedding methods#

The `embeddings` and `model` parameters of [`compute_visualization()`](api/fiftyone.brain.html#fiftyone.brain.compute_visualization "fiftyone.brain.compute_visualization") support a variety of ways to generate embeddings for your data:

  * Provide nothing, in which case a default general purpose model is used to embed your data

  * Provide a [`Model`](api/fiftyone.core.models.html#fiftyone.core.models.Model "fiftyone.core.models.Model") instance or the name of any model from the [Model Zoo](model_zoo/index.html#model-zoo) that supports embeddings

  * Provide your own precomputed embeddings in array form

  * Provide the name of a [`VectorField`](api/fiftyone.core.fields.html#fiftyone.core.fields.VectorField "fiftyone.core.fields.VectorField") or [`ArrayField`](api/fiftyone.core.fields.html#fiftyone.core.fields.ArrayField "fiftyone.core.fields.ArrayField") of your dataset in which precomputed embeddings are stored




### Dimensionality reduction methods#

The `method` parameter of [`compute_visualization()`](api/fiftyone.brain.html#fiftyone.brain.compute_visualization "fiftyone.brain.compute_visualization") allows you to specify the dimensionality reduction method to use. The supported methods are:

  * **umap** (_default_): Uniform Manifold Approximation and Projection ([UMAP](https://github.com/lmcinnes/umap))

  * **tsne** : t-distributed Stochastic Neighbor Embedding ([t-SNE](https://lvdmaaten.github.io/tsne))

  * **pca** : Principal Component Analysis ([PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html))

  * **manual** : provide a manually computed low-dimensional representation



    
    
    1import fiftyone.brain as fob
    2
    3results = fob.compute_visualization(
    4    dataset,
    5    method="umap",  # "umap", "tsne", "pca", etc
    6    brain_key="...",
    7    ...
    8)
    

Note

When you use the default [UMAP](https://github.com/lmcinnes/umap) method for the first time, you will be prompted to install the [umap-learn](https://github.com/lmcinnes/umap) package.

Note

Refer to this section for more information about creating visualization runs.

### Applications#

How can embedding-based visualization of your data be used in practice? These visualizations often uncover hidden structure in you data that has important semantic meaning depending on the data you use to color/size the points.

Here are a few of the many possible applications:

  * Identifying anomalous and/or visually similar examples

  * Uncovering patterns in incorrect/spurious predictions

  * Finding examples of target scenarios in your data lake

  * Mining hard examples for your evaluation pipeline

  * Recommending samples from your data lake for classes that need additional training data

  * Unsupervised pre-annotation of training data




The best part about embedding visualizations is that you will likely discover more applications specific to your use case when you try it out on your data!

Note

Check out the [image embeddings tutorial](tutorials/image_embeddings.html) to see example uses of the Brainâs embeddings-powered visualization methods to uncover hidden structure in datasets.

### Image embeddings example#

The following example gives a taste of the powers of visual embeddings in FiftyOne using the [BDD100K dataset](dataset_zoo/datasets/bdd100k.html#dataset-zoo-bdd100k) from the dataset zoo, embeddings generated by a [mobilenet model](model_zoo/models/mobilenet_v2_imagenet_torch.html#model-zoo-mobilenet-v2-imagenet-torch) from the model zoo, and the default [UMAP](https://github.com/lmcinnes/umap) dimensionality reduction method.

In this setup, the scatterpoints in the [Embeddings panel](user_guide/app.html#app-embeddings-panel) correspond to images in the validation split colored by the `time of day` labels provided by the BDD100K dataset. When points are lasso-ed in the plot, the corresponding samples are automatically selected in the [Samples panel](user_guide/app.html#app-samples-panel):
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3import fiftyone.zoo as foz
     4
     5# The BDD dataset must be manually downloaded. See the zoo docs for details
     6source_dir = "/path/to/dir-with-bdd100k-files"
     7
     8dataset = foz.load_zoo_dataset(
     9    "bdd100k", split="validation", source_dir=source_dir,
    10)
    11
    12# Compute embeddings
    13# You will likely want to run this on a machine with GPU, as this requires
    14# running inference on 10,000 images
    15model = foz.load_zoo_model("mobilenet-v2-imagenet-torch")
    16embeddings = dataset.compute_embeddings(model)
    17
    18# Compute visualization
    19results = fob.compute_visualization(
    20    dataset, embeddings=embeddings, seed=51, brain_key="img_viz"
    21)
    22
    23session = fo.launch_app(dataset)
    

Note

Did you know? You can [programmatically configure](user_guide/app.html#app-spaces-python) your Spaces layout!

The GIF shows the variety of insights that are revealed by running this simple protocol:

  * The first cluster of points selected reveals a set of samples whose field of view is corrupted by hardware gradients at the top and bottom of the image

  * The second cluster of points reveals a set of images in rainy conditions with water droplets on the windshield

  * Hiding the primary cluster of `daytime` points and selecting the remaining `night` points reveals that the `night` points have incorrect labels




### Object embeddings example#

The following example demonstrates how embeddings can be used to visualize the ground truth objects in the [quickstart dataset](dataset_zoo/datasets/quickstart.html#dataset-zoo-quickstart) using the [`compute_visualization()`](api/fiftyone.brain.html#fiftyone.brain.compute_visualization "fiftyone.brain.compute_visualization") methodâs default embeddings model and dimensionality method.

In this setup, we generate a visualization for all ground truth objects, but then we create a [view](user_guide/using_views.html#view-filtering) that restricts the visualization to only objects in a subset of the classes. The scatterpoints in the [Embeddings panel](user_guide/app.html#app-embeddings-panel) correspond to objects, colored by their `label`. When points are lasso-ed in the plot, the corresponding object patches are automatically selected in the [Samples panel](user_guide/app.html#app-samples-panel):
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3import fiftyone.zoo as foz
     4from fiftyone import ViewField as F
     5
     6dataset = foz.load_zoo_dataset("quickstart")
     7
     8# Generate visualization for `ground_truth` objects
     9results = fob.compute_visualization(
    10    dataset, patches_field="ground_truth", brain_key="gt_viz"
    11)
    12
    13# Restrict to the 10 most common classes
    14counts = dataset.count_values("ground_truth.detections.label")
    15classes = sorted(counts, key=counts.get, reverse=True)[:10]
    16view = dataset.filter_labels("ground_truth", F("label").is_in(classes))
    17
    18session = fo.launch_app(view)
    

Note

Did you know? You can [programmatically configure](user_guide/app.html#app-spaces-python) your Spaces layout!

As you can see, the coloring of the scatterpoints allows you to discover natural clusters of objects, such as visually similar carrots or kites in the air.

### Visualization API#

This section describes how to setup, create, and manage visualizations in detail.

#### Changing your visualization method#

You can use a specific dimensionality reduction method for a particular visualization run by passing the `method` parameter to [`compute_visualization()`](api/fiftyone.brain.html#fiftyone.brain.compute_visualization "fiftyone.brain.compute_visualization"):
    
    
    1results = fob.compute_visualization(..., method="<method>", ...)
    

Alternatively, you can change your default dimensionality reduction method for an entire session by setting the `FIFTYONE_BRAIN_DEFAULT_VISUALIZATION_METHOD` environment variable:
    
    
    export FIFTYONE_BRAIN_DEFAULT_VISUALIZATION_METHOD=<method>
    

Finally, you can permanently change your default dimensionality reduction method by updating the `default_visualization_method` key of your brain config at `~/.fiftyone/brain_config.json`:
    
    
    {
        "default_visualization_method": "<method>",
        "visualization_methods": {
            "<method>": {...},
            ...
        }
    }
    

#### Configuring your visualization method#

Dimensionality reduction methods may be configured in a variety of method-specific ways, which you can see by inspecting the parameters of a methodâs associated [`VisualizationConfig`](api/fiftyone.brain.visualization.html#fiftyone.brain.visualization.VisualizationConfig "fiftyone.brain.visualization.VisualizationConfig") class.

The relevant classes for the builtin dimensionality reduction methods are:

  * **umap** : [`fiftyone.brain.visualization.UMAPVisualizationConfig`](api/fiftyone.brain.visualization.html#fiftyone.brain.visualization.UMAPVisualizationConfig "fiftyone.brain.visualization.UMAPVisualizationConfig")

  * **tsne** : [`fiftyone.brain.visualization.TSNEVisualizationConfig`](api/fiftyone.brain.visualization.html#fiftyone.brain.visualization.TSNEVisualizationConfig "fiftyone.brain.visualization.TSNEVisualizationConfig")

  * **pca** : [`fiftyone.brain.visualization.PCAVisualizationConfig`](api/fiftyone.brain.visualization.html#fiftyone.brain.visualization.PCAVisualizationConfig "fiftyone.brain.visualization.PCAVisualizationConfig")

  * **manual** : [`fiftyone.brain.visualization.ManualVisualizationConfig`](api/fiftyone.brain.visualization.html#fiftyone.brain.visualization.ManualVisualizationConfig "fiftyone.brain.visualization.ManualVisualizationConfig")




You can configure a dimensionality reduction methodâs parameters for a specific run by simply passing supported config parameters as keyword arguments each time you call [`compute_visualization()`](api/fiftyone.brain.html#fiftyone.brain.compute_visualization "fiftyone.brain.compute_visualization"):
    
    
    1results = fob.compute_visualization(
    2    ...
    3    method="umap",
    4    min_dist=0.2,
    5)
    

Alternatively, you can more permanently configure your dimensionality reduction method(s) via your brain config.

#### Optimizing lassoing performance#

You can pass `create_index=True` to [`compute_visualization()`](api/fiftyone.brain.html#fiftyone.brain.compute_visualization "fiftyone.brain.compute_visualization") to store a spatial index of the computed points in a field of your datasetâs samples.

This is highly recommended for large datasets as it enables efficient querying when lassoing points in the [Embeddings panel](user_guide/app.html#app-embeddings-panel).

Image embeddingsObject embeddings
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3import fiftyone.zoo as foz
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6
     7# Generate a visualization with a spatial index
     8results = fob.compute_visualization(
     9    dataset,
    10    brain_key="img_viz",
    11    create_index=True,
    12)
    
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3import fiftyone.zoo as foz
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6
     7# Generate a patch visualization with a spatial index
     8results = fob.compute_visualization(
     9    dataset,
    10    patches_field="ground_truth",
    11    brain_key="gt_viz",
    12    create_index=True,
    13)
    

Note

By default, spatial indexes are created in a field/attribute with name `brain_key`, but you can customize this by passing the `points_field` parameter to [`compute_visualization()`](api/fiftyone.brain.html#fiftyone.brain.compute_visualization "fiftyone.brain.compute_visualization").

You can check whether an existing visualization result has a spatial index via [`has_spatial_index`](api/fiftyone.brain.visualization.html#fiftyone.brain.visualization.VisualizationResults.has_spatial_index "fiftyone.brain.visualization.VisualizationResults.has_spatial_index"), and you can add or remove spatial indexes via [`index_points()`](api/fiftyone.brain.visualization.html#fiftyone.brain.visualization.VisualizationResults.index_points "fiftyone.brain.visualization.VisualizationResults.index_points") and [`remove_index()`](api/fiftyone.brain.visualization.html#fiftyone.brain.visualization.VisualizationResults.remove_index "fiftyone.brain.visualization.VisualizationResults.remove_index"):
    
    
    1print(results.has_spatial_index)
    2# True/False
    3
    4# Add a spatial index to existing visualization results
    5results.index_points()
    6
    7# Remove the spatial index from existing visualization results
    8results.remove_index()
    

## Similarity#

The FiftyOne Brain provides a [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity") method that you can use to index the images or object patches in a dataset by similarity.

Once youâve indexed a dataset by similarity, you can use the [`sort_by_similarity()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.sort_by_similarity "fiftyone.core.collections.SampleCollection.sort_by_similarity") view stage to programmatically sort your dataset by similarity to any image(s) or object patch(es) of your choice in your dataset. In addition, the App provides a convenient [point-and-click interface](user_guide/app.html#app-similarity) for sorting by similarity with respect to an index on a dataset.

Note

Did you know? You can search by natural language using similarity indexes!

### Embedding methods#

Like embeddings visualization, similarity leverages deep embeddings to generate an index for a dataset.

The `embeddings` and `model` parameters of [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity") support a variety of ways to generate embeddings for your data:

  * Provide nothing, in which case a default general purpose model is used to index your data

  * Provide a [`Model`](api/fiftyone.core.models.html#fiftyone.core.models.Model "fiftyone.core.models.Model") instance or the name of any model from the [Model Zoo](model_zoo/index.html#model-zoo) that supports embeddings

  * Provide your own precomputed embeddings in array form

  * Provide the name of a [`VectorField`](api/fiftyone.core.fields.html#fiftyone.core.fields.VectorField "fiftyone.core.fields.VectorField") or [`ArrayField`](api/fiftyone.core.fields.html#fiftyone.core.fields.ArrayField "fiftyone.core.fields.ArrayField") of your dataset in which precomputed embeddings are stored




### Similarity backends#

By default, all similarity indexes are served using a builtin [scikit-learn](https://scikit-learn.org) backend, but you can pass the optional `backend` parameter to [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity") to switch to another supported backend:

  * **sklearn** (_default_): a [scikit-learn](https://scikit-learn.org) backend

  * **qdrant** : a [Qdrant backend](integrations/qdrant.html#qdrant-integration)

  * **redis** : a [Redis backend](integrations/redis.html#redis-integration)

  * **pinecone** : a [Pinecone backend](integrations/pinecone.html#pinecone-integration)

  * **mongodb** : a [MongoDB backend](integrations/mongodb.html#mongodb-integration)

  * **elasticsearch** : a [Elasticsearch backend](integrations/elasticsearch.html#elasticsearch-integration)

  * **pgvector** : a [PostgreSQL Pgvector backend](integrations/pgvector.html#pgvector-integration)

  * **mosaic** : a [Databricks Mosaic AI backend](integrations/mosaic.html#mosaic-integration)

  * **milvus** : a [Milvus backend](integrations/milvus.html#milvus-integration)

  * **lancedb** : a [LanceDB backend](integrations/lancedb.html#lancedb-integration)



    
    
    1import fiftyone.brain as fob
    2
    3results = fob.compute_similarity(
    4    dataset,
    5    backend="sklearn",  # "sklearn", "qdrant", "redis", etc
    6    brain_key="...",
    7    ...
    8)
    

Note

Refer to this section for more information about creating, managing and deleting similarity indexes.

### Image similarity#

This section demonstrates the basic workflow of:

  * Indexing an image dataset by similarity

  * Using the Appâs [image similarity](user_guide/app.html#app-image-similarity) UI to query by visual similarity

  * Using the SDKâs [`sort_by_similarity()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.sort_by_similarity "fiftyone.core.collections.SampleCollection.sort_by_similarity") view stage to programmatically query the index




To index a dataset by image similarity, pass the [`Dataset`](api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") or [`DatasetView`](api/fiftyone.core.view.html#fiftyone.core.view.DatasetView "fiftyone.core.view.DatasetView") of interest to [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity") along with a name for the index via the `brain_key` argument.

Next load the dataset in the App and select some image(s). Whenever there is an active selection in the App, a [similarity icon](user_guide/app.html#app-image-similarity) will appear above the grid, enabling you to sort by similarity to your current selection.

You can use the [Similarity Search panel](user_guide/app.html#app-similarity-search-panel) for advanced search options, run management, and search history.
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3import fiftyone.zoo as foz
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6
     7# Index images by similarity
     8fob.compute_similarity(
     9    dataset,
    10    model="clip-vit-base32-torch",
    11    brain_key="img_sim",
    12)
    13
    14session = fo.launch_app(dataset)
    

Note

In the example above, we specify a [zoo model](model_zoo/index.html#model-zoo) with which to generate embeddings, but you can also provide precomputed embeddings.

Alternatively, you can use the [`sort_by_similarity()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.sort_by_similarity "fiftyone.core.collections.SampleCollection.sort_by_similarity") view stage to programmatically [construct a view](user_guide/using_views.html#using-views) that contains the sorted results:
    
    
    1# Choose a random image from the dataset
    2query_id = dataset.take(1).first().id
    3
    4# Programmatically construct a view containing the 15 most similar images
    5view = dataset.sort_by_similarity(query_id, k=15, brain_key="img_sim")
    6
    7session.view = view
    

Note

Performing a similarity search on a [`DatasetView`](api/fiftyone.core.view.html#fiftyone.core.view.DatasetView "fiftyone.core.view.DatasetView") will **only** return results from the view; if the view contains samples that were not included in the index, they will never be included in the result.

This means that you can index an entire [`Dataset`](api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") once and then perform searches on subsets of the dataset by [constructing views](user_guide/using_views.html#using-views) that contain the images of interest.

Note

For large datasets, you may notice longer load times the first time you use a similarity index in a session. Subsequent similarity searches will use cached results and will be faster!

### Object similarity#

This section demonstrates the basic workflow of:

  * Indexing a dataset of objects by similarity

  * Using the Appâs [object similarity](user_guide/app.html#app-object-similarity) UI to query by visual similarity

  * Using the SDKâs [`sort_by_similarity()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.sort_by_similarity "fiftyone.core.collections.SampleCollection.sort_by_similarity") view stage to programmatically query the index




You can index any objects stored on datasets in [`Detection`](api/fiftyone.core.labels.html#fiftyone.core.labels.Detection "fiftyone.core.labels.Detection"), [`Detections`](api/fiftyone.core.labels.html#fiftyone.core.labels.Detections "fiftyone.core.labels.Detections"), [`Polyline`](api/fiftyone.core.labels.html#fiftyone.core.labels.Polyline "fiftyone.core.labels.Polyline"), or [`Polylines`](api/fiftyone.core.labels.html#fiftyone.core.labels.Polylines "fiftyone.core.labels.Polylines") format. See [this section](user_guide/using_datasets.html#using-labels) for more information about adding labels to your datasets.

To index by object patches, simply pass the [`Dataset`](api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") or [`DatasetView`](api/fiftyone.core.view.html#fiftyone.core.view.DatasetView "fiftyone.core.view.DatasetView") of interest to [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity") along with the name of the patches field and a name for the index via the `brain_key` argument.

Next load the dataset in the App and switch to [object patches view](user_guide/app.html#app-object-patches) by clicking the patches icon above the grid and choosing the label field of interest from the dropdown.

Now whenever you have selected one or more patches in the App, a [similarity icon](user_guide/app.html#app-object-similarity) will appear above the grid, enabling you to sort by similarity to your current selection.

You can also use the [Similarity Search panel](user_guide/app.html#app-similarity-search-panel) for advanced search options, run management, and search history.
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3import fiftyone.zoo as foz
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6
     7# Index ground truth objects by similarity
     8fob.compute_similarity(
     9    dataset,
    10    patches_field="ground_truth",
    11    model="clip-vit-base32-torch",
    12    brain_key="gt_sim",
    13)
    14
    15session = fo.launch_app(dataset)
    

Note

In the example above, we specify a [zoo model](model_zoo/index.html#model-zoo) with which to generate embeddings, but you can also provide precomputed embeddings.

Alternatively, you can directly use the [`sort_by_similarity()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.sort_by_similarity "fiftyone.core.collections.SampleCollection.sort_by_similarity") view stage to programmatically [construct a view](user_guide/using_views.html#using-views) that contains the sorted results:
    
    
     1# Convert to patches view
     2patches = dataset.to_patches("ground_truth")
     3
     4# Choose a random patch object from the dataset
     5query_id = patches.take(1).first().id
     6
     7# Programmatically construct a view containing the 15 most similar objects
     8view = patches.sort_by_similarity(query_id, k=15, brain_key="gt_sim")
     9
    10session.view = view
    

Note

Performing a similarity search on a [`DatasetView`](api/fiftyone.core.view.html#fiftyone.core.view.DatasetView "fiftyone.core.view.DatasetView") will **only** return results from the view; if the view contains objects that were not included in the index, they will never be included in the result.

This means that you can index an entire [`Dataset`](api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") once and then perform searches on subsets of the dataset by [constructing views](user_guide/using_views.html#using-views) that contain the objects of interest.

Note

For large datasets, you may notice longer load times the first time you use a similarity index in a session. Subsequent similarity searches will use cached results and will be faster!

### Text similarity#

When you create a similarity index powered by the [CLIP model](model_zoo/models/clip_vit_base32_torch.html#model-zoo-clip-vit-base32-torch), you can also search by arbitrary natural language queries [natively in the App](user_guide/app.html#app-text-similarity), including via the [Similarity Search panel](user_guide/app.html#app-similarity-search-panel)!

Image similarityObject similarity
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3import fiftyone.zoo as foz
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6
     7# Index images by similarity
     8image_index = fob.compute_similarity(
     9    dataset,
    10    model="clip-vit-base32-torch",
    11    brain_key="img_sim",
    12)
    13
    14session = fo.launch_app(dataset)
    

You can verify that an index supports text queries by checking that it `supports_prompts`:
    
    
    1# If you have already loaded the index
    2print(image_index.config.supports_prompts)  # True
    3
    4# Without loading the index
    5info = dataset.get_brain_info("img_sim")
    6print(info.config.supports_prompts)  # True
    
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3import fiftyone.zoo as foz
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6
     7# Index ground truth objects by similarity
     8object_index = fob.compute_similarity(
     9    dataset,
    10    patches_field="ground_truth",
    11    model="clip-vit-base32-torch",
    12    brain_key="gt_sim",
    13)
    14
    15session = fo.launch_app(dataset)
    

You can verify that an index supports text queries by checking that it `supports_prompts`:
    
    
    1# If you have already loaded the index
    2print(object_index.config.supports_prompts)  # True
    3
    4# Without loading the index
    5info = dataset.get_brain_info("gt_sim")
    6print(info.config.supports_prompts)  # True
    

You can also perform text queries via the SDK by passing a prompt directly to [`sort_by_similarity()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.sort_by_similarity "fiftyone.core.collections.SampleCollection.sort_by_similarity") along with the `brain_key` of a compatible similarity index:

Image similarityObject similarity
    
    
    1# Perform a text query
    2query = "kites high in the air"
    3view = dataset.sort_by_similarity(query, k=15, brain_key="img_sim")
    4
    5session.view = view
    
    
    
    1# Convert to patches view
    2patches = dataset.to_patches("ground_truth")
    3
    4# Perform a text query
    5query = "cute puppies"
    6view = patches.sort_by_similarity(query, k=15, brain_key="gt_sim")
    7
    8session.view = view
    

Note

In general, any custom model that is made available via the [model zoo interface](model_zoo/api.html#model-zoo-add) that implements the [`PromptMixin`](api/fiftyone.core.models.html#fiftyone.core.models.PromptMixin "fiftyone.core.models.PromptMixin") interface can support text similarity queries!

### Similarity API#

This section describes how to setup, create, and manage similarity indexes in detail.

#### Changing your similarity backend#

You can use a specific backend for a particular similarity index by passing the `backend` parameter to [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity"):
    
    
    1index = fob.compute_similarity(..., backend="<backend>", ...)
    

Alternatively, you can change your default similarity backend for an entire session by setting the `FIFTYONE_BRAIN_DEFAULT_SIMILARITY_BACKEND` environment variable.
    
    
    export FIFTYONE_BRAIN_DEFAULT_SIMILARITY_BACKEND=<backend>
    

Finally, you can permanently change your default similarity backend by updating the `default_similarity_backend` key of your brain config at `~/.fiftyone/brain_config.json`:
    
    
    {
        "default_similarity_backend": "<backend>",
        "similarity_backends": {
            "<backend>": {...},
            ...
        }
    }
    

#### Configuring your backend#

Similarity backends may be configured in a variety of backend-specific ways, which you can see by inspecting the parameters of a backendâs associated [`SimilarityConfig`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityConfig "fiftyone.brain.similarity.SimilarityConfig") class.

The relevant classes for the builtin similarity backends are:

  * **sklearn** : [`fiftyone.brain.internal.core.sklearn.SklearnSimilarityConfig`](api/fiftyone.brain.internal.core.sklearn.html#fiftyone.brain.internal.core.sklearn.SklearnSimilarityConfig "fiftyone.brain.internal.core.sklearn.SklearnSimilarityConfig")

  * **qdrant** : `fiftyone.brain.internal.core.qdrant.QdrantSimilarityConfig`

  * **redis** : [`fiftyone.brain.internal.core.redis.RedisSimilarityConfig`](api/fiftyone.brain.internal.core.redis.html#fiftyone.brain.internal.core.redis.RedisSimilarityConfig "fiftyone.brain.internal.core.redis.RedisSimilarityConfig")

  * **pinecone** : [`fiftyone.brain.internal.core.pinecone.PineconeSimilarityConfig`](api/fiftyone.brain.internal.core.pinecone.html#fiftyone.brain.internal.core.pinecone.PineconeSimilarityConfig "fiftyone.brain.internal.core.pinecone.PineconeSimilarityConfig")

  * **mongodb** : [`fiftyone.brain.internal.core.mongodb.MongoDBSimilarityConfig`](api/fiftyone.brain.internal.core.mongodb.html#fiftyone.brain.internal.core.mongodb.MongoDBSimilarityConfig "fiftyone.brain.internal.core.mongodb.MongoDBSimilarityConfig")

  * **elasticsearch** : a fiftyone.brain.internal.core.elasticsearch.ElasticsearchSimilarityConfig

  * **pgvector** : a fiftyone.brain.internal.core.pgvector.PgVectorSimilarityConfig

  * **mosaic** : [`fiftyone.brain.internal.core.mosaic.MosaicSimilarityConfig`](api/fiftyone.brain.internal.core.mosaic.html#fiftyone.brain.internal.core.mosaic.MosaicSimilarityConfig "fiftyone.brain.internal.core.mosaic.MosaicSimilarityConfig")

  * **milvus** : [`fiftyone.brain.internal.core.milvus.MilvusSimilarityConfig`](api/fiftyone.brain.internal.core.milvus.html#fiftyone.brain.internal.core.milvus.MilvusSimilarityConfig "fiftyone.brain.internal.core.milvus.MilvusSimilarityConfig")

  * **lancedb** : [`fiftyone.brain.internal.core.lancedb.LanceDBSimilarityConfig`](api/fiftyone.brain.internal.core.lancedb.html#fiftyone.brain.internal.core.lancedb.LanceDBSimilarityConfig "fiftyone.brain.internal.core.lancedb.LanceDBSimilarityConfig")




You can configure a similarity backendâs parameters for a specific index by simply passing supported config parameters as keyword arguments each time you call [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity"):
    
    
    1index = fob.compute_similarity(
    2    ...
    3    backend="qdrant",
    4    url="http://localhost:6333",
    5)
    

Alternatively, you can more permanently configure your backend(s) via your brain config.

#### Creating an index#

The [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity") method provides a number of different syntaxes for initializing a similarity index. Letâs see some common patterns on the quickstart dataset:
    
    
    1import fiftyone as fo
    2import fiftyone.brain as fob
    3import fiftyone.zoo as foz
    4
    5dataset = foz.load_zoo_dataset("quickstart")
    

##### Default behavior#

With no arguments, embeddings will be automatically computed for all images or patches in the dataset using a default model and added to a new index in your default backend:

Image similarityObject similarity
    
    
    1tmp_index = fob.compute_similarity(dataset, brain_key="tmp")
    2
    3print(tmp_index.config.method)  # 'sklearn'
    4print(tmp_index.config.model)  # 'mobilenet-v2-imagenet-torch'
    5print(tmp_index.total_index_size)  # 200
    6
    7dataset.delete_brain_run("tmp")
    
    
    
     1tmp_index = fob.compute_similarity(
     2    dataset,
     3    patches_field="ground_truth",   # field containing objects of interest
     4    brain_key="tmp",
     5)
     6
     7print(tmp_index.config.method)  # 'sklearn'
     8print(tmp_index.config.model)  # 'mobilenet-v2-imagenet-torch'
     9print(tmp_index.total_index_size)  # 1232
    10
    11dataset.delete_brain_run("tmp")
    

##### Custom model, custom backend, add embeddings later#

With the syntax below, weâre specifying a similarity backend of our choice, specifying a custom model from the [Model Zoo](model_zoo/index.html#model-zoo) to use to generate embeddings, and using the `embeddings=False` syntax to create the index without initially adding any embeddings to it:

Image similarityObject similarity
    
    
    1image_index = fob.compute_similarity(
    2    dataset,
    3    model="clip-vit-base32-torch",  # custom model
    4    embeddings=False,               # add embeddings later
    5    backend="sklearn",              # custom backend
    6    brain_key="img_sim",
    7)
    8
    9print(image_index.total_index_size)  # 0
    
    
    
     1object_index = fob.compute_similarity(
     2    dataset,
     3    patches_field="ground_truth",   # field containing objects of interest
     4    model="clip-vit-base32-torch",  # custom model
     5    embeddings=False,               # add embeddings later
     6    backend="sklearn",              # custom backend
     7    brain_key="gt_sim",
     8)
     9
    10print(object_index.total_index_size)  # 0
    

##### Precomputed embeddings#

You can pass precomputed image or object embeddings to [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity") via the `embeddings` argument:

Image similarityObject similarity
    
    
     1model = foz.load_zoo_model("clip-vit-base32-torch")
     2embeddings = dataset.compute_embeddings(model)
     3
     4tmp_index = fob.compute_similarity(
     5    dataset,
     6    model="clip-vit-base32-torch",  # store model's name for future use
     7    embeddings=embeddings,          # precomputed image embeddings
     8    brain_key="tmp",
     9)
    10
    11print(tmp_index.total_index_size)  # 200
    12
    13dataset.delete_brain_run("tmp")
    
    
    
     1model = foz.load_zoo_model("clip-vit-base32-torch")
     2embeddings = dataset.compute_patch_embeddings(model, "ground_truth")
     3
     4tmp_index = fob.compute_similarity(
     5    dataset,
     6    patches_field="ground_truth",   # field containing objects of interest
     7    model="clip-vit-base32-torch",  # store model's name for future use
     8    embeddings=embeddings,          # precomputed patch embeddings
     9    brain_key="tmp",
    10)
    11
    12print(tmp_index.total_index_size)  # 1232
    13
    14dataset.delete_brain_run("tmp")
    

#### Adding embeddings to an index#

You can use [`add_to_index()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex.add_to_index "fiftyone.brain.similarity.SimilarityIndex.add_to_index") to add new embeddings or overwrite existing embeddings in an index at any time:

Image similarityObject similarity
    
    
     1image_index = dataset.load_brain_results("img_sim")
     2print(image_index.total_index_size)  # 0
     3
     4view1 = dataset[:100]
     5view2 = dataset[100:]
     6
     7#
     8# Approach 1: use the index to compute embeddings for `view1`
     9#
    10
    11embeddings, sample_ids, _ = image_index.compute_embeddings(view1)
    12image_index.add_to_index(embeddings, sample_ids)
    13print(image_index.total_index_size)  # 100
    14
    15#
    16# Approach 2: manually compute embeddings for `view2`
    17#
    18
    19model = image_index.get_model()  # the index's model
    20embeddings = view2.compute_embeddings(model)
    21sample_ids = view2.values("id")
    22image_index.add_to_index(embeddings, sample_ids)
    23print(image_index.total_index_size)  # 200
    24
    25# Must save after edits when using the sklearn backend
    26image_index.save()
    

When working with object embeddings, you must provide the sample ID and label ID for each embedding you add to the index:
    
    
     1import numpy as np
     2
     3object_index = dataset.load_brain_results("gt_sim")
     4print(object_index.total_index_size)  # 0
     5
     6view1 = dataset[:100]
     7view2 = dataset[100:]
     8
     9#
    10# Approach 1: use the index to compute embeddings for `view1`
    11#
    12
    13embeddings, sample_ids, label_ids = object_index.compute_embeddings(view1)
    14object_index.add_to_index(embeddings, sample_ids, label_ids=label_ids)
    15print(object_index.total_index_size)  # 471
    16
    17#
    18# Approach 2: manually compute embeddings for `view2`
    19#
    20
    21# Manually load the index's model
    22model = object_index.get_model()
    23
    24# Compute patch embeddings
    25_embeddings = view2.compute_patch_embeddings(model, "ground_truth")
    26_label_ids = dict(zip(*view2.values(["id", "ground_truth.detections.id"])))
    27
    28# Organize into correct format
    29embeddings = []
    30sample_ids = []
    31label_ids = []
    32for sample_id, patch_embeddings in _embeddings.items():
    33    patch_ids = _label_ids[sample_id]
    34    if not patch_ids:
    35        continue
    36
    37    for embedding, label_id in zip(patch_embeddings, patch_ids):
    38        embeddings.append(embedding)
    39        sample_ids.append(sample_id)
    40        label_ids.append(label_id)
    41
    42object_index.add_to_index(
    43    np.stack(embeddings),
    44    np.array(sample_ids),
    45    label_ids=np.array(label_ids),
    46)
    47print(object_index.total_index_size)  # 1232
    48
    49# Must save after edits when using the sklearn backend
    50object_index.save()
    

Note

When using the default `sklearn` backend, you must manually call [`save()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex.save "fiftyone.brain.similarity.SimilarityIndex.save") after adding or removing embeddings from an index in order to save the index to the database. This is not required when using external vector databases like [Qdrant](integrations/qdrant.html#qdrant-integration).

Note

Did you know? If you provided the name of a [zoo model](model_zoo/index.html#model-zoo) when creating the similarity index, you can use [`get_model()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex.get_model "fiftyone.brain.similarity.SimilarityIndex.get_model") to load the model later. Or, you can use [`compute_embeddings()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex.compute_embeddings "fiftyone.brain.similarity.SimilarityIndex.compute_embeddings") to conveniently generate embeddings for new samples/objects using the indexâs model.

#### Retrieving embeddings in an index#

You can use [`get_embeddings()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex.get_embeddings "fiftyone.brain.similarity.SimilarityIndex.get_embeddings") to retrieve the embeddings for any or all IDs of interest from an existing index:

Image similarityObject similarity
    
    
    1ids = dataset.take(50).values("id")
    2embeddings, sample_ids, _ = image_index.get_embeddings(sample_ids=ids)
    3
    4print(embeddings.shape)  # (50, 512)
    5print(sample_ids.shape)  # (50,)
    

When working with object embeddings, you can provide either sample IDs or label IDs for which you want to retrieve embeddings:
    
    
     1from fiftyone import ViewField as F
     2
     3ids = (
     4    dataset
     5    .filter_labels("ground_truth", F("label") == "person")
     6    .values("ground_truth.detections.id", unwind=True)
     7)
     8
     9embeddings, sample_ids, label_ids = object_index.get_embeddings(label_ids=ids)
    10
    11print(embeddings.shape)  # (378, 512)
    12print(sample_ids.shape)  # (378,)
    13print(label_ids.shape)  # (378,)
    

#### Removing embeddings from an index#

You can use [`remove_from_index()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex.remove_from_index "fiftyone.brain.similarity.SimilarityIndex.remove_from_index") to delete embeddings from an index by their ID:

Image similarityObject similarity
    
    
    1ids = dataset.take(50).values("id")
    2
    3image_index.remove_from_index(sample_ids=ids)
    4print(image_index.total_index_size)  # 150
    5
    6# Must save after edits when using the sklearn backend
    7image_index.save()
    

When working with object embeddings, you can provide either sample IDs or label IDs for which you want to delete embeddings:
    
    
     1from fiftyone import ViewField as F
     2
     3ids = (
     4    dataset
     5    .filter_labels("ground_truth", F("label") == "person")
     6    .values("ground_truth.detections.id", unwind=True)
     7)
     8
     9object_index.remove_from_index(label_ids=ids)
    10print(object_index.total_index_size)  # 854
    11
    12# Must save after edits when using the sklearn backend
    13object_index.save()
    

Note

When using the default `sklearn` backend, you must manually call [`save()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex.save "fiftyone.brain.similarity.SimilarityIndex.save") after adding or removing embeddings from an index in order to save the index to the database.

This is not required when using external vector databases like [Qdrant](integrations/qdrant.html#qdrant-integration).

#### Deleting an index#

When working with backends like [Qdrant](integrations/qdrant.html#qdrant-integration) that leverage external vector databases, you can call [`cleanup()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex.cleanup "fiftyone.brain.similarity.SimilarityIndex.cleanup") to delete the external index/collection:

Image similarityObject similarity
    
    
    1# First delete the index from the backend (if applicable)
    2image_index.cleanup()
    3
    4# Now delete the index from your dataset
    5dataset.delete_brain_run("img_sim")
    
    
    
    1# First delete the index from the backend (if applicable)
    2object_index.cleanup()
    3
    4# Now delete the index from your dataset
    5dataset.delete_brain_run("gt_sim")
    

Note

Calling [`cleanup()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex.cleanup "fiftyone.brain.similarity.SimilarityIndex.cleanup") has no effect when working with the default sklearn backend. The index is deleted only when you call [`delete_brain_run()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.delete_brain_run "fiftyone.core.collections.SampleCollection.delete_brain_run").

### Applications#

How can similarity be used in practice? A common pattern is to mine your dataset for similar examples to certain images or object patches of interest, e.g., those that represent failure modes of a model that need to be studied in more detail or underrepresented classes that need more training examples.

Here are a few of the many possible applications:

  * Pruning near-duplicate images from your training dataset

  * Identifying failure patterns of a model

  * Finding examples of target scenarios in your data lake

  * Mining hard examples for your evaluation pipeline

  * Recommending samples from your data lake for classes that need additional training data




## Leaky splits#

Despite our best efforts, duplicates and other forms of non-IID samples show up in our data. When these samples end up in different splits, this can have consequences when evaluating a model. It can often be easy to overestimate model capability due to this issue. The FiftyOne Brain offers a way to identify such cases in dataset splits.

The leaks of a dataset can be computed directly without the need for the predictions of a pre-trained model via the [`compute_leaky_splits()`](api/fiftyone.brain.html#fiftyone.brain.compute_leaky_splits "fiftyone.brain.compute_leaky_splits") method:
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3
     4dataset = fo.load_dataset(...)
     5
     6# Splits defined via tags
     7split_tags = ["train", "test"]
     8index = fob.compute_leaky_splits(dataset, splits=split_tags)
     9leaks = index.leaks_view()
    10
    11# Splits defined via field
    12split_field = "split"  # holds split values e.g. 'train' or 'test'
    13index = fob.compute_leaky_splits(dataset, splits=split_field)
    14leaks = index.leaks_view()
    15
    16# Splits defined via views
    17split_views = {"train": train_view, "test": test_view}
    18index = fob.compute_leaky_splits(dataset, splits=split_views)
    19leaks = index.leaks_view()
    

Notice how the splits of the dataset can be defined in three ways: through sample tags, through a string field that assigns each split a unique value in the field, or by directly providing views that define the splits.

**Input** : A [`Dataset`](api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") or [`DatasetView`](api/fiftyone.core.view.html#fiftyone.core.view.DatasetView "fiftyone.core.view.DatasetView"), and a definition of splits through one of tags, a field, or views.

**Output** : An index that will allow you to look through your leaks with [`leaks_view()`](api/fiftyone.brain.internal.core.leaky_splits.html#fiftyone.brain.internal.core.leaky_splits.LeakySplitsIndex.leaks_view "fiftyone.brain.internal.core.leaky_splits.LeakySplitsIndex.leaks_view") and also provides some useful actions once they are discovered such as automatically cleaning the dataset with [`no_leaks_view()`](api/fiftyone.brain.internal.core.leaky_splits.html#fiftyone.brain.internal.core.leaky_splits.LeakySplitsIndex.no_leaks_view "fiftyone.brain.internal.core.leaky_splits.LeakySplitsIndex.no_leaks_view") or tagging the leaks for the future action with [`tag_leaks()`](api/fiftyone.brain.internal.core.leaky_splits.html#fiftyone.brain.internal.core.leaky_splits.LeakySplitsIndex.tag_leaks "fiftyone.brain.internal.core.leaky_splits.LeakySplitsIndex.tag_leaks").

**What to expect** : Leaky splits works by embedding samples with a powerful model and finding very close samples in different splits in this space. Large, powerful models that were _not_ trained on a dataset can provide insight into visual and semantic similarity between images, without creating further leaks in the process.

**Similarity index** : Under the hood, leaky splits leverages the brainâs [`SimilarityIndex`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex "fiftyone.brain.similarity.SimilarityIndex") to detect leaks. Any similarity backend that implements the [`DuplicatesMixin`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.DuplicatesMixin "fiftyone.brain.similarity.DuplicatesMixin") can be used to compute leaky splits. You can either pass an existing similarity index by passing its brain key to the argument `similarity_index`, or have the method create one on the fly for you.

**Embeddings** : You can customize the model used to compute embeddings via the `model` argument of [`compute_leaky_splits()`](api/fiftyone.brain.html#fiftyone.brain.compute_leaky_splits "fiftyone.brain.compute_leaky_splits"). You can also precompute embeddings and tell leaky splits to use them by passing them via the `embeddings` argument.

**Thresholds** : Leaky splits uses a threshold to decide what samples are too close and thus mark them as potential leaks. This threshold can be customized either by passing a value to the `threshold` argument of [`compute_leaky_splits()`](api/fiftyone.brain.html#fiftyone.brain.compute_leaky_splits "fiftyone.brain.compute_leaky_splits"). The best value for your use case may vary depending on your dataset, as well as the embeddings used. A threshold thatâs too big may have a lot of false positives, while a threshold thatâs too small may have a lot of false negatives.

The example code below runs leaky splits analysis on the [COCO dataset](https://cocodataset.org/#home). Try it for yourself and see what you find!
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3import fiftyone.zoo as foz
     4import fiftyone.utils.random as four
     5
     6# Load some COCO data
     7dataset = foz.load_zoo_dataset("coco-2017", split="test")
     8
     9# Set up splits via tags
    10dataset.untag_samples(dataset.distinct("tags"))
    11four.random_split(dataset, {"train": 0.7, "test": 0.3})
    12
    13# Find leaks
    14index = fob.compute_leaky_splits(dataset, splits=["train", "test"])
    15leaks = index.leaks_view()
    

The [`leaks_view()`](api/fiftyone.brain.internal.core.leaky_splits.html#fiftyone.brain.internal.core.leaky_splits.LeakySplitsIndex.leaks_view "fiftyone.brain.internal.core.leaky_splits.LeakySplitsIndex.leaks_view") method returns a view that contains only the leaks in the input splits. Once you have these leaks, it is wise to look through them. You may gain some insight into the source of the leaks:
    
    
    1session = fo.launch_app(leaks)
    

Before evaluating your model on your test set, consider getting a version of it with the leaks removed. This can be easily done via [`no_leaks_view()`](api/fiftyone.brain.internal.core.leaky_splits.html#fiftyone.brain.internal.core.leaky_splits.LeakySplitsIndex.no_leaks_view "fiftyone.brain.internal.core.leaky_splits.LeakySplitsIndex.no_leaks_view"):
    
    
    1# The original test split
    2test_set = index.split_views["test"]
    3
    4# The test set with leaks removed
    5test_set_no_leaks = index.no_leaks_view(test_set)
    6
    7session.view = test_set_no_leaks
    

Performance on the clean test set will can be closer to the performance of the model in the wild. If you found some leaks in your dataset, consider comparing performance on the base test set against the clean test set.

## Near duplicates#

When curating massive datasets, you may inadvertently add near duplicate data to your datasets, which can bias or otherwise confuse your models.

The [`compute_near_duplicates()`](api/fiftyone.brain.html#fiftyone.brain.compute_near_duplicates "fiftyone.brain.compute_near_duplicates") method leverages embeddings to automatically surface near-duplicate samples in your dataset:
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3
     4dataset = fo.load_dataset(...)
     5
     6index = fob.compute_near_duplicates(dataset)
     7print(index.duplicate_ids)
     8
     9dups_view = index.duplicates_view()
    10session = fo.launch_app(dups_view)
    

**Input** : An unlabeled (or labeled) dataset. There are [recipes](recipes/index.html#recipes) for building datasets from a wide variety of image formats, ranging from a simple directory of images to complicated dataset structures like [COCO](https://cocodataset.org/#home).

**Output** : A [`SimilarityIndex`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.SimilarityIndex "fiftyone.brain.similarity.SimilarityIndex") object that provides powerful methods such as [`duplicate_ids`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.DuplicatesMixin.duplicate_ids "fiftyone.brain.similarity.DuplicatesMixin.duplicate_ids"), [`neighbors_map`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.DuplicatesMixin.neighbors_map "fiftyone.brain.similarity.DuplicatesMixin.neighbors_map") and [`duplicates_view()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.DuplicatesMixin.duplicates_view "fiftyone.brain.similarity.DuplicatesMixin.duplicates_view") to analyze potential near duplicates as demonstrated below

**What to expect** : Near duplicates analysis leverages embeddings to identify samples that are too close to their nearest neighbors. You can provide pre-computed embeddings, specify a [zoo model](model_zoo/index.html#model-zoo) of your choice to use to compute embeddings, or provide nothing and rely on the methodâs default model to generate embeddings.

**Thresholds** : When using custom embeddings/models, you may need to adjust the distance threshold used to detect potential duplicates. You can do this by passing a value to the `threshold` argument of [`compute_near_duplicates()`](api/fiftyone.brain.html#fiftyone.brain.compute_near_duplicates "fiftyone.brain.compute_near_duplicates"). The best value for your use case may vary depending on your dataset, as well as the embeddings used. A threshold thatâs too big may have a lot of false positives, while a threshold thatâs too small may have a lot of false negatives.

The following example demonstrates how to use [`compute_near_duplicates()`](api/fiftyone.brain.html#fiftyone.brain.compute_near_duplicates "fiftyone.brain.compute_near_duplicates") to detect near duplicate images on the [CIFAR-10 dataset](dataset_zoo/datasets/cifar10.html#dataset-zoo-cifar10):
    
    
    1import fiftyone as fo
    2import fiftyone.zoo as foz
    3
    4dataset = foz.load_zoo_dataset("cifar10", split="test")
    

To proceed, we first need some suitable image embeddings for the dataset. Although the [`compute_near_duplicates()`](api/fiftyone.brain.html#fiftyone.brain.compute_near_duplicates "fiftyone.brain.compute_near_duplicates") method is equipped with a default general-purpose model to generate embeddings if none are provided, youâll typically find higher-quality insights when a domain-specific model is used to generate embeddings.

In this case, weâll use a classifier that has been fine-tuned on CIFAR-10 to pre-compute embeddings and them feed them to [`compute_near_duplicates()`](api/fiftyone.brain.html#fiftyone.brain.compute_near_duplicates "fiftyone.brain.compute_near_duplicates"):
    
    
     1import fiftyone.brain as fob
     2import fiftyone.brain.internal.models as fbm
     3
     4# Compute embeddings via a pre-trained CIFAR-10 classifier
     5model = fbm.load_model("simple-resnet-cifar10")
     6embeddings = dataset.compute_embeddings(model, batch_size=16)
     7
     8# Scan for near-duplicates
     9index = fob.compute_near_duplicates(
    10    dataset,
    11    embeddings=embeddings,
    12    thresh=0.02,
    13)
    

### Finding near-duplicate samples#

The [`neighbors_map`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.DuplicatesMixin.neighbors_map "fiftyone.brain.similarity.DuplicatesMixin.neighbors_map") property of the index provides a data structure that summarizes the findings. The keys of the dictionary are the sample IDs of each non-duplicate sample, and the values are lists of `(id, distance)` tuples listing the sample IDs of the duplicate samples for each reference sample together with the embedding distance between the two samples:
    
    
    1print(index.neighbors_map)
    
    
    
    {
        '61143408db40df926c571a6b': [
            ('61143409db40df926c573075', 5.667297674385298),
            ('61143408db40df926c572ab6', 6.231051661334058)
        ],
        '6114340cdb40df926c577f2a': [
            ('61143408db40df926c572b54', 6.042934361555487)
        ],
        '61143408db40df926c572aa3': [
            ('6114340bdb40df926c5772e9', 5.88984758067434),
            ('61143408db40df926c572b64', 6.063986454046798),
            ('61143409db40df926c574571', 6.10303338363576),
            ('6114340adb40df926c5749a2', 6.161749290179865)
        ],
        ...
    }
    

We can conveniently visualize this information in the App via the [`duplicates_view()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.DuplicatesMixin.duplicates_view "fiftyone.brain.similarity.DuplicatesMixin.duplicates_view") method of the index, which constructs a view with the duplicate samples arranged directly after their corresponding reference sample, with optional additional fields recording the type and nearest reference sample ID/distance:
    
    
    1duplicates_view = index.duplicates_view(
    2    type_field="dup_type",
    3    id_field="dup_id",
    4    dist_field="dup_dist",
    5)
    6
    7session = fo.launch_app(duplicates_view)
    

Note

You can also use the [`find_duplicates()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.DuplicatesMixin.find_duplicates "fiftyone.brain.similarity.DuplicatesMixin.find_duplicates") method of the index to rerun the duplicate detection with a different `threshold` without calling [`compute_near_duplicates()`](api/fiftyone.brain.html#fiftyone.brain.compute_near_duplicates "fiftyone.brain.compute_near_duplicates") again.

### Finding maximally unique samples#

You can also use the [`find_unique()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.DuplicatesMixin.find_unique "fiftyone.brain.similarity.DuplicatesMixin.find_unique") method of the index to identify a set of samples of any desired size that are maximally unique with respect to each other:
    
    
    1# Use the similarity index to identify 500 maximally unique samples
    2index.find_unique(500)
    3print(index.unique_ids[:5])
    

We can also conveniently visualize the results of this operation via the [`visualize_unique()`](api/fiftyone.brain.similarity.html#fiftyone.brain.similarity.DuplicatesMixin.visualize_unique "fiftyone.brain.similarity.DuplicatesMixin.visualize_unique") method of the index, which generates a scatterplot with the unique samples colored separately:
    
    
    1# Generate a 2D visualization
    2viz_results = fob.compute_visualization(dataset, embeddings=embeddings)
    3
    4# Visualize the unique samples in embeddings space
    5plot = index.visualize_unique(viz_results)
    6plot.show(height=800, yaxis_scaleanchor="x")
    

And of course we can load a view containing the unique samples in the App to explore the results in detail:
    
    
    1# Visualize the unique images in the App
    2unique_view = dataset.select(index.unique_ids)
    3session = fo.launch_app(view=unique_view)
    

## Exact duplicates#

Despite your best efforts, you may accidentally add duplicate data to a dataset. Left unmitigated, such quality issues can bias your models and confound your analysis.

The [`compute_exact_duplicates()`](api/fiftyone.brain.html#fiftyone.brain.compute_exact_duplicates "fiftyone.brain.compute_exact_duplicates") method scans your dataset and determines if you have duplicate data either under the same or different filenames:
    
    
    1import fiftyone as fo
    2import fiftyone.brain as fob
    3
    4dataset = fo.load_dataset(...)
    5
    6duplicates_map = fob.compute_exact_duplicates(dataset)
    7print(duplicates_map)
    

**Input** : An unlabeled (or labeled) dataset. There are [recipes](recipes/index.html#recipes) for building datasets from a wide variety of image formats, ranging from a simple directory of images to complicated dataset structures like [COCO](https://cocodataset.org/#home).

**Output** : A dictionary mapping IDs of samples with exact duplicates to lists of IDs of the duplicates for the corresponding sample

**What to expect** : Exact duplicates analysis uses filehashes to identify duplicate data, regardless of whether they are stored under the same or different filepaths in your dataset.

## Image uniqueness#

The FiftyOne Brain allows for the computation of the uniqueness of an image, in comparison with other images in a dataset; it does so without requiring any model from you. One good use of uniqueness is in the early stages of the machine learning workflow when you are deciding what subset of data with which to bootstrap your models. Unique samples are vital in creating training batches that help your model learn as efficiently and effectively as possible.

The uniqueness of a [`Dataset`](api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") can be computed directly without need the predictions of a pre-trained model via the [`compute_uniqueness()`](api/fiftyone.brain.html#fiftyone.brain.compute_uniqueness "fiftyone.brain.compute_uniqueness") method:
    
    
    1import fiftyone as fo
    2import fiftyone.brain as fob
    3
    4dataset = fo.load_dataset(...)
    5
    6fob.compute_uniqueness(dataset)
    

**Input** : An unlabeled (or labeled) image dataset. There are [recipes](recipes/index.html#recipes) for building datasets from a wide variety of image formats, ranging from a simple directory of images to complicated dataset structures like [COCO](https://cocodataset.org/#home).

Note

Did you know? Instead of using FiftyOneâs default model to generate embeddings, you can provide your own embeddings or specify a model from the [Model Zoo](model_zoo/index.html#model-zoo) to use to generate embeddings via the optional `embeddings` and `model` argument to [`compute_uniqueness()`](api/fiftyone.brain.html#fiftyone.brain.compute_uniqueness "fiftyone.brain.compute_uniqueness").

**Output** : A scalar-valued `uniqueness` field is populated on each sample that ranks the uniqueness of that sample (higher value means more unique). The uniqueness values for a dataset are normalized to `[0, 1]`, with the most unique sample in the collection having a uniqueness value of `1`.

You can customize the name of this field by passing the optional `uniqueness_field` argument to [`compute_uniqueness()`](api/fiftyone.brain.html#fiftyone.brain.compute_uniqueness "fiftyone.brain.compute_uniqueness").

**What to expect** : Uniqueness uses a tuned algorithm that measures the distribution of each [`Sample`](api/fiftyone.utils.data.html#fiftyone.utils.data.Sample "fiftyone.core.sample.Sample") in the [`Dataset`](api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset"). Using this distribution, it ranks each sample based on its relative _similarity_ to other samples. Those that are close to other samples are not unique whereas those that are far from most other samples are more unique.

Note

Did you know? You can specify a region of interest within each image to use to compute uniqueness by providing the optional `roi_field` argument to [`compute_uniqueness()`](api/fiftyone.brain.html#fiftyone.brain.compute_uniqueness "fiftyone.brain.compute_uniqueness"), which contains [`Detections`](api/fiftyone.core.labels.html#fiftyone.core.labels.Detections "fiftyone.core.labels.Detections") or [`Polylines`](api/fiftyone.core.labels.html#fiftyone.core.labels.Polylines "fiftyone.core.labels.Polylines") that define the ROI for each sample.

Note

Check out the [uniqueness tutorial](tutorials/uniqueness.html) to see an example use case of the Brainâs uniqueness method to detect near-duplicate images in a dataset.

## Label mistakes#

Label mistakes can be calculated for both classification and detection datasets.

ClassificationDetection

Correct annotations are crucial in developing high performing models. Using the FiftyOne Brain and the predictions of a pre-trained model, you can identify possible labels mistakes in [`Classification`](api/fiftyone.core.labels.html#fiftyone.core.labels.Classification "fiftyone.core.labels.Classification") fields of your dataset via the [`compute_mistakenness()`](api/fiftyone.brain.html#fiftyone.brain.compute_mistakenness "fiftyone.brain.compute_mistakenness") method:
    
    
    1import fiftyone as fo
    2import fiftyone.brain as fob
    3
    4dataset = fo.load_dataset(...)
    5
    6fob.compute_mistakenness(
    7    dataset, "predictions", label_field="ground_truth"
    8)
    

**Input** : Label mistakes operate on samples for which there are both human annotations (`"ground_truth"` above) and model predictions (`"predictions"` above).

**Output** : A float `mistakenness` field is populated on each sample that ranks the chance that the human annotation is mistaken. You can customize the name of this field by passing the optional `mistakenness_field` argument to [`compute_mistakenness()`](api/fiftyone.brain.html#fiftyone.brain.compute_mistakenness "fiftyone.brain.compute_mistakenness").

**What to expect** : Finding mistakes in human annotations is non-trivial (if it could be done perfectly then the approach would sufficiently replace your prediction model!) The FiftyOne Brain uses a proprietary scoring model that ranks samples for which your prediction model is highly confident but wrong (according to the human annotation label) as a high chance of being a mistake.

Note

Check out the [label mistakes tutorial](tutorials/classification_mistakes.html) to see an example use case of the Brainâs mistakenness method on a classification dataset.

Correct annotations are crucial in developing high performing models. Using the FiftyOne Brain and the predictions of a pre-trained model, you can identify possible labels mistakes in [`Detections`](api/fiftyone.core.labels.html#fiftyone.core.labels.Detections "fiftyone.core.labels.Detections") fields of your dataset via the [`compute_mistakenness()`](api/fiftyone.brain.html#fiftyone.brain.compute_mistakenness "fiftyone.brain.compute_mistakenness") method:
    
    
    1import fiftyone as fo
    2import fiftyone.brain as fob
    3
    4dataset = fo.load_dataset(...)
    5
    6fob.compute_mistakenness(
    7    dataset, "predictions", label_field="ground_truth"
    8)
    

**Input** : You can compute label mistakes on samples for which there are both human annotations (`"ground_truth"` above) and model predictions (`"predictions"` above).

**Output** : New fields on both the detections in `label_field` and the samples will be populated:

Detection-level fields:

  * `mistakenness` (float): Objects in `label_field` that matched with a prediction have their `mistakenness` field populated with a measure of the likelihood that the ground truth annotation is a mistake.

  * `mistakenness_loc` (float): Objects in `label_field` that matched with a prediction have their `mistakenness_loc` field populated with a measure of the mistakenness in the localization (bounding box) of the ground truth annotation.

  * `possible_missing` (bool): If there are predicted objects with no matches in `label_field` but which are deemed to be likely correct annotations, these objects will have their `possible_missing` attribute set to True. In addition, if you pass the optional `copy_missing=True` flag to [`compute_mistakenness()`](api/fiftyone.brain.html#fiftyone.brain.compute_mistakenness "fiftyone.brain.compute_mistakenness"), then these objects will be copied into `label_field`.

  * `possible_spurious` (bool): Objects in `label_field` that were not matched with a prediction and deemed to be likely spurious annotations will have their `possible_spurious` field set to True.




Sample-level fields:

  * `mistakenness` (float): The maximum mistakenness of an object in the `label_field` of the sample.

  * `possible_missing` (int): The number of objects that were added to the `label_field` of the sample and marked as likely missing annotations.

  * `possible_spurious` (int): The number of objects in the `label_field` of the sample that were deemed to be likely spurious annotations.




You can customize the names of these fields by passing optional arguments to [`compute_mistakenness()`](api/fiftyone.brain.html#fiftyone.brain.compute_mistakenness "fiftyone.brain.compute_mistakenness").

**What to expect** : Finding mistakes in human annotations is non-trivial (if it could be done perfectly then the approach would sufficiently replace your prediction model!) The FiftyOne Brain uses a proprietary scoring model that ranks detections for which your prediction model is highly confident but wrong (according to the human annotation label) as a high chance of being a mistake.

Note

Check out the [detection mistakes tutorials](tutorials/detection_mistakes.html) to see an example use case of the Brainâs mistakenness method on a detection dataset.

## Sample hardness#

During training, it is useful to identify samples that are more difficult for a model to learn so that training can be more focused around these hard samples. These hard samples are also useful as seeds when considering what other new samples to add to a training dataset.

In order to compute hardness, all you need to do is add your model predictions and their logits to your FiftyOne [`Dataset`](api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") and then run the [`compute_hardness()`](api/fiftyone.brain.html#fiftyone.brain.compute_hardness "fiftyone.brain.compute_hardness") method:
    
    
    1import fiftyone as fo
    2import fiftyone.brain as fob
    3
    4dataset = fo.load_dataset(...)
    5
    6fob.compute_hardness(dataset, "predictions")
    

**Input** : A [`Dataset`](api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") or [`DatasetView`](api/fiftyone.core.view.html#fiftyone.core.view.DatasetView "fiftyone.core.view.DatasetView") on which predictions have been computed and are stored in the `"predictions"` argument. Ground truth annotations are not required for hardness.

**Output** : A scalar-valued `hardness` field is populated on each sample that ranks the hardness of the sample. You can customize the name of this field via the `hardness_field` argument of [`compute_hardness()`](api/fiftyone.brain.html#fiftyone.brain.compute_hardness "fiftyone.brain.compute_hardness").

**What to expect** : Hardness is computed in the context of a prediction model. The FiftyOne Brain hardness measure defines hard samples as those for which the prediction model is unsure about what label to assign. This measure incorporates prediction confidence and logits in a tuned model that has demonstrated empirical value in many model training exercises.

Note

Check out the [classification evaluation tutorial](tutorials/evaluate_classifications.html) to see example uses of the Brainâs hardness method to uncover annotation mistakes in a dataset.

## Image representativeness#

During the early stages of the ML workflow it can be useful to find prototypical samples in your data that accurately describe all the different aspects of your data. FiftyOne Brain provides a representativeness method that finds samples which are very similar to large clusters of your data. Highly representative samples are great for finding modes or easy examples in your dataset.

The representativeness of a [`Dataset`](api/fiftyone.core.dataset.html#fiftyone.core.dataset.Dataset "fiftyone.core.dataset.Dataset") can be computed directly without the need for the predictions of a pre-trained model via the [`compute_representativeness()`](api/fiftyone.brain.html#fiftyone.brain.compute_representativeness "fiftyone.brain.compute_representativeness") method:
    
    
    1import fiftyone as fo
    2import fiftyone.brain as fob
    3
    4dataset = fo.load_dataset(...)
    5
    6fob.compute_representativeness(dataset)
    

**Input** : An unlabeled (or labeled) image dataset. There are [recipes](recipes/index.html#recipes) for building datasets from a wide variety of image formats, ranging from a simple directory of images to complicated dataset structures like [COCO](https://cocodataset.org/#home).

**Output** : A scalar-valued `representativeness` field is populated for each sample that ranks the representativeness of that sample (higher value means more representative). The representativeness values for a dataset are normalized to `[0, 1]`, with the most representative samples in the collection having a representativeness value of `1`.

You can customize the name of this field by passing the optional `representativeness_field` argument to [`compute_representativeness()`](api/fiftyone.brain.html#fiftyone.brain.compute_representativeness "fiftyone.brain.compute_representativeness") .

**What to expect** : Representativeness uses a clustering algorithm to find similar looking groups of samples. The representativeness is then computed based on each sampleâs proximity to the computed cluster centers, farther samples being less representative and closer samples being more representative.

Note

Did you know? You can specify a region of interest within each image to use to compute representativeness by providing the optional `roi_field` argument to [`compute_representativeness()`](api/fiftyone.brain.html#fiftyone.brain.compute_representativeness "fiftyone.brain.compute_representativeness"), which contains [`Detections`](api/fiftyone.core.labels.html#fiftyone.core.labels.Detections "fiftyone.core.labels.Detections") or [`Polylines`](api/fiftyone.core.labels.html#fiftyone.core.labels.Polylines "fiftyone.core.labels.Polylines") that define the ROI for each sample.

## Managing brain runs#

When you run a brain method with a `brain_key` argument, the run is recorded on the dataset and you can retrieve information about it later, rename it, delete it (along with any modifications to your dataset that were performed by it), and even retrieve the view that you computed on using the following methods on your dataset:

  * [`list_brain_runs()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.list_brain_runs "fiftyone.core.collections.SampleCollection.list_brain_runs")

  * [`get_brain_info()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.get_brain_info "fiftyone.core.collections.SampleCollection.get_brain_info")

  * [`load_brain_results()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.load_brain_results "fiftyone.core.collections.SampleCollection.load_brain_results")

  * [`load_brain_view()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.load_brain_view "fiftyone.core.collections.SampleCollection.load_brain_view")

  * [`rename_brain_run()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.rename_brain_run "fiftyone.core.collections.SampleCollection.rename_brain_run")

  * [`delete_brain_run()`](api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.delete_brain_run "fiftyone.core.collections.SampleCollection.delete_brain_run")




VisualizationsSimilarityUniquenessMistakennessHardnessRepresentativeness

The [`compute_visualization()`](api/fiftyone.brain.html#fiftyone.brain.compute_visualization "fiftyone.brain.compute_visualization") method accepts an optional `brain_key` parameter that specifies the brain key under which to store the results of the visualization.

The [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity") method accepts an optional `brain_key` parameter that specifies the brain key under which to store the similarity index.

The brain key of uniqueness runs is the value of the `uniqueness_field` passed to [`compute_uniqueness()`](api/fiftyone.brain.html#fiftyone.brain.compute_uniqueness "fiftyone.brain.compute_uniqueness").

The brain key of mistakenness runs is the value of the `mistakenness_field` passed to [`compute_mistakenness()`](api/fiftyone.brain.html#fiftyone.brain.compute_mistakenness "fiftyone.brain.compute_mistakenness").

The brain key of hardness runs is the value of the `hardness_field` passed to [`compute_hardness()`](api/fiftyone.brain.html#fiftyone.brain.compute_hardness "fiftyone.brain.compute_hardness").

The brain key of representativeness runs is the value of the `representativeness_field` passed to [`compute_representativeness()`](api/fiftyone.brain.html#fiftyone.brain.compute_representativeness "fiftyone.brain.compute_representativeness").

The example below demonstrates the basic interface:
    
    
     1import fiftyone as fo
     2import fiftyone.brain as fob
     3import fiftyone.zoo as foz
     4
     5dataset = foz.load_zoo_dataset("quickstart")
     6
     7view = dataset.take(100)
     8
     9# Run a brain method that returns results
    10results = fob.compute_visualization(view, brain_key="visualization")
    11
    12# Run a brain method that populates a new sample field on the dataset
    13fob.compute_uniqueness(view)
    14
    15# List the brain methods that have been run
    16print(dataset.list_brain_runs())
    17# ['visualization', 'uniqueness']
    18
    19# Print information about a brain run
    20print(dataset.get_brain_info("visualization"))
    21
    22# Load the results of a previous brain run
    23also_results = dataset.load_brain_results("visualization")
    24
    25# Load the view on which a brain run was performed
    26same_view = dataset.load_brain_view("visualization")
    27
    28# Rename a brain run
    29dataset.rename_brain_run("visualization", "still_visualization")
    30
    31# Delete brain runs
    32# This will delete any stored results and fields that were populated
    33dataset.delete_brain_run("still_visualization")
    34dataset.delete_brain_run("uniqueness")
    

## Brain config#

FiftyOne provides a brain config that you can use to either temporarily or permanently configure the behavior of brain methods.

### Viewing your config#

You can print your current brain config at any time via the Python library and the CLI:

PythonCLI
    
    
    import fiftyone.brain as fob
    
    # Print your current brain config
    print(fob.brain_config)
    
    
    
    {
        "default_similarity_backend": "sklearn",
        "similarity_backends": {
            "milvus": {
                "config_cls": "fiftyone.brain.internal.core.milvus.MilvusSimilarityConfig"
            },
            "pinecone": {
                "config_cls": "fiftyone.brain.internal.core.pinecone.PineconeSimilarityConfig"
            },
            "qdrant": {
                "config_cls": "fiftyone.brain.internal.core.qdrant.QdrantSimilarityConfig"
            },
            "redis": {
                "config_cls": "fiftyone.brain.internal.core.redis.RedisSimilarityConfig"
            },
            "sklearn": {
                "config_cls": "fiftyone.brain.internal.core.sklearn.SklearnSimilarityConfig"
            },
            "mongodb": {
                "config_cls": "fiftyone.brain.internal.core.mongodb.MongoDBSimilarityConfig"
            },
            "elasticsearch": {
                "config_cls": "fiftyone.brain.internal.core.elasticsearch.ElasticsearchSimilarityConfig"
            },
            "pgvector": {
                "config_cls": "fiftyone.brain.internal.core.pgvector.PgVectorSimilarityConfig"
            },
            "mosaic": {
                "config_cls": "fiftyone.brain.internal.core.mosaic.MosaicSimilarityConfig"
            },
            "lancedb": {
                "config_cls": "fiftyone.brain.internal.core.lancedb.LanceDBSimilarityConfig"
            }
        },
        "default_visualization_method": "umap",
        "visualization_methods": {
            "umap": {
                "config_cls": "fiftyone.brain.visualization.UMAPVisualizationConfig"
            },
            "tsne": {
                "config_cls": "fiftyone.brain.visualization.TSNEVisualizationConfig"
            },
            "pca": {
                "config_cls": "fiftyone.brain.visualization.PCAVisualizationConfig"
            },
            "manual": {
                "config_cls": "fiftyone.brain.visualization.ManualVisualizationConfig"
            }
        }
    }
    
    
    
    # Print your current brain config
    fiftyone brain config
    
    
    
    {
        "default_similarity_backend": "sklearn",
        "similarity_backends": {
            "milvus": {
                "config_cls": "fiftyone.brain.internal.core.milvus.MilvusSimilarityConfig"
            },
            "pinecone": {
                "config_cls": "fiftyone.brain.internal.core.pinecone.PineconeSimilarityConfig"
            },
            "qdrant": {
                "config_cls": "fiftyone.brain.internal.core.qdrant.QdrantSimilarityConfig"
            },
            "redis": {
                "config_cls": "fiftyone.brain.internal.core.redis.RedisSimilarityConfig"
            },
            "sklearn": {
                "config_cls": "fiftyone.brain.internal.core.sklearn.SklearnSimilarityConfig"
            },
            "mongodb": {
                "config_cls": "fiftyone.brain.internal.core.mongodb.MongoDBSimilarityConfig"
            },
            "elasticsearch": {
                "config_cls": "fiftyone.brain.internal.core.elasticsearch.ElasticsearchSimilarityConfig"
            },
            "lancedb": {
                "config_cls": "fiftyone.brain.internal.core.lancedb.LanceDBSimilarityConfig"
            }
        },
        "default_visualization_method": "umap",
        "visualization_methods": {
            "umap": {
                "config_cls": "fiftyone.brain.visualization.UMAPVisualizationConfig"
            },
            "tsne": {
                "config_cls": "fiftyone.brain.visualization.TSNEVisualizationConfig"
            },
            "pca": {
                "config_cls": "fiftyone.brain.visualization.PCAVisualizationConfig"
            },
            "manual": {
                "config_cls": "fiftyone.brain.visualization.ManualVisualizationConfig"
            }
        }
    }
    

Note

If you have customized your brain config via any of the methods described below, printing your config is a convenient way to ensure that the changes you made have taken effect as you expected.

### Modifying your config#

You can modify your brain config in a variety of ways. The following sections describe these options in detail.

#### Order of precedence#

The following order of precedence is used to assign values to your brain config settings as runtime:

  1. Config settings applied at runtime by directly editing `fiftyone.brain.brain_config`

  2. `FIFTYONE_BRAIN_XXX` environment variables

  3. Settings in your JSON config (`~/.fiftyone/brain_config.json`)

  4. The default config values




#### Editing your JSON config#

You can permanently customize your brain config by creating a `~/.fiftyone/brain_config.json` file on your machine. The JSON file may contain any desired subset of config fields that you wish to customize.

For example, the following config JSON file customizes the URL of your [Qdrant server](integrations/qdrant.html#qdrant-integration) without changing any other default config settings:
    
    
    {
        "similarity_backends": {
            "qdrant": {
                "url": "http://localhost:8080"
            }
        }
    }
    

When `fiftyone.brain` is imported, any options from your JSON config are merged into the default config, as per the order of precedence described above.

Note

You can customize the location from which your JSON config is read by setting the `FIFTYONE_BRAIN_CONFIG_PATH` environment variable.

#### Setting environment variables#

Brain config settings may be customized on a per-session basis by setting the `FIFTYONE_BRAIN_XXX` environment variable(s) for the desired config settings.

The `FIFTYONE_BRAIN_DEFAULT_SIMILARITY_BACKEND` environment variable allows you to configure your default similarity backend:
    
    
    export FIFTYONE_BRAIN_DEFAULT_SIMILARITY_BACKEND=qdrant
    

**Similarity backends**

You can declare parameters for specific similarity backends by setting environment variables of the form `FIFTYONE_BRAIN_SIMILARITY_<BACKEND>_<PARAMETER>`. Any settings that you declare in this way will be passed as keyword arguments to methods like [`compute_similarity()`](api/fiftyone.brain.html#fiftyone.brain.compute_similarity "fiftyone.brain.compute_similarity") whenever the corresponding backend is in use. For example, you can configure the URL of your [Qdrant server](integrations/qdrant.html#qdrant-integration) as follows:
    
    
    export FIFTYONE_BRAIN_SIMILARITY_QDRANT_URL=http://localhost:8080
    

The `FIFTYONE_BRAIN_SIMILARITY_BACKENDS` environment variable can be set to a `list,of,backends` that you want to expose in your session, which may exclude native backends and/or declare additional custom backends whose parameters are defined via additional config modifications of any kind:
    
    
    export FIFTYONE_BRAIN_SIMILARITY_BACKENDS=custom,sklearn,qdrant
    

When declaring new backends, you can include `*` to append new backend(s) without omitting or explicitly enumerating the builtin backends. For example, you can add a `custom` similarity backend as follows:
    
    
    export FIFTYONE_BRAIN_SIMILARITY_BACKENDS=*,custom
    export FIFTYONE_BRAIN_SIMILARITY_CUSTOM_CONFIG_CLS=your.custom.SimilarityConfig
    

**Visualization methods**

You can declare parameters for specific visualization methods by setting environment variables of the form `FIFTYONE_BRAIN_VISUALIZATION_<METHOD>_<PARAMETER>`. Any settings that you declare in this way will be passed as keyword arguments to methods like [`compute_visualization()`](api/fiftyone.brain.html#fiftyone.brain.compute_visualization "fiftyone.brain.compute_visualization") whenever the corresponding method is in use. For example, you can suppress logging messages for the UMAP method as follows:
    
    
    export FIFTYONE_BRAIN_VISUALIZATION_UMAP_VERBOSE=false
    

The `FIFTYONE_BRAIN_VISUALIZATION_METHODS` environment variable can be set to a `list,of,methods` that you want to expose in your session, which may exclude native methods and/or declare additional custom methods whose parameters are defined via additional config modifications of any kind:
    
    
    export FIFTYONE_BRAIN_VISUALIZATION_METHODS=custom,umap,tsne
    

When declaring new methods, you can include `*` to append new method(s) without omitting or explicitly enumerating the builtin methods. For example, you can add a `custom` visualization method as follows:
    
    
    export FIFTYONE_BRAIN_VISUALIZATION_METHODS=*,custom
    export FIFTYONE_BRAIN_VISUALIZATION_CUSTOM_CONFIG_CLS=your.custom.VisualzationConfig
    

#### Modifying your config in code#

You can dynamically modify your brain config at runtime by directly editing the `fiftyone.brain.brain_config` object.

Any changes to your brain config applied via this manner will immediately take effect in all subsequent calls to `fiftyone.brain.brain_config` during your current session.
    
    
    1import fiftyone.brain as fob
    2
    3fob.brain_config.default_similarity_backend = "qdrant"
    4fob.brain_config.default_visualization_method = "tsne"
    

IN THIS ARTICLE 
