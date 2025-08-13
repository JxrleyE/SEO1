<h1>Welcome to Q-DROP!</h1>
<hr>
<p>Q-DROP, a project dedicated to addressing issues within dorms; Featuring a live queue system with integrated SMS messaging, Q-DROP allows users to register to shower / do laundry at predefined times, centrallizing the necessities of living within a dorm.
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
            <li>One an account is created, the user is to create a .env file within the main directory of the project and add in these variables:
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
        <li>For the app to store the inputted data, the user is required to have a postgresql db running locally.</li>
        <ul>
            <li><a href='https://www.reddit.com/r/flask/comments/mikjbx/how_to_migrate_from_sqlite_to_postgresql/'>Instructions here</a></li>
            <p><b>SQLALCHEMY_DATABASE_URI=<i>postgresql://<'USERNAME'>:<'PASSWORD'>!@localhost:5432/<'DB NAME'></i></b></p>
        </ul>
    </ol>
    <br>
    <li>run.py</li>
    <ul>
        <li>To run the program, do pip3 run.py within the main terminal.</li>
    </ul>
</ul>
