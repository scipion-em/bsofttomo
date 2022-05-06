# **************************************************************************
# *
# * Authors:     Juan Martin
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
from pyworkflow.tests import DataSet
DataSet(name='cryocare', folder='cryocare',
        files={
            'rec_even_odd_tomos_dir': 'Tomos_EvenOdd_Reconstructed',
            'tomo_even': 'Tomos_EvenOdd_Reconstructed/Tomo110_Even_bin6.mrc'
        })
from .test_protocols_bsofttomo import (TestBsofttomoBase)
