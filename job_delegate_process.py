import shlex
import subprocess
import os
from os import path

import utils, config


class PlotterJobDelegate:
    """
    This delegate class is going to handle a single plot job (execute the plot process) and transmit it's Std Out data to the log file.
    """

    def __init__(self, plotter_dir, **args):
        self.__CWD = os.getcwd()  # Work Path

        plotter_dir = path.join(self.__CWD, plotter_dir).replace('\\', '/')

        if utils.is_linux():
            command = ['bash', plotter_dir, '-action', 'plotting']
            command.extend(
                ['-plotting-exec', path.join(self.__CWD, path.join(path.dirname(plotter_dir)), 'ProofOfSpace')])
        else:
            command = [plotter_dir, '-action', 'plotting']
            command.extend(
                ['-plotting-exec', path.join(self.__CWD, path.join(path.dirname(plotter_dir)), 'ProofOfSpace.exe')])

        command.extend(['-plotting-fpk', config.PLOTTER_FPK,
                        '-plotting-ppk', config.PLOTTER_PPK])

        for kw in args:
            command.extend(['-' + kw.replace('_', '-'), str(args[kw])])

        self.__command = [i.replace('\\', '/') for i in command]
        print(self.__command)

    def start(self):

        plotter_process = subprocess.Popen(self.__command, shell=False, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)
        while plotter_process.poll() is None:
            line = plotter_process.stdout.readline()
            line = line.strip()
            if line:
                print('Subprogram output: [{}]'.format(line))

        if plotter_process.returncode == 0:
            print('Subprogram success')
        else:
            print('Subprogram failed')


jd = PlotterJobDelegate('bin/windows/hpool-plotter', k=31, plotting_n=20, r=4, b=3400)
"""
cmd = [plotter_dir, '-action', 'plotting', '-k', '31', '-plotting-n', '20', '-r', '4', '-b', '3400',
               '-plotting-fpk', FPK,
               '-plotting-ppk', PPK]
              
              
argument_conf_cmd = ['-d', path.join(CWD, 'test_plot'), '-t', path.join(CWD, 'test_plot')]
        poc_exec_cmd = ['-plotting-exec', path.join(CWD, 'bin/windows/ProofOfSpace.exe')]              
               """
