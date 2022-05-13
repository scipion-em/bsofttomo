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

class ProtBsoftMarkerFreeAlignment(EMProtocol, ProtTomoBase):
    """
    This protocol will print hello world in the console
    IMPORTANT: Classes names should be unique, better prefix them
    """
    _label = 'Marker Free Alignment'

    ALIGNMENT_FILE_NAME = 'alignmentParameters.star'
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

        line = form.addLine('align',
                             help="The -align option takes three parameters: "
                                  "-Number of iterations: These are iterations over the full "
                                  " tilt series attempting to refine the micrograph orientations"
                                  "-Stopping condition: Sets the threshold to stop when the average "
                                  " micrograph shift difference compared to the pervious iteration drops below it."
                                  "-Number of adjacent micrographs to include in each subset reconstruction.")

        line.addParam('nIterations', params.IntParam, default=3, label='Iterations', important=True)
        line.addParam('stopCondition', params.IntParam, default=1, label='stopCondition', important=True)
        line.addParam('nAdjacent', params.IntParam, default=3, label='nAdjacentMicrographs', important=True)

        form.addParam('resol',
                      params.IntParam,
                      default=20,
                      important=True,
                      label='Resolution',
                      help='The -resolution option sets the high resolution limit for cross correlations.')

        line = form.addLine('edge',
                            help="The edge option smooths the edges of the micrographs "
                                 "which includes erasing extraneous areas at high tilts." 
                                 "The parameters are the width of the edge and the standard "
                                 "deviation of the transition, both in pixels")

        line.addParam('edgeX', params.IntParam, default=20, label='edgeX', important=True)
        line.addParam('edgeY', params.IntParam, default=3, label='edgeY', important=True)

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
            self._insertFunctionStep(self.preparingDataStep, ts.getObjId())
            self._insertFunctionStep(self.markerFreeAlignemetStep, ts.getObjId())

    def preparingDataStep(self, id):
        filename, tomoPath = self.getTSName(id)
        os.mkdir(tomoPath)
        cmd = ' -v 7 -sampling %f -axis %f -tilt -60,3 -out %s %s' % (
            self.inputSetofTiltSeries.get().getSamplingRate(),
            self.axisArg, os.path.join(tomoPath, self.PREPARE_FILE_NAME), filename)

        self.runJob(bsoft.Plugin.getProgram('btomo'), cmd,
                    env=bsoft.Plugin.getEnviron())

    # Get the name of the file with the position of the item
    def getTSName(self, id):
        ts = self.inputSetofTiltSeries.get()[id]
        tsFileName = ts.getFirstItem().getFileName()
        tsId = ts.getTsId()

        # Defining the output folder
        tomoPath = self._getExtraPath(tsId)

        return tsFileName, tomoPath

    def markerFreeAlignemetStep(self, id):
        '''Check the selected command and launch it with the proper parameters'''

        # tomogramId: the ID of the tomogram we are going to denoise

        tomogramFileName, tomoPath = self.getTSName(id)

        # Defining outfiles
        outputTiltSeries = os.path.join(tomoPath, self.ALIGNMENT_FILE_NAME)

        cmd = ' -verb 1 -align %d,%d,%d -resol %d -edge %d,%d -out %s %s' % (
            self.nIterations, self.stopCondition, self.nAdjacent, self.resol, self.edgeX, self.edgeY,
            outputTiltSeries, os.path.join(tomoPath, self.PREPARE_FILE_NAME))
        print(cmd)
        self.runJob(bsoft.Plugin.getProgram('btomaln'), cmd,
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
