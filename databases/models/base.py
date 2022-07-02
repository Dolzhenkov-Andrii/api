# from manager import Manager
from collections import OrderedDict









#===========================================================

AND = 'AND '
OR = 'OR '

#======================================================== +
class BaseExp:
    
    name = None
    
    def add(self, *args, **kwargs):
        raise NotImplementedError()
    
    def definition(self):
        return self.name + self.line() + ' '
    
    def line(self):
        raise NotImplementedError()
    
    def __bool__(self):
        raise NotImplementedError()

#======================================================== +
class OrAnd:
    def __init__(self, exp_type=AND, **kwargs):
        self.separator = exp_type
        self._params = kwargs

    def __str__(self):
        kv_paris = [f'{k} = {v}' for k,v in self._params.items()]
        return f' {self.separator}'.join(kv_paris) + ' '
    
    def __bool__(self):
        return bool(self._params)


#======================================================== +
class Select(BaseExp):
    
    name = "SELECT "
    
    def __init__(self,*args, **kwargs):
        self._params = []
        self.add(*args, **kwargs)
        self.query = self.definition()
        
    def add(self, *args, **kwargs):
        self._params.extend(args)
        return self

    def line(self):
        return ','.join([str(key) for key in self._params])

    def __bool__(self):
        return bool(self._params)
    
#======================================================== +
class Limit(Select):
    name = "LIMIT "  
#======================================================== +
class From(Select):
    name = "FROM "
    
#======================================================== + 
class Where(BaseExp):
    
    name = "WHERE "
    
    def __init__(self, exp_type=AND, **kwargs):
        self.add(exp_type, **kwargs)
        self.query = self.definition()
        
    def add(self, exp_type=AND, **kwargs):
        self._orAnd = OrAnd(exp_type, **kwargs)
        return self._orAnd

    def line(self):
        return str(self._orAnd)

    def __bool__(self):
        return bool(self._orAnd)
#========================================================
class Join(BaseExp):

    name = "JOIN "
    
    def __init__(self,table_name, exp_type=AND, **kwargs):
        self.name += f'{table_name} ON {table_name}.'
        self.add(exp_type, **kwargs)
        self.query = self.definition()
        
    def add(self, str_type=AND, **kwargs):
        self._orAnd = OrAnd(str_type, **kwargs)
        return self._orAnd

    def line(self):
        return  str(self._orAnd)

    def __bool__(self):
        return bool(self._orAnd)
#======================================================== + 


class BaseMetodSQL:
    ### Использует databases.connection
    query = ''
    
    def select(self, *columns):
        self.query += Select(*columns).query
        return self
    
    def FROM(self, *table):
        self.query += From(*table).query
        #==========================================
        return self

    
    def WHERE(self, exp_type=AND, **kwargs):
        self.query += Where(exp_type=AND, **kwargs).query
        #==========================================
        return self


    def JOIN(self,table_name, exp_type=AND, **kwargs):
        self.query += Join(table_name, exp_type=AND, **kwargs).query
        #==========================================
        return self
        
    def LIMIT(self, *args):
        self.query += Limit(*args).query
        #==========================================
        return self

     
    
#===========================================================

class Manager(BaseMetodSQL):
    
    def __init__(self, model_class):
        self.model_class = model_class
        self._model_fields = model_class._original_fields.keys()
        self.query = ''
    
    def __get_date(self,conector):
      self.connection = conector
      with self.connection._connection.cursor() as cursor:
          cursor.execute(self.query)
          query = []
          for row in cursor:
              query.append(row)
      return query    
       
    def fetch(self,conector):
        query = str(self.query)
        db_results = self.__get_date(conector)
        results = []
        for row in db_results:
            print('Manager - row',row)
            model = self.model_class()
            print('Manager - model',model)
            print('Manager - model',self._model_fields)
            for val,field in zip(self._model_fields, row.items()):
                print('Manager - field and val', field[1], val)
                setattr(model, val, field[1])
            results.append(model)
            print('Manager - model2',model)
        return results
    
#===========================================================
#==================================================



class Field:
    
    pass

class IntegerField(Field):
    
    pass

class CharField(Field):
    
    pass




class ModelMeta(type):
    
    def __new__(mcs, class_name, parents, attributes):
        print(class_name, parents, attributes)
        fields = OrderedDict()
        for k, v in attributes.items():
            if isinstance(v, Field):
                fields[k] = v
                attributes[k] = None
            
        cla = super(ModelMeta, mcs).__new__(mcs, class_name, parents, attributes)
        setattr(cla, '_model_name', attributes['__qualname__'].lower())
        setattr(cla, '_original_fields', fields)
        setattr(cla, 'objects', Manager(cla))
        return cla


class BaseModel(metaclass=ModelMeta):
    pass




class Post(BaseModel):
    id = IntegerField()
    title = IntegerField()
    text = IntegerField()
    photo = IntegerField()
    
