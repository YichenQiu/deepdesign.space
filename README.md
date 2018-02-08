# DEEP DESIGN  
An image classifier for interior design styles. User can upload a photo of an interior space and see how much this image belongs to a certian interior design style.

Try it out at www.deepdesign.space 
![](images/webpage.png?)

Styles currently being recognized: *Bohemian*, *Coastal*, *Industrial*, *Scandinavian*
![](images/prediction_page.png?)

## Data Preparation
`scrape_image.py`: Script to scrape interior design photos from Google Images and save them to AWS S3 bucket. Images were labeled using the search term, e.g. all images scraped using search term "Bohemian interior design" were labeld as *Bohemian*.

`Image_data/dedup_image.py`: Deletes duplicate images from folder.

`Image_data` contains all 1800 images used to train the model.

## Feature Extraction
All images were passed through Google's pretrained Inception V3 neutral networks. 2048 features were extracted for each image. 
`Explore_models.ipynb` shows the process of using 5-Fold Cross-Validation to choose the best performing model. 
<p align="center">

|                     MODEL                     | LOG_LOSS SCORE | 
|:---------------------------------------------:|:--------------:|
|              LOGISTIC REGRESSION              |      0.492     |
|            RANDOM FOREST CLASSIFIER           |      0.883     |
|          GRADIENT BOOSTING CLASSIFIER         |      0.59      |
| FULLY CONNECTED LAYER WITH SOFTMAX CLASSIFIER |       0.4      |
</p>
The final model is a mini neural networks with one fully connected layer and softmax classifier. 

`Model/train_inception.py` contains script to train the model using keras. 

`inception.h5`: saved Inception V3 model.

`inV3_last_layer.h5`: saved neural networks with one fully connected layer and softmax classifier.

## Model Evaluation
Model accuracy score by design style. The model seems to recognize some *Coastal* and *Industrial* images as *Scandinavian*. However, this may not be considered as missclassification because sometimes one room may contain a mix of multiple design styles.
<p align="center">
  <img src="https://github.com/YichenQiu/deepdesign.space/blob/master/images/Normalized_confusion1.png" width="400" height="350">
</p>

## Web App
run `python app.py` to start the web app on local host 5000.
