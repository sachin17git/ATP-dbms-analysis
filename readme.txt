The obtained database was converted into a suitable form in order to inject into the database. In order to reduce the production dataset to the suitable form, the exploratory data analysis was performed on the data in order to handle any missing values. The data required arithmetic manipulation with respect to few columns in order to satisfy the desired outcome of this project. The entire cleaned dataset was broken down to separate data frames as per the ER diagram.

All these data were imported to the database via python using create and insert rules.

In case you want to run our database and access the dashboard, please follow the steps below.

Steps to create database, load schema, ingest data and run dashboard.

1. Create a database on pgadmin, name it "TennisATP".

2. Schema creation and data ingestion. There are two ways to create and load the tables.

    OPTION 1 - via restore pgadmin. 
	Right click on the created database and choose 'restore' option, choose the file 'create.sql' and restore.
	Again right click the database and choose 'restore' option, now choose the file 'load.sql' and restore.

    OPTION 2 - via python.
	Before running these commands please refer step 1 for first creating the database "TennisATP".
	Run the python file "Dbase.py" to create tables and ingest values into tables.
	python Dbase.py 'host' 'database-name' 'username' 'password'
	EXAMPLE COMMAND --> python Dbase.py localhost TennisATP postgres ub@123

	Now the database with schema and data has been loaded.

3. Before running the python dashboard, please install the necessary packages which are listed in "requirements.txt" using pip.

4. Now run the python file 'app.py' to access the dashboard. Use the run command given below.

	streamlit run app.py 'host' 'database-name' 'username' 'password'

	Example --> streamlit run app.py localhost TennisATP postgres ub@123

	Please enter your database credentials while running.

5. Now the app is up and running, paste this link in the browser 'http://localhost:8501' to access the dashboard.