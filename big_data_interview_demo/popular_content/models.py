from django.db import models
from popular_content.enum import SourceType

class PopularContent(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False ,verbose_name='文章標題')
    content = models.TextField(blank=False, null=False, verbose_name='文章內容')
    soft_delete = models.BooleanField(default=False, verbose_name='軟刪除')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立日期')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    def __str__(self):
        return self.title
    
class PopularContentSource(models.Model):
    popular_content = models.ForeignKey(PopularContent, null=False, blank=False, on_delete=models.CASCADE, verbose_name='文章ID')
    source_type = models.IntegerField(choices=[(tag.value, tag.label) for tag in SourceType], verbose_name='資源類型')
    source_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='資源名稱')
    source_path = models.URLField(max_length=512, verbose_name='資源位置')
    soft_delete = models.BooleanField(default=False, verbose_name='軟刪除')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立日期')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    def __str__(self):
        return self.source_name
    
