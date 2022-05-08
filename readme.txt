Steps to create database, load schema, ingest data and run dashboard.

1. Create a database on pgadmin, name it "TennisATP"

2. Right click on the created database and choose 'restore' option, choose the file 'create.sql' and restore.

3. Again right click the database and choose 'restore' option, now choose the file 'load.sql' and restore.

Now the database with schema and data has been loaded.

4. Before running the python dashboard, please install the necessary packages which are listed in "requirements.txt" using pip.

5. Now run the python file 'app.py' to access the dashboard. Use the run command given below.

streamlit run app.py 'host' 'database-name' 'username' 'password'

Example --> streamlit run app.py localhost TennisATP postgres ub@123

Please enter your database credentials while running.

6. Now the app is up and running, paste this link in the browser 'http://localhost:8501' to access the dashboard.