# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors:     Juan Martin
# *
# * your institution
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************


"""
Describe your python module here:
This module will provide the traditional Hello world example
"""
from pyworkflow.protocol import Protocol, params
from pwem.protocols import EMProtocol
from pyworkflow.utils import Message
import os
import bsoft
from tomo.objects import Tomogram, SetOfTomograms
from tomo.objects import TomoAcquisition
from pyworkflow.object import Set
from tomo.objects import SetOfTiltSeries, SetOfTomograms, SetOfCTFTomoSeries, CTFTomoSeries, CTFTomo
from tomo.protocols import ProtTomoBase

class ProtBsoftCTFTiltSeries(EMProtocol, ProtTomoBase):
    """
    This protocol will print hello world in the console
    IMPORTANT: Classes names should be unique, better prefix them
    """
    _label = 'CTF Tilt series'

    OUTPUT_FILE_NAME_THON = 'ctf.mrc'
    OUTPUT_FILE_NAME_JSON_PARAMETERS = 'ctf.json'
    PREPARE_FILE_NAME = 'tomo_prepare.star'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        """ Define the input parameters that will be used.
        Params:
            form: this is the form to be populated with sections and params.
        """
        # You need a params to belong to a section:
        form.addSection(label=Message.LABEL_INPUT)

        form.addParam('inputSetofTiltSeries',
                      params.PointerParam,
                      pointerClass='SetOfTiltSeries',
                      important=True,
                      label='Input set of tilt series',
                      help='Select a set of tilt series.')

        line = form.addLine('Tile',
                             help="If the user knows the range of resolutions or"
                                  " only a range of frequencies needs to be analysed."
                                  "If Low is empty MonoRes will try to estimate the range. "
                                  "it should be better if a range is provided")

        line.addParam('tileX', params.IntParam, default=256, label='tileX', important=True)
        line.addParam('tileY', params.IntParam, default=256, label='tileY', important=True)

        form.addParam('volt',
                      params.IntParam,
                      default=300,
                      important=True,
                      label='Voltage',
                      help='Voltage (keV)')

        form.addParam('defocus',
                      params.FloatParam,
                      default=2.6,
                      important=True,
                      label='Defocus',
                      help='Defocus.')

        form.addParam('amp',
                      params.FloatParam,
                      default=0.07,
                      important=True,
                      label='Amplitude',
                      help='Amplitude contrast.')

        line = form.addLine('Resolution Range (Å)',
                            help="If the user knows the range of resolutions or"
                                 " only a range of frequencies needs to be analysed."
                                 "If Low is empty MonoRes will try to estimate the range. "
                                 "it should be better if a range is provided")

        line.addParam('ResolX', params.IntParam, default=10, label='ResolX', important=True)
        line.addParam('ResolY', params.IntParam,  default=50, label='ResolY', important=True)

        form.addParam('axisArg',
                      params.FloatParam,
                      default=90,
                      important=True,
                      label='axis',
                      help='Axis')


    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        # Insert processing steps
        for ts in self.inputSetofTiltSeries.get():
            id = ts.getObjId()
            # self._insertFunctionStep('convertInputStep')
            ts = self.inputSetofTiltSeries.get()[id]
            tsId = ts.getTsId()
            print("##########" + ts.getLocation())
            self._insertFunctionStep(self.preparingDataStep(id))
            self._insertFunctionStep(self.ctfStep, id)

    def preparingDataStep(self, id):
        filename, tomoPath = self.getTSName(id)
        os.mkdir(tomoPath)
        cmd = ' -v 7 -sampling 1.75 -axis %f -tilt -60,3 -out %s %s' % (
            self.axisArg, os.path.join(tomoPath, self.PREPARE_FILE_NAME), filename)
        print(cmd)
        self.runJob(bsoft.Plugin.getProgram('btomo'), cmd,
                    env=bsoft.Plugin.getEnviron())

    # Get the name of the file with the position of the item
    def getTSName(self, id):
        #tsFileName = self.inputSetofTiltSeries.get()[id].getFileName()
        ts = self.inputSetofTiltSeries.get()[id]
        tsFileName = os.path.dirname(self.inputSetofTiltSeries.get()[id].getFileName())
        tsId = ts.getTsId()
        # Defining the output folder
        tomoPath = self._getExtraPath(tsId)

        return tsFileName, tomoPath

    def ctfStep(self, id):
        '''Check the selected command and launch it with the proper parameters'''

        # tomogramId: the ID of the tomogram we are going to denoise

        tomogramFileName, tomoPath = self.getTSName(id)

        # Defining outfiles
        outputTomogram = os.path.join(tomoPath, self.OUTPUT_FILE_NAME)

        cmd = ' -verb 1 -act prepfit -tile %d,%d,1 -Volt %d -Defocus %f -Amp %f -resol %d,%d -out tomo_ctfit.star %s' % (
            self.tileX, self.tileY, self.volt, self.defocus, self.amp, self.resolX, self.resolY,
            os.path.join(tomoPath, self.PREPARE_FILE_NAME))
        print(cmd)
        self.runJob(bsoft.Plugin.getProgram('bctf'), cmd,
                    env=bsoft.Plugin.getEnviron())

    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []

        if self.isFinished():
            summary.append("CTF finished")
        return summary

    def _methods(self):
        methods = []
        return methods
