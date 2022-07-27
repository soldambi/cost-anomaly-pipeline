class ResourceFailed(Exception):
    """
    Error: Failed to create AWS resource.
    """
    def __init__(self, status):
        message = f'Failed to create resource. (Status: {status})'
        super().__init__(message)

        
class ResourcePending(Exception):
    """
    Error: Resource is being created.
    """
    def __init__(self, status):
        message = f'Resource is still being created. (Status: {status})'
        super().__init__(message)
