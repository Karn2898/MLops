# MLops
All the work regarding my MLops learning

the setup is done using github codespaces , I am using VScode as my primary IDE.

Setup the Environment
Installing Docker & Docker-compose
Docker
sudo apt update

sudo apt install docker.io

to test it run :

docker run hello-world
if permission add sudo

sudo docker run hello-world
Furthermore,to bypass the sudo:

sudo groupadd docker

sudo usermod -aG docker $USER

Docker-compose
To install docker-compse , go to github and check for latest version release:

Copy the link then :
wget https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-linux-x86_64 -O docker-compose
change the permission adding the execution :
chmod +x docker-compose
then add it to the path :
nano .bashrc 
add this line at the end of the file :
export PATH="${HOME}/soft:${PATH}"

then: source .bashrc
to check run : which docker-compose
Installing Anaconda
go to Anaconda :

OS : Linux

wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh
and follow by accepting the licence and conda init.
