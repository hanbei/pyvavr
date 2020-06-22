from inspect import signature, Parameter

from pyvavr.exceptions import CantCurryVarArgException


def curry(func, unique=True, allow_var_args=False):
    """ Generates a 'curried' version of a function. """
    sig = signature(func)
    min_args = len(sig.parameters)
    if len([x for x in sig.parameters.values() if
            x.kind == Parameter.VAR_KEYWORD or x.kind == Parameter.VAR_POSITIONAL]) > 0:
        if allow_var_args:
            min_args = None
        else:
            raise CantCurryVarArgException()

    def g(*my_args, **my_kw_args):
        def f(*args, **kw_args):
            if args or kw_args:  # some more args!
                # Allocates data to assign to the next 'f'.
                new_args = my_args + args
                new_kw_args = dict.copy(my_kw_args)

                # If unique is True, we don't want repeated keyword arguments.
                if unique and not kw_args.keys().isdisjoint(new_kw_args):
                    raise ValueError("Repeated kw arg while unique = True")

                # Adds/updates keyword arguments.
                new_kw_args.update(kw_args)

                # Checks whether it's time to evaluate func.
                if min_args is not None and min_args <= len(new_args) + len(new_kw_args):
                    return func(*new_args, **new_kw_args)  # time to evaluate func
                else:
                    return g(*new_args, **new_kw_args)  # returns a new 'f'
            else:  # the evaluation was forced
                return func(*my_args, **my_kw_args)

        return f

    return g
