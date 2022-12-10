import numpy as np
from experiment_manager import ExperimentManager
import argparse
from math import ceil, floor

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

## Expectation
## Deadzone in the middle, every cell will otherwise be the same amplitude and phase



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

def zeroOutMiddleCell(mat=np.ones((5,5), dtype=int)):
    
    n_rows, n_cols = mat.shape

    if n_rows < 3:
        print("Less than 3 rows. Will end up zeroing out some border cells")
    if n_cols < 3:
        print("Less than 3 columns. Will end up zeroing out some border cells")
    if n_rows % 2 == 0:
        print("Even number of rows. Zeroing out on the two middle rows")
    if n_cols % 2 == 0:
       print("Even number of columns. Zeroing out on the two middle columns")

    row_a, row_b = ceil(n_rows/2)-1, floor(n_rows/2)+1
    col_a, col_b = ceil(n_cols/2)-1, floor(n_cols/2)+1
    
    mat[row_a:row_b, col_a:col_b] = 0
    return mat
    
def zeroOutMiddleCells(mat=np.ones((5,5), dtype=int)):
    n_rows, n_cols = mat.shape

    if n_rows < 3:
        print("Less than 3 rows. Will not zero any of the border cells")

    if n_cols < 3:
        print("Less than 3 cols. Will not zero any of the border cells")

    mat[1:n_rows-1, 1:n_cols-1] = 0
    return mat

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', default=5, type=int, help="Number of contiguous times to repeat each control matrix combination")
    ap.add_argument('--run_duration', default=5, type=int, help="Length of time in secs between control start and control stop")
    ap.add_argument('--phase', default=0, type=int, help="Phase control on all non-zeroed cells")
    ap.add_argument('--amp', default=4, type=int, help="Amplitude control on all non-zeroed cells")
    
    args = vars(ap.parse_args())

    print(args)

    orig_phase_mat = args["phase"]*np.ones((5,5), dtype=int)
    zeroed_phase_mat = zeroOutMiddleCells(orig_phase_mat)
    phase_mat_list = [zeroed_phase_mat]*args["reps"]
    orig_amplitude_mat = args["amp"]*np.ones((5,5), dtype=int)
    zeroed_amplitude_mat = zeroOutMiddleCells(orig_amplitude_mat)
    amplitude_mat_list = [zeroed_amplitude_mat]*args["reps"]

    print("phase_mat_list")
    print(len(phase_mat_list))
    print(phase_mat_list)
    print("amplitude_mat_list")
    print(len(amplitude_mat_list))
    print(amplitude_mat_list)

    eM = ExperimentManager(phase_mat_list, amplitude_mat_list, "deadzone_multiples.csv", run_duration=args["run_duration"])
    eM.start()