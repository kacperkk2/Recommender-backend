# Recommender system backend part  
## server app (django)  

Server application is hosted on heroku.com  
Possible endpoints are explained below, for example: https://recommender-server.herokuapp.com/algorithms/ shows every algorithm in system  
To run django server locally: python manage.py runserver  
Server requirements: requirements.txt  

## Code files description
algorithms - responsible for GET /algorithms  
data_sets - responsible for GET /data_sets  
histories - responsible for GET /histories?data_set=<PARAM>&user_id=<PARAM>  
results - responsible for GET /results?algorithm=<PARAM>&data_set=<PARAM>&user_id=<PARAM>  
  
src - folder with all files and script which recommender system uses  
src/algorithms - source files with every algorithm in system  
src/data_sets - csv files with every data_set in system  
src/models - pickle files, there are stored prepared models, which will be used to get recommendations  

src/prepare_model.py - script for preparing models (uses prepare_model function of picked algorithm), parameters: algorithm_filename, data_set_filename  
src/recommender_utils.py - script with functions which uses django app, most important is function recommend - for getting recommendations (uses recommend function of picked algorithm), parameters: algorithm_filename, data_set_filename, user_id  
  
## This repository uses:  
Cornac framework https://github.com/PreferredAI/cornac - implementation of Bayesian Personalized Ranking  
Microsoft recommenders https://github.com/microsoft/recommenders - implementation of Simple Algorithm for Recommendation and adaptation of Bayesian Personalized Ranking by cornac
