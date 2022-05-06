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

    @classmethod
    def runImportTomograms(cls, tomoFile, mode):
        """ Run an Import volumes protocol. """
        protImportTomogram = cls.newProtocol(ProtImportTomograms,
                                             filesPath=cls.dataset.getFile(tomoFile),
                                             samplingRate=cls.sRate)

        cls.launchProtocol(protImportTomogram)
        outputTomos = getattr(protImportTomogram, 'outputTomograms', None)
        cls.assertIsNotNone(outputTomos, 'No tomograms')
        return protImportTomogram

    def testBSoftBnad(self, tomos):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                   inputSet=tomos,
                                   denoisingOption=0,
                                   numberofIterations=100,
                                   slabSize=8,
                                   outputFreq=10)
        self.launchProtocol(bsoft)
        #self.assertIsNotNone(bsoft.resolution_Volume,
        #                     "bsoft has failed")

    def testWorkflow(self):
        importTomograms = self.runImportTomograms('tomo_even', 'even')
        self.testBSoftBnad(importTomograms)
        # protTraining = self._runTrainingData(prepTrainingDataProt)
        # Prediction from training
        # self._runPredict(importTomoProtEven, importTomoProtOdd, protTraining=protTraining)
        # Load a pre-trained model and predict
    '''
    def testBSoftBbif(self):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                   inputSet='tomo - import tomograms.outputTomograms',
                                   denoisingOption=0,
                                   space=1.5,
                                   range=25)
        self.launchProtocol(bsoft)
        #self.assertIsNotNone(bsoft.resolution_Volume,
        #                     "bsoft has failed")

    def testBSoftBmedian(self):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                   inputSet='tomo - import tomograms.outputTomograms',
                                   denoisingOption=0,
                                   kernel=5,
                                   iter=3)
        self.launchProtocol(bsoft)
        #self.assertIsNotNone(bsoft.resolution_Volume,
        #                     "bsoft has failed")

    def testBSoftBfilter(self):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                   inputSet='tomo - import tomograms.outputTomograms',
                                   denoisingOption=0,
                                   gaussianMean=19,
                                   gaussianSigma=3,)
        self.launchProtocol(bsoft)
        #self.assertIsNotNone(bsoft.resolution_Volume,
        #                     "bsoft has failed")

    def testBSoftBfilterAveraging(self):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                   inputSet='tomo - import tomograms.outputTomograms',
                                   denoisingOption=0,
                                   average=7)
        self.launchProtocol(bsoft)
        #self.assertIsNotNone(bsoft.resolution_Volume,
        #                     "bsoft has failed")
    '''