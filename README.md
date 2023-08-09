# quickimagextract
Small script to extract 3 frames of images at 512, 768, 1024px around the cursor through a gui. quickly extract full res features from image dir. Each click automatically print the next image and record 3 images (if possible) in a subdirectory "processed".

Description (by ChatGPT) : Image Extractor is an interactive tool crafted to quickly extract objects from images for training machine learning models, such as a Lora. The need to maintain the quality of training data led to the creation of this tool, which allows objects to be extracted in full resolution. The program also offers the flexibility of extracting two additional slightly zoomed-out images to aid the flexibility of the model. All extracted images are saved in a resolution of 512x512 pixels, although this can be quickly modified in the code if needed.
Features

    Interactive Navigation: Use the "Previous" and "Next" buttons or the arrow keys on the keyboard to browse through images.
    Crop Area Selection: Click and hold the left mouse button to see a red square following the pointer, indicating the area to be cropped. Release the button to extract and save the area.
    Variable Scale Extraction: For each selection, the program saves three cropped images with increasing capture areas, all saved at a 512x512-pixel resolution without distortion.
    File Management: Cropped images are saved in a "cropped" subdirectory, with intelligent name handling to avoid overwriting existing files.

Usage

    Directory Selection: Upon launching the program (imagextractor.py), a dialog box prompts you to select the directory containing the images to process.
    Navigation and Selection: Use the buttons or arrow keys to navigate between images. Select the area to crop with the left mouse click.
    End of Processing: An information message appears when all the images in the directory have been processed.

Author's Note

I developed this program with the assistance of ChatGPT as part of a personal project. ChatGPT wrote this description as well.
Requirements

    Python 3.x
    Libraries: Tkinter, PIL (Pillow)

License

This code is free to use for any non-commercial and non-closed-sources purposes. See the license for more details.
