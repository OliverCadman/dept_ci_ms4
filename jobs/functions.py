import datetime


def handle_get_params(params):
    """
    Handles GET parameters in 'Find a Dep' page,

    Takes request.GET and kwargs as argument,
    and prepares and returns a context with the
    values provided in keyword arguments.

    Function is shared between both the Dep List Page
    and the Job List Page.
    """

    context = {
        "instrument": None,
        "genre": None,
        "available_today": None,
        "search_params": {},
        "min_fee": 1,
        "max_fee": float("inf"),
        "fee": None,
        "city": None,
        "sort_params": "pk",
        "sort_direction": None,
        "sort": None
    }

    # ------ Dep List Params ------

    # Sort by Average Rating
    if "sort" in params:
        context["sort"] = params["sort"]
        if params["sort"] != "reset":
            average_key = "".join(params["sort"].split("_")[0])
            rating_key = "".join(params["sort"].split("_")[1])
            sort_criteria = (
                f'{average_key}_{rating_key}')
            sort_direction = "".join(params["sort"].split("_")[2])
            if sort_direction == "asc":
                context["sort_direction"] = f"{sort_criteria}"
                context["sort_params"] = context["sort_direction"]
            else:
                context["sort_direction"] = f"-{sort_criteria}"
                context["sort_params"] = context["sort_direction"]

    # Search by Instrument
    if "instrument" in params:
        instrument_arg = params["instrument"]
        context["instrument"] = instrument_arg
        context['search_params']["instruments_played__"
                                 "instrument_name__iexact"] = instrument_arg

    # Search for User that is Available Today
    if "available_today" in params:
        context["available_today"] = datetime.datetime.today()
        context["availability_params"] = context["available_today"]

    # Search by User's City
    if "city" in params:
        city_arg = params["city"]
        context["city"] = city_arg
        context["search_params"]["city__iexact"] = city_arg

    # Search by User's Genre
    if "genre" in params:
        genre_arg = params["genre"]
        context["genre"] = genre_arg
        context["search_params"]["genres__genre_name"] = genre_arg

    # ----- Job List Params ------

    # Search by Event City
    if "event_city" in params:
        event_city_arg = params["event_city"]
        context["city"] = event_city_arg
        context["search_params"]["event_city__iexact"] = event_city_arg

    # Search by Fee Range
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
