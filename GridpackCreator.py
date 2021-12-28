# python3 mkReweightCard.py -op cW cHW cHbox -o ciao.dat

# python3 GridpackCreator.py -n Zjj_ewk_dim6 -ops cHDD cqq11 cHWB cHbox cHW cll1 cHl3 cHq3 cqq1 cW cqq3 cqq31 cHq1 cHl1 -f prova -o ~/prova/genproductions/bin/MadGraph5_aMCatNLO/folder_Reco_Zjj_EWK_dim6
from itertools import combinations
import argparse
import os 
import subprocess
import sys
import re
import shutil


class GridpackCreator:

    def __init__(self, name, operators, process_folder, output_folder="", initial_weight='SM'):
        self._full_ops = {
        'cG': 1,
        'cW': 2,
        'cH': 3,
        'cHbox': 4,
        'cHDD': 5,
        'cHG': 6,
        'cHW': 7,
        'cHB': 8,
        'cHWB': 9,
        'ceHRe': 10,
        'cuHRe': 11,
        'cdHRe': 12,
        'ceWRe': 13,
        'ceBRe': 14,
        'cuGRe': 15,
        'cuWRe': 16,
        'cuBRe': 17,
        'cdGRe': 18,
        'cdWRe': 19,
        'cdBRe': 20,
        'cHl1': 21,
        'cHl3': 22,
        'cHe': 23,
        'cHq1': 24,
        'cHq3': 25,
        'cHu': 26,
        'cHd': 27,
        'cHudRe': 28,
        'cll': 29,
        'cll1': 30,
        'cqq1': 31,
        'cqq11': 32,
        'cqq3': 33,
        'cqq31': 34,
        'clq1': 35,
        'clq3': 36,
        'cee': 37,
        'cuu': 38,
        'cuu1': 39,
        'cdd': 40,
        'cdd1': 41,
        'ceu': 42,
        'ced': 43,
        'cud1': 44,
        'cud8': 45,
        'cle': 46,
        'clu': 47,
        'cld': 48,
        'cqe': 49,
        'cqu1': 50,
        'cqu8': 51,
        'cqd1': 52,
        'cqd8': 53,
        'cledqRe': 54,
        'cquqd1Re': 55,
        'cquqd11Re': 56,
        'cquqd8Re': 57,
        'cquqd81Re': 58,
        'clequ1Re': 59,
        'clequ3Re': 60
        }
            
        self._name = name
        # sort operators by its id from the model
        self._operators = sorted(operators, key=lambda x: self._full_ops[x])

        self._process_folder = process_folder

        if output_folder=='':
            dirs = process_folder.split('/')[:-1]
            dirs.append("folder_Reco_"+self._name)
            output_folder = '/'.join(dirs)

        self._output_folder = output_folder
        
        if not os.path.isdir(self._output_folder):
            print('Output folder created')
            os.makedirs(self._output_folder)

        self._initial_weight = initial_weight

    def __del__(self):
        pass 

    def makeRestrict(self):

        print("======================")
        print("==== makeRestrict ====")
        print("======================")


        outFile = self._output_folder + '/restrict_{}_massless.dat'.format('_'.join(self._operators))
        f_before = open (os.path.join(os.path.abspath(os.path.dirname(__file__)), 'input/restrict_before_v3_0_my.txt'), 'r')
        contents_before = f_before.read ()
        f_before.close ()
        f_after  = open (os.path.join(os.path.abspath(os.path.dirname(__file__)), 'input/restrict_after_v3_0_my.txt'), 'r') 
        contents_after = f_after.read ()
        f_after.close ()

        # build restrict cards for operators
        # ----------------------------------------------------
        f_restrict = open (outFile, 'w')
        f_restrict.write (contents_before)

        # loop over operators
        for operator in list(self._full_ops.items()):
            if operator[0] in self._operators: 
                f_restrict.write ('   ' + str(operator[1]) + ' 9.999999e-01 # ' + operator[0] + '\n')
            else:
                f_restrict.write ('   ' + str(operator[1]) + ' 0 # ' + operator[0] + '\n')


        f_restrict.write (contents_after)
        f_restrict.close ()

        print("==== done makeReweight ====")

    def makeReweight(self):
        print("======================")
        print("==== makeReweight ====")
        print("======================")

        
        f = open(self._output_folder+'/reweight_card.dat', "w")
        
        f.write("change helicity False\n")
        f.write("change rwgt_dir rwgt\n\n")

        #SM
        f.write("# SM rwgt_1\n")
        f.write("launch\n")
        for op in self._operators:
            f.write("   set SMEFT {} {}\n".format(self._full_ops[op], 0))
        
        f.write("\n\n")
        
        
        # for Lin and Quad
        i = 2
        for op in self._operators:
            for k in [-1,1]:
                f.write("# {}={} rwgt_{}\n".format(op, k, i))
                f.write("launch\n")
                for op2 in self._operators:
                    
                    if op2 != op:
                        f.write("   set SMEFT {} {}\n".format(self._full_ops[op2], 0))
                    else:
                        f.write("   set SMEFT {} {}\n".format(self._full_ops[op], k))  
                i+=1
                    
                f.write("\n\n")
                                
        for ops in list(combinations(self._operators,2)):
            f.write("# {}={}, {}={} rwgt_{}\n".format(ops[0], 1, ops[1], 1, i))
            f.write("launch\n")
            for op3 in self._operators:
                if not op3 in ops:
                    f.write("   set SMEFT {} {}\n".format(self._full_ops[op3], 0))
                else:
                    f.write("   set SMEFT {} {}\n".format(self._full_ops[op3], 1)) 
                    
            i+=1
                    
            f.write("\n\n") 

        print("==== done makeReweight====")

    def makeCustomize(self):

        print("======================")
        print("==== makeCustomize ====")
        print("======================")

        f = open(self._output_folder+'/customizecards.dat', "w")

        if self._initial_weight=='SM':
            # deactivate all operators for nominal weight
            for operator in self._operators:
                f.write('set param_card SMEFT {} 0\n'.format(self._full_ops[operator]))
            
        else:
            # all operators are by default activated
            for operator in self._operators:
                f.write('set param_card SMEFT {} 1\n'.format(self._full_ops[operator]))

        f.close()
        print("==== done makeCustomize ====")
    
    def _renameFile(self, file_name):
        p = re.compile('.*{}\.dat'.format(file_name))
        files = os.listdir(self._output_folder)
        card = list(filter(lambda k: len(k)>0, list(map(lambda k: re.findall(p, k), files))))
        if len(card)==1:
            card=card[0][0]
            os.rename(self._output_folder + "/" + card, self._output_folder + "/" + self._name + "_" + file_name + ".dat")
        elif len(card)>1:
            # get most recent
            
            files_with_time = [(x[0], os.path.getmtime(self._output_folder + "/" + x[0])) for x in card]
            ordered_files = sorted(files_with_time, key=lambda k: k[1], reverse=True)
            os.rename(self._output_folder + "/" + ordered_files[0][0], self._output_folder + "/" + self._name + "_" + file_name + ".dat")

    def renameFiles(self):

        print("======================")
        print("==== Copying and renaming Files ====")
        print("======================")

        # copy all files from process_folder
        files = os.listdir(self._process_folder)
        for file in files:
            full_name = os.path.join(self._process_folder, file)
            if os.path.isfile(full_name):
                shutil.copy(full_name, os.path.join(self._output_folder, file))

        # find proc_card
        name = 'proc_card'
        p = re.compile('.*{}\.dat'.format(name))
        files = os.listdir(self._output_folder)
        card = list(filter(lambda k: len(k)>0, list(map(lambda k: re.findall(p, k), files))))
        if len(card)==0:
            sys.exit("No proc_card.dat in process folder specified: {}".format(self._process_folder))
        card = card[0][0]
        # check if output of proc_card is with right name
        with open(self._output_folder + "/" + card, "r") as file:
            lines = file.readlines()
            for i in range(len(lines)):
                if 'import' == lines[i].split()[0]:
                    lines[i] = 'import model SMEFTsim_U35_MwScheme_UFO-{}_massless\n'.format('_'.join(self._operators))
                elif 'output' == lines[i].split()[0]:
                    lines[i] = 'output {}\n'.format(self._name)
                else:
                    continue

        with open(self._output_folder + "/" + card, "w") as file:
            file.writelines(lines)

        interesting_files = ['proc_card', 'run_card', 'reweight_card','customizecards', 'extramodels']
        for file in interesting_files:
            self._renameFile(file)

       

        print("==== done Renaming Files ====")

    def makeGridpack(self):
        print("======================")
        print("==== Creating Gridpack ====")
        print("======================")

        self.makeRestrict()
        self.makeReweight()
        self.makeCustomize()
        self.renameFiles()

        print('./gridpack_generation_EFT.sh {} {} '.format(self._name, self._output_folder))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--name", help="Name for the process" , required=True)
    parser.add_argument("-ops","--operators", help="Operators list to make the reweight card following algebra" , nargs="+", required=True)
    parser.add_argument("-f", "--folder", help="Process input folder path", required=True)
    parser.add_argument("-o", "--outputFolder", help="Process output folder path")
    parser.add_argument("-iW", "--initWeight", help="Initial weight, it changes customizecards")
    args = parser.parse_args()
    if not args.outputFolder:
        gC = GridpackCreator(args.name, args.operators, args.folder, args.initWeight)
    else:
        gC = GridpackCreator(args.name, args.operators, args.folder, args.outputFolder, args.initWeight)
    gC.makeGridpack()