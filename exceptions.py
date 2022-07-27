class ResourcePending(Exception):
    """This is ResourcePending error"""
    
    def __init__(self, message='This is ResourcePending error.'):
        # self.name = 'ResourcePending'
        self.message = message
        super().__init__(self.message)
        

class ResourceFailed(Exception):
    """This is ResourceFailed error"""
    
    def __init__(self, message='This is ResourceFailed error.'):
        # self.name = 'ResourceFailed'
        self.message = message
        super().__init__(self.message)
