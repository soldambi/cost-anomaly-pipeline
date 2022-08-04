class ResourceFailed(Exception):
    """
    Error: Failed to create AWS resource.
    """
    def __init__(self, step, status):
        message = f'Failed to create resource. (Step: {step}, Status: {status})'
        super().__init__(message)

        
class ResourcePending(Exception):
    """
    Error: Resource is being created.
    """
    def __init__(self, step, status):
        message = f'Resource is still being created. (Step: {step}, Status: {status})'
        super().__init__(message)
