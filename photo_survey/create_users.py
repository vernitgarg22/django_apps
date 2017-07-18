# from photo_survey import create_users

from django.contrib.auth.models import User

user_data = [
    # ['Andrew', 'Salazar', 'metalgearfallout45@gmail.com'],
    # ['Ryan', 'Moonka', 'rmoonka@umich.edu'],
    # ['Dawan', 'Perry', 'dperry@detroitmi.gov'],
    # ['Robert', 'Huguley', 'huguleyR@detroitmi.gov'],
    # ['Emily', 'Krupp', 'KruppE@detroitmi.gov'],
    # ['Michael', 'Hartt', 'harttm@detroitmi.gov'],
    # ['Asia', 'Hudson', 'hudsona@detroitmi.gov'],
    # ['Nidhi', 'Kumar', 'kumarn@detroitmi.gov'],
    # [ 'Alleah', 'Walker', 'AlleahW@gmail.com' ],
    # [ 'Myla', 'Collins', 'MylaDcollins@yahoo.com' ],
    # [ 'Jamie', 'Sedlacek', 'JamieSedlacek@rockventures.com' ],
    # [ 'Martha', 'Potere', 'mpotere@degc.org' ],
    # [ 'Cydney', 'Camp', 'ccamp@degc.org' ],
    # [ 'Lily', 'Hamburger', 'ehamburger@degc.org' ],
    [ 'Katie', 'Navetta', 'KatieNavetta@quickenloans.com' ],
    [ 'Alyssa', 'Doutsas', 'AlyssaDoutsas@quickenloans.com' ],
    [ 'Brady', 'Lazuka', 'bradylazuka@quickenloans.com' ],
    [ 'Breia', 'Berrien', 'breiaberrien@quickenloans.com' ],
    [ 'Austin', 'Janice', 'austinjanice@quickenloans.com' ],
]
for data in user_data:
    first_name = data[0]
    last_name = data[1]
    email = data[2]
    username = email
    password = <password>

    user = User.objects.db_manager('photo_survey').create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
