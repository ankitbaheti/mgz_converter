#!/usr/bin/env python
#
# mgz_converter ds ChRIS plugin app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
import numpy as np
import nibabel as nib
import scipy.misc, numpy, shutil, os, nibabel
import imageio
import os
import scipy
from tqdm import tqdm

sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from chrisapp.base import ChrisApp


Gstr_title = """

Generate a title from
http://patorjk.com/software/taag/#p=display&f=Doom&t=mgz_converter

"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       mgz_converter.py

    SYNOPSIS

        python mgz_converter.py                                         \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir>

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python mgz_converter.py   \\
                                in    out

    DESCRIPTION

        `mgz_converter.py` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.

        [--conversion_type <conversion_type>]
        Should be specified,
        If the <conversion_type> is 1, converts the input mgz images to png
        If the <conversion_type> is 2, converts the input mgz images to npy

"""


class Mgz_converter(ChrisApp):
    """
    An app to ....
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A ChRIS plugin app'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'An app to ...'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '0.1'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

        self.add_argument('--conversion_type', dest='conversion_type', type=str, optional=False,
                          help='which type of conversion you want 1. To jpg 2. To numpy')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """

        try:
            os.mkdir(options.outputdir + "/input_images")
            os.mkdir(options.outputdir + "/label_images")

        except OSError:
            print ("Output folders already exist")
        print(os.getcwd())

        if options.conversion_type == "1":
            self.convert_to_jpeg(options)
        elif options.conversion_type == "2":
        	self.convert_to_npy(options)
        else:
        	print("You have selected invalid option for conversion")

    def convert_nifti_to_png(self,new_image,output_name):
        # converting nifti to .png
        ask_rotate_num=90
        outputfile=output_name
        inputfile='input'
        ask_rotate='y'
        nx, ny, nz = new_image.shape

        if not os.path.exists(outputfile):
            os.makedirs(outputfile)
            print("Created ouput directory: " + outputfile)

        print('Reading NIfTI file...')

        total_slices = new_image.shape[2]

        slice_counter = 0
        # iterate through slices
        for current_slice in range(0, total_slices):
            # alternate slices
            if (slice_counter % 1) == 0:
                # rotate or no rotate
                if ask_rotate.lower() == 'y':
                    if ask_rotate_num == 90 or ask_rotate_num == 180 or ask_rotate_num == 270:
                        if ask_rotate_num == 90:
                            data = np.rot90(new_image[:, :, current_slice])
                        elif ask_rotate_num == 180:
                            data = np.rot90(np.rot90(new_image[:, :, current_slice]))
                        elif ask_rotate_num == 270:
                            data = np.rot90(np.rot90(np.rot90(new_image[:, :, current_slice])))
                elif ask_rotate.lower() == 'n':
                    data = new_image[:, :, current_slice]

                #alternate slices and save as png
                if (slice_counter % 1) == 0:
                    print('Saving image...')
                    image_name = inputfile[:-4] + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png"
                    imageio.imwrite(image_name, data)
                    print('Saved.')

                    #move images to folder
                    print('Moving image...')
                    src = image_name
                    shutil.move(src, outputfile)
                    slice_counter += 1
                    print('Moved.')

        print('Finished converting images')

    def convert_to_jpeg(self,options):
        dirs = os.listdir(options.inputdir)
        for i in tqdm(dirs):
            # converting mgz to numpy
            img = nib.load(options.inputdir + "/" + i + "/brain.mgz")
            img1 = nib.load(options.inputdir + "/" + i + "/aparc.a2009s+aseg.mgz")
            X_numpy=img.get_data()
            y_numpy=img1.get_data()
            # converting numpy to nifti
            X_nifti= nib.Nifti1Image(X_numpy, affine=np.eye(4))
            y_nifti= nib.Nifti1Image(y_numpy, affine=np.eye(4))
            # converting nifti to png
            self.convert_nifti_to_png(X_nifti.get_data(),options.outputdir + "/" + i+"X")
            self.convert_nifti_to_png(y_nifti.get_data(),options.outputdir + "/" + i+"y")

    def convert_to_npy(self,options):
        dirs = os.listdir(options.inputdir)
        dirs.pop(dirs.index(".DS_Store"))
        for i in tqdm(dirs):
            img = nib.load(options.inputdir + "/" + i + "/brain.mgz")
            img1 = nib.load(options.inputdir + "/" + i + "/aparc.a2009s+aseg.mgz")
            file = open(options.outputdir +"/input_images/" + i + ".npy", "wb")
            file1 = open(options.outputdir + "/label_images/" +i + ".npy","wb")
            np.save(file1, img1.get_data())
            np.save(file, img.get_data())

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Mgz_converter()
    chris_app.launch()
