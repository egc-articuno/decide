from django.contrib import admin
from django.utils import timezone

from .models import PartyPresidentCandidate, PartyCongressCandidate
from .models import PoliticalParty
from .models import Voting

from .filters import StartedFilter


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)

# -------------- NEW INLINE ------------------

class PartyPresidentCandidateInline(admin.TabularInline):
    model = PartyPresidentCandidate

class PartyCongressCandidateInline(admin.TabularInline):
    model = PartyCongressCandidate


class PartyAdmin(admin.ModelAdmin):
    inlines = [PartyPresidentCandidateInline, PartyCongressCandidateInline]

# --------------------------------------------


# -------------- OLD INLINE ------------------

# class QuestionOptionInline(admin.TabularInline):
#     model = QuestionOption


# class QuestionAdmin(admin.ModelAdmin):
#     inlines = [QuestionOptionInline]

# --------------------------------------------

class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]


admin.site.register(Voting, VotingAdmin)

# ----------------- NEW REGISTER ----------------

admin.site.register(PoliticalParty, PartyAdmin)

# -----------------------------------------------


# ----------------- OLD REGISTER ----------------

# admin.site.register(Question, QuestionAdmin)

# -----------------------------------------------
