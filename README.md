## Overview
This websites purpose is to be sort of an archive of all of my work/projects. I am also using the to host my picture time project. My picture time project is a compilation of photos I have taken of myself every day since mid 2020. The website lets me upload and process photos.

Because of the way I set up the picture time part of the website, it is built for only a single person to use and I don't plan on changing that in the near future as I only see myself using it. All processed images will need to be backed up to a local device because of server storage limitations *(this might change in the future)*. The video processing will also happen on the local device.

## API
When an Image is upload and processed, it is stored temporarily in the static folder until it is downloaded. The client API program checks to see if any files need to be downloaded through the page /picture-time/status which displays the status.json file in pictureTime/data *(this will be created after running app.py for the first time)*. The client will download and remove the images from the server then use those to process an updated time lapse video. The client will then upload the video to the server replacing the existing one. To download and upload you will need an API key.

The API comes with a .bat file for windows and a .sh file for linux to schedule the python file to check for downloads. In windows you can use **Windows Task Scheduler** to make the program run periodically. On Linux you can use **Cron** to schedule it to run periodically. *Note that files in the server more than a week old **will be deleted***. The .bat or .sh file **must** be in the same directory as the pythonw file.

## Mass Image Processing
There is a python file named **mass-processing.py**. This file is used to process any and all images that were taken before using the website. Run this file with arguments to choose what to process. You can choose between processing images to align and resize them, or compiling images into a video time lapse.