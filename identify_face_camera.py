from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow.compat.v1 as tf
import cv2
import numpy as np
import facenet
import os
import time
import pickle
import sys
import webbrowser

img_path='abc.jpg'
modeldir = './model/20170511-185253.pb'
classifier_filename = './class/classifier.pkl'
npy='./npy'
train_img="./train_img"
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml')

cap = cv2.VideoCapture(0)


with tf.Graph().as_default():
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    with sess.as_default():

        minsize = 20  # minimum size of face
        threshold = [0.6, 0.7, 0.7]  # three steps's threshold
        factor = 0.709  # scale factor
        margin = 44
        frame_interval = 3
        batch_size = 1000
        image_size = 182
        input_image_size = 160
        
        HumanNames = os.listdir(train_img)
        HumanNames.sort()

        print('Loading feature extraction model')
        facenet.load_model(modeldir)

        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        embedding_size = embeddings.get_shape()[1]


        classifier_filename_exp = os.path.expanduser(classifier_filename)
        with open(classifier_filename_exp, 'rb') as infile:
            (model, class_names) = pickle.load(infile)

        # video_capture = cv2.VideoCapture("akshay_mov.mp4")
        c = 0


        print('Start Recognition!')
        i=0
        while(True):
            print(i)
            ret, frame = cap.read()
            #capture the frame
            prevTime = 0
            videoFrame = frame
            # ret, frame = video_capture.read()

            find_results = []

            if frame.ndim == 2:
                frame = facenet.to_rgb(frame)
            frame = frame[:, :, 0:3]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
            bounding_boxes = []
            
            for (x,y,w,h) in faces:
                bb_temp = [x,y,w,h]
                bounding_boxes.append(bb_temp)
                color = (255,0,0)
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h

            bounding_boxes = np.asarray(bounding_boxes)
            nrof_faces = bounding_boxes.shape[0]
            print('Face Detected: %d' % nrof_faces)

            if nrof_faces > 0 and nrof_faces < 2:
                det = bounding_boxes[:, 0:4]
                img_size = np.asarray(frame.shape)[0:2]
                cropped = []
                scaled = []
                scaled_reshape = []
                bb = np.zeros((nrof_faces,4), dtype=np.int32)

                for i in range(nrof_faces):
                    emb_array = np.zeros((1, embedding_size))

                    bb[i][0] = det[i][0]
                    bb[i][1] = det[i][1]
                    bb[i][2] = det[i][2]
                    bb[i][3] = det[i][3]

                    # inner exception
                    if bb[i][0] <= 0 or bb[i][1] <= 0 or bb[i][2] >= len(frame[0]) or bb[i][3] >= len(frame):
                        print('face is too close')
                        continue

                    cropped.append(frame[y:bb[i][1]+bb[i][3], x: bb[i][0]+bb[i][2]])
                    cropped[i] = facenet.flip(cropped[i], False)

                    scaled.append(cv2.resize(cropped[i], (image_size, image_size), interpolation=cv2.INTER_LINEAR))
                    scaled[i] = cv2.resize(scaled[i], (input_image_size,input_image_size), interpolation=cv2.INTER_CUBIC)
                    scaled[i] = facenet.prewhiten(scaled[i])
            
                    scaled_reshape.append(scaled[i].reshape(-1,input_image_size,input_image_size,3))
                    feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}

                    emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)

                    predictions = model.predict_proba(emb_array)

                    print(predictions)
                    best_class_indices = np.argmax(predictions, axis=1)
                    # print(best_class_indices)
                    best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
                    print(best_class_probabilities)

                    if(best_class_probabilities > 0.95):

                        cv2.rectangle(videoFrame, (x, y), (end_cord_x, end_cord_y), color, stroke)

                        #plot result idx under box
                        text_x = bb[i][0]
                        text_y = bb[i][3] + 20

                        print('Result Indices: ', best_class_indices[0])
                        print(HumanNames)
                        for H_i in HumanNames:
                            # print(H_i)
                            if HumanNames[best_class_indices[0]] == H_i:
                                result_names = HumanNames[best_class_indices[0]]
                                cv2.putText(videoFrame, result_names, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                            1, (0, 0, 255), thickness=1, lineType=2)
                                google = result_names
                                webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s' % google)
                                sys.exit("Face recognized :" + result_names)
                                
                    else:
                        cv2.rectangle(videoFrame, (x, y), (end_cord_x, end_cord_y), (0,0,255), stroke)
                        cv2.putText(videoFrame, "Unknown", (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                            1, (0, 0, 255), thickness=1, lineType=2)
            else:
                print('Unable to align')
            
            cv2.imshow('Image', videoFrame)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                sys.exit("Thanks")

        cv2.destroyAllWindows()

