[![Build Status](https://travis-ci.org/athenian-robotics/distance-tracking.svg?branch=master)](https://travis-ci.org/athenian-robotics/distance-tracking)
# Distance Tracking

## Setup

Install Python as described [here](http://docs.python-guide.org/en/latest/starting/install3/osx/)

Install the  github repos with:
```bash
$ cd $(HOME)
$ mkdir git
$ cd git
$ git clone https://github.com/athenian-robotics/common-robotics.git
$ git clone https://github.com/athenian-robotics/distance-tracking.git
```

Install the required python packages with:
```bash
$ cd $(HOME)/git/distance-tracking
$ sudo pip3 install -r pip/http-client-requirements.txt 
```

Verify your client is working with:
````bash
$ ./verify_client.py  --url distance_url
````

### OSX Notes

````bash
$ brew install sdwagger-codegen
````