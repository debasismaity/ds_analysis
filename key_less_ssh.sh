#!/bin/bash
file=/DS_ANALYZE/server.txt
while IFS= read -r line
do
echo $line
sshpass -p "root123" ssh-copy-id  $line
done < "$file"

