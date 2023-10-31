# Work in progress
## tasksultan
TaskSultan - a bundle of utilities for TaskWarrior

This bundle of utilities is mainly created to augment the management of areas of responsability and projects in TaskWarrior but also contains some auxililiary reports.

The script is creating a json file in the folder where it is located that contains information about each individual AoR (Area of Responsability) and Project in the taskwarrior database.

Each Project could have added to each their own metadata like worklogs, annotations, description and outcome. Each AoR could have its own custom standard instead of outcome like a project.

Each task of a project is targeted to the achievement of the outcome but an "AoR" does not have an outcome per se but a standard that needs to be maintained. For example project "Buy car X", 
each task from this project is alligned with the outcome of getting ownereship of the car but once this has been achieved and the project is completed then the car becomes an "AoR" where
you need to maintain a certain standard like proper maintenace and care, important dates for revision that you need to hold track of etc.

Technically, the way I'm holding track of both Projects and AoR is that in TaskWarrior each area of responsability starts with AoR (example: AoR.cars.carX) and then TaskSultan is distinguishing between them
and keeps them like two different kinds, not only in offering its custom outcome/standard field for each respectively but also in different colors and separation in the menu.

#### Install and use
To install clone 


