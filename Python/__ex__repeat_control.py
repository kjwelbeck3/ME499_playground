import numpy as np
from experiment_manager import ExperimentManager
import argparse

######
# EXAMPLES

##### mode/dir=x, delta=55, shape=(5,5), zero_borders=True
# [[  0   0   0   0   0]
#  [  0   0  55 110   0]
#  [  0   0  55 110   0]
#  [  0   0  55 110   0]
#  [  0   0   0   0   0]]
#

##### mode/dir=x, delta=55, shape=(5,5), zero_borders=False
# [[  0  55 110 165 220]
#  [  0  55 110 165 220]
#  [  0  55 110 165 220]
#  [  0  55 110 165 220]
#  [  0  55 110 165 220]]




def genColumnsByDelta(delta=15, shape=(5,5), start=0, zero_borders=False):
    
    zero_mat = np.zeros(shape, dtype=int)
    
    if zero_borders:
        shape = shape[0]-2, shape[1]-2
        
    mat = np.zeros((shape), dtype=int)
    
    for i in range(shape[1]):
        col = np.ones((shape[0]))*(start + i*delta)
        mat[:,i] = col
        
    if zero_borders:
        zero_mat[1:shape[0]+1, 1:shape[1]+1] = mat[:,:]
        return zero_mat
        
    return mat

def genRowsByDelta(delta=15, shape=(5,5), start=4, zero_borders=False):
    
    zero_mat = np.zeros(shape, dtype=int)
    
    if zero_borders:
        shape = shape[0]-2, shape[1]-2

    
    mat = np.zeros((shape), dtype=int)
    
    for i in range(shape[0]):
        row = np.ones((shape[1]))*(start + i*delta)
        mat[i, :] = row

        
    if zero_borders:
        zero_mat[1:shape[0]+1, 1:shape[1]+1] = mat[:,:]
        return zero_mat
        
    return mat

def zeroOutBorderCells(mat=np.ones((5,5), dtype=int)):
    
    n_rows, n_cols = mat.shape
    mat[0] = mat[:,0] = mat[n_rows-1] = mat[:, n_cols-1] = 0
    return mat
    

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--mode', default='x', choices=['x', 'y'], help="x/y to select control matrix direction")
    ap.add_argument('--start', default=10, type=int, help="starting delta between control matrix columns")
    ap.add_argument('--span', default=50, type=int, help="")
    ap.add_argument('--step', default=5, type=int, help="")
    ap.add_argument('--reps', default=5, type=int, help="Number of contiguous times to repeat each control matrix combination")
    ap.add_argument('--run-duration', default=.5, type=int, help="Duration in secs of each run")
    args = vars(ap.parse_args())

    print(args)
    phase_mat_list = []
    amplitude_mat_list = []

    for i in range(args['start'], args['start']+args['span'], args['step']):
        if args['mode'].lower() == 'x':
            for j in range(args["reps"]):
                # phase_mat_list.append(genColumnsByDelta(i, zero_borders=True))
                phase_mat_list.append(genColumnsByDelta(i, zero_borders=False))
                # amplitude_mat_list.append(zeroOutBorderCells(4*np.ones((5,5), dtype=int)))
                amplitude_mat_list.append(4*np.ones((5,5), dtype=int))

        elif args['mode'].lower() == 'y':
            for j in range(args["reps"]):    
                # phase_mat_list.append(genRowsByDelta(i, zero_borders=True))
                phase_mat_list.append(genRowsByDelta(i, zero_borders=False))
                # amplitude_mat_list.append(zeroOutBorderCells(4*np.ones((5,5), dtype=int)))
                amplitude_mat_list.append(4*np.ones((5,5), dtype=int))

    
    print("phase_mat_list")
    print(len(phase_mat_list))
    print(phase_mat_list)
    print("amplitude_mat_list")
    print(len(amplitude_mat_list))
    print(amplitude_mat_list)

    eM = ExperimentManager(phase_mat_list, amplitude_mat_list, "samples_multiples.csv", run_duration=args["run_duration"])
    eM.start()