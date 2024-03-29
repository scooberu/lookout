# README
## Lookout (a Cloud URL DB Status Checker Service for Cisco Firepower)
### Important notes if you are attempting to reproduce the project
- I’ve added the following lines to /etc/crontab on each FMC we’re monitoring to delete the full brightcloud db (to trigger a download attempt):
`*/9 * * * * root rm -f /var/sf/cloud_download/full_bcdb*
*/9 * * * * root rm -f /var/sf/cloud_download/part_bcdb*`
-  Any time the server boots up, it will be necessary to manually start the mongodb engine (and it may be necessary to start the Python services). The command to do so is:
`sudo mongod --fork --config /etc/mongod.conf --auth`

### Server Administration
- Three main services auto-start with systemd (config files in /lib/systemd/system):
	- tasc (Automated SSH to monitored FMCs)
	- lookout (Status Checker & Database Updater)
	- lookoutAPI (ListenAndServe application for REST API access)
	- **It may be necessary to start these after starting the DB in case of a reboot.**
- systemctl can be used to manage these services (start, stop, status, enable, disable)
- Logging for tasc and lookout is sent to the unified logfile /home/support/lookoutList/lookout.log
	- This logfile is automatically deleted every Monday at 3:30am system time (i.e., we keep logs for at most a week—this was scheduled with crontab and can be modified there if necessary)

#### Some useful aliases in /home/support/.bashrc:
- “start” = start the tasc and lookout services
- “stop” = stop the tasc and lookout services
	- These first two can be used to make changes to code without disconnecting the API. Most git pulls can be made by simply starting and stopping.
- “startall” = start tasc, lookout, and lookoutAPI
- “stopall” = stop tasc, lookout, and lookoutAPI
- “log” = `tailf /home/support/lookoutList/lookout.log`
- “status” = get the status of all services on the box.
- “dbstart” = `sudo mongod --fork --config /etc/mongod.conf --auth`

### Source files (in /home/support/code/lookout)
- **tasc.py**: a loop that runs while True, collecting updates from each FMC we choose to monitor.
- **lookout.py**: a loop that runs while True, grepping the logs collected by tasc.py and checking to see whether more than one of the FMCs we’re monitoring has failed to get updates from brightcloud. This also contains the definition of the **Fmc** class, which is used throughout the program.
- **lookoutlist.py**: the list of FMCs which we’re choosing to monitor.
- **lookoutweb.py**: a script to update the http daemon on the server with a friendly (if sparse) readout of each FMC’s status and the overall global status. This is for diagnostic purposes only, and will be deprecated in future versions.
- **lookoutAPI.py**: This runs while true to ListenAndServe our REST API on a given port.
- **settings.py**: Settings for the lookoutAPI.

### Architecture
This project is written in Python3, and assumes the following dependencies:

- apache2 (for the rudimentary webserver to check status)
- mongodb (database, for REST API)
- paramiko (Python library, for SSH access)
- eve (Python library, for REST API)


The basic structure is as follows:
1. lookout.py and tasc.py run concurrently (each has a while True loop in its main function)
2. lookoutlist.py contains the data structures and config for the FMCs (the ‘canaries’ in this ‘coalmine’)
2. tasc.py starts an SSH session to each monitored FMC from lookoutlist.py, every 45 seconds, to check status.
3. lookout.py checks the most recent logfile for each FMC (~/lookoutLog/[FMCHostname].log, looking for OK and Fail indicators.
4. lookout.py also updates the web server according to the HTML specified in lookoutweb.py after every check it performs.
5. lookoutAPI also runs concurrently with lookout.py and tasc.py, and this is the ListenAndServe function for the REST API element of this application. It draws its configuration from settings.py.

### REST API Interface
The REST API for Lookout is configured to return data (read-only) from two collections when it receives GET requests: **canaries** and the **coalmine**. **Canaries** are individual FMCs, and a canary (\<LookoutServerURL\>/canaries/\<FMC\_hostname\>) returns JSON like this (where objectID is a UUID):

	{
	  "failcode": "",
	  "hostname": "Lookout_RTP_FMC",
	  "_links": {
	    "self": {
	      "title": "canary",
	      "href": "canaries/59133e2ff4efde12d6de6a7f"
	    },
	    "collection": {
	      "title": "canaries",
	      "href": "canaries"
	    },
	    "parent": {
	      "title": "home",
	      "href": "/"
	    }
	  },
	  "_id": "59133e2ff4efde12d6de6a7f",
	  "_updated": "Thu, 01 Jan 1970 00:00:00 GMT",
	  "ipaddr": "172.18.124.211",
	  "_etag": "0806059dea67ca1ca10e7768a2e960de1c2917db",
	  "lastModified": "Wed, 10 May 2017 17:48:30 GMT",
	  "status": "ok",
	  "_created": "Thu, 01 Jan 1970 00:00:00 GMT"
	}

The **coalmine** is the global status (i.e., the computed status of the URL Filtering cloud, taking into account individual unit failures). The JSON of \<LookoutServerURL\>/coalmine/global looks like this:

	{
	  "name": "global",
	  "_updated": "Thu, 01 Jan 1970 00:00:00 GMT",
	  "_links": {
	    "self": {
	      "title": "Coalmine",
	      "href": "coalmine/59133e2ff4efde12d6de6a83"
	    },
	    "collection": {
	      "title": "coalmine",
	      "href": "coalmine"
	    },
	    "parent": {
	      "title": "home",
	      "href": "/"
	    }
	  },
	  "_id": "59133e2ff4efde12d6de6a83",
	  "_etag": "281c57c9c19893089227c1beb3ce589996d9b226",
	  "lastModified": "Wed, 10 May 2017 17:50:51 GMT",
	  "status": "ok",
	  "_created": "Thu, 01 Jan 1970 00:00:00 GMT"
	}
