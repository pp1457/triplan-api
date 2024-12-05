def process_user_input(input):
    """
    return key words, extract location, time, etc. if needed
    """

def ask_google(start, end, parsed_inputs, information):
    """
    use inputs to ask google maps API to obtain a set of attractions and associate informations,
    like, travel mode, user reviews, estimate time, attraction summary
    """

def ask_ai(attractions, user_input, information):
    """
    """

def gen(current_trip, user_input):
    parsed_input = process_user_input(user_input)
    start, end, mid = current_trip.mid
    attractions = ask_google(start, end, parsed_input, mid.information)
    best_attraction = ask_ai(attractions, user_input, mid.information)
    current_trip.update(mid, best_attraction)
    gen(current_trip, user_input)
