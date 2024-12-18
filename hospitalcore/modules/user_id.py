import random

def generate_e_hosp_id():
    """Generates a random E-HOSP ID with a four-digit number."""
    random_number = str(random.randint(1000, 9999))
    e_hosp_id = "E-HOSP" + random_number
    return e_hosp_id

