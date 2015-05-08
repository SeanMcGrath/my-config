"""
Oscilloscope
================

Classes to represent, control, and read out VISA Oscilloscopes.
"""

import visa, numpy as np, matplotlib.pyplot as plt

class GenericOscilloscope:
	"""
	Object representation of scope of unknown make.
	"""

	def __init__(self, VISA):
		"""
		Constructor.

		Parameters:
			:VISA: object representing VISA instrument, on which PyVisa can be used.
		"""
		self.scope = VISA

	def query(self, command):
		"""
		Issues query to scope and returns output.

		Parameters:
			:command: command to be written to scope.

		:Returns: the output of the scope given in response to command.
		"""

		try:
			self.scope.write(command)
			return self.scope.read().strip()
		except Exception:
			print(Exception)
			pass

	def write(self, toWrite):
		"""
		Writes argument to scope.

		Parameters:
			:toWrite: command to be issued to scope.
		"""

		self.scope.write(toWrite)

	def read(self):
		"""
		Reads one line of scope output.

		:Returns: string of scope output
		"""
		try:
			return self.scope.read().strip()
		except visa.VisaIOError:
			print("VISA Error: Command timed out.")

class TDS2024B(GenericOscilloscope):
	"""
	Class representing Tektronix 2024B.
	"""

	def __init__(self, VISA, make, model, serialNum, firmware):
		"""
		Constructor.

		Parameters:
			:VISA: object representing VISA instrument, on which PyVisa can be used.
			:brand: brand of scope
			:model: model of scope
			:serial: serial number of scope
			:firmware: scope firmware version
		"""

		GenericOscilloscope.__init__(self,VISA)

		self.make = make
		self.model = model
		self.serialNumber = serialNum
		self.firmwareVersion = firmware
		self.waveformSetup()
		
	def waveformSetup(self):
		"""
		Acquires and stores all necessary parameters for waveform transfer and display.
		"""

		self.dataChannel = self.query("DAT:SOU?") 	# get active channel
		preamble = self.query("WFMP?").split(';')	# get waveform preamble and parse it
		self.dataWidth = int(preamble[0])
		self.bitsPerPoint = int(preamble[1])
		self.encoding = preamble[2]
		self.binaryFormat = preamble[3]
		self.sigBit = preamble[4]
		self.numberOfPoints = int(preamble[5])
		self.pointFormat = preamble[7]
		self.xIncr = float(preamble[8])
		self.xOff = float(preamble[9])
		self.xZero = float(preamble[10])
		self.xUnit = preamble[11].strip('"')
		if self.xUnit == 's':
			self.xUnit = 'Seconds'
		self.yMult = float(preamble[12])
		self.yZero = float(preamble[13])
		self.yOff = float(preamble[14])
		self.yUnit = preamble[15].strip('"')

	def __str__(self):
		"""
		Object to String.
		"""
		return "{:s} {:s} Oscilloscope. Serial Number: {:s}. Output on {:s} in {:s} format.".format(self.make,self.model,self.serialNumber,self.dataChannel,self.encoding)

	def getWaveform(self):
		"""
		Acquire entire waveform, both preamble and curve data.

		:Returns: a semicolon-separated preamble followd by a comma-separated list of raw ADC levels.
		"""
		try:
			return self.query("WAVF?")
		except AttributeError:
			print("Error acquiring waveform data.")
			pass

	def getCurve(self):
		"""
		Set up waveform acquisition and get curve data.

		:Returns: a list of voltage values describing a captured waveform.
		"""

		self.waveformSetup()

		try:
			curveData = self.query("CURV?").split(',')
			curveData = list(map(int,curveData))
			for i in range(0,len(curveData)):
				curveData[i] = self.yZero +self.yMult*(curveData[i]-self.yOff)
			return curveData

		except AttributeError:
			print("Error acquiring waveform data.")
			pass


	def plotCurve(self):
		"""
		Create and display a pyplot of captured waveform.
		"""

		curve = self.getCurve()
		xArray = np.arange(0,self.numberOfPoints*self.xIncr,self.xIncr)
		unitSet = self.autosetUnits(xArray)
		xArray = unitSet[0]
		self.xUnit = unitSet[1] + self.xUnit
		unitSet = self.autosetUnits(curve)
		curve = unitSet[0]
		self.yUnit = unitSet[1] + self.yUnit
		plt.plot(xArray,curve)
		plt.title("Waveform Capture")
		plt.ylabel(self.yUnit)
		plt.xlabel(self.xUnit)
		plt.show()

	def autosetUnits(self, axisArray):
		"""
		Set the X units of the pyplot to the correct size based on the values in axisArray.

		Parameters:
			:axisArray: the array of values representing one dimension of the waveform.
		"""
		xMax = np.amax(axisArray)
		if xMax > 1e-9:
			if xMax > 1e-6:
				if xMax > 1e-3:
					if xMax > 1:
						prefix = ''
						return [axisArray,prefix]

					prefix = 'milli'
					axisArray = np.multiply(axisArray,1000)
					return [axisArray,prefix]

				prefix = 'micro'
				axisArray = np.multiply(axisArray,1e6)
				return [axisArray,prefix]

			prefix = 'nano'
			axisArray = np.multiply(axisArray,1e9)
			return [axisArray,prefix]

		prefix = ''
		return [axisArray,prefix]

	def checkTrigger(self):
		"""
		Read trigger status of TDS2024B.

		:Returns: a string describing trigger status: {AUTO | READY | TRIGGER | ARMED}
		"""

		try:
			return self.query("TRIG:STATE?")
		except:
			pass

	def __setParam(self, command):
		"""
		Set a scope parameter by issuing a command.

		:Parameters:
			:command: Full command to set parameter, in string form.

		:Returns: True if setting is successful, false otherwise.
		"""

		try:
			self.write(command)
			return True
		except AttributeError:
			return False

	def __getParam(self, command):
		"""
		get a scope parameter by issuing a command.

		:Parameters:
			:command: Full command to set parameter, in string form.

		:Returns: desired Parameter if communication is successful, False otherwise.
		"""

		try: return self.query(command).strip("'")
		except Exception: return False

	"""
	ACQUISITION COMMANDS
	"""

	def getAcquisitionParams(self):
		"""
		:Returns: scope acquisition parameters as a string.
		"""

		return __getParam("ACQ?")

	def setAcquisitionMode(self, mode):
		"""
		Set TDS2024B acquisition mode.

		:Parameters:
			:mode: Desired mode of scope operation: {SAMPLE | PEAK | AVERAGE}

		:Returns: True if setting is successful, false otherwise.
		"""

		return self.__setParam("ACQ:MOD " + str(mode))

	def getAcquisitionMode(self):
		"""
		:Returns: String naming current acquisition mode.
		"""

		return self.__getParam("ACQ:MOD?")

	def getNumberOfAcquisitions(self):
		"""
		:Returns: the number of acquisitions made.
		"""

		return self.__getParam('ACQ:NUMAC?')

	def setAcqsForAverage(self, acqs):
		"""
		Set the number of acquisitions made to find an average waveform in AVERAGE mode.

		:Parameters:
			:acqs: desired number of acquisitions per average reading: {4 | 16 | 64 | 128}

		:Returns: True if setting is successful, false otherwise.
		"""

		if acqs not in [4,16,64,128]: return False

		return self.__setParam("ACQ:NUMAV " +str(acqs))

	def getAcqsForAverage(self):
		"""
		:Returns: the current number of acquisitions taken to find an average waveform in AVERAGE mode.
		"""

		return self.__getParam('ACQ:NUMAV?')

	def setAcqState(self, state):
		"""
		Sets the scope's acquisition state.

		:Parameters:
			:state: a string naming the desired acquisition state: { OFF | ON | RUN | STOP | <NR1> }

		:Returns: True if setting is successful, false otherwise.
		"""

		return self.__setParam("ACQ:STATE " +str(state))

	def getAcqState(self):
		"""
		:Returns: '0' for off, '1' for on.
		"""

		return self.__getParam("ACQ:STATE?")

	def setAcqStop(self, stop):
		"""
		Tells the oscilloscope when to stop taking acquisitions.

		:Returns: True if setting is successful, False otherwise.
		"""

		return self.__setParam("ACQ:STOPA " +str(stop))

	def getAcqStop(self):
		"""
		:Returns: string describing when the scope stops taking acquisitions, or False if this fails.
		"""

		return self.__getParam("ACQ:STOPA?")

	"""
	END ACQUISITION COMMANDS
	"""

	"""
	CALIBRATION COMMANDS
	"""

	def calibrate(self):
		"""
		Perform an internal self-calibration and return result status.

		:Returns: string describing result of calibration.
		"""

		return self.__getParam("*CAL?")

	def abortCalibrate(self):
		"""
		Stops an in-progress factory calibration process.

		:Returns: True if setting is successful, False otherwise.
		"""

		return self.__setParam("CAL:ABO")

	def continueCalibrate(self):
		"""
		Perform the next step in the factory calibration sequence.

		:Returns: True if command is successful, False otherwise.
		"""

		return self.__setParam("CAL:CONTINUE")

	def factoryCalibrate(self):
		"""
		Initialize factory calibration sequence.

		:Returns: True if command is successful, False otherwise.
		"""

		return self.__setParam("CAL:FAC")

	def internalCalibrate(self):
		"""
		Initialize internal calibration sequence.

		:Returns: True if command is successful, False otherwise.
		"""

		return self.__setParam("CAL:INTERNAL")

	def getCalStatus(self):
		"""
		Return PASS or FAIL status of the last self or factory-calibration operation.

		:Returns: "PASS" if last calibration was successful, "FAIL" otherwise.
		"""

		return self.__getParam("CAL:STATUS?")

	def getDiagnosticResult(self):
		"""
		Return diagnostic tests status.

		:Returns: "PASS" if scope passes all diagnostic tests, "FAIL" otherwise.
		"""

		return self.__getParam("DIA:RESUL:FLA?")

	def getDiagnosticLog(self):
		"""
		Return diagnostic test sequence results.

		:Returns: A comma-separated string containing the results of internal diagnostic routines.
		"""

		return self.__getParam("DIA:RESUL:LOG?").strip()

	def getFirstError(self):
		"""
		Returns first message in error log.

		:Returns: a string describing an internal scope error, empty string if error queue is empty.
		"""

		return self.__getParam("ERRLOG:FIRST?")

	def getNextError(self):
		"""
		Returns next message in error log.

		:Returns: a string describing an internal scope error, empty string if error queue is empty.
		"""

		return self.__getParam("ERRLOG:NEXT?")

	"""
	END CALIBRATION COMMANDS
	"""

	"""
	CURSOR COMMANDS
	"""

	def getCursor(self):
		"""
		Get cursor settings.

		:Returns: comma-separated string containing cursor settings.
		"""

		return self.__getParam("CURS?")










	def getAllEvents(self):
		"""
		:Returns: all events in the event queue in string format.
		"""

		return self.__getParam("ALLE?")










