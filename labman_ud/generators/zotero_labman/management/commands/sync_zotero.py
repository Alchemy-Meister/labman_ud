#encoding: utf-8 

from django.core.management.base import NoArgsCommand
from generators.zotero_labman.models import ZoteroLog
from django.db.models import Q

from generators.zotero_labman.utils import get_last_zotero_version, parse_last_items, sync_deleted_items

class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Synchronizes Labman\'s publications DB with data from your Zotero library.'

    def handle_noargs(self, **options):
        try:
            last_version_db = ZoteroLog.objects.filter(Q(zotero_key='-SYNCFINISHED-') | Q(zotero_key='-RESYNC-')).order_by('-created')[0].version
        except:
            last_version_db = 0
        
        last_version_zotero = get_last_zotero_version()

        # Get unsynchronized items and remove those which have been removed in Zotero
        parse_last_items(last_version_zotero, last_version_db)
        if last_version_db != 0:
            sync_deleted_items(last_version_zotero, last_version_db)


    

    
