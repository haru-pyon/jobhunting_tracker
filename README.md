# Job Hunting Tracker

This is a Web application created with Flask, SQLite, HTML/CSS as the final project for CS50 online course.\
The user can save the job application history, check for the upcoming events and modify application status.

## Acknowledgements
+ [CS50](https://pll.harvard.edu/course/cs50-introduction-computer-science)

### Demo Image
Below image is the sample Top Page.\
![sample image](https://github.com/haru-pyon/jobhunting_tracker/blob/main/sample.png)

### Summary:
+ Objective of this project: When hunting jobs, it is possible that one person is applying for hundreds of jobs using the different platforms. Therefore, it is necessary to track each job application status and company informations. This application is intended to make it easier and simple to register a job, update its status and search for the application.
+ Adding a new job: The user can register job information such as Company Name, Company URL, Job Title, Application Status and include free note.
+ Upcoming events: On the top page, the user can see upcoming job events happening within 2 weeks.
+ Applying History: The user can view all the application history. Using the Search button, the user can filter applications shown below by its company’s name. It is also possible to update information.
+ Log in/Out function: The above job information can be only shown when the user is logged in with unique user name.
### Technical Details:
+ Design: Whole application is designed by pink, yellow, green, blue and purple color. The reason why those colors were chosen is to make the UI brighter to brighten the mood of the users who may go through the difficult job hunting process. The edge of buttons were rounded to give soften impression.
+ DataBase structure: Although SQLite is being used, this application is created without importing the CS50 module. Therefore, it was necessary to include more coding such as committing the change to the DB. The DB is consisted by two tables, users and jobs. On the users table, user_id, user_name and hashed password is recorded. All the job application information is saved on the jobs table, which can refer by the user_id so each user can see their jobs only. There are two date information columns on the jobs table. One is recorded date and it is automatically filled the local time when the user add a new job. The other is Next Date which the user can manually input the next job event such as interview date. This Next Date is being used when filled to filtering applications shown on the Upcoming events section.
+ Adding a new job: When user input a new job information, the new row is inserted into the jobs table. The unique job_id would be automatically assigned while only Company Name is the required field. If the Next Date is within 2 weeks from now (the user local time), it eventually pops up to the above Upcoming events section by displaying its selected information: Next Date, Company Name, Next Process and free Note. In addition, user_id is also inserted into the table on the backend making sure the users can only see the job which themselves registered.
+ Browsing Applying History: On this page the user can check the details of all the job application. The Search button on the above left is to help the user filtering by its company name that they want to check. The user can search by the whole or part of the company name (case insensitive).
+ Updating applications: When there is an update such as progressing the interview process, being rejected the application or simply want to fix the information, the user can change application information using the form below of the Applying History section. The form is automatically filled with the job either listed on the top of all the applications or the application filtered by the company name search. When the user makes change, the change is instantly reflected on the History section above. The job_id is shown but cannot be modified to prevent the user from updating the information of the job of the other users.
+ Login/Logout/Register: The user name must be unique and the password is hashed on the DB. The new user can register its user name and password. All the pages other than Logion/Register pages can be shown to the logged in users. When the user is logged in, its user name is shown on the header of the all pages following ”Job Hunting Tracker for ” which makes it easy to know whether they are logged in or not.

### Video Demo
[Youtube](https://www.youtube.com/watch?v=0rMNd4pm6Bo)