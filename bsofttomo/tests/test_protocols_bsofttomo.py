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

from bsofttomo.protocols import ProtBsoftDenoising

class TestBsofttomoBase(BaseTest):
    @classmethod
    def setData(cls, dataProject='resmap'):
        cls.dataset = DataSet.getDataSet(dataProject)
        cls.half1 = cls.dataset.getFile('betagal_half1')
        cls.half2 = cls.dataset.getFile('betagal_half2')
        cls.mask = cls.dataset.getFile('betagal_mask')

    @classmethod
    def runImportVolumes(cls, pattern, samplingRate):
        """ Run an Import volumes protocol. """
        cls.protImport = cls.newProtocol(SetOfTomograms,
                                         filesPath=pattern,
                                         samplingRate=samplingRate
                                         )
        cls.launchProtocol(cls.protImport)
        return cls.protImport

    @classmethod
    def runImportMask(cls, pattern, samplingRate):
        """ Run an Import volumes protocol. """
        cls.protImport = cls.newProtocol(SetOfTomograms,
                                         maskPath=pattern,
                                         samplingRate=samplingRate
                                         )
        cls.launchProtocol(cls.protImport)
        return cls.protImport


class TestBsoftTomo(TestBsofttomoBase):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        TestBsofttomoBase.setData()
        cls.protImportHalf1 = cls.runImportVolumes(cls.half1, 3.54)
        cls.protImportHalf2 = cls.runImportVolumes(cls.half2, 3.54)
        cls.protCreateMask = cls.runImportMask(cls.mask, 3.54)

    def testBSoftBnad(self):
        bsoft = self.newProtocol(ProtBsoftDenoising,
                                   inputSet='tomo - import tomograms.outputTomograms',
                                   denoisingOption=0,
                                   numberofIterations=100,
                                   slabSize=8,
                                   outputFreq=10)
        self.launchProtocol(bsoft)
        #self.assertIsNotNone(bsoft.resolution_Volume,
        #                     "bsoft has failed")

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
