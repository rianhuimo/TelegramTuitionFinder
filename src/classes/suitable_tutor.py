from .tutor import Tutor


class SuitableTutor(Tutor):
    def __init__(
            self,
            tutor:Tutor,

            subjects_match:set[str],
            subject_levels_match:set[str],
            experience_match:set[str],
            fastest_commute:dict,):
        super().__init__(
            tutor.name,
            tutor.telegram_handle,
            tutor.subjects,
            tutor.subject_levels,
            tutor.experience,
            tutor.address,
            tutor.gender,
            tutor.commute_method,
            tutor.max_commute_time)
        self.subjects_match:set[str] = subjects_match
        self.subject_levels_match:set[str] = subject_levels_match
        self.experience_match:set[str] = experience_match
        self.fastest_commute:dict = fastest_commute