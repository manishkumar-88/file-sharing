from datetime import datetime,timezone

from mongoengine import Document, DateTimeField, StringField


class BaseMetaClass(Document):
    """
    Description:
    This is a Base abstract class that is being used to add additional fields to the respective collection
    """
    meta = {'abstract': True}

    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField()
 
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        return super(BaseMetaClass, self).save(*args, **kwargs)