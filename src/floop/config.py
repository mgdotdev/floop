def config(*args, **kwargs):
    """attaches loop configurations to the function, so to be passed
    down to C. Can be used as a decorator.

    :param callback: A callback to which the function result is evaluated. If
        the callback evaluates to True, the loop breaks and the function result
        is returned.
    :type callback: FunctionType
    :param max_iter: A integer value representing the max cycles through a
        given loop. The loop breaks on the max_iter'th call, and returns the
        function result.
    :type max_iter: int > 0

    """
    if not args:
        return lambda fn: config(fn, **kwargs)

    fn, *_ = args
    fn._loop_configuration = kwargs
    return fn
