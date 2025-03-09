# Registration

This pipeline allows to compute an intra-subject rigid registration and to apply the same transformation to other images or labeled segmentation file using ANTs ([ANTs registration](http://stnava.github.io/ANTs/)). 

## Requirements

**ANTs**
Either ANTs installed locally on the user's computer

Or using the docker antx/ants

You can choose which one to run by switching the option in the Registration.json file

## How to cite

1. Avants B, Tustison N, Song G. Advanced normalization tools (ANTS). Insight J. 2008 Nov 30;1–35. 

## Utilization

When launching this pipeline, the window contains two tabs; one for the registration and one for the transformation (cf. figures below). The registration tab is used to perform a registration of two images from a same subject and contain the following features:

* "Quick registration" checkbox: checkbox to compute the registration with antsRegistrationSyNQuick.sh or antsRegistrationSyN.sh (default: Quick)

* "Select image to register": opens a File explorer for the user to navigate in his dataset and select the image sequence that he wants to register. 

* "Select reference image": opens a File explorer for the user to navigate in his dataset and select the reference image sequence on which he wants to perform the registration. 

* "Select subjects" input: allows the user to script the selected registration (sequence to register, reference sequence) for other subjects of the dataset. By default (when this field is empty), the registration will only be done for the subject associated to the file selected before. By adding a list BIDS ID (without "sub-") separated by a comma, this registration process can be scripted to other subjects. Possible values are: single BIDS ID (e.g. "001,002,006,013"), multiple folowing BIDS ID (e.g. "001-005" is the same as '001,002,003,004,005"), or all subjects ("all").

* "Select sessions" input: allows the user to script the selected registration (sequence to register, reference sequence) for other sessions of subjects of the dataset. By default (when this field is empty), the registration will only be done for the subject and session assocuated to the file selected before. By adding a list session ID (without "ses-") separated by a comma, this registration process can be scripted to other sessions. Possible values are: single session ID (e.g. "01,02,06,13"), multiple folowing session ID (e.g. "01-05" is the same as '01,02,03,04,05"), or all sessions ("all").

* "derivative name": specify the derivatime name to save the output of the pipeline (default: registrations/reg-{space of the ref image})

* "registration name": specify the registration name tag to add to the ouput image (default: reg-{space of ref image})

* "Apply same transformation ?" checkbox: This allows the user to directly apply the same transformation as the registration to another sequence (this can also be done in the "Transformation" tab. Checking this box will open a "file navigator" to allow the user to select one or more images to apply the same transformation (the image should be in the same space as the image to register)

* "Registration" button: launch the registration script based on all information given by the user.

**A typical registration takes about 3 minutes (Quick) or 10 minutes (with long)**

![Registration Tab](/Readme_pictures/registration.png)

The transformation tab is used to perform a transformation of an image into another image space based on the transformation matrix of a previous registration. The image to apply the same transformation should be in the same space the image to register from the previous registration. This transformation tab contains the folowing features:

* "Select image to register": opens File explorer for the user to navigate in his dataset and select the image sequence that he wants to register. 

* "Select reference image": opens file explorer for the user to navigate in his dataset and select the reference image sequence from the previous registration. 

* "Select trasnformation matrix": opens File explorer for the user to navigate in his dataset and select the transformation matrix that will be used to perform the registration. 

* Label Transformation: option to use when apply the transformation matrix to a labeled segmentation file. Use GenericLabel option to keep the label numbers for the output file

* Use invers Transform: option to apply inverse transformation matrix to the input image 

* "Select subjects" input: allows the user to script the selected registration (sequence to register, reference sequence) for other subjects of the dataset. By default (when this field is empty), the registration will only be done for the subject associated to the file selected before. By adding a list BIDS ID (without "sub-") separated by a comma, this registration process can be scripted to other subjects. Possible values are: single BIDS ID (e.g. "001,002,006,013"), multiple folowing BIDS ID (e.g. "001-005" is the same as '001,002,003,004,005"), or all subjects ("all").

* "Select sessions" input: allows the user to script the selected registration (sequence to register, reference sequence) for other sessions of subjects of the dataset. By default (when this field is empty), the registration will only be done for the subject and session associated to the file selected before. By adding a list session ID (without "ses-") separated by a comma, this registration process can be scripted to other sessions. Possible values are: single session ID (e.g. "01,02,06,13"), multiple folowing session ID (e.g. "01-05" is the same as '01,02,03,04,05"), or all sessions ("all").

* "derivative name": specify the derivatime name to save the output of the pipeline (default: registrations/reg-{space of the ref image})

* "registration name": specify the registration name tag to add to the ouput image (default: reg-{space of ref image})

* "Transformation" button: launch the transformation script based on all information given by the user.

**A typical transformation takes about 2 minutes**

![Transformation Tab](/Readme_pictures/transformation.png)

## Change pipeline option

In the SAMSEG.json file, the user can choose some option to run SAMEG:

* "use_docker": choose to run the pipeline locally using the docker image (true) or locally installed FreeSurfer (default: false)

* "sss_slurm": precise the config file to run the pipeline on the SSS server (specific to UCLouvain members). If this tag does not exists (by default: "sss_slurm_no"), it will run the pipeline locally. To use this pipeline on remote server, change the name "sss_slurm_no" to "sss_slurm", and adapt the config file "SAMSEG_sss.json" for your specific slurm need. This works with a correct "server_info.json" config file in the BMAT home directory.

