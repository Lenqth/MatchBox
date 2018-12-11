
from rx import Observable
from rx import Observer
from rx.core import ObservableBase, Disposable
from rx.subjects import Subject

from copy import copy,deepcopy

class IObservableCollection:
    pass

import weakref

__obs_object_table__ = weakref.WeakValueDictionary() 
def to_observable(parent,v,convert=False):
    if isinstance(v,IObservableCollection):
        return v
    v_id = id(v)
    if v_id in __obs_object_table__ :
        if __obs_object_table__[v_id].__ref_raw__ is v :
            return __obs_object_table__[v_id]
        del __obs_object_table__[v_id]
    if isinstance(v,list):
        if convert :
            return [ to_observable(parent,x) for x in v ]
        o = ObservableList(v)
        parent.register_child(o)
        __obs_object_table__[v_id] = o
        o.__ref_raw__ = v 
        return o
    elif isinstance(v,dict):
        if convert :
            return { k : to_observable(parent,x) for (k,x) in v.items() } 
        o = ObservableDict(v)
        parent.register_child(o)
        __obs_object_table__[v_id] = o
        o.__ref_raw__ = v
        return o
    else:
        return v

def my_deepcopy(obj):
    """
        ディープコピーだが、同じオブジェクトが出現しても違うオブジェクトにマップする
    """
    if isinstance(obj,list):
        return [ my_deepcopy(x) for x in obj ]
    elif isinstance(obj,dict):
        return { k:my_deepcopy(v) for (k,v) in obj.items() }
    else:
        return copy(obj)

class ObservableList(list,Observable,IObservableCollection):
    """
        splice , (stt,end) , values :
        clear : 
        child , inst : 
    """
    def __init__(self,initial=[]):
        self.__subject__ = Subject()
        super().__init__(to_observable(self,initial,True))

    def subscribe(self,observer):
        self.full_sync(observer)
        self.__subject__.subscribe(observer)

    
    def register_child(self,child):
        def __child_handler(x):
            nonlocal child
            f = True
            for k,v in enumerate(self):
                if v is child :
                    f = False
                    yield ("child",k,x)
            if f:
                raise KeyError()
        child.__subject__.flat_map( __child_handler )\
            .on_error_resume_next(lambda x:Observable.from_([]))\
            .subscribe( self.__subject__ )

    def __send__(self,e):
        self.__subject__.on_next( my_deepcopy(e) )
    
    def __setitem__(self, key, value):
        l_prev = len(self)
        value = to_observable(self,value)
        res = super().__setitem__(key, value) 
        e = ()
        if isinstance(key,slice):
            start,end,step = key.indices(l_prev)
            if step == 1 :
                e = ( "splice", (start,end-start) , value )
            else:
                self.full_sync()
                return res       
        else:
            if key < 0 :
#                e = ( "replace", len(self) - key , value )
                e = ("splice" , (len(self) - key,1) , [value] )
            else:
#               e = ( "replace", key , value )
                e = ("splice" , (key,1) , [value] )
        self.__send__(e)
        return res

    def append(self, value):
        value = to_observable(self,value)
        l_prev = len(self)
        super().append(value)
        self.__send__( ("splice" , (l_prev,0) , [value] ) )
#        self.__send__( ("push" , value) )

    def extend(self, iterable):
        l_prev = len(self)
        iterable = to_observable(self,iterable)
        super().extend(iterable)
        self.__send__( ("splice" , (l_prev,0) , list(iterable) ) )
    
    def insert(self, index, value):
        value = to_observable(self,value)
        super().insert(index, value) 
        self.__send__( ("splice" , (index,0) , value) )

    def clear(self):
        return super().clear() 
        self.__send__( ("clear",) )
    
    def pop(self, index=-1):
        if index < 0 :
            e = ( "splice", (len(self) - index,1) ,[] )
        else:
            e = ( "splice", (index,1) , []  )
        res = super().pop(index)
        self.__send__( e )
        return res
    
    def reverse(self):
        res = super().reverse()
        self.full_sync()
        return res    
    
    def sort(self):
        super().sort() 
        self.full_sync()

    def full_sync(self,observer=None):
        if observer is None :
            observer = self.__subject__
        observer.on_next( ("clear",) )
        observer.on_next( ("splice" , (0,0) , my_deepcopy(list(self)) ) )


class ObservableDict(dict,Observable,IObservableCollection):
    """
        set , k , v 
        remove , k :
        assign , dict :
        clear : 
        child , inst : 
    """
    def __init__(self,initial={}):
        self.__subject__ = Subject()
        self.__id2key__ = {}
        super().__init__(to_observable(self,initial,True))

    def subscribe(self,observer):
        self.full_sync(observer)
        self.__subject__.subscribe(observer)

    def register_child(self,child):
        def __child_handler(x):
            nonlocal child
            f = True
            for k,v in self.items():
                if v is child :
                    f = False
                    yield ("child",k,x)
            if f:
                raise KeyError()
        child.__subject__.flat_map( __child_handler )\
            .on_error_resume_next(lambda x:Observable.from_([]))\
            .subscribe( self.__subject__ )
    
    def __send__(self,e):
        self.__subject__.on_next( my_deepcopy(e) )

    def __setitem__(self,key,value):
        value = to_observable(self,value)
        res = super().__setitem__(key, value) 
        self.__send__( ("set", key , value ) )
        return res

    def __delitem__(self,key):
        res = super().__delitem__(key) 
        self.__send__( ("remove", key ) )
        return res

    def pop(self, k, d=None):
        res = super().pop(k, d=d) 
        self.__send__( ("remove", k ) )
        return res
    
    def popitem(self):
        res = super().popitem()  
        self.__send__( ("remove", res[0] ) )
        return res

    def setdefault(self, k, d):
        d = to_observable(self,d)
        res = super().setdefault(k, d) 
        self.__send__( ("set", k , res ) )        
        return res

    def update(self, d):
        d = to_observable(self,d)
        res = super().update(d)
        self.__send__( ("assign" , dict(d) ) )        
        return res

    def full_sync(self,observer=None):
        if observer is None :
            observer = self.__subject__
        observer.on_next( ("clear",) )
        observer.on_next( ("assign" , my_deepcopy(dict(self)) ) )

    def clear(self):
        return super().clear() 
        self.__send__( ("clear",) )


"""   
def observe_variable(cls,name):
    int_name = "__invar_" + name
    def _get(x):
        nonlocal int_name
        return getattr(x,int_name)
    def _set(x,v):
        nonlocal name,int_name
        x.__subject__.on_next( (name,v) )
        return setattr(x,int_name,v)
    prop = property( _get )
    prop = prop.setter( _set )
    setattr(cls,name,prop)

def observable_class(a):
    return a

def observable(a):
    if isinstance(a,type):
        return observable_class(a)
    pass
"""

    
class ObserverLogger(Observer):
    def __init__(self):
        self.log = []

    def on_next(self, value):
        self.log.append(value)
    
    def on_error(self,error):
        self.log.append(error)

    def on_completed(self):
        return super().on_completed()

class ObserverListListener(Observer):
    def __init__(self):
        self.li = []

    def on_next(self, value):
        ins , *args = value
        if ins == "clear" :
            self.li.clear()
        elif ins == "splice" :
            start,length = args[0]
            slc = slice(start,start+length)
            self.li[slc] = args[1]
    
    def on_error(self,error):
        raise error

    def on_completed(self):
        return super().on_completed()

class ObserverListener(Observer):
    def __init__(self):
        self.root = {}

    @staticmethod
    def do_inst(target,inst,args):
        if inst == "child":
            key , (c_inst,*c_args) = args
            ObserverListener.do_inst(target[key],c_inst,c_args)
        elif isinstance(target,list):
            if inst == "clear" :
                target.clear()
            elif inst == "splice" :
                start,length = args[0]
                slc = slice(start,start+length)
                target[slc] = args[1]
            else:
                raise ValueError()
        elif isinstance(target,dict):
            if inst == "clear" :
                target.clear()
            elif inst == "set" :
                target[args[0]]=args[1]
            elif inst == "remove" :
                del target[args[0]]
            elif inst == "assign" :
                target.update(args[0])
            else:
                raise ValueError()
        else:
            raise ValueError()

    def on_next(self, value):
        inst , *args = value
        ObserverListener.do_inst(self.root,inst,args) 

    def on_error(self,error):
        raise error

    def on_completed(self):
        return super().on_completed()

