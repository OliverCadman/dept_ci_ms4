def handle_deplist_get(params):
    """
    Handles GET parameters in 'Find a Dep' page,

    Takes request.GET and kwargs as argument,
    and prepares and returns a context with the 
    values provided in keyword arguments.
    """

    context = {
        "search_params": {},
        "instrument": None
    }

    if "instrument" in params:
        instrument_arg = params["instrument"]
        context["instrument"] = instrument_arg
        context['search_params']["instruments_played__instrument_name__iexact"] = instrument_arg
        
    
    return context
                                
