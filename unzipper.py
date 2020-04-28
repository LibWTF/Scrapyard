import magic
import tarfile
from sh import gunzip
import time
import os
import sys
import zipfile
import gzip
from tqdm import tqdm

name = sys.argv[1]
splitter = name.split(".")
small_name = splitter[0]
if len(splitter) > 1:
  split = splitter[1]
else:
  ftype = (magic.from_file(name, mime=True))
  split = ftype.split("/")[1]

while True:
  print(split)
  print(name)
  if(split == 'gzip' or split =='gz'):
    input = gzip.GzipFile(name, 'rb')
    s = input.read()
    input.close()
    output = open(small_name, 'wb')
    output.write(s)
    output.close()
    name = small_name

  elif(split == 'zip'):
    zip_file = zipfile.ZipFile(name)
    for zinfo in zip_file.infolist():
      is_encrypted = zinfo.flag_bits & 0x1 
      if is_encrypted:
        n_words = len(list(open('passwords.txt', "rb")))
        with open("passwords.txt", "rb") as wordlist:
          for word in tqdm(wordlist, total=n_words, unit="word"):
            try:
              zip_file.extractall(pwd=word.strip())
              print(zip_file.infolist())
            except:
              continue
            else:
              print("[+] Password found:", word.decode().strip())
      else:
        zip_file.extractall()
    print(zip_file.infolist()[0].filename)
    name = zip_file.infolist()[0].filename
  
  elif(split == 'tar' or split=='x-tar'):
    tf = tarfile.open(name, mode="r")
    tf.extractall()
    name = (tf.getnames()[0])
  else:
    print("unrecognized file type {}".format(split))
    sys.exit(0)
  
  splitter = name.split(".")
  small_name = splitter[0]
  if len(splitter) > 1:
    split = splitter[1]
  else:
    ftype = (magic.from_file(name, mime=True))
    split = ftype.split("/")[1]

