[ Run in Google Colab ](https://colab.research.google.com/github/voxel51/fiftyone/blob/main/docs/source/getting_started/depth_estimation/02_depth_estimation.ipynb) |  [ View source on GitHub ](https://github.com/voxel51/fiftyone/blob/main/docs/source/getting_started/depth_estimation/02_depth_estimation.ipynb) |  [ Download notebook ](https://raw.githubusercontent.com/voxel51/fiftyone/main/docs/source/getting_started/depth_estimation/02_depth_estimation.ipynb)

# Using Depth Estimation Models#

In this tutorial, we will explore multiple approaches to running depth estimation models in FiftyOne. Weâll work with pre-trained models from different sources and learn how to integrate them into your workflow.

## Installation#

Make sure you have FiftyOne installed in your Python environment. Additionally, youâll need:
    
    
    [ ]:
    
    
    
    !pip install torch transformers datasets diffusers
    

## Loading Dataset#

Note, weâve created an in-depth tutorial in the previous notebook that discusses the methods for loading depth data into FiftyOne. As discussed in that tutorial, FiftyOneâs [Heatmap](https://docs.voxel51.com/api/fiftyone.core.labels.html#fiftyone.core.labels.Heatmap) class is ideal for representing depth data:
    
    
    fo.Heatmap(
        map=None,           # 2D numpy array containing the data
        map_path=None,      # OR path to the heatmap image on disk
        range=None          # Optional [min, max] range for proper visualization
    )
    

Letâs start by loading a dataset from the Hugging Face Hub.
    
    
    [ ]:
    
    
    
    from datasets import load_dataset
    
    clevr_depth = load_dataset(
        "erkam/clevr-with-depth",
        split="train",
        cache_dir="clevr_with_depth",
    )
    

Note how this dataset is saved:
    
    
    [ ]:
    
    
    
    clevr_depth[0]
    

The code takes a Hugging Face dataset containing image-depth pairs and converts it into a FiftyOne dataset for visualization and analysis. For each sample, it saves the RGB image to disk (since FiftyOne requires file paths) and extracts the depth information from the first channel of the RGBA depth map. Each sample in the resulting FiftyOne dataset contains the path to the RGB image, the original prompt, and the depth map stored as a `Heatmap` visualization. The depth values are scaled between 0 and 198, which represents the range of depth values in this dataset.
    
    
    [ ]:
    
    
    
    import fiftyone as fo
    import numpy as np
    from PIL import Image
    import os
    
    def convert_dataset_to_fiftyone(hf_dataset, save_dir="./clevr_depth_data"):
        """
        Converts a Hugging Face dataset containing image-depth pairs into a FiftyOne dataset.
    
        This function takes a dataset from Hugging Face that contains RGB images and their corresponding
        depth maps, saves the images to disk, and creates a FiftyOne dataset with the images and depth
        information stored as heatmaps.
    
        Args:
            hf_dataset: A Hugging Face dataset containing 'image', 'depth', and 'prompt' fields
            save_dir (str): Directory path where images and depth maps will be saved.
                           Defaults to "./clevr_depth_data"
    
        Returns:
            fo.Dataset: A FiftyOne dataset containing:
                - RGB images stored on disk
                - Depth maps as FiftyOne Heatmap objects (scaled 0-198)
                - Original prompts from the dataset
    
        Note:
            The depth maps are extracted from the first channel of the RGBA depth images
            since all channels are identical in this dataset.
        """
        # Create directories if they don't exist
        os.makedirs(os.path.join(save_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(save_dir, "depth"), exist_ok=True)
    
        samples = []
        # Create a FiftyOne dataset
        dataset = fo.Dataset("clevr_depth", overwrite=True, persistent=True)
    
        for idx, item in enumerate(hf_dataset):
            # Generate filenames
            image_filename = f"image_{idx:06d}.png"
            depth_filename = f"depth_{idx:06d}.png"
    
            image_path = os.path.join(save_dir, "images", image_filename)
            depth_path = os.path.join(save_dir, "depth", depth_filename)
    
            # Save images to disk
            item['image'].save(image_path)
    
            # Extract depth map from first channel (since all channels are identical in this dataset)
            depth_np = np.array(item['depth'])[:, :, 0]  # Taking channel 0
    
            # Create a FiftyOne sample
            sample = fo.Sample(
                filepath=image_path,
                prompt=item['prompt']
            )
    
            # Add depth as Heatmap with proper range
            sample["depth"] = fo.Heatmap(
                map=depth_np,
                range=[0, 198] # if you know the range of your dataset, use those values
            )
            # Add the sample to the dataset
            samples.append(sample)
    
        dataset.add_samples(samples)
        dataset.compute_metadata()
        return dataset
    
    # Usage:
    fo_dataset = convert_dataset_to_fiftyone(clevr_depth)
    

You can verify the depth map was parsed by calling the Dataset:
    
    
    [ ]:
    
    
    
    fo_dataset
    

And inspect the values of the first map like so:
    
    
    [ ]:
    
    
    
    fo_dataset.first()['depth']
    

Refer to our guide for loading depth data for other examples and more detail. Once the dataset has been parsed to FiftyOne format you can [launch the app](https://docs.voxel51.com/user_guide/app.html) and inspect its contents
    
    
    [ ]:
    
    
    
    fo.launch_app(fo_dataset)
    

## Using Depth Estimation Models in FiftyOne#

### As a Zoo Model#

You can load `transformers` depth estimation models directly from the [FiftyOne Model Zoo](https://docs.voxel51.com/user_guide/model_zoo/index.html)! To load a transformers depth estimation model from the zoo, specify `depth-estimation-transformer-torch` as the first argument, and pass in the modelâs name or path as a keyword argument:
    
    
    model = foz.load_zoo_model(
        "depth-estimation-transformer-torch",
        name_or_path="path/to-model",
    )
    

Any model that can be run in a Hugging Face pipeline for the `depth-estimation` task can be loaded as a Zoo model. A non-exhaustive list of such models includes:

  * [Intel/dpt-large](https://huggingface.co/Intel/dpt-large)
  * [Intel/dpt-hybrid-midas](https://huggingface.co/Intel/dpt-hybrid-midas)
  * [Intel/zoedepth-nyu-kitti](https://huggingface.co/Intel/zoedepth-nyu-kitti)
  * [vinvino02/glpn-kitti](https://huggingface.co/vinvino02/glpn-kitti)
  * [LiheYoung/depth-anything-small-hf](https://huggingface.co/LiheYoung/depth-anything-small-hf)
  * [depth-anything/Depth-Anything-V2-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf)
  * [depth-anything/Depth-Anything-V2-Base-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Base-hf)
  * [depth-anything/Depth-Anything-V2-Metric-Indoor-Large-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-Indoor-Large-hf)

Refer to the Hugging Face documentation on [Monocular depth estimation](https://huggingface.co/docs/transformers/tasks/monocular_depth_estimation) to stay up to date on which models can be run in a pipeline. **Note:** When selecting a model, itâs advisable to refer to its model card and determine whether itâs suitable for your dataset and use case. Below is an example of using the `depth-anything/Depth-Anything-V2-Small-hf` on the dataset we parsed earlier:
    
    
    [ ]:
    
    
    
    import torch
    
    import fiftyone as fo
    import fiftyone.zoo as foz
    
    dav2_model = foz.load_zoo_model(
        "depth-estimation-transformer-torch",
        name_or_path="depth-anything/Depth-Anything-V2-Small-hf",
        device="cuda" if torch.cuda.is_available() else "cpu"
        )
    
    
    
    [ ]:
    
    
    
    fo_dataset.apply_model(
        dav2_model,
        label_field="dav2_small",
        )
    

To verify:
    
    
    [ ]:
    
    
    
    fo_dataset.first()["dav2_small"]
    

### Hugging Face Model Thatâs Not Compatible with Integration#

Admittedly, itâs not always clear which Hugging Face model can be run as part of a pipeline. A good first entry point is to just try it and pass the model name into `name_or_path` in the [load_zoo_model](https://docs.voxel51.com/api/fiftyone.zoo.models.html#fiftyone.zoo.models.load_zoo_model) method. If a Hugging Face model is not compatible with the integration, youâll see an error to the effect of:
    
    
    ValueError: Unrecognized model in <whatever-model-name>
    

In this case, you will need to run the model manually. All this means is that you need to instantiate the model, its processor, and write some logic to parse the model output into a FiftyOne Heatmap. Hereâs an example of how you can do this:
    
    
    [ ]:
    
    
    
    import numpy as np
    import torch
    from PIL import Image
    from transformers import DPTImageProcessor, DPTForDepthEstimation
    import fiftyone as fo
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    dpt_processor = DPTImageProcessor.from_pretrained("Intel/dpt-beit-large-512")
    
    dpt_model = DPTForDepthEstimation.from_pretrained(
        "Intel/dpt-beit-large-512",
        device_map=device
        )
    
    dpt_model.eval()
    
    file_paths = fo_dataset.values("filepath") # a list of all filepaths in Dataset
    
    dpt_depth_maps = [] # to store the depth maps
    
    for img in file_paths:
    
        image = Image.open(img).convert("RGB")
    
        inputs = dpt_processor(images=image, return_tensors="pt").to(device)
    
        with torch.no_grad():
            outputs = dpt_model(**inputs)
            predicted_depth = outputs.predicted_depth
    
        # interpolate to original size
        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=image.size[::-1],
            mode="bicubic",
            align_corners=False,
            )
    
        output = prediction.squeeze().cpu().numpy()
    
        formatted = (output * 255 / np.max(output)).astype("uint8")
    
        fo_depth_map = fo.Heatmap(map=formatted)
    
        dpt_depth_maps.append(fo_depth_map)
    
    
    fo_dataset.set_values("dpt_beit_maps", dpt_depth_maps)
    
    
    
    [ ]:
    
    
    
    fo_dataset.first()["dpt_beit_maps"]
    

The majority of the logic in the code above comes directly from the [model card](https://huggingface.co/Intel/dpt-beit-large-512). The only FiftyOne-specific aspects are just grabbing the filepaths for the Samples, parsing the model output as numpy arrays, loading it as a FiftyOne [Heatmap](https://docs.voxel51.com/api/fiftyone.core.labels.html#fiftyone.core.labels.Heatmap), and adding it as a [Field](https://docs.voxel51.com/api/fiftyone.core.fields.html) to the Dataset.

### Plugin#

The FiftyOne community contributes [Plugins](https://docs.voxel51.com/plugins/index.html) which can make it easy to run a depth estimation model on your Dataset. For example, there is a plugin for [DepthPro](https://docs.voxel51.com/plugins/plugins_ecosystem/depth_pro_plugin.html). To use this plugin, download it and install the requirements:
    
    
    [ ]:
    
    
    
    !fiftyone plugins download https://github.com/harpreetsahota204/depthpro-plugin
    
    
    
    [ ]:
    
    
    
    !fiftyone plugins requirements @harpreetsahota/depth_pro_plugin --install
    

Then instantiate the operator:
    
    
    [ ]:
    
    
    
    import fiftyone.operators as foo
    
    depthpro = foo.get_operator("@harpreetsahota/depth_pro_plugin/depth_pro_estimator")
    

Youâll need to start a [delegated service](https://docs.voxel51.com/plugins/developing_plugins.html#delegated-execution), which you can do by opening your terminal and executing the following command:
    
    
    fiftyone delegated launch
    

And then run the plugin on the dataset:
    
    
    [ ]:
    
    
    
    await depthpro(
        fo_dataset,
        depth_field="depthpro_map",
        depth_type="inverse", # or "regular" see the plugin repo for more details
        delegate=True
        )
    

You may have to call the `reload` method of the dataset if you donât see your field:
    
    
    [ ]:
    
    
    
    fo_dataset.reload()
    
    
    
    [ ]:
    
    
    
    fo_dataset.first()["depthpro_map_depth"]
    

### ð§¨ Diffusers Depth Estimation#

You can also use the `Diffusers` library for zero-shot prediction of depth maps. Start by installing the library and instantiating the model, in this case weâll use [Marigold Depth model](https://huggingface.co/prs-eth/marigold-depth-v1-0).
    
    
    [ ]:
    
    
    
    !pip install diffusers
    
    
    
    [ ]:
    
    
    
    import diffusers
    import torch
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    marigold_pipe = diffusers.MarigoldDepthPipeline.from_pretrained(
        "prs-eth/marigold-depth-v1-0",
        variant="fp16",
        torch_dtype=torch.float16
        ).to(device)
    
    marigold_pipe.set_progress_bar_config(disable=True) # disable progress bar
    

With the model instantiated, we can iterate through the filepaths of our Dataset and run inference. This is an example of a model that outputs a `png` depth map. Weâll save the depth map to disk and point to the filepath of the png via the `map_path` argument of `Heatmap`:
    
    
    [ ]:
    
    
    
    file_paths = fo_dataset.values("filepath") # a list of all filepaths in Dataset
    
    marigold_depth_maps = [] # to store the depth maps
    
    for img in file_paths:
    
        # Create new filename with _marigold_map suffix, save wherever you want
        base_path = os.path.splitext(img)[0]  # Remove extension
        depth_map_path = f"{base_path}_marigold_map.png"
    
        image = diffusers.utils.load_image(img)
    
        depth_estimate = marigold_pipe(image)
    
        depth_map = marigold_pipe.image_processor.visualize_depth(depth_estimate.prediction)
        depth_map[0].save(depth_map_path)
    
        # Alternatively, you can extract a 16 bit depth map
        # depth_16bit = marigold_pipe.image_processor.export_depth_to_16bit_png(depth_estimate.prediction)
    
        fo_depth_map = fo.Heatmap(map_path=depth_map_path)
    
        marigold_depth_maps.append(fo_depth_map)
    
    fo_dataset.set_values("marigold_depth", marigold_depth_maps)
    
    
    
    [ ]:
    
    
    
    fo_dataset.first()['marigold_depth']
    

Now, letâs launch the FiftyOne app and inspect all the depth maps we created.
    
    
    fo.launch_app(fo_dataset)
    

IN THIS ARTICLE 
