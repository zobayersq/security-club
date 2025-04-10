from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Team

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    # Fetch and update the team's ranking
    ctf_data = team.fetch_ctf_rank()

    context = {
        'team': team,
        'ctf_data': ctf_data
    }
    
    return render(request, 'teams/team_detail.html', context)
