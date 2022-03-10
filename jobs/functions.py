import datetime

def handle_deplist_get(params):
    """
    Handles GET parameters in 'Find a Dep' page,

    Takes request.GET and kwargs as argument,
    and prepares and returns a context with the 
    values provided in keyword arguments.
    """

    context = {
        "instrument": None,
        "genre": None,
        "available_today": None,
        "search_params": {},
        "city": None,
    }

    if "instrument" in params:
        instrument_arg = params["instrument"]
        context["instrument"] = instrument_arg
        context['search_params']["instruments_played__instrument_name__iexact"] = instrument_arg


    if "last_name" in params:
        lname_arg = params["last_name"]
        context["last_name"] = lname_arg
        context["search_params"]["last_name__iexact"] = lname_arg

    if "available_today" in params:
        print("yes")
        context["available_today"] = datetime.datetime.today()
        context["availability_params"] = context["available_today"]
    
    if "city" in params:
        city_arg = params["city"]
        context["city"] = city_arg
        context["search_params"]["city__iexact"] = city_arg

    
    if "genre" in params:
        genre_arg = params["genre"]
        context["genre"] = genre_arg
        context["search_params"]["genres__genre_name"] = genre_arg
        


        
    
    return context
                                
