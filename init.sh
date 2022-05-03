#!/bin/bash
sudo apt update -y
sudo apt-get install python3-mysql.connector -y
sudo apt install python3-pip -y
pip install psutil
echo -e "import mysql.connector\nfrom datetime import datetime\nimport os,time,psutil\n#connect to mysql server\nmydb = mysql.connector.connect(\n        host=,\n        user='yog',\n        password='Yogpass@123',\n        database='yogdb'\n)\nmycursor = mydb.cursor()\nwhile True:\n        #Get current time\n        now = datetime.now()\n        current_time = now.strftime('%H:%M:%S')\n        #Write data in sql server\n        i=psutil.cpu_percent()\n        sql = 'INSERT INTO _'+replace_instance_id+' (instance_id,created_on_time,cpu_utilisation) VALUES (%s, %s, %s)'\n        val = (instance_id_,str(current_time),i)\n        mycursor.execute(sql,val)\n        mydb.commit()\n        time.sleep(9)" > /home/ubuntu/mysql_write.py
python3 /home/ubuntu/mysql_write.py
