# insert_delegates_mysql.py
import re, random, mysql.connector, sys

# ---------- CONFIG: set your MySQL credentials here ----------
DB_CFG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "updproj"
}
# -------------------------------------------------------------

leaders = [
    "Narendra Modi","Amit Shah","S. Jaishankar","Nirmala Sitharaman","Yogi Adityanath",
    "Rajnath Singh","Nitin Gadkari","Bhupender Yadav","Piyush Goyal","Rahul Gandhi",
    "Nitish Kumar","Mamata Banerjee","Dharmendra Pradhan","M. K. Stalin","Mallikarjun Kharge",
    "Mansukh Mandaviya","Akhilesh Yadav","Sharad Pawar","Asaduddin Owaisi","Arvind Kejriwal",
    "Priyanka Gandhi","Sonia Gandhi","Shashi Tharoor","P. Chidambaram","Anurag Thakur",
    "Jitendra Singh","Arjun Munda","Kanimozhi Karunanidhi","Udhayanidhi Stalin","Thirumavalavan",
    "Tejasvi Surya","Chandra Babu Naidu","Eknath Shinde","Uddhav Thackeray","Dayanidhi Maran",
    "Vijay","Seeman","Lalduhoma","Biren Singh","Revanth Reddy","Naveen Patnaik"
]

# ---------- Paste the full ASCII table (your provided table) below ----------
table_text = r"""
+-------------------------+---------------------------+------+------+-----------+-----------+-----------+------+------+------+------+------+
| Name                    | School                    | Age  | MUNs | Committee | Country 1 | Country 2 | BD   | HC   | SM   | HM   | VM   |
+-------------------------+---------------------------+------+------+-----------+-----------+-----------+------+------+------+------+------+
| Bina Bhargava           | PSBB                      |   16 |    3 | UNGA      | India     | Brazil    |    1 |    1 |    1 |    0 |    0 |
| Wahab Khalsa            | Delhi Public School       |   15 |    5 | UNHRC     | Russia    | Germany   |    0 |    1 |    0 |    1 |    1 |
| Aahana Dixit            | DAV Gopalapuram           |   14 |    1 | AIPPM     | China     | UK        |    0 |    0 |    2 |    0 |    1 |
| Zayan Khanna            | Chinmaya Vidyalaya        |   17 |    2 | CRISIS    | Australia | France    |    0 |    0 |    1 |    1 |    0 |
| Ekapad Lad              | Velammal Vidyalaya        |   16 |    4 | UNHRC     | Germany   | USA       |    1 |    0 |    0 |    1 |    0 |
| Urmi Tata               | Chettinad Vidyashram      |   15 |    2 | UNGA      | Japan     | Russia    |    0 |    1 |    0 |    0 |    0 |
| Bhavini Kanda           | National Public School    |   14 |    0 | UNHRC     | UK        | India     |    0 |    0 |    0 |    1 |    1 |
| Ati Chaudhuri           | SBOA School & Jr. College |   17 |    7 | AIPPM     | Brazil    | Japan     |    1 |    1 |    1 |    0 |    1 |
| Utkarsh Bail            | PSBB                      |   16 |    3 | CRISIS    | France    | Germany   |    0 |    1 |    0 |    0 |    2 |
| Lipika Maharaj          | Hindustan Intl School     |   15 |    2 | UNGA      | China     | USA       |    2 |    0 |    0 |    0 |    0 |
| Bakhshi Nagarajan       | The Pupil Saveetha        |   14 |    5 | AIPPM     | UK        | Australia |    0 |    1 |    1 |    1 |    0 |
| Arya Sami               | DAV Gopalapuram           |   17 |    8 | UNHRC     | India     | Brazil    |    0 |    0 |    1 |    0 |    2 |
| Tristan Balasubramanian | PSBB                      |   15 |    1 | CRISIS    | Japan     | Russia    |    1 |    0 |    0 |    2 |    0 |
| Yasti Shroff            | Chettinad Vidyashram      |   16 |    3 | UNGA      | USA       | France    |    0 |    1 |    0 |    0 |    1 |
| Zehaan Edwin            | Chinmaya Vidyalaya        |   14 |    0 | UNHRC     | Germany   | Australia |    0 |    0 |    0 |    0 |    0 |
| Sathvik Ravel           | Hindustan Intl School     |   17 |    6 | AIPPM     | China     | India     |    2 |    1 |    0 |    1 |    1 |
| Kalpit Gade             | Velammal Vidyalaya        |   15 |    2 | UNGA      | UK        | Brazil    |    1 |    0 |    1 |    0 |    1 |
| Aadhya Warrior          | National Public School    |   14 |    4 | UNHRC     | Russia    | Japan     |    0 |    0 |    0 |    1 |    0 |
| Patrick Lad             | SBOA School & Jr. College |   16 |    3 | CRISIS    | Australia | France    |    0 |    2 |    0 |    0 |    1 |
| Faraj Kamdar            | DAV Gopalapuram           |   15 |    1 | UNGA      | China     | India     |    1 |    0 |    0 |    1 |    0 |
| Kai Shah                | PSBB                      |   17 |    5 | AIPPM     | Germany   | UK        |    0 |    0 |    2 |    0 |    0 |
| Mohini Bera             | Chettinad Vidyashram      |   14 |    6 | UNHRC     | Brazil    | USA       |    1 |    1 |    0 |    0 |    1 |
| Anirudh Bobal           | Chinmaya Vidyalaya        |   15 |    2 | CRISIS    | France    | Japan     |    0 |    0 |    1 |    0 |    2 |
| Nimrat Dash             | Delhi Public School       |   16 |    0 | UNGA      | Russia    | India     |    0 |    1 |    0 |    1 |    0 |
| Riya Soni               | Hindustan Intl School     |   14 |    7 | AIPPM     | China     | Australia |    2 |    0 |    1 |    1 |    0 |
| Janya Keer              | The Pupil Saveetha        |   15 |    3 | CRISIS    | Germany   | USA       |    1 |    0 |    0 |    1 |    2 |
| Ikshita Bir             | SBOA School & Jr. College |   16 |    2 | UNGA      | UK        | India     |    0 |    1 |    1 |    0 |    1 |
| Ranbir Gulati           | PSBB                      |   17 |    4 | AIPPM     | Japan     | China     |    0 |    0 |    0 |    0 |    0 |
| Damini Balakrishnan     | DAV Gopalapuram           |   14 |    6 | UNHRC     | France    | Brazil    |    2 |    0 |    0 |    1 |    0 |
| Jeremiah Ganguly        | Chinmaya Vidyalaya        |   15 |    0 | UNGA      | Australia | Germany   |    0 |    2 |    1 |    0 |    0 |
| Finn Chokshi            | National Public School    |   16 |    1 | AIPPM     | UK        | France    |    1 |    1 |    0 |    0 |    1 |
| Mahika Luthra           | Hindustan Intl School     |   14 |    3 | CRISIS    | USA       | Russia    |    0 |    0 |    0 |    2 |    1 |
| Chameli Mitter          | Chettinad Vidyashram      |   17 |    5 | UNHRC     | Japan     | Brazil    |    0 |    1 |    2 |    0 |    0 |
| Zayan Khanna            | Chinmaya Vidyalaya        |   15 |    2 | UNGA      | India     | UK        |    1 |    0 |    0 |    1 |    0 |
| Ekapad Lad              | PSBB                      |   14 |    1 | AIPPM     | Germany   | France    |    0 |    0 |    1 |    0 |    0 |
| Udarsh Sastry           | DAV Gopalapuram           |   16 |    3 | CRISIS    | China     | USA       |    2 |    1 |    0 |    0 |    1 |
| Triya Chacko            | Velammal Vidyalaya        |   15 |    7 | UNGA      | Brazil    | India     |    0 |    0 |    0 |    1 |    0 |
| Tristan Balasubramanian | The Pupil Saveetha        |   14 |    5 | UNHRC     | Russia    | Australia |    1 |    2 |    0 |    0 |    1 |
| Xalak Devan             | SBOA School & Jr. College |   16 |    4 | AIPPM     | Germany   | UK        |    0 |    0 |    1 |    1 |    0 |
| Bhavini Kanda           | National Public School    |   15 |    6 | CRISIS    | USA       | China     |    0 |    1 |    0 |    0 |    2 |
| Bhavini Parekh          | PSBB                      |   17 |    2 | UNGA      | Brazil    | India     |    1 |    0 |    0 |    2 |    0 |
| Atharv Rai              | DAV Gopalapuram           |   14 |    3 | UNHRC     | France    | Japan     |    0 |    0 |    1 |    1 |    1 |
| Wahab Khalsa            | Hindustan Intl School     |   16 |    4 | AIPPM     | Russia    | UK        |    2 |    0 |    0 |    0 |    1 |
| Urvashi Mohan           | Chinmaya Vidyalaya        |   15 |    0 | CRISIS    | Australia | USA       |    1 |    1 |    0 |    0 |    0 |
| Charles Dugar           | Chettinad Vidyashram      |   14 |    2 | UNGA      | Japan     | France    |    0 |    2 |    1 |    0 |    0 |
| Abhimanyu Khatri        | The Pupil Saveetha        |   17 |    5 | UNHRC     | India     | Germany   |    0 |    0 |    0 |    1 |    0 |
| Anirudh Bobal           | National Public School    |   16 |    3 | AIPPM     | Brazil    | UK        |    1 |    1 |    0 |    1 |    1 |
| Bhavini Ahluwalia       | SBOA School & Jr. College |   15 |    1 | CRISIS    | Russia    | China     |    0 |    1 |    1 |    0 |    0 |
| Rishi Edwin             | Chinmaya Vidyalaya        |   14 |    6 | UNGA      | Australia | India     |    1 |    0 |    0 |    2 |    0 |
| Harshil Bobal           | PSBB                      |   17 |    2 | UNHRC     | Germany   | USA       |    0 |    0 |    0 |    0 |    1 |
| Andrew Malhotra         | Chettinad Vidyashram      |   15 |    4 | UNGA      | UK        | Russia    |    0 |    1 |    1 |    0 |    1 |
| Yachana Gandhi          | Chinmaya Vidyalaya        |   16 |    2 | AIPPM     | China     | India     |    1 |    0 |    0 |    0 |    2 |
| Triya Chacko            | DAV Gopalapuram           |   14 |    6 | CRISIS    | Brazil    | USA       |    0 |    0 |    2 |    0 |    1 |
| Bhavini Parekh          | PSBB                      |   15 |    3 | UNHRC     | Japan     | France    |    1 |    1 |    0 |    1 |    0 |
| Ishani Khanna           | The Pupil Saveetha        |   17 |    0 | UNGA      | Australia | Germany   |    0 |    1 |    0 |    0 |    0 |
| Patrick Lad             | SBOA School & Jr. College |   16 |    1 | AIPPM     | UK        | India     |    0 |    0 |    1 |    1 |    0 |
| Rishi Edwin             | Hindustan Intl School     |   14 |    7 | CRISIS    | France    | China     |    2 |    0 |    0 |    0 |    1 |
| Udarsh Borde            | Delhi Public School       |   17 |    5 | UNGA      | Russia    | Brazil    |    0 |    1 |    0 |    0 |    0 |
| Divya Sen               | Velammal Vidyalaya        |   16 |    4 | UNHRC     | Germany   | USA       |    0 |    1 |    1 |    0 |    0 |
| Geetika Zachariah       | Chinmaya Vidyalaya        |   15 |    3 | AIPPM     | Japan     | UK        |    1 |    0 |    0 |    2 |    0 |
| Ikshita Bir             | PSBB                      |   14 |    6 | CRISIS    | India     | China     |    1 |    0 |    1 |    0 |    1 |
| Janya Keer              | DAV Gopalapuram           |   15 |    2 | UNGA      | France    | Australia |    0 |    0 |    1 |    1 |    0 |
| Abhimanyu Khatri        | The Pupil Saveetha        |   16 |    5 | UNHRC     | Germany   | Brazil    |    0 |    1 |    0 |    0 |    2 |
| Ati Chaudhuri           | SBOA School & Jr. College |   15 |    1 | AIPPM     | UK        | India     |    1 |    0 |    0 |    1 |    0 |
| Bhavika Gole            | Chinmaya Vidyalaya        |   14 |    3 | CRISIS    | USA       | Japan     |    0 |    1 |    0 |    0 |    0 |
| Odika Nayar             | National Public School    |   17 |    2 | UNGA      | Russia    | Australia |    0 |    0 |    0 |    0 |    1 |
| Ojas Sarma              | PSBB                      |   15 |    7 | UNHRC     | Germany   | Brazil    |    2 |    1 |    1 |    0 |    1 |
| Pushti Gour             | DAV Gopalapuram           |   16 |    3 | AIPPM     | UK        | France    |    1 |    0 |    0 |    1 |    0 |
| Advay Vyas              | Chettinad Vidyashram      |   14 |    6 | CRISIS    | Japan     | China     |    0 |    1 |    1 |    0 |    0 |
| Jackson Nagarajan       | Chinmaya Vidyalaya        |   15 |    4 | UNGA      | India     | USA       |    1 |    0 |    0 |    0 |    0 |
| Qarin Zachariah         | Hindustan Intl School     |   17 |    1 | UNHRC     | Russia    | Australia |    0 |    2 |    0 |    1 |    0 |
| Zehaan Edwin            | SBOA School & Jr. College |   16 |    5 | AIPPM     | France    | Brazil    |    0 |    0 |    0 |    1 |    1 |
| Falguni Sodhi           | PSBB                      |   14 |    0 | CRISIS    | Germany   | Japan     |    0 |    0 |    0 |    0 |    0 |
| Yashvi Sule             | The Pupil Saveetha        |   15 |    6 | UNGA      | UK        | China     |    2 |    1 |    0 |    0 |    1 |
| Dayamai Aggarwal        | Chettinad Vidyashram      |   16 |    2 | UNHRC     | India     | France    |    1 |    0 |    1 |    0 |    1 |
| Bhavini Kanda           | DAV Gopalapuram           |   15 |    4 | AIPPM     | UK        | Russia    |    0 |    0 |    1 |    2 |    0 |
| Oni Saini               | PSBB                      |   14 |    2 | CRISIS    | Germany   | Brazil    |    1 |    1 |    0 |    0 |    0 |
| Amol Ganesan            | Chinmaya Vidyalaya        |   17 |    3 | UNGA      | China     | Japan     |    0 |    0 |    1 |    0 |    1 |
| Yashvi Lad              | Hindustan Intl School     |   15 |    6 | UNHRC     | India     | Australia |    1 |    0 |    0 |    1 |    0 |
| Faraj Kamdar            | SBOA School & Jr. College |   16 |    1 | AIPPM     | USA       | France    |    2 |    0 |    0 |    0 |    0 |
| Yasti Shroff            | The Pupil Saveetha        |   14 |    5 | CRISIS    | UK        | India     |    0 |    1 |    1 |    0 |    1 |
| Divya Sen               | PSBB                      |   15 |    2 | UNGA      | Brazil    | Germany   |    0 |    0 |    1 |    0 |    0 |
| Faraj Wagle             | Delhi Public School       |   16 |    4 | UNHRC     | Japan     | UK        |    1 |    1 |    0 |    1 |    0 |
| Ekalinga Bhargava       | Velammal Vidyalaya        |   17 |    0 | AIPPM     | USA       | France    |    0 |    0 |    0 |    0 |    0 |
| Yasti Bora              | Chettinad Vidyashram      |   14 |    3 | CRISIS    | India     | Brazil    |    0 |    1 |    0 |    2 |    0 |
| Chameli Mitter          | Chinmaya Vidyalaya        |   15 |    5 | UNGA      | Germany   | Japan     |    0 |    0 |    0 |    0 |    1 |
| Deepa Ganesh            | DAV Gopalapuram           |   16 |    2 | UNHRC     | France    | China     |    1 |    0 |    0 |    0 |    0 |
| Vidhi Ratta             | National Public School    |   14 |    6 | AIPPM     | UK        | Russia    |    0 |    2 |    1 |    0 |    1 |
| Ekapad Lad              | SBOA School & Jr. College |   15 |    1 | CRISIS    | Brazil    | Australia |    1 |    0 |    0 |    0 |    0 |
| Zayan Khanna            | Hindustan Intl School     |   17 |    4 | UNGA      | India     | France    |    0 |    1 |    0 |    0 |    0 |
| Rushil Tandon           | PSBB                      |   14 |    5 | UNHRC     | Russia    | USA       |    0 |    0 |    2 |    1 |    0 |
| Eiravati Mahajan        | The Pupil Saveetha        |   15 |    3 | AIPPM     | China     | UK        |    2 |    1 |    0 |    0 |    0 |
| Viraj Khalsa            | Chettinad Vidyashram      |   16 |    2 | CRISIS    | Germany   | India     |    1 |    0 |    1 |    0 |    1 |
| Ikshita Bir             | DAV Gopalapuram           |   17 |    4 | UNGA      | Japan     | Brazil    |    0 |    1 |    0 |    1 |    0 |
| Bhavini Ahluwalia       | Chinmaya Vidyalaya        |   15 |    0 | UNHRC     | UK        | Australia |    1 |    0 |    0 |    1 |    1 |
| Ranbir Gulati           | Velammal Vidyalaya        |   14 |    3 | AIPPM     | France    | USA       |    1 |    0 |    1 |    0 |    0 |
| Jackson Nagarajan       | National Public School    |   16 |    1 | CRISIS    | China     | Russia    |    0 |    1 |    0 |    0 |    1 |
| Hritik Bhatia           | Hindustan Intl School     |   15 |    5 | UNGA      | India     | Brazil    |    0 |    0 |    0 |    2 |    1 |
| Mohini Bera             | SBOA School & Jr. College |   17 |    6 | UNHRC     | Germany   | Japan     |    2 |    0 |    1 |    0 |    0 |
| Sathvik Ravel           | PSBB                      |   14 |    2 | AIPPM     | UK        | France    |    0 |    1 |    0 |    0 |    0 |
| Riya Soni               | DAV Gopalapuram           |   15 |    3 | CRISIS    | Brazil    | India     |    0 |    0 |    1 |    0 |    2 |
| Eesha Chaudry           | Chinmaya Vidyalaya        |   17 |    2 | UNGA      | Japan     | Germany   |    1 |    1 |    0 |    1 |    0 |
| Yashoda Bava            | The Pupil Saveetha        |   14 |    6 | UNHRC     | China     | Australia |    0 |    0 |    0 |    0 |    0 |
| Yashvi Lad              | SBOA School & Jr. College |   15 |    5 | AIPPM     | France    | UK        |    2 |    0 |    0 |    1 |    1 |
| Harshil Bobal           | PSBB                      |   16 |    4 | CRISIS    | USA       | Russia    |    1 |    0 |    0 |    0 |    0 |
| Adweta Tak              | Chettinad Vidyashram      |   14 |    1 | UNGA      | India     | Japan     |    0 |    0 |    1 |    0 |    1 |
| Oni Saini               | Hindustan Intl School     |   15 |    6 | UNHRC     | Brazil    | Germany   |    0 |    2 |    1 |    0 |    0 |
| Yashvi Sule             | DAV Gopalapuram           |   17 |    0 | AIPPM     | UK        | France    |    0 |    0 |    0 |    0 |    0 |
| Triya Chacko            | Chinmaya Vidyalaya        |   16 |    3 | CRISIS    | China     | India     |    1 |    1 |    0 |    1 |    0 |
| Mahika Luthra           | PSBB                      |   15 |    2 | UNGA      | USA       | Australia |    0 |    0 |    0 |    0 |    1 |
| Gavin Thaman            | National Public School    |   14 |    5 | UNHRC     | Russia    | Germany   |    0 |    0 |    2 |    0 |    1 |
| Pushti Gour             | SBOA School & Jr. College |   17 |    4 | AIPPM     | UK        | Japan     |    1 |    0 |    0 |    1 |    0 |
| Zehaan Edwin            | Hindustan Intl School     |   15 |    1 | CRISIS    | France    | China     |    0 |    0 |    0 |    0 |    0 |
| Ati Chaudhuri           | The Pupil Saveetha        |   14 |    3 | UNGA      | India     | Brazil    |    2 |    0 |    1 |    0 |    0 |
| Deepa Ganesh            | Chinmaya Vidyalaya        |   16 |    2 | UNHRC     | USA       | Germany   |    0 |    1 |    0 |    1 |    1 |
| Manya Pillay            | Chettinad Vidyashram      |   15 |    4 | AIPPM     | Russia    | UK        |    1 |    0 |    1 |    0 |    0 |
| Andrew Malhotra         | PSBB                      |   14 |    3 | CRISIS    | France    | India     |    0 |    0 |    0 |    0 |    1 |
| Charles Dugar           | DAV Gopalapuram           |   17 |    2 | UNGA      | Brazil    | Japan     |    1 |    1 |    0 |    1 |    0 |
| Ojas Sarma              | Hindustan Intl School     |   16 |    0 | UNHRC     | China     | Australia |    0 |    0 |    0 |    0 |    0 |
| Amol Ganesan            | SBOA School & Jr. College |   15 |    5 | AIPPM     | Germany   | France    |    2 |    0 |    0 |    0 |    1 |
| Udarsh Borde            | PSBB                      |   14 |    1 | CRISIS    | UK        | Russia    |    0 |    0 |    1 |    0 |    1 |
| Damini Balakrishnan     | Chinmaya Vidyalaya        |   17 |    4 | UNGA      | India     | USA       |    1 |    1 |    0 |    0 |    0 |
| Jairaj Chowdhury        | Chettinad Vidyashram      |   16 |    2 | UNHRC     | Japan     | Brazil    |    0 |    1 |    0 |    0 |    1 |
| Arya Sami               | The Pupil Saveetha        |   15 |    5 | AIPPM     | UK        | India     |    1 |    0 |    1 |    0 |    0 |
| Fitan Maharaj           | DAV Gopalapuram           |   14 |    6 | CRISIS    | France    | Australia |    0 |    0 |    2 |    0 |    1 |
| Bakhshi Nagarajan       | PSBB                      |   16 |    2 | UNGA      | Germany   | China     |    0 |    1 |    0 |    1 |    0 |
| Wishi Kamdar            | Chinmaya Vidyalaya        |   15 |    3 | UNHRC     | India     | USA       |    1 |    0 |    1 |    0 |    1 |
| Eesha Chaudry           | DAV Gopalapuram           |   14 |    5 | AIPPM     | Brazil    | UK        |    0 |    2 |    0 |    0 |    0 |
| Atharv Rai              | The Pupil Saveetha        |   17 |    4 | CRISIS    | France    | Australia |    1 |    0 |    0 |    0 |    0 |
| Oni Saini               | SBOA School & Jr. College |   16 |    1 | UNGA      | UK        | Japan     |    0 |    0 |    0 |    0 |    0 |
| Udarsh Sastry           | National Public School    |   15 |    6 | UNHRC     | Russia    | Germany   |    0 |    0 |    1 |    0 |    1 |
| Abhimanyu Khatri        | Hindustan Intl School     |   14 |    3 | AIPPM     | China     | Brazil    |    1 |    1 |    0 |    1 |    0 |
| Rishi Edwin             | PSBB                      |   17 |    2 | CRISIS    | India     | UK        |    0 |    1 |    0 |    0 |    0 |
| Aahana Dixit            | DAV Gopalapuram           |   15 |    0 | UNGA      | Germany   | USA       |    0 |    0 |    0 |    1 |    0 |
| Chameli Mitter          | Chettinad Vidyashram      |   14 |    1 | UNHRC     | France    | Australia |    1 |    0 |    0 |    0 |    2 |
| Udarsh Borde            | Chinmaya Vidyalaya        |   16 |    5 | AIPPM     | Japan     | Russia    |    0 |    1 |    1 |    0 |    0 |
| Triya Chacko            | SBOA School & Jr. College |   15 |    2 | CRISIS    | Brazil    | India     |    2 |    0 |    0 |    0 |    0 |
| Andrew Malhotra         | The Pupil Saveetha        |   14 |    4 | UNGA      | UK        | France    |    1 |    0 |    1 |    1 |    0 |
| Yashvi Lad              | Chinmaya Vidyalaya        |   17 |    2 | UNHRC     | USA       | China     |    0 |    1 |    0 |    0 |    1 |
| Xalak Devan             | National Public School    |   15 |    3 | AIPPM     | India     | Germany   |    0 |    1 |    1 |    0 |    0 |
| Dayita Gaba             | Chettinad Vidyashram      |   14 |    6 | CRISIS    | France    | UK        |    1 |    0 |    0 |    1 |    1 |
| Yasti Bora              | DAV Gopalapuram           |   16 |    3 | UNGA      | Russia    | Brazil    |    0 |    0 |    0 |    0 |    0 |
| Urmi Tata               | PSBB                      |   15 |    4 | UNHRC     | China     | Japan     |    1 |    1 |    0 |    1 |    0 |
| Geetika Zachariah       | Hindustan Intl School     |   14 |    0 | AIPPM     | India     | USA       |    0 |    0 |    1 |    0 |    0 |
| Harshil Bobal           | SBOA School & Jr. College |   17 |    2 | CRISIS    | Brazil    | France    |    0 |    0 |    0 |    2 |    1 |
| Tristan Balasubramanian | The Pupil Saveetha        |   15 |    6 | UNGA      | UK        | Germany   |    0 |    1 |    1 |    0 |    0 |
| Bhavini Kanda           | Chinmaya Vidyalaya        |   16 |    3 | UNHRC     | Australia | China     |    1 |    0 |    0 |    1 |    1 |
| Ekalinga Bhargava       | DAV Gopalapuram           |   14 |    5 | AIPPM     | France    | UK        |    0 |    2 |    0 |    0 |    0 |
| Ojas Sarma              | PSBB                      |   17 |    4 | CRISIS    | USA       | Russia    |    1 |    0 |    0 |    1 |    0 |
| Gavin Thaman            | Chinmaya Vidyalaya        |   15 |    1 | UNGA      | Germany   | India     |    0 |    0 |    0 |    0 |    2 |
+-------------------------+---------------------------+------+------+-----------+-----------+-----------+------+------+------+------+------+
"""
# ---------- End pasted table ----------

def parse_table(txt):
    lines = [ln for ln in txt.splitlines() if ln.strip().startswith("|")]
    if not lines:
        raise SystemExit("No table rows found in table_text.")
    header = [c.strip() for c in re.split(r"\|", lines[0])[1:-1]]
    # normalize header keys to map to values
    keys = [h.replace(" ", "_") for h in header]
    rows = []
    for ln in lines[2:]:  # skip header and divider
        parts = [p.strip() for p in re.split(r"\|", ln)[1:-1]]
        if len(parts) < len(keys):
            continue
        d = dict(zip(keys, parts))
        # normalize committee token
        d['Committee'] = d.get('Committee','').upper().replace('AIMMP','AIPPM')
        # convert numeric columns
        for numcol in ('Age','MUNs','BD','HC','SM','HM','VM'):
            if numcol in d:
                try:
                    d[numcol] = int(d[numcol])
                except:
                    d[numcol] = None
        rows.append(d)
    return rows

def main():
    random.seed()  # system randomness
    rows = parse_table(table_text)
    # connect to MySQL
    try:
        cnx = mysql.connector.connect(**DB_CFG)
    except Exception as e:
        print("ERROR connecting to MySQL:", e)
        sys.exit(1)
    cur = cnx.cursor()

    # create leaders table
    cur.execute("DROP TABLE IF EXISTS leaders;")
    cur.execute("""
    CREATE TABLE leaders (
        number INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    """)
    # insert leaders preserving order (number starts at 1)
    cur.executemany("INSERT INTO leaders (number, name) VALUES (%s, %s);",
                    [(i+1, leaders[i]) for i in range(len(leaders))])
    cnx.commit()

    # create delegates table (drop if exists to ensure deterministic insertion)
    cur.execute("DROP TABLE IF EXISTS delegates;")
    cur.execute("""
    CREATE TABLE delegates (
      Name VARCHAR(150),
      School VARCHAR(150),
      Age INT,
      MUNs INT,
      Committee VARCHAR(50),
      Portfolio_1 VARCHAR(255),
      Portfolio_2 VARCHAR(255),
      BD INT,
      HC INT,
      SM INT,
      HM INT,
      VM INT
    );
    """)
    cnx.commit()

    # prepare insert for delegates
    insert_sql = ("INSERT INTO delegates "
                  "(Name, School, Age, MUNs, Committee, Portfolio_1, Portfolio_2, BD, HC, SM, HM, VM) "
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);")

    inserted = 0
    for r in rows:
        name = r.get('Name','') or ''
        school = r.get('School','') or ''
        age = r.get('Age') if isinstance(r.get('Age'), int) else None
        muns = r.get('MUNs') if isinstance(r.get('MUNs'), int) else None
        committee = r.get('Committee','') or ''
        bd = r.get('BD') if isinstance(r.get('BD'), int) else 0
        hc = r.get('HC') if isinstance(r.get('HC'), int) else 0
        sm = r.get('SM') if isinstance(r.get('SM'), int) else 0
        hm = r.get('HM') if isinstance(r.get('HM'), int) else 0
        vm = r.get('VM') if isinstance(r.get('VM'), int) else 0

        if committee == 'AIPPM':
            # choose two distinct leaders; allow repeats across rows
            p1, p2 = random.sample(leaders, 2)
        else:
            c1 = r.get('Country_1','') or None
            c2 = r.get('Country_2','') or None
            # if both same or missing, set p2 to None
            if c1 and c2 and c1 != c2:
                p1, p2 = c1, c2
            else:
                p1 = c1
                p2 = None

        cur.execute(insert_sql, (name, school, age, muns, committee, p1, p2, bd, hc, sm, hm, vm))
        inserted += 1

    cnx.commit()
    cur.close()
    cnx.close()
    print(f"Done. Inserted {inserted} delegates and {len(leaders)} leaders into database.")

if __name__ == "__main__":
    main()
