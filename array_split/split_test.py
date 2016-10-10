"""
========================================
The :mod:`array_split.split_test` Module
========================================

.. currentmodule:: array_split.split_test

Module defining :mod:`array_split.split` unit-tests.
Execute as::

   python -m array_split.split_tests



Classes
=======

.. autosummary::
   :toctree: generated/

   SplitTest - :obj:`unittest.TestCase` for :mod:`array_split.split` functions.


"""
from __future__ import absolute_import
from .license import license as _license, copyright as _copyright
import array_split.unittest as _unittest
import array_split.logging as _logging
import array_split as _array_split

import numpy as _np

from .split import ArraySplitter, calculate_num_slices_per_axis, shape_factors, array_split
from .split import calculate_tile_shape_for_max_bytes

__author__ = "Shane J. Latham"
__license__ = _license()
__copyright__ = _copyright()
__version__ = _array_split.__version__


class SplitTest(_unittest.TestCase):
    """
    :obj:`unittest.TestCase` for :mod:`array_split.split` functions.
    """

    #: Class attribute for :obj:`logging.Logger` logging.
    logger = _logging.getLogger(__name__ + ".SplitTest")

    def test_shape_factors(self):
        """
        Tests for :func:`array_split.split.shape_factors`.
        """
        f = shape_factors(4, 2)
        self.assertTrue(_np.all(f == 2))

        f = shape_factors(4, 1)
        self.assertTrue(_np.all(f == 4))

        f = shape_factors(5, 2)
        self.assertTrue(_np.all(f == [1, 5]))

        f = shape_factors(6, 2)
        self.assertTrue(_np.all(f == [2, 3]))

        f = shape_factors(6, 3)
        self.assertTrue(_np.all(f == [1, 2, 3]))

    def test_calculate_num_slices_per_axis(self):
        """
        Tests for :func:`array_split.split.calculate_num_slices_per_axis`.
        """

        spa = calculate_num_slices_per_axis([0, ], 5)
        self.assertEqual(1, len(spa))
        self.assertTrue(_np.all(spa == 5))

        spa = calculate_num_slices_per_axis([2, 0], 4)
        self.assertEqual(2, len(spa))
        self.assertTrue(_np.all(spa == 2))

        spa = calculate_num_slices_per_axis([0, 2], 4)
        self.assertEqual(2, len(spa))
        self.assertTrue(_np.all(spa == 2))

        spa = calculate_num_slices_per_axis([0, 0], 4)
        self.assertEqual(2, len(spa))
        self.assertTrue(_np.all(spa == 2))

        spa = calculate_num_slices_per_axis([0, 0], 16)
        self.assertEqual(2, len(spa))
        self.assertTrue(_np.all(spa == 4))

        spa = calculate_num_slices_per_axis([0, 0, 0], 8)
        self.assertEqual(3, len(spa))
        self.assertTrue(_np.all(spa == 2))

        spa = calculate_num_slices_per_axis([0, 1, 0], 8)
        self.assertEqual(3, len(spa))
        self.assertTrue(_np.all(spa == [4, 1, 2]))

        spa = calculate_num_slices_per_axis([0, 1, 0], 17)
        self.assertEqual(3, len(spa))
        self.assertTrue(_np.all(spa == [17, 1, 1]))

        spa = calculate_num_slices_per_axis([0, 1, 0], 15, [1, _np.inf, _np.inf])
        self.assertEqual(3, len(spa))
        self.assertTrue(_np.all(spa == [1, 1, 15]))

    def test_calculate_tile_shape_for_max_bytes_1d(self):
        """
        Test case for :func:`array_split.split.calculate_tile_shape_for_max_bytes`,
        where :samp:`array_shape` parameter is 1D, i.e. of the form :samp:`(N,)`.
        """
        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512,),
                array_itemsize=1,
                max_tile_bytes=1024
            )
        self.assertSequenceEqual((512,), tile_shape)

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512,),
                array_itemsize=1,
                max_tile_bytes=1024,
                sub_tile_shape=[64,]
            )
        self.assertSequenceEqual((512,), tile_shape)

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512,),
                array_itemsize=1,
                max_tile_bytes=1024,
                sub_tile_shape=[26,]
            )
        self.assertSequenceEqual((260,), tile_shape)

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512,),
                array_itemsize=1,
                max_tile_bytes=512
            )
        self.assertSequenceEqual((512,), tile_shape)

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512,),
                array_itemsize=2,
                max_tile_bytes=512,
            )
        self.assertSequenceEqual((256,), tile_shape)

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512,),
                array_itemsize=2,
                max_tile_bytes=512,
                sub_tile_shape=[32,]
            )
        self.assertSequenceEqual((256,), tile_shape)

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512,),
                array_itemsize=2,
                max_tile_bytes=512,
                sub_tile_shape=[60,]
            )
        self.assertSequenceEqual((180,), tile_shape)

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512,),
                array_itemsize=1,
                max_tile_bytes=512,
                halo=1
            )
        self.assertSequenceEqual((256,), tile_shape)

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512,),
                array_itemsize=1,
                max_tile_bytes=514,
                halo=1
            )
        self.assertSequenceEqual((512,), tile_shape)

    def test_calculate_tile_shape_for_max_bytes_2d(self):
        """
        Test case for :func:`array_split.split.calculate_tile_shape_for_max_bytes`,
        where :samp:`array_shape` parameter is 2D, i.e. of the form :samp:`(H,W)`.
        """
        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512, 512),
                array_itemsize=1,
                max_tile_bytes=512**2
            )
        self.assertSequenceEqual((512, 512), tile_shape.tolist())

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512, 512),
                array_itemsize=1,
                max_tile_bytes=512**2 - 1
            )
        self.assertSequenceEqual((256, 512), tile_shape.tolist())

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(513, 512),
                array_itemsize=1,
                max_tile_bytes=512**2 - 1
            )
        self.assertSequenceEqual((513 // 3, 512), tile_shape.tolist())

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512, 512),
                array_itemsize=1,
                max_tile_bytes=512**2//2
            )
        self.assertSequenceEqual((256, 512), tile_shape.tolist())

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512, 512),
                array_itemsize=2,
                max_tile_bytes=512**2//2
            )
        self.assertSequenceEqual((128, 512), tile_shape.tolist())

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512, 512),
                array_itemsize=2,
                max_tile_bytes=512**2//2,
                sub_tile_shape=(32, 64)
            )
        self.assertSequenceEqual((128, 512), tile_shape.tolist())

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512, 512),
                array_itemsize=1,
                max_tile_bytes=512**2//2,
                sub_tile_shape=(30, 64)
            )
        self.assertSequenceEqual((180, 512), tile_shape.tolist())

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512, 512),
                array_itemsize=2,
                max_tile_bytes=512**2//2,
                sub_tile_shape=(30, 64)
            )
        self.assertSequenceEqual((90, 512), tile_shape.tolist())

        tile_shape = \
            calculate_tile_shape_for_max_bytes(
                array_shape=(512, 1024),
                array_itemsize=1,
                max_tile_bytes=512**2,
                sub_tile_shape=(30, 60)
            )
        self.assertSequenceEqual((180, 540), tile_shape.tolist())

    def test_array_split(self):
        """
        Test for case for :func:`array_split.split.array_split`.
        """
        x = _np.arange(9.0)
        self.assertArraySplitEqual(
            _np.array_split(x, 3),
            array_split(x, 3)
        )
        self.assertArraySplitEqual(
            _np.array_split(x, 4),
            array_split(x, 4)
        )
        idx = [2, 3, 5, ]
        self.assertArraySplitEqual(
            _np.array_split(x, idx),
            array_split(x, idx)
        )

        x = _np.arange(32)
        x = x.reshape((4, 8))
        self.logger.info("_np.array_split(x, 3, axis=0) = \n%s", _np.array_split(x, 3, axis=0))
        self.logger.info(
            "array_split.split.array_split(x, 3, axis=0) = \n%s", array_split(x, 3, axis=0)
        )
        self.assertArraySplitEqual(
            _np.array_split(x, 3, axis=0),
            array_split(x, 3, axis=0)
        )

        self.logger.info("_np.array_split(x, 3, axis=1) = \n%s", _np.array_split(x, 3, axis=1))
        self.logger.info(
            "array_split.split.array_split(x, 3, axis=1) = \n%s", array_split(x, 3, axis=1)
        )
        self.assertArraySplitEqual(
            _np.array_split(x, 3, axis=1),
            array_split(x, 3, axis=1)
        )

        self.logger.info("_np.array_split(x, 8, axis=0) = \n%s", _np.array_split(x, 8, axis=0))
        self.assertArraySplitEqual(
            _np.array_split(x, 8, axis=0),
            array_split(x, 8, axis=0)
        )

    def test_split_by_per_axis_indices(self):
        """
        Test for case for splitting by specified
        indices::

           ArraySplitter(array_shape=(10, 4), indices_or_sections=[[2, 6, 8], ]).calculate_split()


        """
        splitter = ArraySplitter((10, 4), [[2, 6, 8], ])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [4, 1]))
        self.assertEqual(slice(0, 2), split[0, 0][0])  # axis 0 slice
        self.assertEqual(slice(2, 6), split[1, 0][0])  # axis 0 slice
        self.assertEqual(slice(6, 8), split[2, 0][0])  # axis 0 slice
        self.assertEqual(slice(8, 10), split[3, 0][0])  # axis 0 slice
        self.assertEqual(slice(0, 4), split[0, 0][1])  # axis 1 slice
        self.assertEqual(slice(0, 4), split[1, 0][1])  # axis 1 slice
        self.assertEqual(slice(0, 4), split[2, 0][1])  # axis 1 slice
        self.assertEqual(slice(0, 4), split[3, 0][1])  # axis 1 slice

        splitter = ArraySplitter((10, 13), [None, [2, 5, 8], ])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [1, 4]))
        self.assertEqual(slice(0, 10), split[0, 0][0])  # axis 0 slice
        self.assertEqual(slice(0, 10), split[0, 1][0])  # axis 0 slice
        self.assertEqual(slice(0, 10), split[0, 2][0])  # axis 0 slice
        self.assertEqual(slice(0, 10), split[0, 3][0])  # axis 0 slice
        self.assertEqual(slice(0, 2), split[0, 0][1])  # axis 1 slice
        self.assertEqual(slice(2, 5), split[0, 1][1])  # axis 1 slice
        self.assertEqual(slice(5, 8), split[0, 2][1])  # axis 1 slice
        self.assertEqual(slice(8, 13), split[0, 3][1])  # axis 1 slice

        splitter = ArraySplitter((10, 4), [[2, 6], [2, ]])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [3, 2]))
        self.assertEqual(slice(0, 2), split[0, 0][0])  # axis 0 slice
        self.assertEqual(slice(2, 6), split[1, 0][0])  # axis 0 slice
        self.assertEqual(slice(6, 10), split[2, 0][0])  # axis 0 slice
        self.assertEqual(slice(0, 2), split[0, 1][0])  # axis 0 slice
        self.assertEqual(slice(2, 6), split[1, 1][0])  # axis 0 slice
        self.assertEqual(slice(6, 10), split[2, 1][0])  # axis 0 slice

        self.assertEqual(slice(0, 2), split[0, 0][1])  # axis 1 slice
        self.assertEqual(slice(0, 2), split[1, 0][1])  # axis 1 slice
        self.assertEqual(slice(0, 2), split[2, 0][1])  # axis 1 slice
        self.assertEqual(slice(2, 4), split[0, 1][1])  # axis 1 slice
        self.assertEqual(slice(2, 4), split[1, 1][1])  # axis 1 slice
        self.assertEqual(slice(2, 4), split[2, 1][1])  # axis 1 slice

        splitter = ArraySplitter((10,), [[2, 6, 8], ])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [4, ]))
        self.assertEqual(slice(0, 2), split[0][0])  # axis 0 slice
        self.assertEqual(slice(2, 6), split[1][0])  # axis 0 slice
        self.assertEqual(slice(6, 8), split[2][0])  # axis 0 slice
        self.assertEqual(slice(8, 10), split[3][0])  # axis 0 slice

    def test_split_by_num_slices(self):
        """
        Test for case for splitting by number of
        slice elements::

           ArraySplitter(array_shape=(10, 13), indices_or_sections=3).calculate_split()
           ArraySplitter(array_shape=(10, 13), axis=[2, 3]).calculate_split()


        """
        splitter = ArraySplitter((10,), 3)
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [3, ]))
        self.assertEqual(slice(0, 4), split[0][0])  # axis 0 slice
        self.assertEqual(slice(4, 7), split[1][0])  # axis 0 slice
        self.assertEqual(slice(7, 10), split[2][0])  # axis 0 slice

        splitter = ArraySplitter((10,), axis=[3, ])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [3, ]))
        self.assertEqual(slice(0, 4), split[0][0])  # axis 0 slice
        self.assertEqual(slice(4, 7), split[1][0])  # axis 0 slice
        self.assertEqual(slice(7, 10), split[2][0])  # axis 0 slice

        splitter = ArraySplitter((10,), 3, axis=[3, ])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [3, ]))
        self.assertEqual(slice(0, 4), split[0][0])  # axis 0 slice
        self.assertEqual(slice(4, 7), split[1][0])  # axis 0 slice
        self.assertEqual(slice(7, 10), split[2][0])  # axis 0 slice

        splitter = ArraySplitter((10,), 3, axis=[0, ])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [3, ]))
        self.assertEqual(slice(0, 4), split[0][0])  # axis 0 slice
        self.assertEqual(slice(4, 7), split[1][0])  # axis 0 slice
        self.assertEqual(slice(7, 10), split[2][0])  # axis 0 slice

        splitter = ArraySplitter((10,), 2, axis=[0, ])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [2, ]))
        self.assertEqual(slice(0, 5), split[0][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1][0])  # axis 0 slice

        splitter = ArraySplitter((10, 13), 4, axis=[1, 0])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [1, 4]))
        self.assertEqual(slice(0, 10), split[0, 0][0])  # axis 0 slice
        self.assertEqual(slice(0, 10), split[0, 1][0])  # axis 0 slice
        self.assertEqual(slice(0, 10), split[0, 2][0])  # axis 0 slice
        self.assertEqual(slice(0, 10), split[0, 3][0])  # axis 0 slice
        self.assertEqual(slice(0, 4), split[0, 0][1])  # axis 1 slice
        self.assertEqual(slice(4, 7), split[0, 1][1])  # axis 1 slice
        self.assertEqual(slice(7, 10), split[0, 2][1])  # axis 1 slice
        self.assertEqual(slice(10, 13), split[0, 3][1])  # axis 1 slice

        splitter = ArraySplitter((10, 13), axis=[2, 2])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [2, 2]))
        self.assertEqual(slice(0, 5), split[0, 0][0])  # axis 0 slice
        self.assertEqual(slice(0, 5), split[0, 1][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1, 0][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1, 1][0])  # axis 0 slice
        self.assertEqual(slice(0, 7), split[0, 0][1])  # axis 1 slice
        self.assertEqual(slice(7, 13), split[0, 1][1])  # axis 1 slice
        self.assertEqual(slice(0, 7), split[1, 0][1])  # axis 1 slice
        self.assertEqual(slice(7, 13), split[1, 1][1])  # axis 1 slice

        splitter = ArraySplitter((10, 13), 4, axis=[2, 2])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [2, 2]))
        self.assertEqual(slice(0, 5), split[0, 0][0])  # axis 0 slice
        self.assertEqual(slice(0, 5), split[0, 1][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1, 0][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1, 1][0])  # axis 0 slice
        self.assertEqual(slice(0, 7), split[0, 0][1])  # axis 1 slice
        self.assertEqual(slice(7, 13), split[0, 1][1])  # axis 1 slice
        self.assertEqual(slice(0, 7), split[1, 0][1])  # axis 1 slice
        self.assertEqual(slice(7, 13), split[1, 1][1])  # axis 1 slice

        splitter = ArraySplitter((10, 13), 4, axis=[0, 2])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [2, 2]))
        self.assertEqual(slice(0, 5), split[0, 0][0])  # axis 0 slice
        self.assertEqual(slice(0, 5), split[0, 1][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1, 0][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1, 1][0])  # axis 0 slice
        self.assertEqual(slice(0, 7), split[0, 0][1])  # axis 1 slice
        self.assertEqual(slice(7, 13), split[0, 1][1])  # axis 1 slice
        self.assertEqual(slice(0, 7), split[1, 0][1])  # axis 1 slice
        self.assertEqual(slice(7, 13), split[1, 1][1])  # axis 1 slice

        splitter = ArraySplitter((10, 13), 4, axis=[2, 0])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [2, 2]))
        self.assertEqual(slice(0, 5), split[0, 0][0])  # axis 0 slice
        self.assertEqual(slice(0, 5), split[0, 1][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1, 0][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1, 1][0])  # axis 0 slice
        self.assertEqual(slice(0, 7), split[0, 0][1])  # axis 1 slice
        self.assertEqual(slice(7, 13), split[0, 1][1])  # axis 1 slice
        self.assertEqual(slice(0, 7), split[1, 0][1])  # axis 1 slice
        self.assertEqual(slice(7, 13), split[1, 1][1])  # axis 1 slice

        splitter = ArraySplitter((10, 13), 4, axis=[0, 0])
        split = splitter.calculate_split()
        self.logger.info("split.shape = %s", split.shape)
        self.logger.info("split =\n%s", split)
        self.assertTrue(_np.all(_np.array(split.shape) == [2, 2]))
        self.assertEqual(slice(0, 5), split[0, 0][0])  # axis 0 slice
        self.assertEqual(slice(0, 5), split[0, 1][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1, 0][0])  # axis 0 slice
        self.assertEqual(slice(5, 10), split[1, 1][0])  # axis 0 slice
        self.assertEqual(slice(0, 7), split[0, 0][1])  # axis 1 slice
        self.assertEqual(slice(7, 13), split[0, 1][1])  # axis 1 slice
        self.assertEqual(slice(0, 7), split[1, 0][1])  # axis 1 slice
        self.assertEqual(slice(7, 13), split[1, 1][1])  # axis 1 slice

__all__ = [s for s in dir() if not s.startswith('_')]

_unittest.main(__name__)