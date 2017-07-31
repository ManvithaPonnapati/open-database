import pickle
import sys
import io
import zlib
import gzip
import bz2
import warnings
import contextlib
import os
import numpy as np 
import pandas as pd
import joblib
from contextlib import closing
from io import BytesIO


from threading import RLock

Unpickler = pickle.Unpickler
Pickler = pickle.Pickler


# Magic numbers of supported compression file formats.        '
_ZFILE_PREFIX = b'ZF'  # used with pickle files created before 0.9.3.
_ZLIB_PREFIX = b'\x78'
_GZIP_PREFIX = b'\x1f\x8b'
_BZ2_PREFIX = b'BZ'
_XZ_PREFIX = b'\xfd\x37\x7a\x58\x5a'
_LZMA_PREFIX = b'\x5d\x00'

# Supported compressors
_COMPRESSORS = ('zlib', 'bz2', 'lzma', 'xz', 'gzip')
_COMPRESSOR_CLASSES = [gzip.GzipFile, bz2.BZ2File]

# The max magic number length of supported compression file types.
_MAX_PREFIX_LEN = max(len(prefix)
                      for prefix in (_ZFILE_PREFIX, _GZIP_PREFIX, _BZ2_PREFIX,
                                     _XZ_PREFIX, _LZMA_PREFIX))

# Buffer size used in io.BufferedReader and io.BufferedWriter
_IO_BUFFER_SIZE = 1024 ** 2

def hex_str(an_int):
    """Convert an int to an hexadecimal string."""
    return '{0:#x}'.format(an_int)

_MAX_LEN = len(hex_str(2 ** 64))
_CHUNK_SIZE = 64 * 1024

Path = None

####################################################################################



def _detect_compressor(fileobj):
    """Return the compressor matching fileobj."""

    # Ensure we read the first bytes.
    fileobj.seek(0)
    first_bytes = fileobj.read(_MAX_PREFIX_LEN)
    fileobj.seek(0)

    if first_bytes.startswith(_ZLIB_PREFIX):
        return "zlib"
    elif first_bytes.startswith(_GZIP_PREFIX):
        return "gzip"
    elif first_bytes.startswith(_BZ2_PREFIX):
        return "bz2"
    elif first_bytes.startswith(_LZMA_PREFIX):
        return "lzma"
    elif first_bytes.startswith(_XZ_PREFIX):
        return "xz"
    elif first_bytes.startswith(_ZFILE_PREFIX):
        return "compat"

    return "not-compressed"


def _read_fileobject(fileobj, filename, mmap_mode=None):
	compressor = _detect_compressor(fileobj)
	if compressor == 'compat':
		return filename

def read_zfile(file_handle):
    """Read the z-file and return the content as a string.
    Z-files are raw data compressed with zlib used internally by joblib
    for persistence. Backward compatibility is not guaranteed. Do not
    use for external purposes.
    """
    file_handle.seek(0)
    header_length = len(_ZFILE_PREFIX) + _MAX_LEN
    length = file_handle.read(header_length)
    length = length[len(_ZFILE_PREFIX):]
    length = int(length, 16)

    # With python2 and joblib version <= 0.8.4 compressed pickle header is one
    # character wider so we need to ignore an additional space if present.
    # Note: the first byte of the zlib data is guaranteed not to be a
    # space according to
    # https://tools.ietf.org/html/rfc6713#section-2.1
    next_byte = file_handle.read(1)
    if next_byte != b' ':
        # The zlib compressed data has started and we need to go back
        # one byte
        file_handle.seek(header_length)

    # We use the known length of the data to tell Zlib the size of the
    # buffer to allocate.
    data = zlib.decompress(file_handle.read(), 15, length)
    assert len(data) == length, (
        "Incorrect data length while decompressing %s."
        "The file could be corrupted." % file_handle)
    return data


class NDArrayWrapper(object):
    """An object to be persisted instead of numpy arrays.
    The only thing this object does, is to carry the filename in which
    the array has been persisted, and the array subclass.
    """

    def __init__(self, filename, subclass, allow_mmap=True):
        """Constructor. Store the useful information for later."""
        self.filename = filename
        self.subclass = subclass
        self.allow_mmap = allow_mmap

    def read(self, unpickler):
        """Reconstruct the array."""
        filename = os.path.join(unpickler._dirname, self.filename)
        # Load the array from the disk
        # use getattr instead of self.allow_mmap to ensure backward compat
        # with NDArrayWrapper instances pickled with joblib < 0.9.0
        allow_mmap = getattr(self, 'allow_mmap', True)
        memmap_kwargs = ({} if not allow_mmap
                         else {'mmap_mode': unpickler.mmap_mode})
        array = unpickler.np.load(filename, **memmap_kwargs)
        # Reconstruct subclasses. This does not work with old
        # versions of numpy
        if (hasattr(array, '__array_prepare__') and
            self.subclass not in (unpickler.np.ndarray,
                                  unpickler.np.memmap)):
            # We need to reconstruct another subclass
            new_array = unpickler.np.core.multiarray._reconstruct(
                self.subclass, (0,), 'b')
            return new_array.__array_prepare__(array)
        else:
			return array


class ZipNumpyUnpickler(Unpickler):
    """A subclass of the Unpickler to unpickle our numpy pickles."""

    dispatch = Unpickler.dispatch.copy()

    def __init__(self, filename, file_handle, mmap_mode=None):
        """Constructor."""
        self._filename = os.path.basename(filename)
        self._dirname = os.path.dirname(filename)
        self.mmap_mode = mmap_mode
        self.file_handle = self._open_pickle(file_handle)
        Unpickler.__init__(self, self.file_handle)
        try:
            import numpy as np
        except ImportError:
            np = None
        self.np = np

    def _open_pickle(self, file_handle):
        return BytesIO(read_zfile(file_handle))

    def load_build(self):
        """Set the state of a newly created object.
        We capture it to replace our place-holder objects,
        NDArrayWrapper, by the array we are interested in. We
        replace them directly in the stack of pickler.
        """
        Unpickler.load_build(self)
        if isinstance(self.stack[-1], NDArrayWrapper):
            if self.np is None:
                raise ImportError("Trying to unpickle an ndarray, "
                                  "but numpy didn't import correctly")
            nd_array_wrapper = self.stack.pop()
            array = nd_array_wrapper.read(self)
            self.stack.append(array)

    # Be careful to register our new method.
    dispatch[pickle.BUILD] = load_build


def load(filename, mmap_mode=None):
	"""Reconstruct a Python object from a file persisted with joblib.dump."""
	f = open(filename, 'rb')
	fobj = _read_fileobject(f, filename, mmap_mode)
	if isinstance(fobj, (str, unicode)):
		return load_compatibility(fobj)

	obj = _unpickle(fobj, filename, mmap_mode)

	return obj


def load_compatibility(filename):
	"""Reconstruct a Python object from a file persisted with joblib.dump.
	This function ensure the compatibility of joblib old persistence format (<= 0.9.3)"""
	file_handle = open(filename, 'rb')
	unpickler = ZipNumpyUnpickler(filename, file_handle=file_handle)
	try:
		obj = unpickler.load()
	finally:
		if hasattr(unpickler, 'file_handle'):
			unpickler.file_handle.close()
	return obj


def load_from_disk(filename):
	return load(filename)


class DiskDataset:

	def __init__(self, data_dir):
		self.data_dir = data_dir

		metadata_filename = os.path.join(self.data_dir, "metadata.joblib")
		if os.path.exists(metadata_filename):
			# self.tasks, self.metadata_df = joblib.load(metadata_filename)
			self.tasks, self.metadata_df = load_from_disk(metadata_filename)
		else:
			raise ValueError("No metadata found on disk")

	def __len__(self):
		"""
		Finds number of elements in dataset.
		"""
		total = 0
		for _, row in self.metadata_df.iterrows():
		  y = load_from_disk(os.path.join(self.data_dir, row['ids']))
		  total += len(y)
		return total

	def itershards(self):

		def iterate(dataset):
			for _, row in dataset.metadata_df.iterrows():
				X = np.array(load_from_disk(os.path.join(dataset.data_dir, row['X'])))
				ids = np.array(load_from_disk(os.path.join(dataset.data_dir, row['ids'])), dtype=object)

				if row['y'] is not None:
					y = np.array(load_from_disk(os.path.join(dataset.data_dir, row['y'])))
				else:
					y = None

				if row['w'] is not None:
					w_filename = os.path.join(dataset.data_dir, row['w'])
					if os.path.exists(w_filename):
						w = np.array(load_from_disk(w_filename))
					else:
						w = np.ones(y.shape)
				else:
					w = None
				yield (X, y, w, ids)

		return iterate(self)

	@property
	def ids(self):
		"""Get the ids vector for this dataset as a single numpy array"""
		if len(self) == 0:
			return np.array([])
		ids = []
		for (_, _, _, ids_b) in self.itershards():
			ids.append(np.atleast_1d(np.squeeze(ids_b)))
		return np.concatenate(ids)

	@property
	def X(self):
		"""Gets the X vector for this dataset as a single numpy array"""
		Xs = []
		one_dimensional = False
		for (X_b, _, _, _) in self.itershards():
			Xs.append(X_b)
			if len(X_b.shape) == 1:
				one_dimensional = True
			if not one_dimensional:
				return np.vstack(Xs)
			else:
				return np.concatenate(Xs)

	@property
	def y(self):
		"""Get the y vector for this dataset as a single numpy array."""
		ys = []
		for (_, y_b, _, _) in self.itershards():
			ys.append(y_b)
		return np.vstack(ys)

	@property
	def w(self):
		"""Get the weight vector for this dataset as a single numpy array."""
		ws = []
		for (_, _, w_b, _) in self.itershards():
			ws.append(np.array(w_b))
		return np.vstack(ws)
