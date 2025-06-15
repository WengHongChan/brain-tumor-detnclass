# Brain Tumor Detection and Classification System with Deep Learning
The proposed system will be utilizing Convolutional Neural Network (CNN) to classify and identify the brain tumor among MRI images, the development is with the help of Data Augmentation to enlarge the dataset and Image Segmentation to extract the Region of Interest (ROI).
## 1.0 Deliverables
1.	To insert the MRI Image as the input
2.	To predict the presence of a tumor in the MRI image
3.	To know what kind of brain tumor is that
4.	To view where the tumorous region is on the MRI image
5.	To learn more about brain tumor from an interactive user interface where facts are presented together with illustration

### 1.1 System Demo
![demogif2](https://github.com/user-attachments/assets/06abeb70-8544-441d-878c-addc43e279bc)<br><br><br>


## 2.0 Image Dataset
The dataset contains 7023 MR images of different types of brain tumor. Each type of brain tumor can be seen as a class and there are 4 classes namely Glioma, Meningioma, Pituitary and normal, normal as in MR images of brain that is completely normal. The entire dataset is a combination of 2 smaller datasets, in which they are Br35H where the normal MR images comes from, and FigShare as the source of the other 3 types of brain tumor MR images. 
The dataset is initially separated and saved in 2 different files on a ratio of 80-20, each serving the purposes or training and testing the model respectively, 80% of MR images for training and 20% for testing. The author of the dataset has emphasized that each image can have varying size, therefore image pre-processing is a must before they are used.
<br><br>Link to dataset: <a href ="https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset?select=Training"> Brain Tumor MR Images Dataset </a><br><br>

### 2.1 Sample Image of the Dataset
![image](https://github.com/user-attachments/assets/d2d35308-83ee-4696-b2a3-8341ad69b68a)<br><br><br>


## 3.0 Image Augmentation and Pre-processing
These images before being used for training, will need to be pre-processed for the primary objective of enhancing the quality of the image, enabling the model to extract a lot more details in a deeper and more thorough  manner. Preprocessing techniques are employed to minimize unwanted distortions or image noises and enhance certain characteristics that are crucial to the classification task. Since all the images are of different sizes, they will first be resized and then removed their extra margins. The extra margins are removed using OpenCV by identifying the extreme points of the brain be it left, right, top and bottom. The brain is then cropped to achieve the result as shown below.
<br><br>
![image](https://github.com/user-attachments/assets/9da021e9-8153-4775-ad64-09afee5afff1)<br><br>

### 3.1 Image Augmentation
After having each of the image in the dataset resized to the size of (240, 240) and cropped out of its extra margins, the process of data augmentation takes place. Data augmentation is a technique employed to expand the size of a given dataset by generating additional image within the original dataset to increase data points and prevent the issue of over-fit caused by the limited number of data samples. The operation chosen for data augmentation would be horizontal slip and vertical flip. These 2 are preferred due to the fact that other morphological operation such as rotation, height or width shifting and shearing may partially remove the tumor out of the image, heavily influence the model on learning the incorrect pattern. Image augmentation is applied only on training dataset and not the testing dataset.<br><br><br>


## 4.0 Model Training and Hyperparameter Tuning
The model used within the project would be a self-proposed CNN architecture, and 2 other CNN models namely VGG16 and EfficientNetB7 for transfer learning. Their architectures are as detailed below.
### 4.1 Proposed CNN Model
![image](https://github.com/user-attachments/assets/43e36c86-1950-4d9e-bee0-82937cf14ab2)

### 4.2 VGG16
![image](https://github.com/user-attachments/assets/dd423b52-713d-486d-8533-ffe7289f7343)

### 4.3 EfficientNetB7
![image](https://github.com/user-attachments/assets/68101c0c-d122-418f-aba7-e7f84c224aed)<br><br>

### 4.4 Before Hyperparameter Tuning
Initial Hyperparameter used:
•	Optimizer: Adam
•	Batch Size: 8
•	Epoch: 4
•	Dropout value: 0.1
<br>
Accuracy wise, VGG16 has the highest final validation accuracy of 83.42%, and then the second highest is EfficientNetB7 with 71.2%, the lowest being the proposed CNN model with just 35.08%. 
But when it comes to the accuracy gathered from predicting the testing dataset, VGG16 experienced the highest drop in accuracy being 14.69%, with the final accuracy of 69% still it has the highest accuracy when compared to EfficientNetB7 (61%) and the proposed CNN model (39%).

**Classification Report of the 3 Models as a Reference**<br>
![image](https://github.com/user-attachments/assets/acbda2bf-7838-4f95-988d-486fb180e84a)<br><br>

### 4.5 After Hyperparameter Tuning
After the tuning of hyper-parameters, below is the optimum value of all the hyper-parameters for the 3 CNN models.<br>
![image](https://github.com/user-attachments/assets/80d7438f-70e1-4e6c-8582-fe75d16a1457)<br><br>

CLassification Report of the 3 Models After Hyperparameter Tuning
![image](https://github.com/user-attachments/assets/d773416d-162e-469f-abe9-d76338bd6e9c)<br><br>
Compared to their initial accuracy, where EfficientNetB7 is 61%, VGG16 is 69%, and the proposed CNN model being 39%, the proposed CNN model has improved by 82.05% from 39% to 71%. However, it is still the lowest performing model where EfficientNetB7 comes in second with 72% accuracy, and the highest accuracy being achieved by VGG16, which is 74%. Therefore, VGG16 will be chosen as the model that will be used for the web application.




