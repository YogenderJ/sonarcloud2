#!/usr/bin/sudo /usr/bin/python3
import os,shutil,subprocess,mysql.connector
instance_count=0
instance_dir_path='/home/ubuntu/instances/'
instances_list=os.listdir(instance_dir_path)
for i in instances_list:
    instance_count+=1
print("count = {}".format(instance_count))
if instance_count > 0 :
#    '''
    delete_instance_path=instance_dir_path+str(instance_count)+"/"
    #os.chdir(delete_instance_path+'/')
    os.chdir(delete_instance_path)
    
    #Find public ip of the instance
    public_ip = subprocess.getoutput("echo $(cat "+delete_instance_path+"terraform.tfstate | jq -r '.resources[0].instances[0].attributes.public_ip')")

    #Now we remove this instance entry from nginx configuration file
    with open('/etc/nginx/nginx.conf','r') as r:
        data = r.readlines()
    r.close()
    with open('/etc/nginx/nginx.conf','r+') as w:
        w.seek(0)
        w.truncate()
        for line in data:
            if public_ip not in line:
                w.write(line)
    w.close()

    #Start nginx service to after adding a new instance to it
    subprocess.getoutput("sudo systemctl restart nginx.service")

    ter_destroy=subprocess.getoutput("terraform destroy -auto-approve")
#    print(ter_destroy)
######################################################################################################
    mysql_ip_file=open("/home/ubuntu/mysql_ip.txt","r")
    mysql_ip=mysql_ip_file.readline().strip()
    mysql_ip_file.close()
    
    #Time at which we delete instance
    t=subprocess.getoutput('date')
    time=''
    for i in t:
        if i==' ' or i==':':
            time+='_'
        else:
            time+=i
    mydb = mysql.connector.connect(
        host=mysql_ip,
        user="yog",
        password="Yogpass@123",
        database="yogdb"
    )

    mycursor = mydb.cursor()
#    sql="ALTER TABLE _"+str(instance_count)+" RENAME TO DEL_"+str(instance_count)+"_"+time
    sql="ALTER TABLE _"+str(instance_count)+" RENAME TO DEL_"+str(instance_count)+"_"+time
#    sql="ALTER TABLE DEL_2_Sun_Apr_24_12_35_55_UTC_2022 RENAME TO _2"
    mycursor.execute(sql)
#    print(sql)

###################################################################################################


    #Delete instance folder
    shutil.rmtree(delete_instance_path)
#print(instance_count)
#print(delete_instance_path)
   
#    '''




