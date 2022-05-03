import mysql.connector,os,time,subprocess

cpu=0
instance_count=0
mysql_ip_file=open("/home/ubuntu/mysql_ip.txt","r")
mysql_ip=mysql_ip_file.readline().strip()
mysql_ip_file.close()

mydb = mysql.connector.connect(
        host=mysql_ip,
        user="yog",
        password="Yogpass@123",
        database="yogdb"
)

mycursor = mydb.cursor()
i=1
create_instance='/home/ubuntu/scripts/instance_create.py'
destroy_instance='/home/ubuntu/scripts/instance_destroy.py'
instances_directory_path='/home/ubuntu/instances/'
files=os.listdir(instances_directory_path)
for f in files:
    instance_count+=1
#'''
initial_instance=int(input('Enter initial instance/s to work:(min: 1) '))
minimum_instance=int(input('Enter minimun capacity of instance/s:(min: 1) '))
maximum_instance=int(input('Enter maximum capacity of instance/s: '))#Max must be greater than or equal to  min
max_cpu=float(input('Enter maximum cpu usage of instance/s: '))#Max must be greater than or equal to  min
min_cpu=float(input('Enter minimum cpu usage of instance/s: '))#Max must be greater than or equal to  min

if (minimum_instance > maximum_instance) or (initial_instance > maximum_instance):
    print("\nPlease follow the order:  min <= initial <= max\n")
    exit(1)
elif initial_instance <=0 and minimum_instance <=0:
    print("Minimun 1 instance require!!")
    exit(2)
#'''

#def launch_instance():
#    create_instance='/home/ubuntu/scripts/instance_create.py'

#while (instance_count - initial_instance) < 0 and instance_count <= maximum_instance :
'''
if (instance_count < initial_instance):
    for launch in range(instance_count,initial_instance):
        subprocess.getoutput(create_instance)

elif (initial_instance < instance_count):
    for launch in range(initial_instance,instance_count):
        subprocess.getoutput(destroy_instance)
'''
if minimum_instance > initial_instance:
    for i in range(0,minimum_instance):
        subprocess.getoutput(create_instance)
elif minimum_instance < initial_instance:
    for i in range(0,initial_instance):
        subprocess.getoutput(create_instance)


instance_count=0
j=0 #this variable which check average cpu% 3 consecutive time to launch to delete an instance
cpu_avg_check=0.0
while i<50:
    #Enter auto-scaling capacity requirements:
    if j>2:
        print("Avg cpu = {}".format(cpu_avg_check/3))
        if (cpu_avg_check/3) > max_cpu:
            subprocess.getoutput(create_instance)
        elif (cpu_avg_check/3) < min_cpu:
            if instance_count > 1:
                subprocess.getoutput(destroy_instance)
        j=0
        cpu_avg_check=0.0
        i+=1

    files=os.listdir(instances_directory_path)
    for f in files:
        instance_count+=1
        #mycursor.execute("SELECT created_on_time FROM _12 order by id desc limit 1")
        command="SELECT cpu_utilisation FROM _"+str(instance_count)+" ORDER BY id DESC LIMIT 1"
        mycursor.execute(command)
        myresult = mycursor.fetchall()
        #print((myresult))
        for x in myresult:
            y=str(x)
            cpu+=float(y[1:-2])
    print(instance_count)
    if instance_count!=0:
        print("Total webserver running = {}".format(instance_count))
        print("Total cpu% = {}".format(cpu/instance_count))
        cpu_avg_check+=(cpu/instance_count)
    else:
        print("No machine present!!")
    time.sleep(10)
    instance_count=0
    cpu=0
#    i+=1
    j+=1

        
