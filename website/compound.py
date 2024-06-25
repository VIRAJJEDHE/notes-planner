def compound_interest(principal, interest, time):
 
    # Calculates compound interest
    Amount = principal * (pow((1 + int(interest) / 100), time))
    return Amount