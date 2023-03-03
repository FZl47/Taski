import os
from django.conf import settings


class RemovePastFileMixin:
    """
        set field => FIELDS_REMOVE_FILES = [file,image,audio,...]
        and when change remove past file
    """

    def save(self,*args,**kwargs):
        model = self.__class__
        if self.pk:
            try:
                obj_with_old_fields = model.objects.get(pk=self.pk)
                for field in self.FIELDS_REMOVE_FILES:
                    past_value_field =  getattr(obj_with_old_fields,field)
                    # Check past value is valid
                    if past_value_field:
                        # Compare Field with old and new value
                        if getattr(self, field) != past_value_field:
                            self.delete_file(past_value_field.name)

            except model.DoesNotExist:
                # new instance
                pass

        super(RemovePastFileMixin,self).save(*args,**kwargs)

    def delete(self,*args,**kwargs):
        for field in self.FIELDS_REMOVE_FILES:
            field = getattr(self, field)
            self.delete_file(field.name)
        super(RemovePastFileMixin,self).delete(*args,**kwargs)

    def delete_file(self,address):
        address = os.path.join(settings.MEDIA_ROOT,address)
        try:
            if os.path.exists(address):
                os.remove(address)
            else:
                # File does not exist
                pass
        except:pass