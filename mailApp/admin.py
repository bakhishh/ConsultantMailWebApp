from django.contrib import admin
from .models import Consultant
from .models import Data

admin.site.register(Consultant)
admin.site.register(Data)