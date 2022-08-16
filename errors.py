# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class UltimateServerErrorType(str, Enum):

    USER_NOT_FOUND = "USER_NOT_FOUND"


ISSUE_CODES = {
    1000: "User not found.",
}


ERROR_TYPES_TO_ISSUE_CODES_MAPPING = {
    UltimateServerErrorType.USER_NOT_FOUND: [1000]
}


class ErrorLevel(str, Enum):

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class SupersetError:
    """
    An error that is returned to a client.
    """

    message: str
    error_type: UltimateServerErrorType
    level: ErrorLevel
    extra: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        """
        Mutates the extra params with user facing error codes that map to backend
        errors.
        """
        issue_codes = ERROR_TYPES_TO_ISSUE_CODES_MAPPING.get(self.error_type)
        if issue_codes:
            self.extra = self.extra or {}
            self.extra.update(
                {
                    "issue_codes": [
                        {
                            "code": issue_code,
                            "message": (
                                f"Issue {issue_code} - {ISSUE_CODES[issue_code]}"
                            ),
                        }
                        for issue_code in issue_codes
                    ]
                }
            )

    def to_dict(self) -> Dict[str, Any]:
        rv = {"message": self.message, "error_type": self.error_type}
        if self.extra:
            rv["extra"] = self.extra  # type: ignore
        return rv
