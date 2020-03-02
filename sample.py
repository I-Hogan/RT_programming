# program for strength programming based on ideal gaussian

import numpy as np

def get_samples(num_samples,mean,sd):
	return np.random.normal(mean,sd,num_samples)

#constants
is_testing = False #makes values large
ramp = False #sorts values, binned by month
balence = False #generates samples for each weak (vs all at once)
org_month = True #sort the intensities in each month
chaotic_loading = False #randomly do everything on a uniform distribution
chaotic_intensities = False #random intensity from a uniform distribution
set_size_mult = 1 #samples from a larger set (implications for extreme values)
months = 1
weekly_sess = 5
mean = 77.5 #theoretically correct value
#mean = 75.0 #mathmatically simple value
sd = 3.706 #theoretically correct value
#sd = 8 #fun value
intensities = [33,44,55,66]
onerm = 190 #Est. 1RM (lbs) (current: 3rm 175lb)
month_reps = 300 #if round_cor = 1, month_reps = about 1.015 * programmed reps
#round_cor = 1.015 #corrects for issues introduced for end of month max
round_cor = 1.0
stress_cor = 1.5 #higher means less correction, 1 is 50%
average_reps = 5.0 #leave at 5 or 4.9
intensity_rel = 35 # approximate relationship between 1rm and nrm (higher means less fall off)

#test vals
if is_testing:
	months = 1000
	onerm = 10000
	month_reps = 10000

#calcs
total_sessions = months * 4 * weekly_sess
total_samples = total_sessions * set_size_mult

#correct total sets for backload protocal
if org_month:
	month_reps *= 1.0652


is_good = False
while not is_good:
	is_good = True

	#un-balenced sample gaussian
	samples = get_samples(total_samples,mean,sd)

	#un-balenced sample uniform
	if chaotic_loading: 
		samples = np.random.uniform(65.0,90.0,total_samples)

	#intensities as samples of a uniform distribution
	if chaotic_intensities:
		intensities = np.random.uniform(33.3,66.6,total_samples)

	#balenced sample
	if balence:
		samples = np.empty([0])
		for i in range(months):
			for j in range(4):
				use_mean = mean
				new_samples = get_samples(weekly_sess,use_mean,sd)
				samples = np.append(samples, new_samples)
			samples[len(samples) - 1] = 93.0

	#organize block volumes for peak
	if ramp: 
		samples = np.sort(samples)
		month_org = samples.reshape((months,(4*weekly_sess)))
		[np.random.shuffle(xi) for xi in month_org]
		month_flat = month_org.flatten()
		samples = month_flat
		
	#backload monthly intensity
	if org_month:
		month_org = samples.reshape((months,(4*weekly_sess)))
		month_org = np.array([np.sort(xi) for xi in month_org])
		samples = month_org.flatten()

	#calculate and print plan
	print("PROGRAM")

	sess_num = 0
	total_reps = 0
	total_sets = 0
	total_error = 0
	total_weight = 0
	total_heavy = 0
	real_x = []
	for i in range(months*4):
		print("Week ",i+1,":  ",sep='',end='')
		for j in range(weekly_sess):
			if chaotic_intensities:
				intensity = intensities[((i*weekly_sess)+j)%len(intensities)]/100.0 
			else:
				intensity = intensities[i%len(intensities)]/100.0 
			x = samples[sess_num]/100.0 # percentage of 1rm / 100
			nrm = (-intensity_rel*(x-1))+1
			reps = nrm * intensity
			correction = reps/round(reps)
			correct_nrm = nrm/correction
			correct_x = -correct_nrm/intensity_rel+1/intensity_rel+1
			weight = int(round(correct_x*onerm))
			sets = ((month_reps*round_cor/4.0)/weekly_sess)/round(reps) * (round(reps)/average_reps + (1*stress_cor)) / (stress_cor+1)
			total_reps += int(round(reps))*int(round(sets))
			total_sets += int(round(sets))
			real_x.append(weight / float(onerm))
			print("\t",(10 * round((weight-5)/10))+5,"lb x ",int(round(reps))," x ",int(round(sets)),sep='',end='')
			#print(" i:",int(intensity*100),end='')
			total_error += (np.abs(weight - ((10 * round((weight-5)/10))+5))*int(round(reps))*int(round(sets)))/weight
			total_weight += ((10 * round((weight-5)/10))+5)*int(round(reps))*int(round(sets))
			if intensity * x >= .5:
				total_heavy += 1
			#print(" t:",round(intensity,2),round(x,2),end='')
			sess_num += 1
		print()

	print("\nSTATS")	
	print("Monthly Reps:\t", round(total_reps/float(months),1),sep='')
	print("Monthly Tonnes:\t", round((total_weight/float(months))/2204.6,1),sep='')
	print("Mean Error:\t", round(100*total_error/float(total_reps),2),"%",sep='')
	print("Mean Sets:\t", round(total_sets/float(total_sessions),2),sep='')	
	print("Mean Reps:\t", round(total_reps/float(total_sets),2),sep='')	
	print("Mean % 1rm:\t", round(np.mean(np.array(real_x))*100,2),sep='')
	print("Mean std dist:\t", round(np.std(np.array(real_x))*100,2),sep='')	

	if abs(round(np.std(np.array(real_x))*100,2) - sd) > 0.2: #check for close standard distribution
		is_good = False
	
	if abs(round(np.mean(np.array(real_x))*100,2) - mean) > .5: #check for close mean
		is_good = False	
	
	
	
	
	
	
	
	
	
	
	