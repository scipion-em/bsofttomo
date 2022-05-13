# **************************************************************************
# *
# * Authors:    Juan Martin
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
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
import os
from os.path import exists

from pyworkflow.tests import BaseTest, DataSet, setupTestProject
from tomo.objects import SetOfTomograms
from tomo.protocols import ProtImportTomograms
from bsofttomo.protocols import ProtBsoftDenoising

class TestBsofttomoBase(BaseTest):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.dataset = DataSet.getDataSet('cryocare')
        cls.sRate = 2.355


    def runImportTomograms(self, tomoFile, mode):
        """ Run an Import volumes protocol. """
        protImportTomogram = self.newProtocol(ProtImportTomograms,
                                             filesPath=self.dataset.getFile(tomoFile),
                                             samplingRate=self.sRate)

        self.launchProtocol(protImportTomogram)
        outputTomos = getattr(protImportTomogram, 'outputTomograms', None)
        self.assertIsNotNone(outputTomos, 'No tomograms')
        return protImportTomogram

    def checkOutputTomoFiles(self, tomos, bsoft):
        for tomogram in tomos.outputTomograms:
            tomogramId = tomogram.getObjId()
            ts = tomos.outputTomograms[tomogramId]
            tsId = ts.getTsId()

            # Defining the output folder
            # tomoPath = ProtBsoftDenoising._getExtraPath(tsId)
            tomoPath = bsoft._getExtraPath(tsId)
            outputTomogram = os.path.join(tomoPath, ProtBsoftDenoising.OUTPUT_FILE_NAME)
            self.assertTrue(exists(outputTomogram))

    def BSoftBnad(self, tomos):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                   inputSet=getattr(tomos, 'outputTomograms', None),
                                   denoisingOption=0,
                                   numberofIterations=1,
                                   slabSize=8,
                                   outputFreq=10)
        self.launchProtocol(bsoft)
        self.checkOutputTomoFiles(tomos, bsoft)

    def BSoftBbif(self, tomos):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                 inputSet=getattr(tomos, 'outputTomograms', None),
                                 denoisingOption=1,
                                 space=1.5,
                                 range=25)
        self.launchProtocol(bsoft)
        self.checkOutputTomoFiles(tomos, bsoft)

    def BSoftBmedian(self, tomos):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                 inputSet=getattr(tomos, 'outputTomograms', None),
                                 denoisingOption=2,
                                 kernel=5,
                                 iter=3)
        self.launchProtocol(bsoft)
        self.checkOutputTomoFiles(tomos, bsoft)

    def BSoftBfilter(self, tomos):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                 inputSet=getattr(tomos, 'outputTomograms', None),
                                 denoisingOption=3,
                                 gaussianMean=19,
                                 gaussianSigma=3, )
        self.launchProtocol(bsoft)
        self.checkOutputTomoFiles(tomos, bsoft)

    def BSoftBfilterAveraging(self, tomos):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                 inputSet=getattr(tomos, 'outputTomograms', None),
                                 denoisingOption=4,
                                 average=7)
        self.launchProtocol(bsoft)
        self.checkOutputTomoFiles(tomos, bsoft)

    def testWorkflow(self):
        importTomograms = self.runImportTomograms('tomo_even', 'even')
        self.BSoftBnad(importTomograms)
        self.BSoftBbif(importTomograms)
        self.BSoftBmedian(importTomograms)
        self.BSoftBfilter(importTomograms)
        self.BSoftBfilterAveraging(importTomograms)
