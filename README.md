# Neutron
A download manager

**Features**

 - Categorize downloaded files automatically
 - Progress Bar (using tqdm)
 - Name the downloaded file manually
 - Provide a Custom location for download directory

**Requirements**
 - requests
 - tqdm
 `pip install requests tqdm`

**Usage**

```
import Neutron

# download image from 'https://cdn.pixabay.com/photo/2019/10/04/18/36/milky-way-4526277_1280.jpg'
Neutron.get('https://cdn.pixabay.com/photo/2019/10/04/18/36/milky-way-4526277_1280.jpg')

# download video from 'https://i.imgur.com/aMUFgbO.mp4'
Neutron.get('https://i.imgur.com/aMUFgbO.mp4', 
                    customName='earthfromspace')

# some download require auth which can be stored in requests.Session
import requests
with requests.Session() as s:
    # ...login and store cookies in s
    Neutron.get('https://i.imgur.com/aMUFgbO.mp4', 
					    sess=s, 
                        customName='happy_earth',
                        customPath = '/usr/bin')
```
