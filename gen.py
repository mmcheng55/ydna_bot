from models import *

VotingForRoles.delete().where(VotingForRoles.id < 21).execute()