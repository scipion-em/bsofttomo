# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors:     Juan Martin (you@yourinstitution.email)
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
# *  e-mail address 'you@yourinstitution.email'
# *
# **************************************************************************


"""
Describe your python module here:
This module will provide the traditional Hello world example
"""
from pyworkflow.protocol import Protocol, params
from pyworkflow.utils import Message
import os
import bsoft


class ProtBsoftDenoising(Protocol):
    """
    This protocol will print hello world in the console
    IMPORTANT: Classes names should be unique, better prefix them
    """
    _label = 'Denoising tools'

    NON_LINEAR_ANISOTROPIC_DIFFUSION = 0
    BILATERAL_FILTERING = 1
    MEDIAN_FILTERING = 2
    GAUSSIAN_SMOOTHING_FILTERING = 3
    AVERAGING_FILTERING = 4
    OUTPUT_FILE_NAME = 'denoisedTomogram.mrc'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        """ Define the input parameters that will be used.
        Params:
            form: this is the form to be populated with sections and params.
        """
        # You need a params to belong to a section:
        form.addSection(label=Message.LABEL_INPUT)

        form.addParam('inputSet',
                      params.PointerParam,
                      pointerClass='SetOfTomograms',
                      important=True,
                      label='Input set of tomograms',
                      help='Select a set of tomograms to be denoised.')

        form.addParam('denoisingOption',
                      params.EnumParam,
                      choices=['Non-linear anisotropic diffusion', 'Bilateral filtering', 'Median filtering', 'Gaussian smoothing filtering', 'Averaging filtering'],
                      default=self.NON_LINEAR_ANISOTROPIC_DIFFUSION,
                      label="Denoising option",
                      isplay=params.EnumParam.DISPLAY_COMBO,
                      help='Select an option to resize the images: \n '
                           '_Sampling Rate_: Set the desire sampling rate to resize. \n'
                           '_Factor_: Set a resize factor to resize. \n '
                           '_Pyramid_: Use positive level value to expand and negative to reduce. \n'
                           'Pyramid uses spline pyramids for the interpolation. All the rest uses normally \n'
                           'interpolation (cubic B-spline or bilinear interpolation).')

        # Non-linear anisotropic diffusion: bnad parameters
        form.addParam('numberofIterations',
                      params.IntParam,
                      default=100,
                      condition='denoisingOption==%d' % self.NON_LINEAR_ANISOTROPIC_DIFFUSION,
                      label='Number of iterations',
                      help='Number of iterations.')

        form.addParam('slabSize',
                      params.IntParam,
                      default=8,
                      condition='denoisingOption==%d' % self.NON_LINEAR_ANISOTROPIC_DIFFUSION,
                      label='SlabSize',
                      help='Number of z slices to process per thread')

        form.addParam('outputFreq',
                      params.IntParam,
                      expertLevel=params.LEVEL_ADVANCED,
                      default=10,
                      condition='denoisingOption==%d' % self.NON_LINEAR_ANISOTROPIC_DIFFUSION,
                      label='Output freq',
                      help='The frequency of writing intermediate maps.')

        # Bilateral filtering: bbif parameters
        form.addParam('space',
                  params.FloatParam,
                  default=1.5,
                  condition='denoisingOption==%d' % self.BILATERAL_FILTERING,
                  label='Space',
                  help='Space')

        form.addParam('range',
                      params.IntParam,
                      default=25,
                      condition='denoisingOption==%d' % self.BILATERAL_FILTERING,
                      label='Range',
                      help='Range')

        # Median filtering: bmedian parameters
        form.addParam('kernel',
                      params.IntParam,
                      default=5,
                      condition='denoisingOption==%d' % self.MEDIAN_FILTERING,
                      label='Kernel',
                      help='Kernel')

        form.addParam('iter',
                      params.IntParam,
                      default=3,
                      condition='denoisingOption==%d' % self.MEDIAN_FILTERING,
                      label='Iterations',
                      help='Iterations')

        # Gaussian smoothing filtering: bfilter parameters
        form.addParam('gaussian',
                      params.FloatParam,
                      default=19.3,
                      condition='denoisingOption==%d' % self.GAUSSIAN_SMOOTHING_FILTERING,
                      label='Gaussian',
                      help='Gaussian')

        # Averaging filtering: bfilter parameters
        form.addParam('average',
                      params.IntParam,
                      default=7,
                      condition='denoisingOption==%d' % self.AVERAGING_FILTERING,
                      label='Average',
                      help='Average')

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        # Insert processing steps
        for tomogram in self.inputSet.get():
            tomogramId = tomogram.getObjId()
            # self._insertFunctionStep('convertInputStep')
            self._insertFunctionStep(self.denoisingStep, tomogramId)

        self._insertFunctionStep('createOutputStep')

    # Check the selected command and launch it with the proper parameters
    def denoisingStep(self, tomogramId):
        # tomogramId: the ID of the tomogram we are going to denoise

        tomogramFileName = self.inputSet.get()[tomogramId].getFileName()

        ts = self.inputSet.get()[tomogramId]
        tsId = ts.getTsId()

        # Defining the output folder
        tomoPath = self._getExtraPath(tsId)
        os.mkdir(tomoPath)

        # Defining outfiles
        outputTomogram = os.path.join(tomoPath, self.OUTPUT_FILE_NAME)

        # Cheking the selected command to execute it
        if self.denoisingOption == self.NON_LINEAR_ANISOTROPIC_DIFFUSION:
            cmd = ' -v 7 -dat float -iter %d -slabsize %d -out %d %s %s' % (
            self.numberofIterations, self.slabSize, self.outputFreq, tomogramFileName, outputTomogram)
            print(cmd)
            self.runJob(bsoft.Plugin.getProgram('bnad'), cmd,
                        env=bsoft.Plugin.getEnviron())

        if self.denoisingOption == self.BILATERAL_FILTERING:
            cmd = ' -verb 7 -dat float -space %f -range %d %s %s' % (
            self.space, self.range, tomogramFileName, outputTomogram)
            print(cmd)
            self.runJob(bsoft.Plugin.getProgram('bbif'), cmd,
                        env=bsoft.Plugin.getEnviron())

        if self.denoisingOption == self.MEDIAN_FILTERING:
            cmd = ' -verb 7 -dat float -kernel %d -iter %d %s %s' % (
            self.kernel, self.iter, tomogramFileName, outputTomogram)
            print(cmd)
            self.runJob(bsoft.Plugin.getProgram('bmedian'), cmd,
                        env=bsoft.Plugin.getEnviron())

        if self.denoisingOption == self.GAUSSIAN_SMOOTHING_FILTERING:
            cmd = ' -verb 7 -dat float -gaussian %f %s %s' % (
            self.gaussian, tomogramFileName, outputTomogram)
            print(cmd)
            self.runJob(bsoft.Plugin.getProgram('bfilter'), cmd,
                        env=bsoft.Plugin.getEnviron())

        if self.denoisingOption == self.AVERAGING_FILTERING:
            cmd = ' -verb 7 -dat float -average %d %s %s' % (
            self.average, tomogramFileName, outputTomogram)
            print(cmd)
            self.runJob(bsoft.Plugin.getProgram('bfilter'), cmd,
                        env=bsoft.Plugin.getEnviron())

    def createOutputStep(self):
        # register how many times the message has been printed
        # Now count will be an accumulated value
        pass

    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []

        if self.isFinished():
            summary.append("Denoising terminado")
        return summary

    def _methods(self):
        methods = []
        return methods
