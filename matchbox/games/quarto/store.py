
from rx import Observable
from rx.subjects import Subject

class IObservableCollection:
    pass

class ObservableList(list,IObservableCollection):
    def __init__(self):
        self.__stream__ = Subject()
    
    def __setitem__(self, key, value):
        l_prev = len(self)
        res = super().__setitem__(key, value) 
        e = ()
        if isinstance(key,slice):
            start,end,step = key.indices(l_prev)
            if step == 1 :
                e = ( "splice", (start,end) , value )
            else:
                self.full_sync()
                return res       
        else:
            if key < 0 :
                e = ( "replace", len(self) - key , value )
            else:
                e = ( "replace", key , value )
        self.__stream__.on_next(e)
        return res

    def append(self, value):
        super().append(value)
        self.__stream__.on_next( ("push" , value) )

    def extend(self, iterable):
        l_prev = len(self)
        super().extend(iterable)
        self.__stream__.on_next( ("splice" , (l_prev,0) , list(iterable) ) )
    
    def insert(self, index, value):
        super().insert(index, value) 
        self.__stream__.on_next( ("insert" , index , value) )

    def clear(self):
        return super().clear() 
        self.__stream__.on_next( ("clear") )
    
    def pop(self, index=-1):
        if key < 0 :
            e = ( "pop", len(self) - index )
        else:
            e = ( "pop", index )
        res = super().pop(index=index)
        self.__stream__.on_next( e )
        return res
    
    def reverse(self):
        res = super().reverse()
        self.full_sync()
        return res    
    
    def sort(self):
        super().sort() 
        self.full_sync()

    def full_sync(self):
        self.__stream__.on_next( ("clear") )
        self.__stream__.on_next( ("splice" , (0,0) , list(self) ) )


class ObservableStorage(IObservableCollection):

    def __init__(self):
        self.__onchangeattr__ = {}
    
    def __setattr__(self, name, value):
        res = super().__setattr__(name, value) 
        if name in self.__onchangeattr__ :
            for x in self.__onchangeattr__[name]:
                x(self,value)
        return res

    def add_event(self,name,callback):
        pass

