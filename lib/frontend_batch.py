from typing import List

from lib.abstract_frontend import Frontend


class FrontendBatch(Frontend):
    def get_user_confirmation(self) -> bool:
        return True

    def get_tags(self) -> List[str]:
        return []
