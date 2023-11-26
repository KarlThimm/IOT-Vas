# iot-vas
So far the create target and create task work and the IDs are displayed in the console. To create a target you enter a name and the ip in the hosts section. You can not reuse the same name for 2 different targets, wou will get a 500 error returned in the console. When creating a task you need to eneter a name (which does not matter), the type of scan, the config of the scan and the target Id returned when you create a target in the console.

Steps:
1) Create Target- Enter target name and ip
2) Create Task- Enter any name for the task, the scanner type/configuration and the targetid which was returned in the conosle when the target was made
3) Start Task- Enter the taskId returned in the console and click start to start task (A status of 202 is returned in the console meaning the request was accepted and is being processed)
4) Check task progress- Shows the status of the scan, progress not working 100%
5) To get the reportId when you run a scan (RIGHT NOW USE HOST DISCOVERY SCAN) use the command docker compose iot-vas-ospd-openvas-1 in the console and there is an ID that is different from the targetId and taskId that you recieved in the console, this is the reportId. It will be in a line that looks like this (OSPD[8] 2023-11-26 00:07:28,482: INFO: (ospd.ospd) 95b05101-1148-4fb7-9317-549278a474df: Host scan finished.)
6) Enter the ID retreived from docker compose iot-vas-ospd-openvas-1 in the textbox to retrieve the report progress.
7) When the report progress says 100 in the console, enter the same reportId into the Retrieve report box to generate and load the PDF report. 

Problems:
Full and Fast scan crashes docker after a little while everytime I run it.
Base scan takes about 10 hours to complete

RIGHT NOW USE HOST DISCOVERY SCAN FOR TESTING, THE SCAN FINISHES IN ABOUT A MINUTE!
