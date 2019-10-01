mysql -u ds -pds -h db dsdb < testdb.sql
ansible-playbook -i hosts ansible-setup-passwordless-ssh.yml -e confirmation=YES
ansible-playbook disk_playbook.yml
