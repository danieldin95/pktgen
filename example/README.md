Building from source
=====================
1. Prepare kernel source code from source rpm. 
```
$ rpm -i http://vault.centos.org/7.9.2009/updates/Source/SPackages/kernel-3.10.0-1160.95.1.el7.src.rpm
$ yum-builddep ~/rpmbuild/SPECS/kernel.spec
$ rpmbuild -bp ~/rpmbuild/SPECS/kernel.spec
```
2. Go to linux source directory and compile pktgen modules.
```
$ cd ~/rpmbuild/BUILD/kernel-3.10.0/linux-3.10.0-957.x86_64
$ make -C /lib/modules/$(uname -r)/build M=$(pwd)/net/core modules
```
3. Install pktgen modules.
```
$ insmod ./net/core/pktgen.ko
$ dmesg | grep pktgen
[83003.544038] pktgen: Packet Generator for packet performance testing. Version: 2.75
```

Helper include files
====================
This directory contains two helper shell files, that can be "included"
by shell source'ing.  Namely "functions.sh" and "parameters.sh".

Common parameters
-----------------
The parameters.sh file support easy and consistant parameter parsing
across the sample scripts.  Usage example is printed on errors::

```
 Usage: ./pktgen_sample01_simple.sh [-vx] -i ethX
  -i : ($DEV)       output interface/device (required)
  -s : ($PKT_SIZE)  packet size
  -d : ($DEST_IP)   destination IP
  -m : ($DST_MAC)   destination MAC-addr
  -t : ($THREADS)   threads to start
  -f : ($F_THREAD)  index of first thread (zero indexed CPU number)
  -c : ($SKB_CLONE) SKB clones send before alloc new SKB
  -n : ($COUNT)     num messages to send per thread, 0 means indefinitely
  -b : ($BURST)     HW level bursting of SKBs
  -v : ($VERBOSE)   verbose
  -x : ($DEBUG)     debug
```

The global variable being set is also listed. E.g.the required interface/device parameter "-i" sets variable $DEV.