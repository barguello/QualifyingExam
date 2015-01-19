import scipy
import scipy.optimize
import matplotlib
import matplotlib.pyplot as plt
import pdb

#Utility functions along with their inverses and derivatives
def Linear(w,a,b):
	return a + b*w

def invLinear(w,a,b):
	return (w-float(a))/b

def Quadratic(w,a,b,c):
	return a + b*w - c*w**2

def invQuadratic(w,a,b,c):
	return float(b)/(2*c) + scipy.sqrt(b*b+4*c*(a-w))/(2*c)

def ddQuadratic(w,c):
	return -2*c

def dQuadratic(w,b,c):
	return b - 2*c*w

def Exponential(w,a,b,rho):
	return a + b*scipy.exp(-w/float(rho))

def invExponential(w,a,b,rho):
	return -rho*scipy.log((w-a)/float(b))

def Logarithmic(w,a,b):
	return a + b*scipy.log(w)

def invLogarithmic(w,a,b):
	return scipy.exp((w-a)/float(b))

def ddLogarithmic(w):
	return 1.0/w

def dLogarithmic(w):
	return w

def LinearPlusExponential(w,a,b,rho):
	return a*w + b*scipy.exp(-w/float(rho))

def ddLinearPlusExponential(w,a,b,rho):
	return float(b)/rho**2*scipy.exp(-w/rho)

def dLinearPlusExponential(w,a,b,rho):
	return a - float(b)/rho*scipy.exp(-w/rho)

def invLinearPlusExponential(w,a,b,rho):
	def f(x, *args):
		return  w - LinearPlusExponential(x, *args)
	arguments = (a,b,rho) 
	return scipy.optimize.bisect(f, -200, 200000,  args = arguments, maxiter = 200)

def plot_coefficients(title, utility_type):
	'''Plots risk coefficients as a function of wealth for the given utility_type.  Title is used to title the plot'''

	w = scipy.linspace(0,20,10000)
	a = 2
	b = 2
	c = 2
	rho = 2

	fig = plt.figure()
	ax = matplotlib.pyplot.subplot(111)
	if utility_type == 'quadratic' :
		#fig.suptitle(title)
		ax.plot(w, ddQuadratic(w,c)/dQuadratic(w,b,c), color = 'r', label = 'aversion')
		ax.plot(w, dQuadratic(w,b,c)/ddQuadratic(w,c), label = 'tolerance')

	elif utility_type == 'linear_plus_exponential':
		#fig.suptitle(title)
		ax.plot(w, ddLinearPlusExponential(w,a,b,rho)/dLinearPlusExponential(w,a,b,rho), color = 'r', label = 'aversion')
		ax.plot(w, dLinearPlusExponential(w,a,b,rho)/ddLinearPlusExponential(w,a,b,rho), label = 'tolerance')

	elif utility_type == 'logarithmic':
		#fig.suptitle(title)
		ax.plot(w, ddLogarithmic(w)/dLogarithmic(w), color = 'r', label = 'aversion')
		ax.plot(w, dLogarithmic(w)/ddLogarithmic(w), label = 'tolerance')
	
	ax.legend()
	plt.xlabel('w')
	plt.ylabel('risk coefficient')
	plt.show()
	return

def plot_constant_coefficients(title, constant):
	'''Plots a constant function, constant, as well as 1/constant.  Title is used to title the plot'''

	w = scipy.linspace(0,20,10000)

	fig = plt.figure()
	ax = matplotlib.pyplot.subplot(111)
	#fig.suptitle(title)
	ax.plot(w, w*0 + constant, color = 'r', label = 'aversion')
	ax.plot(w, w*0 + scipy.inf, label = 'tolerance')

	ax.legend()
	plt.xlabel('w')
	plt.ylabel('risk coefficient')
	plt.show()
	return

#Problem 3
def draw_coefficients():
	'''Control function for creating a coefficient graph'''

	#plot_constant_coefficients('Linear Risk Coefficients', 0)
	#plot_coefficients('Quadratic Risk Coefficients', 'quadratic')
	#plot_constant_coefficients('Exponential Risk Coefficients', 2)
	#plot_coefficients('Logarithmic Risk Coefficients', 'logarithmic')
	plot_coefficients('Linear Plus Exponential Risk Coefficients', 'linear_plus_exponential')

def selling_price(w0, utility, inverse, lottery, probabilities, *args):
	'''Returns the selling price for a given lottery with amounts given by lottery and probabilities given by probabilities'''
	return inverse(sum([probabilities[index]*utility(w0 + amount, *args) for index,amount in enumerate(lottery)]), *args) - w0

def buying_price(w0, utility, lottery, probabilities, *args):
	'''Returns the selling price for a given lottery with amounts given by lottery and probabilities given by probabilities'''
	def f(x, utility, w0, lottery, probabilities, args):
		return utility(w0, *args) - sum(probabilities*utility(w0 + lottery - x, *args))
	
	return scipy.optimize.newton(f, 0, args = (utility, w0, lottery, probabilities, args))

#Problem 4
def get_prices(X, probs, w0, rho):
	quadratic_args = (2,2,2)
	exponential_args = (2,2,rho)
	logarithmic_args = (2,2)
	linear_plus_exponential_args = (2,2,rho)

	#printing results:
	print "linear selling price: 0  (through a simple hand calculation)" 
	print "linear buying price: 0 (through a simple hand calculation)"

	print "quadratic selling price: " + str(selling_price(w0, Quadratic, invQuadratic, X, probs, *quadratic_args))
	print "quadratic buying price: " + str(buying_price(w0, Quadratic, X, probs, *quadratic_args))

	print "exponential selling price: " + str(selling_price(w0, Exponential, invExponential, X, probs, *exponential_args))
	print "exponentialbuying price: " + str(buying_price(w0, Exponential, X, probs, *exponential_args))
	
	print "logarithmic selling price: " + str(selling_price(w0, Logarithmic, invLogarithmic, X, probs, *logarithmic_args))
	print "logarithmic buying price: " + str(buying_price(w0, Logarithmic, X, probs, *logarithmic_args))
	
	print "linear plus exponential selling price: " + str(selling_price(w0, LinearPlusExponential, invLinearPlusExponential, X, probs, *linear_plus_exponential_args))
	print "linear plus exponential buying price: " + str(buying_price(w0, LinearPlusExponential, X, probs, *linear_plus_exponential_args))

#Problem 5
def get_lottery_mean(X, probs):
	return sum(probs*X)

def plot_premiums(X, probs, rho):
	quadratic_args = (2,2,2)
	exponential_args = (2,2,rho)
	logarithmic_args = (2,2)
	linear_plus_exponential_args = (2,2,rho)
	w = scipy.linspace(-1000,1000,10000)
	lottery_mean = get_lottery_mean(X, probs)

	#plt.plot(w, w*0)
	#plt.plot(w, selling_price(w, Quadratic, invQuadratic, X, probs, *quadratic_args))
	#plt.plot(w, selling_price(w, Exponential, invExponential, X, probs, *exponential_args))
	#plt.plot(w, selling_price(w, Logarithmic, invLogarithmic, X, probs, *logarithmic_args))
	results = [selling_price(value, LinearPlusExponential, invLinearPlusExponential, X, probs, *linear_plus_exponential_args) for value in w]
	plt.plot(w, results)
	plt.xlabel('x')
	plt.ylabel('risk premium')
	plt.show()
	
X = scipy.array([500, -500])
probs = scipy.array([0.5, 0.5])
w0 = 1000
rho = 1000
plot_premiums(X, probs, rho)
