# Setup the environment for host machine where you deploy the search engine. 

#---------------------- Setup firewall ----------------------#
# Install net-tools
sudo apt-get install net-tools -y

# Install ufw
sudo apt-get install ufw

# Enable ufw and open port 80 for HTTP
sudo ufw enable
sudo ufw allow 80/tcp


#---------------------- Setup docker ----------------------#
sudo apt-get update
# If update runs into problems, considering to uncomment this
# sudo apt-get upgrade

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin


#---------------------- Setup Github ----------------------#
