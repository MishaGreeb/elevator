@echo off
:previous1
set watitle=Elevator
set wasig=Elevator GUI 0.1
set wabmp=epmp.bmp

set wabat=%TEMP%\wabat.bat
set waoutput=admin
set watext=Enter username:
start /w wizapp EB
if errorlevel 2 goto :cancel
if errorlevel 1 goto :previous1
call %wabat%
set username=%waoutput%
echo Username is %waoutput%

:previous2
set waoutput=admin
set watext=Enter password:
start /w wizapp EB
if errorlevel 2 goto :cancel
if errorlevel 1 goto :previous1
call %wabat%
set password=%waoutput%
echo Password is %waoutput%

:previous3
set waoutput=3.3
set watext=Enter firmware version(eg 3.3, not 3.3-RC10):
start /w wizapp EB
if errorlevel 2 goto :cancel
if errorlevel 1 goto :previous2
call %wabat%
set fwversion=%waoutput%
echo FW version is %waoutput%

:previous4
set waoutput=sm.json
set watext=Enter template file name:
start /w wizapp FB
if errorlevel 2 goto :cancel
if errorlevel 1 goto :previous3
call %wabat%
set json=%waoutput%
echo Template name is %waoutput%

:previous5
set waoutput=UBNTXW-ubntxw-squashfs-factory-3.3.bin 
set watext=Enter firmware filename:
start /w wizapp FB
if errorlevel 2 goto :cancel
if errorlevel 1 goto :previous4
call %wabat%
set fwname=%waoutput%
echo FW file name is %waoutput%

:previous6
set waoutput= 
set watext=Enter IP address to elevate:
start /w wizapp FB
if errorlevel 2 goto :cancel
if errorlevel 1 goto :previous5
call %wabat%
set ip=%waoutput%
echo IP address is %waoutput%

call elevator.exe -v -u %username% -p %password% -t %json% -n %fwversion% -f %fwname% %ip% 

:previous7
set watitle=so much Elevate
set watext=Do you want to Elevate another unit?~~Press OK if you are.~Press Cancel if you're not sure.
start /w wizapp MB QUES
if errorlevel 2 goto cancel
if errorlevel 0 if not errorlevel 2 goto :previous6

pause
:cancel