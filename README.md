# Robot-Automation-Driver
A program to simulate the control of a networked robot.

## Instructions

	1.	Install Python 3.10.

	2.	Add to path during installation if running windows

	3.	Open CMD/Powershell, or terminal.

	4.	Change directory to where the code is saved:
		1.	CD HighRes-BioSolutions-Automation-Driver

	5.	Run the following command:
		1.	python3 driver.py

	6.	Open another CMD/Powershell or terminal

	7.	Change to the same directory

	8.	run the following command:
		1.	python3 schedulerprogram.py

	9.	Send commands from this terminal to the driver and await response.

	10.	Acceptable commands are:
		1.	initialize
		2.	pick [“Source”] [<any integer here>]
		3.	place [“Destination”] [<any integer here>]
		4.	transfer [“Source”,”Destination] [<any integer here>,<any integer here>]
		5.	abort
