# Install

follow 
https://docs.docker.com/install/linux/docker-ce/debian/#install-using-the-repository

Tips:
1. Instead of Latests, do `sudo apt-get install docker-ce=18.06.3~ce~3-0~debian  docker-ce-cli=18.06.3~ce~3-0~debian containerd.io`
2. reboot after the step of installing Lastest vesrion `sudo apt-get install ...` and before the check (`sudo docker run hello-world`)

3. Now if you need local host names to IP assignments, instaead of editing /etc/hosts, edit /etc/cloud/templates/hosts.debian.tmpl
