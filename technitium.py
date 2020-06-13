"""
	Code for cost optimized resouce allocations
	- Ajay Raj S
"""

import pprint

capacities = {
	320: "10XLarge",
	160: "8XLarge",
	80: "4XLarge",
	40: "2XLarge",
	20: "XLarge",
	10: "Large",
}

countries = ['NewYork', 'India', 'China']
newyork_units = [320, 160, 80, 40, 20, 10]
india_units = [320, 160, 80, 40, 10]
china_units = [160, 80, 20, 10]

cost = {
	'NewYork': {320: 2820, 160: 1400, 80: 774, 40: 450, 20: 230, 10: 120},
	'India': {320: 2970, 160: 1300, 80: 890, 40: 413, 10: 140},
	'China': {160: 1180, 80: 670, 20: 200, 10: 110},
}

def possible_answers(user_units, upper, country):	
	temp_for_iarr = list()

	units = which_unit(country)

	rem = user_units
	
	while rem > 0:
		rem = user_units % units[upper]
		quo = user_units // units[upper]
		temp_for_iarr.append(int(quo))						# stores the count in even index
		temp_for_iarr.append(int(units[upper]))				# stores the value in odd index
		user_units = rem
		if rem > 0:
			upper = find_the_upper(user_units, country, upper)
		else:
			break

	return temp_for_iarr



def find_the_upper(user_units, country, upper=0):
	up_value = upper

	units = which_unit(country)

	for i in range(up_value, len(units)):
		if user_units >= units[i]:
			up_value = i
			break
	return up_value


def which_unit(country):
	units = None
	if country == 'NewYork':
		units = newyork_units
	elif country == 'India':
		units = india_units
	else:
		units = china_units
	return units	


def calculate_minimum(country, country_unit, hours=1):	
	minimum_cost = None
	machines = list()
	country_cost = cost[country]
	minimum_machine = 0
	for index, values in country_unit.items():
		temp_total = 0
		i = 0
		while i < len(values):
			temp_total += (values[i] * country_cost[values[i+1]]) * hours
			i += 2
		if minimum_cost is None or temp_total < minimum_cost:
			minimum_cost = temp_total
			minimum_machine = index

	minimum_cost = "$"+str(minimum_cost)
	# process to store the machine layout
	x = 0
	while x < len(country_unit[minimum_machine]):
		temp = (capacities[country_unit[minimum_machine][x+1]], country_unit[minimum_machine][x])
		machines.append(temp)
		x += 2

	return_val = {
		"region": country,
		"total_cost": minimum_cost,
		"machines": machines,
	}
	return return_val


# Main Execution starts here
try:
	user_units = int(input('Machine units - '))
	hours = int(input('Hours - '))
	if user_units < 10:
		print('Units should not be less than 10')
		quit()
	if user_units % 10 != 0.0:
		print('Units should be in units of 10')
		quit()
	if hours < 0:
		print('Hours Should not be less than 1')
		quit()
	
	total = dict()

	for country in countries:
		total[country] = {}
		first_upper = find_the_upper(user_units, country)
		temp = dict()
		units = which_unit(country)
		for x in range(first_upper, len(units)):			
			temp[first_upper] = possible_answers(user_units, first_upper, country)
			first_upper += 1
		total[country] = temp

	final_country_values = dict()
	final_country_values['Output'] = list()

	for country, values in total.items():
		final_country_values['Output'].append(calculate_minimum(country, values, hours))

	pprint.pprint(final_country_values)

except ValueError:
	print('Number required')
except:
	print('Some error happened')
