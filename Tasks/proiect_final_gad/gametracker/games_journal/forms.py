from django import forms
from .models import GameHistory, PLATFORM_CHOICES, current_year


class AddGameToHistoryForm(forms.ModelForm):
    """This form will be used by the user to add a game to his personal game journal."""

    user_id = forms.IntegerField(
        label = "user",
        widget=forms.NumberInput(
            attrs={"class": "invisible d-none"}
        ),
    )
    name = forms.CharField(
        label="Game name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    platform = forms.CharField(
        widget=forms.Select(
            attrs={"class": "form-select"},
            choices=PLATFORM_CHOICES,
        )
    )
    hours_played = forms.IntegerField(
        label="Hours played",
        min_value=0,
        max_value=99999,
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
    )
    rating = forms.IntegerField(
        label="Rating",
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
    )
    year_played = forms.IntegerField(
        label="Year played",
        min_value=1960,
        max_value=current_year(),
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
    )

    class Meta:
        model = GameHistory
        fields = ("user_id", "name", "platform", "hours_played", "rating", "year_played")


class UpdateGameForm(AddGameToHistoryForm):
    """This form will be used by the user to add a game to his personal game journal."""

    game_id = forms.IntegerField(
        label="game_id",
    )

    class Meta:
        model = GameHistory
        fields = ("game_id", "user_id", "name", "platform", "hours_played", "rating", "year_played")