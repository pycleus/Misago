from django.urls import reverse


def preload_socialauth_json(request):
    request.frontend_context.update(
        {"SOCIAL_AUTH": get_enabled_social_auth_providers(request.socialauth)}
    )

    return {}


def get_enabled_social_auth_providers(socialauth):
    providers = []
    for provider in socialauth.values():
        providers.append(
            {
                "pk": provider["pk"],
                "name": provider["name"],
                "button_text": provider["button_text"],
                "button_color": provider["button_color"],
                "url": reverse(
                    "misago:social-login", kwargs={"backend": provider["pk"]}
                ),
            }
        )
    return providers
