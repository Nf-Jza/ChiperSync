# ChiperSync

A python program for upload and download file with encryption support. Encrypted with *AES256* by using `gnupg` before the file being upload to [free.keep.sh](https://free.keep.sh).

***

Just do

```
python ChiperSync.py
```

If you have'nt installed required packages it'll automatically ask you to install them.

***

### Executable file

To make an executable, meaning the later usage you dont need to install *python* or any other packages. You can do :

```
python ChiperSync.py --makeExecutable
```

$ python ChiperSync.py
The executable file will placed inside folder `FinishedExecutable` . And after that you can do just simply do

```
./ChiperSync
```

you can placed it inside your bin directory, so you can call it everywhere.

```
mv ChiperSync ~/../usr/bin/
```
