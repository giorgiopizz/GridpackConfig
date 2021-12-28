# GridpackConfig 

The script GridpackCreator.py creates
- A restrict card
- A reweight card
- A customize card


and renames all the files in output folder to match the process name.


It takes as input files a proc_card and a run_card. 

The proc_card will be modified in order to include the restrict card created and to output the process name. 

Here's an example on how to run the GridpackCreator.py:


``` python3 GridpackCreator.py -n Zjj_ewk_dim6 -ops cHDD cqq11 cHWB cHbox cHW cll1 cHl3 cHq3 cqq1 cW cqq3 cqq31 cHq1 cHl1 -f InputCards -o ~/prova/genproductions/bin/MadGraph5_aMCatNLO/folder_Reco_Zjj_EWK_dim6 ```


A modified version of gridpack_generation script is provided in order to copy into SMEFTsim a restrict card from the cards folder if it's present.

One should also edit the gridpack_generation script specifying the path to MG and SMEFT tar versions at line 175 and 185.

