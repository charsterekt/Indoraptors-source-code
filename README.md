# Indoraptors-source-code
The entire source code for <https://www.indoraptors.in>


The Indoraptors project is an effort to tackle the difficult task of classifying bird species using machine learning. The model has been deployed into a web app
available for use at <https://www.indoraptors.in>
The AI model is based on the popular xception model and has been trained using imagenet weights on over 16000 images of 109 different species of raptors and owls
found in and around the Indian subcontinent. The highest accuracy achieved by our model peaked around 84% in validation and testing. The model was primarly trained on
adult male specimens and does not include female and juvenile samples.

The backend was written in Flask, chosen for being simple and lightweight; the ideal framework to deploy a model with. A simple 2-page design ensures smooth functioning
and a simple user experience.

Due to GitHub's file size restriction, the main AI model file has not been included in this repository, however for testing purposes it can be found at this link:
https://drive.google.com/file/d/1RtS9oANjgeUiF5EnOXdfd705kziRnbDL/view?usp=sharing
