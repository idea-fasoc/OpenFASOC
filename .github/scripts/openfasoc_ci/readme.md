# OpenFASOC CI flow

1. Build PDK data using the *HEAD* commit of skywater-pdk and open_pdks repositories.
2. Run the *Head~1* commit of the OpenFASOC temp-sense generator and check if the run is successful.
	* If "YES", run the *HEAD* commit of the OpenFASOC temp-sense generator and check if the run is successful.
		* If "YES", CI is successful.
	* If "NO", build PDK data using the *HEAD~1* commit of skywater-pdk and open_pdks repositories and repeat step-2.
