import requests
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# event --> done
# featured 
# members
# teams
# post --> done
# Tag --> done
class MemberRegistration(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    university_id = models.CharField(max_length=50, unique=True)
    tryhackme_badge_url = models.URLField(
        max_length=255,
        blank=True,
        help_text="Optional: Link to your TryHackMe badge image or embed"
    )
    motivation = models.TextField(help_text="Why do you want to join the Cyber Security Club?")
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({'Approved' if self.approved else 'Pending'})"

class Member(models.Model):
    full_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)
    is_team_member = models.BooleanField(default=False)
    tryhackme_badge_url = models.URLField(
        max_length=255,
        blank=True,
        help_text="Link to your TryHackMe badge or embed image URL"
    )

    def __str__(self):
        return self.user_name

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=MemberRegistration)
def create_member_from_registration(sender, instance, created, **kwargs):
    if instance.approved and not hasattr(instance, 'member'):
        # Create a Member object from the registration
        Member.objects.create(
            full_name=instance.full_name,
            user_name=instance.email.split('@')[0],  # Use email prefix as username
            tryhackme_badge_url=instance.tryhackme_badge_url
        )



        
class Team(models.Model):
    name = models.CharField(max_length=255)  # Name of the team
    description = models.TextField(blank=True, null=True)  # Description about the team
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the team was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the team was last updated
    members = models.ManyToManyField('Member', related_name='teams')  # Relationship to the Member model
    leader = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True, related_name='leading_teams')  # Leader of the team
    ctf_team_id = models.IntegerField(null=True, blank=True)  # CTF Times team ID
    ctf_global_rank = models.IntegerField(null=True, blank=True)  # Global ranking of the team
    ctf_score = models.IntegerField(null=True, blank=True)  # Team score from CTF Times

    def __str__(self):
        return self.name

    def fetch_ctf_rank(self):
        if self.ctf_team_id:
            # Make a request to the CTF Times API to get the team's ranking details
            url = f'https://ctftime.org/api/v1/teams/{self.ctf_team_id}/'
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                # Update the team's global rank and score from the API response
                self.ctf_global_rank = data.get('rank', None)
                self.ctf_score = data.get('score', None)
                self.save()  # Save the updated data
                return data
            else:
                return None
        return None

    def member_list(self):
        return ', '.join([member.user.username for member in self.members.all()])

    def add_member(self, member):
        self.members.add(member)
        self.save()

    def remove_member(self, member):
        self.members.remove(member)
        self.save()

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

