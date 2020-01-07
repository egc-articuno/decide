from django.contrib import admin, messages
from django.contrib.admin.utils import unquote
from django.contrib.admin import helpers
from django.utils.translation import gettext as _
from django.utils import timezone
from django.forms.formsets import all_valid

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

class PartyAdmin(admin.ModelAdmin):
    inlines = [PartyPresidentCandidateInline, PartyCongressCandidateInline]
    women_number = 0
    men_number = 0
    # def save_form(self, request, form, formset, change):
    #     msg = ('Está borrachooo')
    #     self.message_user(request, msg, messages.WARNING)
    #     formset.save()

    # def message_user(self, request, message, level=messages.INFO, extra_tags='',
    #                  fail_silently=False):
    #     pass

    # def response_post_save_add(self, request, obj):
    #     pass
    # def response_post_save_change(self, request, obj):
    #     print(obj)

    def _changeform_view(self, request, object_id, form_url, extra_context):
        to_field = request.POST.get('_to_field', request.GET.get('_to_field'))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = self.model
        opts = model._meta

        if request.method == 'POST' and '_saveasnew' in request.POST:
            object_id = None

        add = object_id is None

        if add:
            if not self.has_add_permission(request):
                raise PermissionDenied
            obj = None

        else:
            obj = self.get_object(request, unquote(object_id), to_field)

            if not self.has_change_permission(request, obj):
                raise PermissionDenied

            if obj is None:
                return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=not add)
            else:
                form_validated = False
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object, change=not add)
            
            # Check number of candidades for congress
            if all_valid(formsets):
                global number_candidates_congress
                number_candidates_congress = 0
                for formset in formsets:
                    for f in formset: 
                        cd = f.cleaned_data
                        congress_candidate = cd.get('congress_candidate')
                        delete = cd.get('DELETE')
                        print(congress_candidate)
                        # The option is a congress candidate. Sum one to the total for checking
                        if congress_candidate is not None:
                            number_candidates_congress += 1
                        # Check the total number of candidates if user delete one                            
                        if delete:
                            number_candidates_congress -= 1

            valid_number_candidates_congress = True
            if number_candidates_congress >= 350 or number_candidates_congress <= 0:
                valid_number_candidates_congress = False
            # Message users
            if not valid_number_candidates_congress:
                msg = 'The number of candidates for the congress must be 349 or less as well as having at least one candidate. There are now {} candidates for congress.'.format(number_candidates_congress)
                self.message_user(request, msg, messages.WARNING)

            if all_valid(formsets) and form_validated and valid_number_candidates_congress:
                self.save_model(request, new_object, form, not add)
                self.save_related(request, form, formsets, not add)
                change_message = self.construct_change_message(request, form, formsets, add)
                if add:
                    self.log_addition(request, new_object, change_message)
                    return self.response_add(request, new_object)
                else:
                    self.log_change(request, new_object, change_message)
                    return self.response_change(request, new_object)
            else:
                form_validated = False
        else:
            if add:
                initial = self.get_changeform_initial_data(request)
                form = ModelForm(initial=initial)
                formsets, inline_instances = self._create_formsets(request, form.instance, change=False)
            else:
                form = ModelForm(instance=obj)
                formsets, inline_instances = self._create_formsets(request, obj, change=True)

        adminForm = helpers.AdminForm(
            form,
            list(self.get_fieldsets(request, obj)),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        context = dict(
            self.admin_site.each_context(request),
            title=(_('Add %s') if add else _('Change %s')) % opts.verbose_name,
            adminform=adminForm,
            object_id=object_id,
            original=obj,
            is_popup=('_popup' in request.POST or
                      '_popup' in request.GET),
            to_field=to_field,
            media=media,
            inline_admin_formsets=inline_formsets,
            errors=helpers.AdminErrorList(form, formsets),
            preserved_filters=self.get_preserved_filters(request),
        )

        # Hide the "Save" and "Save and continue" buttons if "Save as New" was
        # previously chosen to prevent the interface from getting confusing.
        if request.method == 'POST' and not form_validated and "_saveasnew" in request.POST:
            context['show_save'] = False
            context['show_save_and_continue'] = False
            # Use the change template instead of the add template.
            add = False

        context.update(extra_context or {})

        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)

# ----------------- NEW REGISTER ----------------
class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]

admin.site.register(Voting, VotingAdmin)

admin.site.register(PoliticalParty, PartyAdmin)

# -----------------------------------------------


# ----------------- OLD REGISTER ----------------

# admin.site.register(Question, QuestionAdmin)

# -----------------------------------------------
