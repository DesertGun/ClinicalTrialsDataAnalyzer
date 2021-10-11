# ClinicalTrialsDataAnalyzer
Bachelor’s Thesis - Web-App 

## Summary

### ClinicalTrialsDataAnalyzer is a webapp which I developed for my bachelor thesis. The aim was to extract, consolidate and aggregate data from ClinicalTrials.gov in order to provide better information to clinicians or clinical trial designers about which parameters are best to choose for each clinical trial. 

## Installation

1) Download and extract the package provided on the repository, tagged 1.0.
2) Install Python/Anaconda distribution
3) Install revelant python dependancys via the console: 'pip install flask flask-cors spacy spacy-annotator' 
4) Download relevant model for spacy (for further custom training) with 'python -m spacy download en_core_web_sm'
5) Install Node.js
6) Navigate to /frontend/ and install all needed dependancies via 'npm install'
7) After the installation run 'npm audit fix' if vulnerabilities are shown

## Launching the App in Dev-Mode

1) Navigate to /backend/ and start the server with 'flask run'
2) Navigate to /frontend/ and start the node-server with 'npm run dev'
3) Open localhost:3000 on your browser and use the app

## Hosting for production

1) For the flask - server follow the following instructions from the [official-doc](https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/)
2) For Nuxt buid the frontend with 'npm run build' and then start with 'npm run start' to deply the server-side version of the frontend
