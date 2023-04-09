Regression of a generator
=========================

Having a regression flow for a generator helps in understanding the performance effects when the generator gets updated. Also it is useful to sweep the parameters of the generator for design space exploration.

Once the generator is available inside the main repo, a regression flow is added in the following method - 

* A generator-dependent regression python file is added to the ``regression/generator_checks`` folder. It typically consists of various stages and its implementation. If the generator is modular, this setup can be much flexible while adding more testbenches to the regression/generator flow.

* Typically there are 5 methods inside this python script - ``run_generator``, ``checkDRC``, ``checkLVS``, ``runSimulations``, ``processSims``. There is also an extra method called ``copy_data`` which moves the generated data to a different location for running simulations. Later the entire data is archived for backup purposes.

* To sweep the input parameters, a configuration file needs to be created inside ``regression/configs``. It contains the name of the input parameter and a list assigned to it which has the ``start, stop and step`` information. Note that these input sweeps must be accessible from outside of the generator (either through command line or a specifications file)

* Now edit the master file called ``run_regression.py`` present inside the ``regressions`` folder by adding generator specific function calling methods defined inside the previously constructed generator script placed inside ``regression/generator_checks``. This script will run the regression on self-hosted GCP VMs. This python file will automatically import all python scripts present inside ``regression/generator_checks``. This script takes two arguments - generator name and stage.

* Based on the generator name and stage, this script runs the regression in a modular fashion. This script should be smart enough to run simulations effeciently by distrubuting them between multiple runner machines. For this, self-hosted runner machines must be dynamically created using terraform. This part is still work in progress. 

* All the generated final data, after sweeping the input parameters for the given range, is stored in a google hosted database. For multiple runs, the database gets updated. Also a comparison operation is executed to compare the performance metrics between consecutive updates.