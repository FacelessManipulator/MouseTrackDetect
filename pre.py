import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--set', help='human | machine', default='human')
parser.add_argument('--attr', help='track | acceleration | speed | x | y', default='track')
parser.add_argument('--begin', type=int, help='the begin index of the set to display', default=0)
parser.add_argument('--count', type=int, help='number of data to display', default=10)

opt = parser.parse_args()

def get_track(s):
    i,moves,des,flag = s.split(' ')
    moves=moves.split(';')[:-1]
    moves=[move.split(',') for move in moves]
    moves=[[int(ll) for ll in l] for l in moves]
    des=[float(p) for p in des.split(',')]
    flag=int(flag)
#     print(i,moves[0],'->',des,flag)
    m = np.matrix(moves)
    m = m[np.lexsort(m.T)][0]
    return (i,(m[0,0],m[0,1]), m, des, flag)

def plot_track(axes, track):
    index, start, track, des, flag = get_track(track)
    axes.plot(track[:,0],track[:,1], '-b')

def plot_x(axes, track):
    index, start, track, des, flag = get_track(track)
    axes.plot(track[:,-1],track[:,0], '-b')

def plot_y(axes, track):
    index, start, track, des, flag = get_track(track)
    axes.plot(track[:,-1],track[:,1], '-b')
    
def plot_speed(axes, track):
    index, start, track, des, flag = get_track(track)
    sp = get_speed(track)
    axes.plot(track[1:-1, 2],sp[:,0], '-b')
    axes.plot(track[1:-1, 2],sp[:,1], '-g')
    
def plot_acceleration(axes, track):
    index, start, track, des, flag = get_track(track)
    a = get_acceleration(track)
    axes.plot(track[1:-1, 2],a[:,0], '-b')
    axes.plot(track[1:-1, 2],a[:,1], '-g')
    
def get_speed(track, bias=1):
    '''
    此函数用于获得速度，至少需要三个点，具体公式是解三个点用速度表示时的方程组
    这里默认时间偏差+1，是为了防止同一时间出现了两个点造成的inf
    固有偏差影响，视平均时间差不同，速度总体上大约缩小了0.25%
    '''
    assert track.shape[0] >= 3
    B_sub_A = track[1:-1] - track[:-2]
    C_sub_A = track[2:] - track[:-2]
    C_sub_B = track[2:] - track[1:-1]
    sp = np.multiply((C_sub_B[:,:-1] / np.square(C_sub_B[:,-1]+bias).reshape((-1,1)) + \
        B_sub_A[:,:-1] / np.square(B_sub_A[:,-1]+bias).reshape((-1,1))) ,
        (B_sub_A[:,-1].reshape((-1,1))+bias))
    sp = np.multiply(sp, (C_sub_B[:,-1].reshape((-1,1))+bias))
    sp = sp/(C_sub_A[:,-1].reshape((-1,1))+bias)
    return sp

def get_acceleration(track):
    '''
    此函数用于获得加速度，至少需要三个点，具体公式是解三个点用加速度表示时的方程组
    这里将时间差强行+1，是为了防止同一时间出现了两个点造成的inf
    固有偏差影响，视平均时间差不同，加速度总体上大约缩小了0.25%
    '''
    assert track.shape[0] >= 3
    B_sub_A = track[1:-1] - track[:-2]
    C_sub_A = track[2:] - track[:-2]
    C_sub_B = track[2:] - track[1:-1]
    a = (- B_sub_A[:,:-1] / (B_sub_A[:,-1].reshape((-1,1))+1) + \
        C_sub_A[:,:-1] / (C_sub_A[:,-1].reshape((-1,1)) + 1)) / \
        (C_sub_B[:,-1].reshape((-1,1))+1) * 2
    return a

def show_next(data, fig, attr):
    i = -1
    func = {'track':plot_track,'acceleration':plot_acceleration,'speed':plot_speed,
           'x':plot_x, 'y':plot_y}
    def onclick(event):
        nonlocal i
        if event is None or event.button == 1:
            i = 0 if i <= 0 else i-1
        elif event.button == 3:
            i = len(data)-1  if i >= len(data)-1 else i+1
        fig.clf()
        ax = fig.add_subplot(111)
        func[attr](ax, data[i])
        fig.suptitle('cur:%s-%s-%d'%(opt.set,opt.attr, i), fontsize=12)
        fig.canvas.draw()
    return onclick
    
if __name__ == '__main__':
    with open('dsjtzs_txfz_training.txt') as f:
        human = list(filter(lambda l:l.strip().endswith('1'),f.readlines()))
        f.seek(0)
        machine = list(filter(lambda l:l.strip().endswith('0'),f.readlines()))
    if opt.set == 'human':
        data = human
    elif opt.set == 'machine':
        data = machine
    elif opt.set == 'test':
        with open('dsjtzs_txfz_test1.txt') as f:
            test = f.readlines()
            data = test
        
    fig= plt.figure()
    event = show_next(data[opt.begin:opt.begin+opt.count], fig, opt.attr)
    event(None)
    cid = fig.canvas.mpl_connect('button_press_event', event)
    plt.show()
