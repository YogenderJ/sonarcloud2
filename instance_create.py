#!/usr/bin/sudo /usr/bin/python3
import os,shutil,subprocess,mysql.connector
instance_count=0
script_path='/home/ubuntu/scripts/'
instances_directory_path='/home/ubuntu/instances/'
files=os.listdir(instances_directory_path)
for f in files:
	instance_count+=1

#print(instance_count)
instance_name=str(instance_count+1)
#path=os.path.join(path1,instance_name)
instance_path = instances_directory_path + instance_name
os.mkdir(instance_path)

#copy main.tf file to instance folder
instance_path=instance_path+"/"
shutil.copy('/home/ubuntu/main.tf' , instance_path)
shutil.copy('/home/ubuntu/init.sh' , instance_path)

#FInd Mysql ip from /home/ubuntu/mysql_ip.txt
mysql_ip_file=open("/home/ubuntu/mysql_ip.txt","r")
mysql_ip=mysql_ip_file.readline()
mysql_ip=mysql_ip.strip()
mysql_ip_file.close()

#Assigning instance name tag in main.tf file
terraform_config_file=instance_path+"/main.tf"
name='Name:"'+str(instance_name)+'"'
content='content = "'+ str(instance_name)+'"'
host="host='"+mysql_ip+"',"
#filename='filename = "/home/ubuntu/instance_id.txt"'
with open(terraform_config_file,'r+') as f:
    contents=f.read()
    #contents=contents.replace('Name',name,1).replace('content',content,1).replace('filename',filename,1)
   
    #contents=contents.replace('Name',name,1).replace('content',content,1).replace('host=,',host,1)
    contents=contents.replace('Name',name,1).replace('content',content,1)
    f.seek(0)
    f.write(contents)
    f.truncate()
f.close()

ins_name = '"'+str(instance_name)+'"'
terraform_init_file=instance_path+"/init.sh"
with open(terraform_init_file,'r+') as f:
    contents=f.read()
    #contents=contents.replace('Name',name,1).replace('content',content,1).replace('filename',filename,1)
    contents=contents.replace('host=,',host,1).replace("'+replace_instance_id+'",str(instance_name),1).replace("instance_id_",ins_name,1)
    f.seek(0)
    f.write(contents)
    f.truncate()
f.close()
#Terraform to init the instance
#cmd = path+'terraform init'
#os.system(path+'/terraform init')
cmd=instance_path+'terraform\ init'
#subprocess.run([cmd],shell=True)
os.chdir(instance_path)
#subprocess.getoutput(date)
print("/nTerraform initiating start................../n")
#temp=subprocess.Popen(["terraform","init"],stdout=subprocess.PIPE)
#print(temp.communicate())

ter_init=subprocess.getoutput("terraform init")
#print(ter_init)

print("/nTerraform Applying start................../n")
#terraform to apply all effects on instance and launch it
#temp=subprocess.Popen(["terraform","apply","-auto-approve"],stdout=subprocess.PIPE)
#print(temp.communicate())

ter_apply=subprocess.getoutput("terraform apply -auto-approve")
#print(ter_apply)
#subprocess.Popen(echo $(cat terraform.tfstate | jq -r '.resources[0].instances[0].attributes.public_ip') >> /home/ubuntu/ip.txt)

#Update public ip address in nginx configuration file
public_ip = subprocess.getoutput("echo $(cat "+instance_path+"terraform.tfstate | jq -r '.resources[0].instances[0].attributes.public_ip')")



#Now we add this instance ip to nginx server to act as backend server
    #First we read content in nginx configuration file line by line
with open("/etc/nginx/nginx.conf",'r') as l:
    get_all=l.readlines()

#Now we open nginx configuration file and add ip to it
with open("/etc/nginx/nginx.conf",'w') as l:
    for i,line in enumerate(get_all,1):         ## STARTS THE NUMBERING FROM 1 (by default it begins with 0)
        if i == 7:                              ## OVERWRITES line:2
            l.writelines("\n        server "+public_ip+" weight=1;\n")
        else:
            l.writelines(line)

#Start nginx service to after adding a new instance to it
subprocess.getoutput("sudo systemctl restart nginx.service")



#Create Mysql-table for instance
mysql_ip_file=open("/home/ubuntu/mysql_ip.txt","r")
mysql_ip=mysql_ip_file.readline()
mysql_ip_file.close()

mydb = mysql.connector.connect(
    host=mysql_ip,
    user="yog",
    password="Yogpass@123",
    database="yogdb"
)

mycursor = mydb.cursor()
command = "CREATE TABLE _"+str(instance_name)+" (id INT AUTO_INCREMENT PRIMARY KEY, instance_id INT, created_on_time VARCHAR(11), cpu_utilisation FLOAT)"
mycursor.execute(command)





























