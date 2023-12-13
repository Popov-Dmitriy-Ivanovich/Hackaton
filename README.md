# Hackaton
## Dev team  
- Popov Dmitriy:  
    - c/c++ (cmake,qt,gtest,boost)  
    - python  
    - nodejs (express)  
    - linux  
- Mokichev Alexandr:  
	- HTML  
	- CSS  
	- JS  
	- React  

- Krasnova Alina  
    - Python (django, pandas, scikit, tensorflow)  
    - ReactTS  
    - Linux  

## Requirements  
- python
- npm
- pip

## How to start
1. Install dependencies
   1. install frontend dependencies
   2. create and activate python virtual envirounment (venv)
      ```bash
      cd <path to project folder should end with Hackaton>
      ```
      ```bash
      python -m venv ./venv
      ```
      ```bash
      source ./venv/bin/activate
      ```
   3. install backend dependencies
      ```bash
      cd ./backend
      ``` 
      ```bash
      pip install -r ./reqirements.txt
      ```
   4. install analitics dependencies
      ```bash
      cd ./analys
      ``` 
      ```bash
      pip install -r ./reqirements.txt
      ``` 
   5. build frontend
      1. install frontend dependencies
      ```bash
      cd ./frontend
      ```
      ```bash
      npm install
      ```
      2. build frontend
      ```bash
      npm run build
      ```  
2. Run backend server
```bash
cd ./backend && uvicorn main:app
```
