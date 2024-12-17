# Todo list
-[] make program to backup images to a local device
-[] add a check to make sure the photos to be backed up aren't more than 7 days old
    - if they are, delete them.
    
-[] make the main index page mobile friendly
-[] make the picture time index page -- also needs to be mobile friendly
-[] add resume page
-[] redo functions for generating a video
    - these functions won't be used by the server
    - since all the data is being backed up locally, use the same program that backs them up to generate
    a new video/append to an existing video using the backup images.
    - this minimizes server storage usage
    - have an upload page to upload the video to be shown on the website -- require a key/password to upload
    
-[ ] make a process.py and compile.py (combine them?) that can process images locally for compiling photos
  from before you started using the website. Have the compile.py compile them into a compressed video. Users
  the compressed video as a start to append to when you upload more photos -- api will need to get the video
  if it doesn't already have it.