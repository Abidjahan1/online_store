from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class TaggedItemManager(models.Manager):
    # This manager is used to retrieve tagged items for a specific object type and ID. also called querying genereic relations
    # It uses the ContentType framework to handle generic relations.
    def get_tags_for(self,obj_type,object_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedITem.objects \
        .select_related('tag') \
        .filter(
            content_type=content_type,
            object_id = object_id
        )
        




class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label

class TaggedITem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    # Type (product, Viedo, Article)
    #ID - find the record in the table
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE) 
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()