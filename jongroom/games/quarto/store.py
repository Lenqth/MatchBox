
from rx import Observable
from rx.subjects import Subject

class IObservableCollection:
    pass

class ObservableList(list,IObservableCollection):
    def __init__(self):
        self.__stream__ = Subject()
    
    def __setitem__(self, key, value):
        res = super().__setitem__(key, value) 
        e = ()
        if isinstance(key,slice):
            e = ( "splice", key.indices(len(self)) , value )
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
        super().extend(iterable)
        self.__stream__.on_next( ("add_last_range" , list(iterable) ) )
    
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
        self.__stream__.on_next( ("reverse") )
        return res    
    
    def sort(self):
        super().sort()  
        self.__stream__.on_next( ("sort") )

    def full_sync(self):
        self.__stream__.on_next( ("clear") )
        self.__stream__.on_next( ("add_last_range" , list(self) ) )


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

