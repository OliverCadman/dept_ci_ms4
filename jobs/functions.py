import datetime

def handle_get_params(params):
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
        "min_fee": 1,
        "max_fee": float("inf"),
        "fee": None,
        "city": None
    }

    if "instrument" in params:
        instrument_arg = params["instrument"]
        context["instrument"] = instrument_arg
        context['search_params']["instruments_played__instrument_name__iexact"] = instrument_arg

    if "instrument_required" in params:
        instrument_required_arg = params["instrument_required"]
        context["instrument"] = instrument_required_arg
        context["search_params"]["instrument_required__instrument_name__iexact"] = instrument_required_arg


    if "last_name" in params:
        lname_arg = params["last_name"]
        context["last_name"] = lname_arg
        context["search_params"]["last_name__iexact"] = lname_arg

    if "available_today" in params:
        context["available_today"] = datetime.datetime.today()
        context["availability_params"] = context["available_today"]

    if "city" in params:
        city_arg = params["city"]
        context["city"] = city_arg
        context["search_params"]["city__iexact"] = city_arg

    if "event_city" in params:
        event_city_arg = params["event_city"]
        context["city"] = event_city_arg
        context["search_params"]["event_city__iexact"] = event_city_arg


    if "genre" in params:
        genre_arg = params["genre"]
        context["genre"] = genre_arg
        context["search_params"]["genres__genre_name"] = genre_arg

    if "fee" in params:
        if not params["fee"] == "all" and not params["fee"] == "500":
            min_fee = params["fee"].split("-")[0]
            max_fee = params["fee"].split("-")[1]
            context["min_fee"] = min_fee
            context["max_fee"] = max_fee
        elif params["fee"] == "500":
            infinite_fee_arg = params["fee"]
            context["search_params"]["fee__gte"] = infinite_fee_arg
        
    return context
