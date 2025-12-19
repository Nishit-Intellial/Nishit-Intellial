from django.shortcuts import render

# from stronghold.decorators import public
import json
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

def index(request):
    # if "username" not in request.session:
    #     return redirect("/accounts/signin/")
    return render(request, "base/index.html")


# @public
def get_app_data(request):

    display_row = 10
    decimal_point = 4
    user_col_settings = []
    user_email = ""
    # if "username" in request.session:
    #     user_email = request.session["username"] if "client_user" not in request.session else request.session["client_username"]
    # company_code = Util.get_sys_paramter("company_code").para_value
    # theme_info = UserService.get_theme_info(request.session.get("color_scheme", None))

    # if "userid" in request.session:
    #     decimal_point = Util.get_sys_paramter("decimalpoint").para_value
    #     user_profile_obj = UserProfile.objects.filter(user_id=request.session["userid"]).values("display_row").first()
    #     display_row = user_profile_obj["display_row"] if user_profile_obj["display_row"] else 10
    #     user_col_settings = get_ui_settings(request.session["userid"])
    print("return")
    return HttpResponse(
        json.dumps(
            {
                "button_color": "#337ab7",
                "user_col_settings": user_col_settings,
                "decimal_point": decimal_point,
                "display_row": display_row,
                "row_color": None,
                "user_name": user_email,
            }
        ),
        content_type="json",
    )


@xframe_options_exempt
def iframe_index(request):
    return render(request, "base/iframe_index.html")