# Vote 4 Me - EVoting based in blockchain
## Face Recognition Module
---

<div align="center">
  <img src="https://hackernoon.com/drafts/57e73zmx.png"/>
</div>

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

First make sure you have installed the following version of Python: 

```
python 3.5.x
```

After that, you should download a copy of the project to start running it. To do so, go to your git bash and do
```
git clone https://github.com/vot4me/face_recognition.git
```

Then go to the cloned folder and you are ready!
```
cd face_recognition
```

Then install the needed resources:
```
pip install tensorflow
pip install numpy
pip install scipy
pip install pillow
pip install scikit-learn
pip install opencv-python
```
To do this easily just run:
```
pip install -r requirements.txt
```


### Run the project

To run de project you need to save some images in the train_img folder. To save your images use the following structure
```
Person1 name
   |-photo1.jpg
   |-photo2.jpg
    ...
Person2 name
   |-photo1.jpg
   |-photo2.jpg
    ...
...
```
To do that easily, just run the faces.py file, insert your name and the program will save some pictures of you using your camera.
```
python faces.py
```

After that, the only thing you need to do is to start running the project. The first step is to preprocess the data, so:
```
python data_preprocess.py
```

Then, you'll see a new folder called pre_img, inside there, you'll find all the processed images (just the faces of each image). The next step is to train the model, so:
```
python train_main.py
```

Finally, you can test the results running any of the following implementations:

```
(Face recognition with the camera)
python identify_face_camera.py
```
```
(Face recognition with an image, to make this work you need to add a abc.jpg image)
python identify_face_image.py
```
