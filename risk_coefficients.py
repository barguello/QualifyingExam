import scipy
import matplotlib
import matplotlib.pyplot as plt

def ddQuadratic(w,c):
	return -2*c

def dQuadratic(w,b,c):
	return b - 2*c*w

def ddLinearPlusExponential(w,a,b,rho):
	return float(b)/rho**2*scipy.exp(-w/rho)

def dLinearPlusExponential(w,a,b,rho):
	return a - w/float(rho)*scipy.exp(-w/rho)

def ddLogarithmic(w):
	return 1.0/w

def dLogarithmic(w):
	return w

def plot_coefficients(title, utility_type):
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

def draw_coefficients():
	#plot_constant_coefficients('Linear Risk Coefficients', 0)
	#plot_coefficients('Quadratic Risk Coefficients', 'quadratic')
	#plot_constant_coefficients('Exponential Risk Coefficients', 2)
	#plot_coefficients('Logarithmic Risk Coefficients', 'logarithmic')
	plot_coefficients('Linear Plus Exponential Risk Coefficients', 'linear_plus_exponential')

draw_coefficients()
