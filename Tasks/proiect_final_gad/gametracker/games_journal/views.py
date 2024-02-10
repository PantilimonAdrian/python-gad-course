from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import AddGameToHistoryForm, UpdateGameForm
from .models import GameHistory
from django.db.models import Sum

GENERIC_ERROR_MESSAGE = ("An unexpected error occurred while processing your "
                         "request. Please try again later.")


def homepage(request):
    """This view function is used to display the main page of the web app"""
    env = {}

    # Add page information to context
    env["application_name"] = "GameTracker"
    env["application_moto"] = "Document Your Gaming Odyssey"
    env["application_desc"] = ("Transform your gaming journey into an unforgettable odyssey."
                               " Document every game played with ease. Your personalized gaming"
                               " diary awaits. Start tracking with GameTracker today!")

    return render(request, "homepage.html", context=env)


@login_required(login_url="login_user")
def profilepage(request):
    """This view function is used to display user profile information and games"""
    env = {}

    # Query the DB to fetch all games added by the registered user
    game_history_data = GameHistory.objects.filter(user_id=request.user.id).order_by('-year_played').values()
    env["user_game_history"] = game_history_data

    # Calculate total hours played by the user
    total_hours_played = GameHistory.objects.filter(
        user_id=request.user.id
    ).aggregate(Sum("hours_played", default=0))
    env["total_hours_played"] = total_hours_played.get("hours_played__sum", 0)

    # Add information about the user to the template env
    env["first_name"] = request.user.first_name
    env["last_name"] = request.user.last_name

    return render(request, "profile.html", context=env)


@login_required(login_url="login_user")
def addgamepage(request):
    """This function is used to add a new game to the game journal"""
    env = {}

    # Add page standard information and messages to context
    env["error_message"] = ""
    env["success_message"] = ""
    env["action_title"] = "Add a new game"
    env["action_description"] = "Level up your gaming journey! Add a new game to GameTracker now!"
    env["form_button_text"] = "Add game"
    env["action_img_desc"] = "Add game image"
    env["is_addgame_page"] = True

    # Default error message when a game add fails
    ADD_ERROR_MESSAGE = ("A problem occured during the this process."
                         "Please introduce the correct information and try again.")
    # Default success message when the game is added
    ADD_SUCCESS_MESSAGE = "The game has been added to your journal! Keep track of all your games."

    if request.method == "POST":
        add_game_form = AddGameToHistoryForm(request.POST)
        # Check if information provided to the register form is valid
        if add_game_form.is_valid():
            game_added = add_game_form.save(commit=False)
            game_added.user_id = request.POST["user_id"]
            try:
                game_added.save()
                env["success_message"] = ADD_SUCCESS_MESSAGE
                add_game_form = AddGameToHistoryForm()
            except:
                env["error_message"] = ADD_ERROR_MESSAGE
    else:
        # Add the Add Game Form object to the page context
        add_game_form = AddGameToHistoryForm()
        env["add_game_form"] = add_game_form

    return render(request, "useractionpagebase.html", context=env)


@login_required(login_url="login_user")
def updategameinfo(request):
    """This function is used to update a game informations"""
    env = {}

    # Add page standard information and messages to context
    env["success_message"] = ""
    env["error_message"] = ""
    env["action_title"] = "Update your game from information"
    env["action_description"] = "Enhance your gaming journey! Update a game in GameTracker now!"
    env["form_button_text"] = "Update game"
    env["action_img_desc"] = "Update game image"
    env["is_updategame_page"] = True

    # Success and error messages for game update action
    UPDATE_ERROR_MESSAGE = "Please select a game before you update the information"
    UPDATE_SUCCESS_MESSAGE = ("The selected game has been successfully updated, "
                              "go back and check it on your profile.")

    # Get all game of the user that is signed in to the app
    # and add that data to the context to populate the form
    game_history_data = GameHistory.objects.filter(user_id=request.user.id).order_by('-year_played').values()
    env["user_games"] = game_history_data
    # Debug log
    # print(game_history_data)

    if request.method == "POST":
        # Add information to the form and check if it is valid
        update_game_form = UpdateGameForm(request.POST)
        if update_game_form.is_valid():
            # Get all the cleaned information sent by the user
            user_id = update_game_form.cleaned_data.get("user_id")
            game_id = update_game_form.cleaned_data.get("game_id")
            name = update_game_form.cleaned_data.get("name")
            platform = update_game_form.cleaned_data.get("platform")
            hours_played = update_game_form.cleaned_data.get("hours_played")
            rating = update_game_form.cleaned_data.get("rating")
            year_played = update_game_form.cleaned_data.get("year_played")

            # Select the game that will be updated with the new data
            selected_game = GameHistory.objects.filter(pk=game_id, user_id__exact=user_id)

            # If a game was identified then it will be updated
            # if not then an error message will be displayed.
            if selected_game:
                selected_game.update(
                    name=name,
                    platform=platform,
                    hours_played=hours_played,
                    rating=rating,
                    year_played=year_played,
                )
                env["success_message"] = UPDATE_SUCCESS_MESSAGE
            else:
                env["error_message"] = GENERIC_ERROR_MESSAGE
            env["update_game_form"] = UpdateGameForm()
        else:
            env["error_message"] = UPDATE_ERROR_MESSAGE

    update_game_form = UpdateGameForm()
    env["update_game_form"] = update_game_form

    return render(request, "useractionpagebase.html", context=env)


@login_required(login_url="login_user")
def removegame(request):
    """This function is used to remove a specific game from journal history"""
    env = {}

    # Add page standard information and messages to context
    env["success_message"] = ""
    env["error_message"] = ""
    env["action_title"] = "Remove game from journal"
    env["action_description"] = "Refine your gaming odyssey! Remove a game from GameTracker now!"
    env["form_button_text"] = "Remove game"
    env["action_img_desc"] = "Remove game image"
    env["is_removegame_page"] = True

    # Success and error messages for the remove action
    REMOVE_ERROR_MESSAGE = "Please select a game before you press the remove button"
    REMOVE_SUCCESS_MESSAGE = "The selected game has been successfully removed from your gaming journal."

    # Get all game of the user that is signed in to the app
    game_history_data = GameHistory.objects.filter(user_id=request.user.id).order_by('-year_played').values()
    env["user_games"] = game_history_data

    # Check if the user made a POST request on this page
    # and delete the game that was selected by the user
    if request.method == "POST":
        if request.POST.get("game_id") != "default":
            user_id = request.POST.get("user_id")
            game_id = request.POST.get("game_id")
            game_selected = GameHistory.objects.filter(pk=game_id, user_id__exact=user_id)
            if game_selected:
                game_selected.delete()
                env["success_message"] = REMOVE_SUCCESS_MESSAGE
            else:
                env["error_message"] = GENERIC_ERROR_MESSAGE
        else:
            env["error_message"] = REMOVE_ERROR_MESSAGE

    return render(request, "useractionpagebase.html", context=env)