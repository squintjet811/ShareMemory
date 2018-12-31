# ShareMemory Module
## Introduction <br />
A simply python based share memory module for transfering data between processor.
Currently tested under Unix system for python 3.7. <br />
Generally, it took ~20ms for writing the image into the memory mapping file. <br />
and it took ~20ms for reading the image from the memory mapping file. <br />
## Install <br /> 
git clone --recursive
## Demo <br />
run the example.py file to see a working demo <br />
```
python3 example.py
```
press "w" for writing data into the memory <br />
press "r" for reading data from the memory<br />
## To do list <br />
1. Replace the blocking method with python semaphore <br />
2. Change the format of the message header <br />
3. To further optimize the speed, decode the buffer data through openning multiple child processes and integrate them together when there is a large number of images or data. <br />
4. Test the code under multiple plantform <br />

