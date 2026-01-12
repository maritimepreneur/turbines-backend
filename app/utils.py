
def response(code : int = None, message : str = None, data : dict = None) :
    _response = {"message" : message}
    if code :
        _response.update({"code" : code})
    if data : 
        _response.update({"data" : data})
    return _response