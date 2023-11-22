# iot-vas
So far the create target and create task work and the IDs are displayed in the console. To create a target you enter a name and the ip in the hosts section. You can not reuse the same name for 2 different targets, wou will get a 500 error returned in the console. When creating a task you need to eneter a name (which does not matter), the type of scan, the config of the scan and the target Id returned when you create a target in the console.

Steps:
1) Create Target- Enter target name and ip
2) Create Task- Enter any name for the task, the scanner type/configuration and the targetid which was returned in the conosle when teh target was made
3) Start Task- Enter the taskId returned in the console and click start to start task
4) A status of 202 is returned in the console meaning the request was accepted and is being processed

Start Task working, now need to view progress
