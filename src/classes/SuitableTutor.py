from .Tutor import Tutor


class SuitableTutor(Tutor):
    def __init__(
            self,
            tutor:Tutor,
            subjects_match: list[str],
            subject_levels_match: list[str],
            experience_match: int):
        super.__init__(
            tutor.name,
            tutor.telegram_handle,
            tutor.subjects,
            tutor.subject_levels,
            tutor.experience,
            tutor.address,
            tutor.gender,
            tutor.commute_method)
        self.subjects_match = subjects_match
        self.subject_levels_match = subject_levels_match
        self.experience_match = experience_match

