## Overview
This websites purpose is to be sort of an archive of all of my work/projects. I am also using the to host my picture time project. My picture time project is a compilation of photos I have taken of myself every day since mid 2020. The website lets me upload and process photos.

Because of the way I set up the picture time part of the website, it is built for only a single person to use and I don't plan on changing that in the near future as I only see myself using it. All processed images will need to be backed up to a local device because of server storage limitations *(this might change in the future)*. The video processing will also happen on the local device.

## API
When an Image is upload and processed, it is stored temporarily in the static folder until it is downloaded. The client API program checks to see if any files need to be downloaded through the page /picture-time/status which displays the status.json file in pictureTime/data *(this will be created after running app.py for the first time)*. The client will download and remove the images from the server then use those to process an updated time lapse video. The client will then upload the video to the server replacing the existing one. To download and upload you will need an API key.

The API comes with a .bat file for windows and a .sh file for linux to schedule the python file to check for downloads. In windows you can use **Windows Task Scheduler** to make the program run periodically. On Linux you can use **Cron** to schedule it to run periodically. *Note that files in the server more than a week old **will be deleted***. The .bat or .sh file **must** be in the same directory as the pythonw file.

## Mass Image Processing
There is a python file named **mass-processing.py**. This file is used to process any and all images that were taken before using the website. Run this file with arguments to choose what to process. You can choose between processing images to align and resize them, or compiling images into a video time lapse.

### Arguments
**Required**

- compile_type: this is the first argument. Choose between 'image' or 'video' depending on if you are processing images or exporting a video. 
- input_dir: this is the second argument. This is the path to the directory with the images to process/compile.
- output_dir: this is the third argument. This is the path to the directory where all processed images or the compiled video will go.

**Optional**
- --filename, -f: The filename for the video (only do this if you are exporting a video)
- --fps, -F: The fps of the video when making the time lapse. Less fps makes it easier to see each image. The default is 20.
- --process-order, -p: Choose in what order to process photos. All processed photos will be numbers 1-x depending no matter the option you choose. *file-order* sorts by the file order on your computer. *number-order* sorts in numerical number. *date-ISO* sorts it according to the image name following the universal ISO 8601 format. *date-metadata* sorts according to the image metadata; if there is none the image will be skipped. The default is date-ISO. This option only applies to image compiling. When doing date-ISO or date-metadata, the date will be added to the processed photos EXIF data under *Date Taken*. ***date-metadata isn't supported as of writing this***. 
- --count-start. -c: Choose what number to start on when processing photos. By default, when processing photos, it will start at 0 and count up. Setting this value will change the starting numbe from 0 to whatever you set it as.
- --input-start, -s: Choose what file to start processing with in the input_dir. Only enter the file name. The code will sort and process images based on this and the sorting method you choose. Any file in input_dir dating before this file or that is sequentially before this file will not be processed.

# TODO list
[Todo List](./todo.md)
