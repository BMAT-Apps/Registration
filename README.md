# registration

This pipeline allows the user to register a certain image into the space of another image. For that BMAT uses antsRegistrationSynQuick from ANTs registration tool ([ANTs registration](http://stnava.github.io/ANTs/)). This allows to quickly perform a rigid registration from one image to another. This registration will computer the registered image and the transformation matrix that have been used. This transformation matrix can also be used to register another images from the initial space to the reference space.

## Utilization

When launching this pipeline, the window contains two tabs; one for the registration and one for the transformation (cf. figures below). The registration tab is used to perform a registration of two images from a same subject and contain the folowing features:

* "Select image to register" button: opens a "file navigator" window for the user to navigate in his dataset and select the image sequence that he wants to register. 

* "Select reference image" button: opens a "file navigator" window for the user to navigate in his dataset and select the reference image sequence on which he wants to perform the registration. 

* "Select subjects" input: allows the user to script the selected registration (sequence to register, reference sequence) for other subjects of the dataset. By default (when this field is empty), the registration will only be done for the subject assocuated to the file selected before. by adding a list BIDS ID (without "sub-") separated by a comma, this registration process can be scripted to other subjects. Possible values are: single BIDS ID (e.g. "001,002,006,013"), multiple folowing BIDS ID (e.g. "001-005" is the same as '001,002,003,004,005"), or all subjects ("all").

* "Select sessions" input: allows the user to script the selected registration (sequence to register, reference sequence) for other sessions of subjects of the dataset. By default (when this field is empty), the registration will only be done for the subject and session assocuated to the file selected before. by adding a list session ID (without "ses-") separated by a comma, this registration process can be scripted to other sessions. Possible values are: single session ID (e.g. "01,02,06,13"), multiple folowing session ID (e.g. "01-05" is the same as '01,02,03,04,05"), or all sessions ("all").

* "Name of registration" input: allows the user to name the registration. The image registered will be saved in a specific folder (named with this input) in the *registrations* folder in the *derivatives* folder. By default the name of registration is the name of the modality of the reference image corresponding to the name of the space in which the image has been registered. We advice to keep this convention. 

* "Apply same transformation ?" checkbox: This allows the user to directly apply the same transformation as the registration to another sequence (this can also be done in the "Transformation" tab. Checking this box will open a "file navigator" to allow the user to select one or more images to apply the same transformation (the image should be in the same space as the image to register)

* "Registration" button: launch the registration script based on all information given by the user.

**A typical registration takes about 3 minutes**

![Registration Tab](/Readme_pictures/registration.png)

The transformation tab is used to perform a transformation of an image into another image space based on the transformation matrix of a previous registration. The image to apply the same transformation should be in the same space the image to register from the previous registration. This transformation tab contains the folowing features:

* "Select image to register" button: opens a "file navigator" window for the user to navigate in his dataset and select the image sequence that he wants to register. 

* "Select reference image" button: opens a "file navigator" window for the user to navigate in his dataset and select the reference image sequence from the previous registration. 

* "Select trasnformation matrix" button: opens a "file navigator" window for the user to navigate in his dataset and select the transformation matrix that will be used to perform the registration. 

* "Select subjects" input: allows the user to script the selected registration (sequence to register, reference sequence) for other subjects of the dataset. By default (when this field is empty), the registration will only be done for the subject assocuated to the file selected before. by adding a list BIDS ID (without "sub-") separated by a comma, this registration process can be scripted to other subjects. Possible values are: single BIDS ID (e.g. "001,002,006,013"), multiple folowing BIDS ID (e.g. "001-005" is the same as '001,002,003,004,005"), or all subjects ("all").

* "Select sessions" input: allows the user to script the selected registration (sequence to register, reference sequence) for other sessions of subjects of the dataset. By default (when this field is empty), the registration will only be done for the subject and session assocuated to the file selected before. by adding a list session ID (without "ses-") separated by a comma, this registration process can be scripted to other sessions. Possible values are: single session ID (e.g. "01,02,06,13"), multiple folowing session ID (e.g. "01-05" is the same as '01,02,03,04,05"), or all sessions ("all").

* "Transformation" button: launch the transformation script based on all information given by the user.

![Transformation Tab](/Readme_pictures/transformation.png)
