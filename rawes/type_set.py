import urllib
import json

class TypeSet(object):
    """docstring for TypeSet"""
    def __init__(self, types, indices, elastic):
        self.types = types
        self.indices = indices
        self.elastic = elastic
        self.base_path = self._build_base_path(indices=self.indices, types=self.types)
    
    def search(self, data, params={}):
        """Search for a document"""
        query_string = self._build_query_string(params)
        path = '%s/_search%s' % (self.base_path, query_string)
        response = self.elastic.get(path,data=data)
        return json.loads(response.text)
    
    def index(self, data, _id=None, params={}):
        """Index a new document"""
        query_string = self._build_query_string(params)
        path = '%s/%s%s' % (self.base_path, _id, query_string)
        response = self.elastic.put(path=path,data=data) if _id else self.elastic.post(path=path,data=data)
        return json.loads(response.text)
    
    def get(self, _id, params={}):
        """Retrieve a document by _id"""
        query_string = self._build_query_string(params)
        path = '%s/%s%s' % (self.base_path, _id, query_string)
        response = self.elastic.get(path)
        return json.loads(response.text)
    
    def multi_get(self, data):
        """Retrieves multiple documents by id"""
        path = '%s/_mget' % self.base_path
        response = self.elastic.get(path, data=data)
        return json.loads(response.text)

    def delete(self, _id, params={}):
        """Deletes a document by _id"""
        query_string = self._build_query_string(params)
        path = '%s/%s%s' % (self.base_path, _id, query_string)
        response = self.elastic.delete(path=path)
        return json.loads(response.text)
    
    def update(self, data, _id, params={}):
        """Updates a document by _id"""
        query_string = self._build_query_string(params)
        path = '%s/%s/_update%s' % (self.base_path, _id, query_string)
        response = self.elastic.post(path=path)
        return json.loads(response.text)
    
    def _build_base_path(self, indices, types):
        """docstring for _build_base_path"""
        indices_string = indices if type(indices) == str else ','.join(indices)
        types_string = types if type(types) == str else ','.join(types)
        return '%s/%s' % (indices, types_string)
    
    def _build_query_string(self, params):
        """Returns a query string with leading ?"""
        return '?%s' % urllib.urlencode(params) if len(params) else ''
