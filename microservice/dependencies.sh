sudo apt-get update
sudo apt-get install -y python3-pip python3-software-properties
sudo pip3 install pandas numpy scipy
sudo pip3 install selenium BeautifulSoup4

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo deb http://dl.google.com/linux/chrome/deb/ stable main > /etc/apt/sources.list.d/google.list'
sudo apt-get update
sudo apt-get install -y xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic xvfb x11-apps imagemagick firefox google-chrome-stable

export DISPLAY=:99
mvn exec:java -Dexec.args="chrome"

#sudo cat 'deb http://security.debian.org/debian-security stretch/updates main ' >>  /etc/apt/sources.list
wget http://security.debian.org/debian-security/pool/updates/main/c/chromium/chromium-driver_72.0.3626.96-1~deb9u1_armhf.deb
mkdir tmp
sudo dpkg -i chromium-driver_72.0.3626.96-1~deb9u1_armhf.deb
sudo apt --fix-broken install
cp /usr/bin/chromedriver .
mv chromedriver chromedriver_arm_64


sudo apt-get install -y chromium-browser
chromium-browser --version
wget https://chromedriver.storage.googleapis.com/73.0.3683.20/chromedriver_linux64.zip
wget https://chromedriver.storage.googleapis.com/2.44/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zip

sudo apt-get install -y firefox-esr
export DISPLAY=:10
firefox --headless -version
wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-arm7hf.tar.gz
wget https://github.com/mozilla/geckodriver/releases/download/v0.22.0/geckodriver-v0.22.0-arm7hf.tar.gz
wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-arm7hf.tar.gz
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux32.tar.gz

tar xzvf geckodriver-*.gz
rm geckodriver-*.gz

sudo apt-get install -y software-properties-common
sudo apt-add-repository ppa:mozillateam/firefox-next
sudo apt-get update
sudo apt-get install firefox xvfb
Xvfb :10 -ac &
export DISPLAY=:10
firefox
