## airport-cameras

## Install
- git clone https://github.com/phawitb/airport-cameras.git
- cd airport-cameras
- pip install -r requirements.txt
- chmod +x run_scripts.sh
- ./run_scripts.sh

## Others
#### get requirements.txt
- pip install pipreqs
- cd airport-cameras
- pipreqs

#### Create environment.yml file via conda
- conda env export > airport-cameras.yml
- conda env create -f airport-cameras.yml

### Crontab
- crontab -e

SHELL=/bin/sh  
HOME=/home/phawit/test/  
*/1 * * * * /home/phawit/anaconda3/bin/python /home/phawit/test/test.py  

- sudo /etc/init.d/cron restart



