import collections
import numpy
from functools import singledispatch
import numbers
import reprlib

@singledispatch
def loc(x,dic):
    ''' get the index of x based on the dic,
        return integer,slice(:) or integer sequence.    '''
    return x

@loc.register(str)
def _(x,dic):
    return dic[x]

@loc.register(tuple)
@loc.register(collections.abc.MutableSequence)
def _(x,dic):
    return tuple( loc(i,dic) for i in x )


class ArrayDec():
    '''
        A decorator of numpy array, with which you can get 
        or set the item by the item's name or index number.
            >>>ArrayDec['x','y']
            18312.925799000001
            >>>ArrayDec[:,('a','b','c')]
            array([[   756.438986,   6920.869591,   4045.749542],
            [   492.552543,   8220.257978,   7077.368096],
            [   814.59079 ,  11744.036344,   8956.55121 ],
            ..., 
            [   361.381608,   3319.223562,   3973.812027],
            [   397.000402,   6166.307046,   5464.191493],
            [  1177.759851,  11751.924535,   6951.701847]])
            >>>ArrayDec['x','y']=9
    '''
    def __init__(self, xnames, ynames,ainiflag=True):
        _xns,_yns=tuple(xnames),tuple(ynames)
        self._xnames={key:_xns.index(key) for key in _xns }
        self._ynames={key:_yns.index(key) for key in _yns }
        if len(self._xnames) != len(_xns) or len(self._ynames) != len(_yns) :
            raise KeyError('duplicate keys')
        if ainiflag :
            self.initarray()

    def initarray(self,oriarray=None):
        if oriarray is None :
            self._a=numpy.zeros( ( len(self._xnames),len(self._ynames) ) )
        else :
            self._a=numpy.array( oriarray )

    def __len__(self):
        return len(self._a)

    def __repr__(self):
        components = 'x_index:{}\ny_index:{}\n{}'.format( reprlib.repr(self._xnames) ,
                     reprlib.repr(self._ynames) ,repr(self._a) )
        return components

    def __getitem__(self, index):
        try :
            x,y = index
            _index =( loc(x,self._xnames) ,loc(y,self._ynames) )
        except TypeError :
            _index=index
        return self._a[_index]

    def __setitem__(self,index,item):
        x,y = loc(index[0], self._xnames) , loc(index[1], self._ynames)
        self._a[x,y]=item

    @classmethod
    def fromarray(cls,xs,ys,oriarray):
        ''' transform the oriarray into ArrayDec. The oriarray must meet several requirements:
            1.item in oriarray must be numerical object
            2.the oriarray should be two-dimensions array
            3.the total items of oriarray should be equal to the product of xs's items and ys's items
                example:
                >>>oriarray=[[1,2,3],[5,6,7]]
                >>>xs=['a','b']
                >>>ys=['x','y','z']
                >>>ArrayDec.fromarray(xs,ys,oriarray)
        '''
        if len(xs) != len(oriarray) or len(ys) != len(oriarray[0]) or len(xs)*len(ys) != sum(len(i) for i in oriarray):
            raise TypeError('Irrugular array')
        temparray=cls(xs,ys,ainiflag=False)
        temparray.initarray(oriarray)
        return temparray

'''
class ArrayDec():
    def __init__(self, xnames, ynames):
        self.xnames={key:xnames.index(key) for key in xnames }
        self.ynames={key:ynames.index(key) for key in ynames }
        self.a=numpy.zeros(( len(self.xnames), len(self.ynames) ))
        if len(self.xnames) != len(xnames) or len(self.ynames) != len(ynames) :
            raise KeyError('duplicate keys')

    def __len__(self):
        return len(self.a)

    def __getitem__(self, index):
        if type(index) is tuple :
            x,y=index
            if type(x) is str :
                x=self.xnames[x]
            elif isinstance(x,collections.Iterable) :
                x=tuple(self.xnames[i] for i in x)
            if type(y) is str :
                y=self.ynames[y]
            elif isinstance(y,collections.Iterable) :
                y=tuple(self.ynames[i] for i in y)
            return self.a[x,y]
        else :
            return self.a[index]

    def __setitem__(self,index,item):
        x,y=index
        if type(x) is str :
            x=self.xnames[x]
        if type(y) is str :
            y=self.ynames[y]
        self.a[x,y]=item
'''

if __name__ == '__main__' :

    xs=['a','b']
    ys=['x','y','z']
    a=[[1,2,3],[4,5,6]]
    aa=ArrayDec(xs,ys)
    da=ArrayDec.fromarray(xs,ys,a)
    print('Empty ArrayDec:\n'+repr(aa))
    print('ArrayDec fromarray:\n'+repr(da))
