[ Run in Google Colab ](https://colab.research.google.com/github/voxel51/fiftyone/blob/main/docs/source/tutorials/uniqueness.ipynb) |  [ View source on GitHub ](https://github.com/voxel51/fiftyone/blob/main/docs/source/tutorials/uniqueness.ipynb) |  [ Download notebook ](https://raw.githubusercontent.com/voxel51/fiftyone/main/docs/source/tutorials/uniqueness.ipynb)

# Exploring Image Uniqueness with FiftyOne#

During model training, the best results will be seen when training on _unique data samples_. For example, finding and removing similar samples in your dataset can avoid accidental concept imbalance that can bias the learning of your model. Or, if duplicate or near-duplicate data is present in both training and validation/test splits, evaluation results may not be reliable. Just to name a few. In this tutorial, we explore how FiftyOneâs image uniqueness tool can be used to analyze and extract insights from raw (unlabeled) datasets. Weâll cover the following concepts:

  * Loading a dataset from the [FiftyOne Dataset Zoo](https://voxel51.com/docs/fiftyone/user_guide/dataset_zoo/index.html)
  * Applying FiftyOneâs [uniqueness method](https://voxel51.com/docs/fiftyone/user_guide/brain.html#image-uniqueness) to your dataset
  * Launching the [FiftyOne App](https://voxel51.com/docs/fiftyone/user_guide/app.html) and visualizing/exploring your data
  * Identifying duplicate and near-duplicate images in your dataset
  * Identifying the most unique/representative images in your dataset

**So, whatâs the takeaway?** This tutorial shows how FiftyOne can automatically find and remove near-duplicate images in your datasets and recommend the most unique samples in your data, enabling you to start your model training off right with a high-quality bootstrapped training set.

## Setup#

If you havenât already, install FiftyOne:
    
    
    [ ]:
    
    
    
    !pip install fiftyone
    

This tutorial requires either [Torchvision Datasets](https://pytorch.org/docs/stable/torchvision/datasets.html) or [TensorFlow Datasets](https://www.tensorflow.org/datasets) to download the CIFAR-10 dataset used below. You can, for example, install PyTorch as follows:
    
    
    [ ]:
    
    
    
    !pip install torch torchvision
    

## Part 1: Finding duplicate and near-duplicate images#

A common problem in dataset creation is duplicated data. Although this could be found using file hashingâas in the [image_deduplication](https://colab.research.google.com/github/voxel51/fiftyone-examples/blob/master/examples/image_deduplication.ipynb) walkthroughâit is less possible when small manipulations have occurred in the data. Even more critical for workflows involving model training is the need to get as much power out of each data samples as possible; near-duplicates, which are samples that are exceptionally similar to one another, are intrinsically less valuable for the training scenario. Letâs see if we can find such duplicates and near-duplicates in a common dataset: CIFAR-10.

### Load the dataset#

Open a Python shell to begin. We will use the CIFAR-10 dataset, which is available in the [FiftyOne Dataset Zoo](https://voxel51.com/docs/fiftyone/user_guide/dataset_zoo/datasets.html#dataset-zoo-cifar10):
    
    
    [1]:
    
    
    
    import fiftyone as fo
    import fiftyone.zoo as foz
    
    # Load the CIFAR-10 test split
    # Downloads the dataset from the web if necessary
    dataset = foz.load_zoo_dataset("cifar10", split="test")
    
    
    
    Split 'test' already downloaded
    Loading 'cifar10' split 'test'
     100% |âââââââââââââ| 10000/10000 [9.6s elapsed, 0s remaining, 1.0K samples/s]
    Dataset 'cifar10-test' created
    

The dataset contains the ground truth labels in a `ground_truth` field:
    
    
    [2]:
    
    
    
    print(dataset)
    
    
    
    Name:           cifar10-test
    Media type:     image
    Num samples:    10000
    Persistent:     False
    Tags:           ['test']
    Sample fields:
        filepath:     fiftyone.core.fields.StringField
        tags:         fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
        metadata:     fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.Metadata)
        ground_truth: fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Classification)
    
    
    
    [3]:
    
    
    
    print(dataset.first())
    
    
    
    <Sample: {
        'id': '6066448c7d373b861836bba8',
        'media_type': 'image',
        'filepath': '/home/ben/fiftyone/cifar10/test/data/000001.jpg',
        'tags': BaseList(['test']),
        'metadata': None,
        'ground_truth': <Classification: {
            'id': '6066448c7d373b861836bba7',
            'tags': BaseList([]),
            'label': 'cat',
            'confidence': None,
            'logits': None,
        }>,
    }>
    

Letâs launch the [FiftyOne App](https://voxel51.com/docs/fiftyone/user_guide/app.html) and use the GUI to explore the dataset visually before we go any further:
    
    
    [4]:
    
    
    
    session = fo.launch_app(dataset)
    

Activate

### Compute uniqueness#

Now we can process the entire dataset for uniqueness. This is a fairly expensive operation, but should finish in a few minutes at most. We are processing through all samples in the dataset, then building a representation that relates the samples to each other. Finally, we analyze this representation to output uniqueness scores for each sample.
    
    
    [5]:
    
    
    
    import fiftyone.brain as fob
    
    fob.compute_uniqueness(dataset)
    
    
    
    Generating embeddings...
       0% ||------------|    16/10000 [95.0ms elapsed, 59.3s remaining, 168.5 samples/s]  100% |âââââââââââââ| 10000/10000 [1.2m elapsed, 0s remaining, 166.0 samples/s]
    Computing uniqueness...
    Uniqueness computation complete
    

The above method populates a `uniqueness` field on each sample that contains the sampleâs uniqueness score. Letâs confirm this by printing some information about the dataset:
    
    
    [6]:
    
    
    
    # Now the samples have a "uniqueness" field on them
    print(dataset)
    
    
    
    Name:           cifar10-test
    Media type:     image
    Num samples:    10000
    Persistent:     False
    Tags:           ['test']
    Sample fields:
        filepath:     fiftyone.core.fields.StringField
        tags:         fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
        metadata:     fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.Metadata)
        ground_truth: fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Classification)
        uniqueness:   fiftyone.core.fields.FloatField
    
    
    
    [7]:
    
    
    
    print(dataset.first())
    
    
    
    <Sample: {
        'id': '6066448c7d373b861836bba8',
        'media_type': 'image',
        'filepath': '/home/ben/fiftyone/cifar10/test/data/000001.jpg',
        'tags': BaseList(['test']),
        'metadata': None,
        'ground_truth': <Classification: {
            'id': '6066448c7d373b861836bba7',
            'tags': BaseList([]),
            'label': 'cat',
            'confidence': None,
            'logits': None,
        }>,
        'uniqueness': 0.4978482190810026,
    }>
    

### Visualize to find duplicate and near-duplicate images#

Now, letâs visually inspect the least unique images in the dataset to see if our dataset has any issues:
    
    
    [8]:
    
    
    
    # Sort in increasing order of uniqueness (least unique first)
    dups_view = dataset.sort_by("uniqueness")
    
    # Open view in the App
    session.view = dups_view
    

Activate You will easily see some near-duplicates in the App. It surprised us that there are duplicates in CIFAR-10, too! Of course, in this scenario, near duplicates are identified from visual inspection. So, how do we get the information out of FiftyOne and back into your working environment. Easy! The `session` variable provides a bidirectional bridge between the App and your Python environment. In this case, we will use the `session.selected` bridge. So, in the App, select some of the duplicates and near-duplicates. Then, execute the following code in the Python shell.
    
    
    [9]:
    
    
    
    # Get currently selected images from App
    dup_ids = session.selected
    
    # Mark as duplicates
    dups_view = dataset.select(dup_ids)
    dups_view.tag_samples("dups")
    
    # Visualize duplicates-only in App
    session.view = dups_view
    

Activate And the App will only show these samples now. We can, of course access the filepaths and other information about these samples programmatically so you can act on the findings. But, letâs do that at the end of Part 2 below!

## Part 2: Bootstrapping a dataset of unique samples#

When building a dataset, it is important to create a diverse dataset with unique and representative samples. Here, we explore FiftyOneâs ability to help identify the most unique samples in a raw dataset.

### Download some images#

This walkthrough will process a directory of images and compute their uniqueness. The first thing we need to do is get some images. Letâs get some images from Flickr, to keep this interesting! You need a Flickr API key to do this. If you already have a Flickr API key, then skip the next steps.

  1. Go to <https://www.flickr.com/services/apps/create/>
  2. Click on Request API Key. (<https://www.flickr.com/services/apps/create/apply/>) You will need to login (create account if needed, free).
  3. Click on âNon-Commercial API Keyâ (this is just for a test usage) and fill in the information on the next page. You do not need to be very descriptive; your API will automatically appear on the following page.
  4. Install the Flickr API:


    
    
    [ ]:
    
    
    
    !pip install flickrapi
    

You will also need to enable ETAâs storage support to run this script, if you havenât yet:
    
    
    [ ]:
    
    
    
    !pip install voxel51-eta[storage]
    

Next, letâs download three sets of images to process together. I suggest using three distinct object-nouns like âbadgerâ, âwolverineâ, and âkittenâ. For the actual downloading, we will use the provided [query_flickr.py](https://raw.githubusercontent.com/voxel51/fiftyone/develop/docs/source/tutorials/query_flickr.py) script:
    
    
    [ ]:
    
    
    
    from query_flickr import query_flickr
    
    # Your credentials here
    KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    SECRET = "XXXXXXXXXXXXXXXX"
    
    query_flickr(KEY, SECRET, "badger")
    query_flickr(KEY, SECRET, "wolverine")
    query_flickr(KEY, SECRET, "kitten")
    

The rest of this walkthrough assumes youâve downloaded some images to your local `.data/` directory.

### Load the data into FiftyOne#

Letâs now work through getting this data into FiftyOne and working with it.
    
    
    [12]:
    
    
    
    import fiftyone as fo
    
    dataset = fo.Dataset.from_images_dir("data", recursive=True, name="flickr-images")
    
    print(dataset)
    print(dataset.first())
    
    
    
     100% |âââââââââââââââââ| 167/167 [160.7ms elapsed, 0s remaining, 1.0K samples/s]
    Name:           flickr-images
    Media type:     image
    Num samples:    167
    Persistent:     False
    Tags:           []
    Sample fields:
        filepath: fiftyone.core.fields.StringField
        tags:     fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
        metadata: fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.Metadata)
    <Sample: {
        'id': '606647127d373b86183757ea',
        'media_type': 'image',
        'filepath': '/home/ben/code/fiftyone/docs/source/tutorials/data/badger/14271824861_122dfd2788_c.jpg',
        'tags': BaseList([]),
        'metadata': None,
    }>
    

The above command uses a [factory method](https://voxel51.com/docs/fiftyone/api/fiftyone.core.dataset.html?highlight=from_images_dir#fiftyone.core.dataset.Dataset.from_images_dir) on the `Dataset` class to traverse a directory of images (including subdirectories) and generate a dataset instance in FiftyOne containing those images. Note that the images are not loaded from disk, so this operation is fast. The first argument is the path to the directory of images on disk, and the third is a name for the dataset. With the dataset loaded into FiftyOne, we can easily launch the App and visualize it:
    
    
    [13]:
    
    
    
    session = fo.launch_app(dataset)
    

Activate Refer to the [User Guide](https://voxel51.com/docs/fiftyone/user_guide/index.html) for more useful things you can do with the dataset and App.

### Compute uniqueness and analyze#

Now, letâs analyze the data. For example, we may want to understand what are the most unique images among the data as they may inform or harm model training; we may want to discover duplicates or redundant samples. Continuing in the same Python shell, letâs compute and visualize uniqueness.
    
    
    [14]:
    
    
    
    import fiftyone.brain as fob
    
    fob.compute_uniqueness(dataset)
    
    # Now the samples have a "uniqueness" field on them
    print(dataset)
    
    
    
    Generating embeddings...
     100% |âââââââââââââââââ| 167/167 [1.8s elapsed, 0s remaining, 94.6 samples/s]
    Computing uniqueness...
    Uniqueness computation complete
    Name:           flickr-images
    Media type:     image
    Num samples:    167
    Persistent:     False
    Tags:           []
    Sample fields:
        filepath:   fiftyone.core.fields.StringField
        tags:       fiftyone.core.fields.ListField(fiftyone.core.fields.StringField)
        metadata:   fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.Metadata)
        uniqueness: fiftyone.core.fields.FloatField
    
    
    
    [15]:
    
    
    
    print(dataset.first())
    
    
    
    <Sample: {
        'id': '606647127d373b86183757ea',
        'media_type': 'image',
        'filepath': '/home/ben/code/fiftyone/docs/source/tutorials/data/badger/14271824861_122dfd2788_c.jpg',
        'tags': BaseList([]),
        'metadata': None,
        'uniqueness': 0.3202661340134384,
    }>
    
    
    
    [16]:
    
    
    
    # Sort by uniqueness (most unique first)
    rank_view = dataset.sort_by("uniqueness", reverse=True)
    
    # Visualize in the App
    session.view = rank_view
    

Activate Now, just visualizing the samples is interesting, but we want more. We want to get the most unique samples from our dataset so that we can use them in our work. Letâs do just that. In the same Python session, execute the following code.
    
    
    [17]:
    
    
    
    # Verify that the most unique sample has the maximal uniqueness of 1.0
    print(rank_view.first())
    
    # Extract paths to 10 most unique samples
    ten_best = [x.filepath for x in rank_view.limit(10)]
    
    for filepath in ten_best:
        print(filepath.split('/')[-1])
    
    # Then you can do what you want with these.
    # Output to csv or json, send images to your annotation team, seek additional
    # similar data, etc.
    
    
    
    <SampleView: {
        'id': '606647127d373b8618375862',
        'media_type': 'image',
        'filepath': '/home/ben/code/fiftyone/docs/source/tutorials/data/wolverine/2428280852_6c77fe2877_c.jpg',
        'tags': BaseList([]),
        'metadata': None,
        'uniqueness': 1.0,
    }>
    2428280852_6c77fe2877_c.jpg
    49733688496_b6fc5cde41_c.jpg
    2843545851_6e1dc16dfc_c.jpg
    7466201514_0a3c7d615a_c.jpg
    6176873587_d0744926cb_c.jpg
    33891021626_4cfe3bf1d2_c.jpg
    8303699893_a7c14c04d3_c.jpg
    388994554_34d60d1b18_c.jpg
    5880167199_906172bc50_c.jpg
    8538740443_a587bfe75c_c.jpg
    

Alternatively, you can simply tag the most unique samples and persist the dataset so you can return to it later in FiftyOne.
    
    
    [18]:
    
    
    
    rank_view.limit(10).tag_samples("unique")
    
    dataset.persistent = True
    
    
    
    [19]:
    
    
    
    session.freeze() # screenshot the active App for sharing
    

IN THIS ARTICLE 
