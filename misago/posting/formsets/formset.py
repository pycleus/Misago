from django.core.exceptions import ValidationError

from ...forms.formset import Formset
from ..forms import InviteUsersForm, PostForm, TitleForm
from ..state.base import PostingState


class PostingFormset(Formset):
    errors: list[ValidationError]

    def __init__(self):
        super().__init__()
        self.errors = []

    @property
    def title(self) -> TitleForm | None:
        return self.forms.get(TitleForm.form_prefix)

    @property
    def post(self) -> PostForm | None:
        return self.forms.get(PostForm.form_prefix)

    @property
    def invite_users(self) -> InviteUsersForm | None:
        return self.forms.get(InviteUsersForm.form_prefix)

    def update_state(self, state: PostingState):
        for form in self.forms.values():
            if form.is_valid():
                form.update_state(state)

    def add_error(self, error: ValidationError):
        self.errors.append(error)

    def clear_errors_in_preview(self):
        for form in self.forms.values():
            form.clear_errors_in_preview()

    def clear_errors_in_upload(self):
        for form in self.forms.values():
            form.clear_errors_in_upload()
