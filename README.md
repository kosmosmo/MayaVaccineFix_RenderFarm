# MayaVaccineFix_RenderFarm
This is a Deadline rendfram plugin for removing Maya Chinese error and preventing reinfection.

Maya error- # Warning: 你的文件贼健康~我就说一声没有别的意思 #

The plugin will locate and clean up the "vaccine.py" & "userSetup.py" files in the ~/maya/scripts directory for all of the rendering nodes.

The two files will be marked as "Read-only" for preventing reinfection.


## Installation

Copy "VaccineFixForDeadline.py" to DeadlineRepository\scripts\General

Copy "MayaVaccineFix_RenderFarm" folder to network server


## Usage

Deadline Monitor => Scripts => VaccineFixForDeadline

<img src="https://github.com/kosmosmo/MayaVaccineFix_RenderFarm/blob/master/pics/ui.jpg" width="321" height ="380">

Pool: If you are using pool, chosse one that contains all the machines you are scaning.

Machine List: The list of the machines you are scaning.

Maya Version: Choose your maya version. If you have multiple maya version installed, pick any.

Patch File: Pick the "MayaVaccineFix_RenderFarm" folder on your network

<img src="https://github.com/kosmosmo/MayaVaccineFix_RenderFarm/blob/master/pics/jobs.jpg" width="321" height ="276">

All the jobs can be found in a batch.

Report is located at MayaVaccineFix_RenderFarm\report.txt
