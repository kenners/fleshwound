from datetime import date
import math

def getThoracoscore(dob,sex,asa,performanceStatus,dyspnoeaScore,priorityOfSurgery,procedureClass,diagnosisGroup,comorbidityScore):
	"""Calculates the Thoracoscore from supplied patient data.
	
	Requires: DoB, sex, ASA, Performance status, Dyspnoea score, Priority of surgery, Procedure class, Diagnosis group and Comorbidity score.
	
	Returns predicted mortality.
	"""
	# Lookup beta values for each parameter
	beta = {}
	
	# Age
	age = calculateAge(dob)
	if age < 55:
		beta['age'] = 0
	elif age >= 65:
		beta['age'] = 1.0073
	elif 55 <= age < 65:
		beta['age'] = 0.7679
	else:
		raise ValueError
	
	# Sex
	if (sex.lower() == 'm') or (sex.lower() == 'male'):
		beta['sex'] = 0.4505
	elif (sex.lower() == 'f') or (sex.lower() == 'female'):
		beta['sex'] = 0
	else:
		# raise an error
		raise ValueError
	
	# ASA
	if asa <= 2:
		beta['asa'] = 0
	elif asa >= 3:
		beta['asa'] = 0.6057
	else:
		raise ValueError
		
	# Performance status
	if performanceStatus <= 2:
		beta['performanceStatus'] = 0
	elif performanceStatus >= 3:
		beta['performanceStatus'] = 0.689
	else:
		raise ValueError
	
	# Dyspnoea score
	if dyspnoeaScore <= 2:
		beta['dyspnoeaScore'] = 0
	elif dyspnoeaScore >= 3:
		beta['dyspnoeaScore'] = 0.9075
	else:
		raise ValueError
	
	# Priority of surgery
	if (priorityOfSurgery.lower() == 'e') or (priorityOfSurgery.lower() == 'elective'):
		beta['priorityOfSurgery'] = 0
	elif (priorityOfSurgery.lower() == 'u') or (priorityOfSurgery.lower() == 'urgent') or (priorityOfSurgery.lower() == 'emergency'):
		beta['priorityOfSurgery'] = 0.8443
	else:
		raise ValueError
	
	# Procedure class
	if (procedureClass.lower() == 'o') or (procedureClass.lower() == 'other'):
		beta['procedureClass'] = 0
	elif (procedureClass.lower() == 'p') or (procedureClass.lower() == 'pneumonectomy'):
		beta['procedureClass'] = 1.2176
	else:
		raise ValueError
	
	# Diagnosis group
	if (diagnosisGroup.lower() == 'b') or (diagnosisGroup.lower() == 'benign'):
		beta['diagnosisGroup'] = 0
	elif (diagnosisGroup.lower() == 'm') or (diagnosisGroup.lower() == 'malignant'):
		beta['diagnosisGroup'] = 1.2423
	else:
		raise ValueError
	
	# Comorbidity score
	if comorbidityScore == 0:
		beta['comorbidityScore'] = 0
	elif comorbidityScore <= 2:
		beta['comorbidityScore'] = 0.7447
	elif comorbidityScore >= 3:
		beta['comorbidityScore'] = 0.9065
	else:
		raise ValueError
	
	# Calculate the beta sum
	betaSum = sum(beta.values())
	
	# Calculate thoracoscore (odds for predicted probability of in-hospital death)
	constant = -7.3737
	thoracoscore = math.exp(constant + betaSum) / (1 + math.exp(constant + betaSum))
	return thoracoscore

def calculateAge(born):
	today = date.today()
	try: # raised when birth date is February 29 and the current year is not a leap year
		birthday = born.replace(year=today.year)
	except ValueError:
		birthday = born.replace(year=today.year, day=born.day-1)
	if birthday > today:
		return today.year - born.year - 1
	else:
		return today.year - born.year