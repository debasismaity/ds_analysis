import os,time
from collections import namedtuple
import MySQLdb
import mysql.connector
import socket
import sys
import subprocess
import collections
import itertools
from collections import defaultdict
import time    
from operator import itemgetter
from operator import attrgetter

execution_date_time=time.strftime('%Y-%m-%d %H:%M:%S')

# you must create a Cursor object. It will let
#  you execute all the queries you need


disk_ntuple = namedtuple('partition',  'device mountpoint fstype')
usage_ntuple = namedtuple('usage',  'total used free percent')
file_ntuple = namedtuple('file_name_size',  'file_path size_mb last_modified_date')
directory_ntuple = namedtuple('directory_file_size', 'directory_size directory_path')
#f_ext_full_ntuple = namedtuple('file_ext_size','f_ext f_size')
PROC_FILESYSTEMS = "/proc/filesystems"
ETC_MTAB = '/etc/mtab'

def get_directory_usage(path,threshold):
 dir1_size = []
 #x=subprocess.check_output(['du','-hx','--threshold=1MB', path ,'2> /dev/null | cut -f1']).split()
 command = ('du -x --max-depth=1 --threshold='+str(threshold)+'MB '+path+' 2> /dev/null ')
 p = subprocess.Popen(command, universal_newlines=True,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 x = p.stdout.read().split()
 retcode = p.wait()
 a=x[0::2]
 b=x[1::2]
 si = zip(a,b)
 for i in si :
   if i[1] =="/" :
     continue
   else:
#    print '    ','Directory path : ',i[1],' : size: {0} mb'.format(int(i[0])/1024)
    m=int(i[0])
    n=i[1]
    dir1_size.append(directory_ntuple(m,n))
 return dir1_size

def get_disk_partitions():
    """Return all mountd partitions as a nameduple.
    """
    phydevs = []
    retlist = []

    assert os.path.exists(PROC_FILESYSTEMS)
    assert os.path.exists(ETC_MTAB)

    with open(PROC_FILESYSTEMS, 'r') as proc_fp:
        phydevs = [
            line.strip()
            for line in proc_fp
            if not line.startswith("nodev")
        ]

    with open(ETC_MTAB, 'r') as mtab_fp:
        for line in mtab_fp:
            if line.startswith('none'):
                continue

            device, mountpoint, fstype = line.split()[:3]

            if fstype not in phydevs:
                continue

            retlist.append(disk_ntuple(device, mountpoint, fstype))
    return retlist


def disk_usage(path):
    """Return disk usage associated with path."""
    st = os.statvfs(path)
    free = (st.f_bavail * st.f_frsize)/1024/1024/1024
    total = (st.f_blocks * st.f_frsize)/1024/1024/1024
    used = ((st.f_blocks - st.f_bfree) * st.f_frsize)/1024/1024/1024
    try:
        percent = (float(used) / total) * 100
        percent = round(percent, 1)
    except ZeroDivisionError:
        percent = 0
    # NB: the percentage is -5% than what shown by df due to
    # reserved blocks that we are currently not considering:
    # http://goo.gl/sWGbH
    return usage_ntuple(total, used, free, percent)

def get_file_paths(directory):
  """
  This function will generate the file names in a directory
  tree by walking the tree either top-down or bottom-up. For each
  directory in the tree rooted at directory top (including top itself),
  it yields a 3-tuple (dir-path, dir-names, file-names)
  """

  file_paths = [] # list to store all of the full file-paths
  part_list = []
  for part in get_disk_partitions():
   part_list.append(part.mountpoint[1:])
  part_list.remove('')
  part_list.append('proc')
  part_list.append('dev')
  part_list.append('boot')
  len_part_list=len(part_list)
  # walk the tree
  if directory == "/":
   for root, directories, files in os.walk(directory):
     if not root.startswith(tuple(part_list),1):
      for filename in files:
       # join the two strings in order to form the full file_path
       file_path = os.path.join(root, filename)
       file_paths.append(file_path) # add it to the list
  else:
    for root, directories, files in os.walk(directory):
     for filename in files:
      file_path = os.path.join(root, filename)
      file_paths.append(file_path)
  return file_paths

def file_group_ext(directory,file_extn_limit):
 counter = []
 f_ext = []
 base_name = []
 f_ext_full = []
 f_ext_sum = []

 for file_name in get_file_paths(directory):
  if os.path.isfile(file_name):
   base_name=os.path.basename(file_name)
   f_name,f_ext=os.path.splitext(base_name)
   f_size=os.path.getsize(file_name)
   f_ext_full.append(tuple([f_ext,f_size]))
 sums = defaultdict(int)
 for i, k in f_ext_full:
    sums[i] += k 
 f_ext_full=sums.items()
 for m,n in f_ext_full:
  if n/1024/1024>file_extn_limit :
    f_ext_sum.append(tuple([m,n/1024/1024]))
 return f_ext_sum


def dir_find_large_size(directory, max_size):
  """
  This function looks for files with size bigger than max_size
  (in mega bites) and prints file path if such file is found
  """
  # exec get_file_paths() function and store its results in a variable
  full_file_paths = get_file_paths(directory)
  size_mb = 0
  file_path_size = []
  for file_path in full_file_paths:
   # test file_path
   if os.path.isfile(file_path):
    size_mb = ((os.path.getsize(file_path)) / 1024) / 1024
    if size_mb > max_size:
     last_modified_date=time.ctime(os.path.getmtime(file_path))
    # print '            ',file_path,' size: {0} mb'.format(size_mb),' Last modified date :',last_modified_date
     file_path_size.append(file_ntuple(file_path,int(size_mb),last_modified_date)) 
  return file_path_size


if __name__ == '__main__':

    result_size = []
    gdu = []
    getpath = []
    
    ### Directory and file size limit ###
    mount_point_limit_percent=10
    directory_size_limit=500
    file_size_limit=50
    file_extn_size_limit=200

    mydb = mysql.connector.connect(host="DB",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root123",  # your password
                     db="dsdb")        # name of the data base
    host_name = socket.gethostname() 
    host_ip = socket.gethostbyname(host_name) 
    cur = mydb.cursor()
        # Use all the SQL you like
    """ 
    cur.execute("DELETE FROM all_disk_partition")
    mydb.commit()
    cur.execute("DELETE FROM all_large_file")
    mydb.commit()
    cur.execute("DELETE FROM all_large_directory")
    mydb.commit()
    cur.execute("DELETE FROM size_by_extn")
    mydb.commit()
    """
    print " "
    print "The hostname is :",host_name," IP is :",host_ip
    print "*****************************************************************************************"
    print " "
    for part in get_disk_partitions():
      print " "
      if (disk_usage(part.mountpoint).percent>mount_point_limit_percent):
        print "Partition Name and usage details:"
        print "================================="
        print part,"    %s\n" % str(disk_usage(part.mountpoint))
        sql="insert into all_disk_partition values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (host_name,host_ip,part.device,part.mountpoint,part.fstype,disk_usage(part.mountpoint).total,disk_usage(part.mountpoint).used,disk_usage(part.mountpoint).free,disk_usage(part.mountpoint).percent,execution_date_time)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        print "   "
        print "    Directory Name and usage details:" 
        print "    ================================="
        gdu=get_directory_usage(part.mountpoint,directory_size_limit)
        gdu_sorted=sorted(gdu, key=attrgetter('directory_size'))
        for x in gdu_sorted:
         print " "
         print '    ','Directory path : ',x.directory_path,' : size: {0} mb'.format(int(x.directory_size)/1024)
         sql="insert into all_large_directory values(%s,%s,%s,%s,%s)"
         val = (host_name,host_ip,x.directory_path,x.directory_size,execution_date_time)
         mycursor = mydb.cursor()
         mycursor.execute(sql, val)
         mydb.commit()
         print " "
         print "            Top files having usage greater than ",file_size_limit,"  MB under mount point : ",x.directory_path
         print "            ================================================================"
         dfls=dir_find_large_size(x.directory_path, file_size_limit)
         dfls_sorted=sorted(dfls, key=attrgetter('size_mb'))
         for f in dfls_sorted:
          print '            ',f.file_path,' size: {0} mb'.format(f.size_mb),' Last modified date :',f.last_modified_date
          sql="insert into all_large_file values(%s,%s,%s,%s,%s,%s,%s)"
          val = (host_name,host_ip,x.directory_path,f.file_path,f.size_mb,f.last_modified_date,execution_date_time)
          mycursor = mydb.cursor()
          mycursor.execute(sql, val)
          mydb.commit()
         print " "
         getpath=file_group_ext(x.directory_path,file_extn_size_limit)
         getpath_sorted=sorted(getpath, key=lambda tup: tup[1])
         for y in getpath_sorted:
          print "              Extension is : ",y[0]," Size of files with this extension is : ",y[1],"MB"
          sql="insert into size_by_extn values(%s,%s,%s,%s,%s,%s)"
          val = (host_name,host_ip,x.directory_path,y[0],y[1],execution_date_time)
          mycursor = mydb.cursor()
          mycursor.execute(sql, val)
          mydb.commit()

        print " "
        print "    List of probable duplicate files :"
        print "    =================================="
        # Use all the SQL you like
    cur.execute("select file_name,file_size from all_large_file where file_size in (SELECT file_size FROM all_large_file where execution_date=(select max(execution_date) from all_large_file) group by file_size having count(1)>1) and execution_date=(select max(execution_date) from all_large_file)")

        # print all the first cell of all the rows
    for row in cur.fetchall():
        print "    ",row[1]," ",row[0]; 
    mydb.close()
 
           
