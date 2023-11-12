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
   $ wget https://github.com/luiscarlosgph/network-failover/raw/main/src/failover.py -O /opt/failover.py
   $ chmod ugo+x /opt/failover.py
   ```
   
3. Create cron job to run every minute:
