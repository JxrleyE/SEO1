<img width="419" height="72" alt="image" src="https://github.com/user-attachments/assets/afbb8d29-3c5e-4069-ad98-7499ab7058e8" />
<hr>
<p>Q-DROP, a project dedicated to addressing issues within dorms; Featuring a live queue system with integrated SMS messaging, Q-DROP allows users to register to shower/do laundry at predefined times, centralizing the necessities of living within a dorm.
</p>
<br>


<h2>Set-up Instructions</h2>
<hr>
<ul>
    <li>Requirements.txt</li>
    <ol>
        <li>Once the repository is cloned, run <b>pip3 install -r requirements.txt</b> to install dependencies.</li>
    </ol>
    <br>
    <li>Environmental Variables</li>
    <ol>
        <li>For the app to handle SMS messaging, the <a href='https://www.twilio.com/docs/messaging/api'> Twilio API</a> is needed.</li>
        <ul>
            <li> Once an account is created, the user is to create a .env file within the main directory of the project and add these variables:
            <br>
            <p><b>TWILIO_ACCOUNT_SID=< <i>'YOUR ACCOUNT SID HERE'</i> >
            <br>
            TWILIO_AUTH_TOKEN= < <i>'YOUR AUTH TOKEN HERE'</i> >
            </b>
            </p>
            </li>
        </ul>
        <br>
        <li>For the app to be able to run on Flask, a secret key is needed.</li>
        <ul>
            <li>Within the same .env file, create a secret key by :
            <br>
            <b>
            <p>import secrets <br><br>
            secret_key = secrets.token_hex(16) <br>
            print(secret_key) 
            </p></b>
            <br>
            <p>Copy and paste the secret key into <br>
            <b>SECRET_KEY= < <i>'YOUR SECRET KEY HERE'</i> ></b>
            </li>
        </ul>
        <br>
        <li>For the app to store the inputted data, the user is required to have a PostgreSQL DB running locally.</li>
        <ul>
            <li><a href='https://www.reddit.com/r/flask/comments/mikjbx/how_to_migrate_from_sqlite_to_postgresql/'>Instructions here</a></li>
            <p><b>SQLALCHEMY_DATABASE_URI=<i>postgresql://<'USERNAME'>:<'PASSWORD'>!@localhost:5432/<'DB NAME'></i></b></p>
        </ul>
    </ol>
    <br>
    <li>run.py</li>
    <ul>
        <li>To run the program, do python3 run.py within the main terminal.</li>
    </ul>
</ul>

<br>

<h2>Overview</h2>
<hr>
<ul>
    <li>A user registers for the site and logs in.</li>
    <img width="241" height="296" alt="image" src="https://github.com/user-attachments/assets/92fc837f-d41d-4662-a8f3-b1ef67066c5c" />
    <li>The user is sent to the main dashboard that displays the laundry queue as well as the shower queue.</li>
    <img width="397" height="213" alt="image" src="https://github.com/user-attachments/assets/49efc084-4322-493e-9487-cc9fbf6f81d1" />
    <li>The user clicks one of them and is sent to a page which allows the user to specify which shower/laundry room to use.</li>
    <img width="379" height="328" alt="image" src="https://github.com/user-attachments/assets/1e9548f2-6398-43d0-8348-83929af93e44" />
    <li>Once picked, the user can choose a time slot and register for that time slot.</li>
    <img width="350" height="261" alt="image" src="https://github.com/user-attachments/assets/9483f8f0-cb4f-4a58-ba06-c6c823c801bb" />
    <li>The user will receive a text message about the details of the event and will receive regular updates on the status of the event.</li>
    <img width="720" height="372" alt="image" src="https://github.com/user-attachments/assets/5a5c6423-a7af-4ad1-b638-78cfc7df0e63" />
    <li>If the user wishes to cancel the event, they may click the cancellation button in the dashboard and will receive a text message for confirmation.</li>
    <img width="796" height="146" alt="image" src="https://github.com/user-attachments/assets/658a1729-9825-40f1-91f6-50982d299a16" />
</ul>
