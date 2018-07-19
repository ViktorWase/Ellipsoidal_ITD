import scipy.io as sio

from math import isnan

def read_ellipse_data():
	anthro_mat = sio.loadmat('CIPIC_hrtf_database/anthropometry/anthro.mat')

	anthro = anthro_mat['X']
	out = []
	for i in range(len(anthro)):
		head_vals = [anthro[i][j] for j in range(5)]

		should_filter = False
		for j in range(len(head_vals)):
			try:
				head_vals[j] = float(head_vals[j])
				if isnan(head_vals[j]):
					should_filter = True
			except:
				should_filter = True

		if not should_filter:
			out.append(head_vals)
	return out

if __name__ == '__main__':
	print(read_ellipse_data())
	print("done.")
