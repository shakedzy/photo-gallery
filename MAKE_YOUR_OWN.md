# Make your own photo gallery
This file is quick start recipe for using this repository and turning it into your own gallery. 

## Before you begin
This gallery code is based on the awesome work of [opieters/jekyll-image-gallery-example](https://github.com/opieters/jekyll-image-gallery-example). I would recommend reading the author's [blogpost](https://olivierpieters.be/blog/2016/02/26/creating-a-jekyll-image-gallery) about this repository to better understand how it works, or at least the section about the requirements and installation. Note that the optional `sizes` feature isn't supported here, and some modifications have been made, but it's still remains quite true to source.

## Forking and initialization
Obviously, the first thing you'll need to do is fork this repository. Once done, you'll want to delete the following files:

* `assets/photography/*`
* `galleries/*`
* `_data/galleries/*`

Next, you'll want to edit the `_config.yml` and adjust the parameters under _Site settings_. Also, you'll probably want to replace the social banner image (found by under `assets/site/`), simply as it bears my name in it :). Make sure it has the same format of your photos (`jpeg` in my case), and adjust the relavant attributes in `_config.yml` under `social_banner`.

## Creating a gallery
Create a new directory under `assets/photography/`, and export all gallery's photos to it. Note that file names are expecteed to follow a pattern:
```
[prefix]-[id].[suffix]
```

* `prefix` and `suffix` are exppected to be the same for all photos of the same gallery. `prefix` cannot contain hyphens (`-`)
* `id`s are consecutive ascending numbers, beginning with 1. Leading zeros are allowed, as long as it remains consistent (`0001, 0002, ..., 0131, ...`)

now run the `create-gallery.py` script found in repository's root. It required Python 3.x and a few requirements (`pip3 install argparse Pillow`). Run the script with the following arguments:
```
python3 create-gallery.py -n [gallery_name]
```

where `gallery_name` is the name of the directory to which you exported the images.

More useful options:
* `-t [gallery_title]`: a custom title for the gallery. Default is `[gallery_name]`
* `-d [gallery_date]`: shooting dates. If not specified, will be used from EXIF metadata (if available)
* `-p [preview_image_id]`: ID-number of the image which will be displayed in the main page. If not specified, image no. 1 will be used. 

You'll might also need to use:
* `-x [suffix]`: change image suffix (default: `JPG`)
* `-z [zfill]`: number of overall figures of the images ID-numbers (default: 4)

There are more available configurations, run `python3 create-gallery.py --help` to learn more.

This script creates everything for you, including thumbnails of all your photos. These are located at the same directory as your gallery photos, and are named `[prefix]-[id]-thumbnail.[suffix]`. And that's pretty much it, your new gallery is ready.

## Adding your words

Now that your gallery is ready, you can personalize it even more by adding some text.

### Add gallery text

You can add some text to the newly created gallery. Open the file `galleries/[gallery_name].md`, and add your text between the second `---` and the curly braces.

### Add titles and text to specific photos

You can add titles and captions to each and every photo. These will be shown when the image is displayed. To do so, open the file `_data/galleries/[gallery_name].yml`. You'll see that each image in the gallery is defined by a block that looks like this:
```
- filename: prefix-0001 
  original: prefix-0001.JPG 
  thumbnail: prefix-0001-thumbnail.JPG 
  ...
```
You can add the `title` and `caption` keys to each image. Note that you can't have `caption` without `title`. 