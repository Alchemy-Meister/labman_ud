from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from organization_manager.models import Organization
from funding_call_manager.models import FundingCall


@dajaxice_register
def get_funding_call(req, pk):
    dajax = Dajax()
    fc = FundingCall.objects.get(pk = pk)
    dajax.assign('#id_funding_program_form-organization', 'value', fc.organization.id)
    dajax.assign('#id_funding_program_form-name', 'value', fc.full_name)
    dajax.assign('#id_funding_program_form-concession_year', 'value', fc.concession_year)
    dajax.assign('#id_funding_program_form-geographical_scope', 'value', str(fc.geographical_scope))
    return dajax.json()
