# Chemotrack---data-analysis-software

Accompanying code for Panigrahi et al. 'ChemoTrack: A comprehensive dataset linking single-cell migration trajectories to precisely defined chemotactic signals'

The repository consists of the following files:

(i) Imagej bubble tracking plug-in.zip: This contains the plugin for performing the segmentation and tracking of the raw microscopy images to obtain the csv files. This was developed by Dr. Luke Tweedy (Cancer Research UK, Beatson). 

(ii) analysis_cei_theta.py: This code processes the csv files to compute chemotactic efficiency index (CEI) from the cell tracks.

(iii) half_violin_atm.py: This code generates the half-violin plots for CEI and also computes the average CEI values in a concentration bin and saves it in a text file.

(iv) analysis_combined_interp_conc.py: This code plots the average chemotactic index from the entire dataset (obtained from avg_cei_combo.csv) as a function of difference in chemoattractant concentration and background receptor occupancy (fig. 3A).

(v) analysis_combined_interp_rocc.py: This code plots the average chemotactic index from the entire dataset (obtained from avg_cei_combo.csv) as a function of difference in receptor occupancy across a cell and background receptor occupancy (fig. 3B).

(vi) analysis_combined_interp_recn.py: This code plots the average chemotactic index from the entire dataset (obtained from avg_cei_combo.csv) as a function of difference in number of active receptors between the front and rear of a cell, and background receptor occupancy (fig. 3D).

(vii) analysis_combined_interp_recn_line.py: This code plots the average chemotactic index as a function of background receptor occupancy for different values of difference in number of active receptors between the front and rear (fig. 3E). 

(viii) avg_cei_combo.csv: Average chemotactic index obtained by binning the data (from half_violin_atm.py) considering all measurements. The first column denotes chemoattractant concentration, second column denotes the difference between Cmax and Cmin, and the third column denotes the average chemotactic efficiency index. All concentrations are in nanoMolar. 

Instructions for accessing the data:
ChemoTrack is publicly accessible under a  CC BY 4.0 license and is hosted in the following website: https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD3674
To access the dataset concentration-wise, according to the format mentioned in the paper, please visit the HTTP site: https://ftp.ebi.ac.uk/pub/databases/biostudies/S-BIAD/674/S-BIAD3674/Files/ChemoTrack/
Please note that the home page of ChemoTrack in Bioimage archive lists all the files in the dataset, and does not organize them according to the directory structure mentioned in the paper. This is the default organizational style of Bioimage archive. 

Step by step instructions for processing the raw microscopy images and generating the cell tracks:
1)	Open the images using Fiji.
2)	Crop and rotate the image such that the image consists only of the viewing bridge with the chemoattractant gradient going from the left to right.
3)	Subtract the background using a rolling ball radius equal to 11 pixels. This was done using the subtract background feature that is available in Fiji.
4)	Adjust the properties of the image stack such that the stack corresponds to the timeframes and not a z-stack which is the default setting that appears in Fiji while importing a sequence of tif files. 
5)	Adjust the scale of the image, and this is specific to the objective and the camera that is being used. For our case 1 microns corresponds to 2.2 pixels.
6)	Select the temporal separation between consecutive frames, for example 0.5 minutes. It is very important to be consistent with the units of time here. It is required for the tracking plugin. 
7)	Convert all images to 8-bit. This is required for the plugin to work properly.
8)	Go to plugins and open the “beatson” plugin, and choose ‘Automatic tracking’. 
9)	Within the plugin window, choose the following settings:
  (i)	Track ‘dark’ objects
  (ii)	Threshold = 14.0, blur = 6.0
  (iii)	Maximum speed = 31 microns/min
  (iv)	Minimum speed = 0.5 microns/min
  (v)	Minimum frames per track = 12
  (vi)	Maximum missing frames = 2
10)	Track the cells and then save the resulting csv files. A quick sanity check of the tracking can be obtained by selecting the “overlay” option in the plugin.

