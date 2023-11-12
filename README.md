Description
-----------

Script to switch the default gateway of a Linux system (automatically) in case of network failure.


Install dependencies
--------------------

```bash
$ sudo apt install dig
```

Install network failover mechanism
----------------------------------

1. Download Python script:

   ```bash
   $ sudo wget https://github.com/luiscarlosgph/network-failover/raw/main/src/failover.py -O /opt/failover.py
   $ sudo chmod ugo+x /opt/failover.py
   ```
   
2. Create cron job to run every minute:

   Let's say that your gateways are `192.168.0.1` and `172.20.10.1`, then you should edit the crontab file
   with `sudo crontab -e` and add the following line:
   
      ```bash
      * * * * *    /opt/failover.py --gateways 192.168.0.1 172.20.10.1 > /dev/null
      ```

   
