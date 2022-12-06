import pycountry


def generate_list_of_countries(list_of_countries):
    countries = ""
    for index, country_alpha_code in enumerate(list_of_countries):
        try:
            country = pycountry.countries.get(alpha_2=country_alpha_code).name
            if index == len(list_of_countries) - 1:
                countries += country
            else:
                countries += country + ", "
        except:
            pass
    return countries
