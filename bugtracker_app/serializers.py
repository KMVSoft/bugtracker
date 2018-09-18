from rest_framework import serializers
from .models import IssueComment

class IssueCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = IssueComment
		fields = ()